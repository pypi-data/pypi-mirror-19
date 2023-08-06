# Dystros
# Copyright (C) 2016 Jelmer Vernooij <jelmer@jelmer.uk>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; version 2
# of the License or (at your option) any later version of
# the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA  02110-1301, USA.

"""Abstract WebDAV server implementation..

This module contains an abstract WebDAV server. All caldav/carddav specific
functionality should live in dystros.caldav/dystros.carddav respectively.
"""

# TODO(jelmer): Add authorization support

import collections
import hashlib
import logging
import posixpath
import urllib.parse
from wsgiref.util import request_uri

from defusedxml.ElementTree import fromstring as xmlparse
# Hmm, defusedxml doesn't have XML generation functions? :(
from xml.etree import ElementTree as ET

DEFAULT_ENCODING = 'utf-8'
COLLECTION_RESOURCE_TYPE = '{DAV:}collection'
PRINCIPAL_RESOURCE_TYPE = '{DAV:}principal'


PropStatus = collections.namedtuple(
    'PropStatus', ['statuscode', 'responsedescription', 'prop'])


def etag_matches(condition, actual_etag):
    """Check if an etag matches an If-Matches condition.

    :param condition: Condition (e.g. '*', '"foo"' or '"foo", "bar"'
    :param actual_etag: ETag to compare to. None nonexistant
    :return: bool indicating whether condition matches
    """
    if actual_etag is None and condition:
        return False
    for etag in condition.split(','):
        if etag.strip(' ') == '*':
            return True
        if etag.strip(' ') == actual_etag:
            return True
    else:
        return False


class NeedsMultiStatus(Exception):
    """Raised when a response needs multi-status (e.g. for propstat)."""


class DAVStatus(object):
    """A DAV response that can be used in multi-status."""

    def __init__(self, href, status=None, error=None, responsedescription=None,
                 propstat=None):
        self.href = href
        self.status = status
        self.error = error
        self.propstat = propstat
        self.responsedescription = responsedescription

    def __repr__(self):
        return "<%s(%r, %r, %r)>" % (
            type(self).__name__, self.href, self.status, self.responsedescription)

    def get_single_body(self, encoding):
        if self.propstat and len(self._propstat_by_status()) > 1:
            raise NeedsMultiStatus()
        if self.propstat:
            [ret] = list(self._propstat_xml())
            body = ET.tostringlist(ret, encoding)
            return body, ('text/xml; encoding="%s"' % encoding)
        else:
            body = self.responsedescription or ''
            return body, ('text/plain; encoding="%s"' % encoding)

    def _propstat_by_status(self):
        bystatus = {}
        for propstat in self.propstat:
            bystatus.setdefault(
                (propstat.statuscode, propstat.responsedescription), []).append(
                        propstat.prop)
        return bystatus

    def _propstat_xml(self):
        bystatus = self._propstat_by_status()
        for (status, rd), props in sorted(bystatus.items()):
            propstat = ET.Element('{DAV:}propstat')
            ET.SubElement(propstat,
                '{DAV:}status').text = 'HTTP/1.1 ' + status
            if rd:
                ET.SubElement(propstat,
                    '{DAV:}responsedescription').text = responsedescription
            propresp = ET.SubElement(propstat, '{DAV:}prop')
            for prop in props:
                propresp.append(prop)
            yield propstat

    def aselement(self):
        ret = ET.Element('{DAV:}response')
        ET.SubElement(ret, '{DAV:}href').text = self.href
        if self.status:
            ET.SubElement(ret, '{DAV:}status').text = 'HTTP/1.1 ' + self.status
        if self.error:
            ET.SubElement(ret, '{DAV:}error').append(self.error)
        if self.responsedescription:
            ET.SubElement(ret,
                '{DAV:}responsedescription').text = self.responsedescription
        if self.propstat is not None:
            for ps in self._propstat_xml():
                ret.append(ps)
        return ret


class DAVProperty(object):
    """Handler for listing, retrieving and updating DAV Properties."""

    # Property name (e.g. '{DAV:}resourcetype')
    name = None

    # Whether to include this property in 'allprop' PROPFIND requests.
    # https://tools.ietf.org/html/rfc4918, section 14.2
    in_allprops = True

    # Whether this property is protected (i.e. read-only)
    protected = True

    # Resource type this property belongs to. If None, get_value()
    # will always be called.
    resource_type = None

    def get_value(self, resource, el):
        """Get property with specified name.

        :param resource: Resource for which to retrieve the property
        :param el: Element to populate
        :raise KeyError: if this property is not present
        """
        raise KeyError(self.name)

    def set_value(self, resource, el):
        """Set property.

        :param resource: Resource to modify
        :param el: Element to get new value from
        """
        raise NotImplementedError(self.set_value)

    def remove(self, resource):
        """Remove property.

        :param resource: Resource to modify
        """
        raise NotImplementedError(self.remove)


class DAVResourceTypeProperty(DAVProperty):
    """Provides {DAV:}resourcetype."""

    name = '{DAV:}resourcetype'

    protected = True

    resource_type = None

    def get_value(self, resource, el):
        for rt in resource.resource_types:
            ET.SubElement(el, rt)


class DAVDisplayNameProperty(DAVProperty):
    """Provides {DAV:}displayname.

    https://tools.ietf.org/html/rfc4918, section 5.2
    """

    name = '{DAV:}displayname'
    resource_type = None

    def get_value(self, resource, el):
        el.text = resource.get_displayname()

    # TODO(jelmer): allow modification of this property
    # protected = True


class DAVGetETagProperty(DAVProperty):
    """Provides {DAV:}getetag.

    https://tools.ietf.org/html/rfc4918, section 15.6
    """

    name = '{DAV:}getetag'
    resource_type = None
    protected = True

    def get_value(self, resource, el):
        el.text = resource.get_etag()


def format_datetime(dt):
    s = "%04d%02d%02dT%02d%02d%02dZ" % (
        dt.year,
        dt.month,
        dt.day,
        dt.hour,
        dt.minute,
        dt.second
    )
    return s.encode('utf-8')


class DAVCreationDateProperty(DAVProperty):
    """Provides {DAV:}creationdate.

    https://tools.ietf.org/html/rfc4918, section 23.2
    """

    name = '{DAV:}creationdate'
    resource_type = None
    protected = True

    def get_value(self, resource, el):
        el.text = format_datetime(resource.get_creationdate())


class DAVGetContentTypeProperty(DAVProperty):
    """Provides {DAV:}getcontenttype.

    https://tools.ietf.org/html/rfc4918, section 13.5
    """

    name = '{DAV:}getcontenttype'
    resource_type = None
    protected = True

    def get_value(self, resource, el):
        el.text = resource.get_content_type()


class DAVCurrentUserPrincipalProperty(DAVProperty):
    """Provides {DAV:}current-user-principal.

    See https://tools.ietf.org/html/rfc5397
    """

    name = '{DAV:}current-user-principal'
    resource_type = None
    in_allprops = False

    def __init__(self, current_user_principal):
        super(DAVCurrentUserPrincipalProperty, self).__init__()
        self.current_user_principal = current_user_principal

    def get_value(self, resource, el):
        """Get property with specified name.

        :param name: A property name.
        """
        ET.SubElement(el, '{DAV:}href').text = self.current_user_principal


class DAVPrincipalURLProperty(DAVProperty):

    name = '{DAV:}principal-URL'
    resource_type = '{DAV:}principal'
    in_allprops = True

    def get_value(self, resource, el):
        """Get property with specified name.

        :param name: A property name.
        """
        ET.SubElement(el, '{DAV:}href').text = resource.get_principal_url()


class DAVSupportedReportSetProperty(DAVProperty):

    name = '{DAV:}supported-report-set'
    resource_type = '{DAV:}collection'
    in_allprops = False

    def __init__(self, reporters):
        self._reporters = reporters

    def get_value(self, resource, el):
        for name in self._reporters:
            ET.SubElement(el, name)


class GetCTagProperty(DAVProperty):
    """getctag property

    """

    name = '{http://calendarserver.org/ns/}getctag'
    resource_type = COLLECTION_RESOURCE_TYPE
    in_allprops = False
    protected = True

    def get_value(self, resource, el):
        el.text = resource.get_ctag()


LOCK_SCOPE_EXCLUSIVE = '{DAV:}exclusive'
LOCK_SCOPE_SHARED = '{DAV:}shared'
LOCK_TYPE_WRITE = '{DAV:}write'


ActiveLock = collections.namedtuple(
    'ActiveLock',
    ['lockscope', 'locktype', 'depth', 'owner', 'timeout','locktoken',
        'lockroot'])


class DAVResource(object):
    """A WebDAV resource."""

    # A list of resource type names (e.g. '{DAV:}collection')
    resource_types = []

    def get_displayname(self):
        """Get the resource display name."""
        raise KeyError

    def get_creationdate(self):
        """Get the resource creation date.

        :return: A datetime object
        """
        raise NotImplementedError(self.get_creationdate)

    def get_supported_locks(self):
        """Get the list of supported locks.

        This should return a list of (lockscope, locktype) tuples.
        Known lockscopes are LOCK_SCOPE_EXCLUSIVE, LOCK_SCOPE_SHARED
        Known locktypes are LOCK_TYPE_WRITE
        """
        raise NotImplementedError(self.get_supported_locks)

    def get_active_locks(self):
        """Return the list of active locks.

        :return: A list of ActiveLock tuples
        """
        raise NotImplementedError(self.get_active_locks)

    def get_content_type(self):
        """Get the content type for the resource.

        This is a mime type like text/plain
        """
        raise NotImplementedError(self.get_content_type)

    def get_owner(self):
        """Get an href identifying the owner of the resource.

        Can be None if owner information is not known.
        """
        raise NotImplementedError(self.get_owner)

    def get_etag(self):
        """Get the etag for this resource.

        Contains the ETag header value (from Section 14.19 of [RFC2616]) as it
        would be returned by a GET without accept headers.
        """
        raise NotImplementedError(self.get_etag)

    def get_body(self):
        """Get resource contents.

        :return: Iterable over bytestrings."""
        raise NotImplementedError(self.get_body)

    def set_body(self, body, replace_etag=None):
        """Set resource contents.

        :param body: Iterable over bytestrings
        :return: New ETag
        """
        raise NotImplementedError(self.set_body)


class DAVCollection(DAVResource):
    """Resource for a WebDAV Collection."""

    resource_types = DAVResource.resource_types + [COLLECTION_RESOURCE_TYPE]

    def members(self):
        """List all members.

        :return: List of (name, DAVResource) tuples
        """
        raise NotImplementedError(self.members)

    def get_member(self, name):
        """Retrieve a member by name.

        :param name: Name of member to retrieve
        :return: A DAVResource
        """
        raise NotImplementedError(self.get_member)

    def delete_member(self, name, etag=None):
        """Delete a member with a specific name.

        :param name: Member name
        :param etag: Optional required etag
        :raise KeyError: when the item doesn't exist
        """
        raise NotImplementedError(self.delete_member)

    def create_member(self, name, contents):
        """Create a new member with specified name and contents.

        :param name: Member name
        :param etag: Optional required etag
        :return: ETag for the new member
        """
        raise NotImplementedError(self.create_member)

    def create_collection(self, name):
        """Create a subcollection with the specified name.

        :param name: Subcollection name
        """
        raise NotImplementedError(self.create_collection)

    def get_sync_token(self):
        """Get sync-token for the current state of this collection.
        """
        raise NotImplementedError(self.get_sync_token)

    def iter_differences_since(self, old_token, new_token):
        """Iterate over differences in this collection.

        Should return an iterator over (name, old resource, new resource) tuples.
        If one of the two didn't exist previously or now, they should be None.

        If old_token is None, this should return full contents of the
        collection.

        May raise NotImplementedError if iterating differences is not
        supported.
        """
        raise NotImplementedError(self.iter_differences_since)

    def get_ctag(self):
        raise NotImplementedError(self.getctag)


class DAVPrincipal(DAVResource):
    """Resource for a DAV Principal."""

    resource_Types = DAVResource.resource_types + [PRINCIPAL_RESOURCE_TYPE]

    def get_principal_url(self):
        """Return the principal URL for this principal.

        :return: A URL identifying this principal.
        """
        raise NotImplementedError(self.get_principal_url)


def get_property(resource, properties, name):
    """Get a single property on a resource.

    :param resource: DAVResource object
    :param properties: Dictionary of properties
    :param name: name of property to resolve
    :return: PropStatus items
    """
    responsedescription = None
    ret = ET.Element(name)
    try:
        prop = properties[name]
    except KeyError:
        statuscode = '404 Not Found'
        logging.warning(
            'Client requested unknown property %s',
            name)
    else:
        try:
            if (prop.resource_type is not None and
                prop.resource_type not in resource.resource_types):
                raise KeyError
            prop.get_value(resource, ret)
        except KeyError:
            statuscode = '404 Not Found'
        else:
            statuscode = '200 OK'
    return PropStatus(statuscode, responsedescription, ret)


def get_properties(resource, properties, requested):
    """Get a set of properties.

    :param resource: DAVResource object
    :param properties: Dictionary of properties
    :param requested: XML {DAV:}prop element with properties to look up
    :return: Iterator over PropStatus items
    """
    for propreq in list(requested):
        yield get_property(resource, properties, propreq.tag)


def traverse_resource(base_resource, depth, base_href):
    """Traverse a resource.

    :param base_resource: Resource to traverse from
    :param depth: Depth ("0", "1", ...)
    :param base_href: href for base resource
    :return: Iterator over (URL, Resource) tuples
    """
    me = (base_href, base_resource)
    if depth == "0":
        return iter([me])
    elif depth == "1":
        ret = [me]
        if COLLECTION_RESOURCE_TYPE in base_resource.resource_types:
            for (name, resource) in base_resource.members():
                href = urllib.parse.urljoin(base_href+'/', name)
                if COLLECTION_RESOURCE_TYPE in resource.resource_types:
                    # caldavzap/carddavmate require this
                    href += '/'
                ret.append((href, resource))
        return iter(ret)
    raise NotImplementedError


class DAVReporter(object):
    """Implementation for DAV REPORT requests."""

    name = None

    def report(self, request_body, resources_by_hrefs, properties, href,
               resource, depth):
        """Send a report.

        :param request_body: XML Element for request body
        :param resources_by_hrefs: Function for retrieving resource by HREF
        :param properties: Dictionary mapping names to DAVProperty instances
        :param href: Base resource href
        :param resource: Resource to start from
        :param depth: Depth ("0", "1", ...)
        :return: Iterator over DAVStatus objects
        """
        raise NotImplementedError(self.report)


class DAVExpandPropertyReporter(DAVReporter):
    """A expand-property reporter.

    See https://tools.ietf.org/html/rfc3253, section 3.8
    """

    name = '{DAV:}expand-property'

    def _populate(self, prop_list, resources_by_hrefs, properties, href,
                  resource):
        """Expand properties for a resource.

        :param prop_list: DAV:property elements to retrieve and expand
        :param resources_by_hrefs: Resolve resource by HREF
        :param properties: Available properties
        :param href: href for current resource
        :param resource: current resource
        :return: DAVSstatus object
        """
        ret = []
        for prop in prop_list:
            prop_name = prop.get('name')
            # FIXME: Resolve prop_name on resource
            propstat = get_property(resource, properties, prop_name)
            new_prop = ET.Element(propstat.prop.tag)
            child_hrefs = [prop_child.text for prop_child in propstat.prop
                           if prop_child.tag == '{DAV:}href']
            child_resources = resources_by_hrefs(child_hrefs)
            for prop_child in propstat.prop:
                if prop_child.tag != '{DAV:}href':
                    new_prop.append(prop_child)
                else:
                    child_resource = child_resources[prop_child.text]
                    if child_resource is None:
                        # FIXME: What to do if the referenced href is invalid?
                        # For now, let's just keep the unresolved href around
                        new_prop.append(prop_child)
                    else:
                        response = self._populate(
                            prop, properties, prop_child.text, child_resource)
                        new_prop.append(response.aselement())
            propstat = PropStatus(
                propstat.statuscode, propstat.responsedescription, prop=new_prop)
            ret.append(propstat)
        return DAVStatus(href, '200 OK', propstat=ret)

    def report(self, request_body, resources_by_hrefs, properties, href,
               resource, depth):
        return self._populate(request_body, resources_by_hrefs, properties,
                              href, resource)


class DAVSupportedLockProperty(DAVProperty):
    """supportedlock property.

    See rfc4918, section 15.10.
    """

    name = '{DAV:}supportedlock'
    resource_type = None
    protected = True

    def get_value(self, resource, el):
        for (lockscope, locktype) in resource.get_supported_locks():
            entry = ET.SubElement(el, '{DAV:}lockentry')
            scope_el = ET.SubElement(entry, '{DAV:}lockscope')
            ET.SubElement(scope_el, lockscope)
            type_el = ET.SubElement(entry, '{DAV:}locktype')
            ET.SubElement(type_el, locktype)


class DAVLockDiscoveryProperty(DAVProperty):
    """lockdiscovery property.

    See rfc4918, section 15.8
    """

    name = '{DAV:}lockdiscovery'
    resource_type = None
    protected = True

    def get_value(self, resource, el):
        for activelock in resource.get_active_locks():
            entry = ET.SubElement(el, '{DAV:}activelock')
            type_el = ET.SubElement(entry, '{DAV:}locktype')
            ET.SubElement(type_el, activelock.locktype)
            scope_el = ET.SubElement(entry, '{DAV:}lockscope')
            ET.SubElement(scope_el, activelock.lockscope)
            ET.SubElement(entry, '{DAV:}depth').text = str(activelock.depth)
            if activelock.owner:
                ET.SubElement(entry, '{DAV:}owner').text = activelock.owner
            if activelock.timeout:
                ET.SubElement(entry, '{DAV:}timeout').text = activelock.timeout
            if activelock.locktoken:
                locktoken_el = ET.SubElement(entry, '{DAV:}locktoken')
                href = ET.SubElement(locktoken_el, '{DAV:}href')
                href.text = activelock.locktoken
            if activelock.lockroot:
                locktoken_el = ET.SubElement(entry, '{DAV:}lockroot')
                href = ET.SubElement(locktoken_el, '{DAV:}href')
                href.text = activelock.lockroot


class WellknownResource(DAVResource):
    """Resource for well known URLs.

    See https://tools.ietf.org/html/rfc6764
    """

    def __init__(self, server_root):
        self.server_root = server_root

    def get_etag(self):
        return '"%s"' % hashlib.md5(b''.join(self.get_body())).hexdigest()

    def get_content_length(self):
        return len(b''.join(self.get_body()))

    def get_body(self):
        return [self.server_root.encode(DEFAULT_ENCODING)]


class DAVBackend(object):
    """WebDAV backend."""

    def get_resoure(self, relpath):
        raise NotImplementedError(self.get_resource)


class WebDAVApp(object):
    """A wsgi App that provides a WebDAV server.

    A concrete implementation should provide an implementation of the
    lookup_resource function that can map a path to a DAVResource object
    (returning None for nonexistant objects).
    """

    out_encoding = DEFAULT_ENCODING

    def __init__(self, backend):
        self.backend = backend
        self.properties = {}
        self.reporters = {}

    def _request_href(self, environ):
        """Returns a href that can be used externally."""
        return environ['SCRIPT_NAME'] + environ['PATH_INFO']

    def register_properties(self, properties):
        for p in properties:
            self.properties[p.name] = p

    def register_reporters(self, reporters):
        for r in reporters:
            self.reporters[r.name] = r

    def _get_dav_features(self, environ):
        # TODO(jelmer): Support access-control
        return ['1', '2', '3', 'calendar-access', 'addressbook']

    def _get_allowed_methods(self, environ):
        """List of supported methods on this endpoint."""
        # TODO(jelmer): Look up resource to determine supported methods.
        return ([n[3:] for n in dir(self) if n.startswith('do_')] +
                [n[4:] for n in dir(self) if n.startswith('dav_')])

    def _send_not_found(self, environ, start_response):
        path = request_uri(environ)
        start_response('404 Not Found', [])
        return [b'Path ' + path.encode(DEFAULT_ENCODING) + b' not found.']

    def _send_method_not_allowed(self, environ, start_response):
        start_response('405 Method Not Allowed', [
            ('Allow', ', '.join(self._get_allowed_methods(environ)))])
        return []

    def do_GET(self, environ, start_response):
        r = self.backend.get_resource(environ['PATH_INFO'])
        if r is None:
            return self._send_not_found(environ, start_response)
        current_etag = r.get_etag()
        if_none_match = environ.get('HTTP_IF_NONE_MATCH', None)
        if if_none_match and etag_matches(if_none_match, current_etag):
            start_response('304 Not Modified', [])
            return []
        start_response('200 OK', [
            ('ETag', current_etag),
            ('Content-Type', r.get_content_type()),
            ('Content-Length', str(r.get_content_length())),
        ])
        return r.get_body()

    def do_DELETE(self, environ, start_response):
        r = self.backend.get_resource(environ['PATH_INFO'])
        if r is None:
            return self._send_not_found(environ, start_response)
        container_path, item_name = posixpath.split(posixpath.normpath(environ['PATH_INFO']))
        pr = self.backend.get_resource(container_path)
        if pr is None:
            return self._send_not_found(environ, start_response)
        current_etag = r.get_etag()
        if_match = environ.get('HTTP_IF_MATCH', None)
        if if_match is not None and not etag_matches(if_match, current_etag):
            start_response('412 Precondition Failed', [])
            return []
        pr.delete_member(item_name, current_etag)
        start_response('204 No Content', [])
        return []

    def do_PUT(self, environ, start_response):
        new_contents = self._readBody(environ)
        path = posixpath.normpath(environ['PATH_INFO'])
        r = self.backend.get_resource(path)
        if r is not None:
            current_etag = r.get_etag()
        else:
            current_etag = None
        if_match = environ.get('HTTP_IF_MATCH', None)
        if if_match is not None and not etag_matches(if_match, current_etag):
            start_response('412 Precondition Failed', [])
            return []
        if r is not None:
            new_etag = r.set_body([new_contents], current_etag)
            start_response('204 No Content', [
                ('ETag', new_etag)])
            return []
        container_path, name = posixpath.split(path)
        r = self.backend.get_resource(container_path)
        if r is not None:
            new_etag = r.create_member(name, [new_contents])
            start_response('201 Created', [
                ('ETag', new_etag)])
            return []
        return self._send_not_found(environ, start_response)

    def _readBody(self, environ):
        try:
            request_body_size = int(environ['CONTENT_LENGTH'])
        except KeyError:
            return environ['wsgi.input'].read()
        else:
            return environ['wsgi.input'].read(request_body_size)

    def _send_dav_responses(self, start_response, responses):
        if isinstance(responses, DAVStatus):
            try:
                (body, body_type) = responses.get_single_body(
                    self.out_encoding)
            except NeedsMultiStatus:
                responses = [responses]
            else:
                start_response(responses.status, [
                    ('Content-Type', body_type),
                    ('Content-Length', str(sum(map(len, body))))])
                return body
        ret = ET.Element('{DAV:}multistatus')
        for response in responses:
            ret.append(response.aselement())
        body_type = 'text/xml; charset="%s"' % self.out_encoding
        body = ET.tostringlist(ret, encoding=self.out_encoding)
        start_response('207 Multi-Status', [
            ('Content-Type', body_type),
            ('Content-Length', str(sum(map(len, body))))])
        return body

    def _get_resources_by_hrefs(self, environ, hrefs):
        """Retrieve multiple resources by href.
        """
        # TODO(jelmer): Bulk query hrefs in a more efficient manner
        for href in hrefs:
            if not href.startswith(environ['SCRIPT_NAME']):
                resource = None
            else:
                resource = self.backend.get_resource(href[len(environ['SCRIPT_NAME']):])
            yield (href, resource)

    def dav_REPORT(self, environ):
        # See https://tools.ietf.org/html/rfc3253, section 3.6
        r = self.backend.get_resource(environ['PATH_INFO'])
        if r is None:
            return DAVStatus(request_uri(environ), '404 Not Found')
        depth = environ.get("HTTP_DEPTH", "0")
        #TODO(jelmer): check Content-Type; should be something like
        # 'text/xml; charset="utf-8"'
        et = xmlparse(self._readBody(environ))
        try:
            reporter = self.reporters[et.tag]
        except KeyError:
            logging.warning(
                'Client requested unkown REPORT %s',
                et.tag)
            return DAVStatus(request_uri(environ), '403 Forbidden',
                error=ET.Element('{DAV:}supported-report'))
        return reporter.report(
            et, lambda hrefs: self._get_resources_by_hrefs(environ, hrefs),
            self.properties, self._request_href(environ), r, depth)

    def dav_PROPFIND(self, environ):
        base_resource = self.backend.get_resource(environ['PATH_INFO'])
        if base_resource is None:
            return DAVStatus(request_uri(environ), '404 Not Found')
        depth = environ.get("HTTP_DEPTH", "0")
        #TODO(jelmer): check Content-Type; should be something like
        # 'text/xml; charset="utf-8"'
        et = xmlparse(self._readBody(environ))
        if et.tag != '{DAV:}propfind':
            # TODO-ERROR(jelmer): What to return here?
            return DAVStatus(
                request_uri(environ), '500 Internal Error',
                'Expected propfind tag, got ' + et.tag)
        try:
            [requested] = et
        except IndexError:
            return DAVStatus(request_uri(environ), '500 Internal Error',
                'Received more than one element in propfind.')
        if requested.tag == '{DAV:}prop':
            ret = []
            for href, resource in traverse_resource(
                    base_resource, depth, self._request_href(environ)):
                propstat = get_properties(
                    resource, self.properties, requested)
                ret.append(DAVStatus(href, '200 OK', propstat=list(propstat)))
            # By my reading of the WebDAV RFC, it should be legal to return
            # '200 OK' here if Depth=0, but the RFC is not super clear and
            # some clients don't seem to like it .
            return ret
        else:
            # TODO(jelmer): implement allprop and propname
            # TODO-ERROR(jelmer): What to return here?
            return DAVStatus(
                request_uri(environ), '500 Internal Error',
                'Expected prop tag, got ' + requested.tag)

    def dav_PROPPATCH(self, environ):
        resource = self.backend.get_resource(environ['PATH_INFO'])
        if resource is None:
            return DAVStatus(request_uri(environ), '404 Not Found')
        et = xmlparse(self._readBody(environ))
        if et.tag != '{DAV:}propertyupdate':
            # TODO-ERROR(jelmer): What to return here?
            return DAVStatus(
                request_uri(environ), '500 Internal Error',
                'Expected properyupdate tag, got ' + et.tag)
        propstat = []
        for el in et:
            if el.tag not in ('{DAV:}set', '{DAV:}remove'):
                return DAVStatus(request_uri(environ), '500 Internal Error',
                    'Unknown tag %s in propertyupdate' % el.tag)
            try:
                [requested] = el
            except IndexError:
                return DAVStatus(request_uri(environ), '500 Internal Error',
                    'Received more than one element in propertyupdate/set.')
            if requested.tag != '{DAV:}prop':
                return DAVStatus(
                    request_uri(environ), '500 Internal Error',
                    'Expected prop tag, got ' + requested.tag)
            for propel in requested:
                try:
                    handler = self.properties[propel.tag]
                except KeyError:
                    logging.warning(
                        'client attempted to modify unknown property %r',
                        propel.tag)
                    propstat.append(
                        PropStatus('404 Not Found', None,
                            ET.Element(propel.tag)))
                else:
                    if handler.protected:
                        # TODO(jelmer): Signal
                        # {DAV:}cannot-modify-protected-property error
                        statuscode = '409 Conflict'
                    elif el.tag == '{DAV:}remove':
                        handler.remove(resource)
                        statuscode = '200 OK'
                    elif el.tag == '{DAV:}set':
                        handler.set_value(resource, propel)
                        statuscode = '200 OK'
                    propstat.append(
                        PropStatus(statuscode, None, ET.Element(propel.tag)))

        return [DAVStatus(
            request_uri(environ), propstat=propstat)]

    def do_MKCOL(self, environ, start_response):
        # TODO(jelmer): Implement extended-mkcol - https://tools.ietf.org/html/rfc5689
        resource = self.backend.get_resource(environ['PATH_INFO'])
        if resource is not None:
            start_response('405 Method Not Allowed', [])
            return []
        container_path, item_name = posixpath.split(posixpath.normpath(environ['PATH_INFO']))
        pr = self.backend.get_resource(container_path)
        if pr is None:
            start_response('409 Conflict', [])
            return []
        pr.create_collection(item_name)
        start_response('201 Created', [])
        return []

    def do_OPTIONS(self, environ, start_response):
        # RFC7231 requires that if there is no response body,
        # Content-Length: 0 must be sent. This implies that there is
        # content (albeit empty), and thus a 204 is not a valid reply.
        # Thunderbird also fails if a 204 is sent rather than a 200.
        start_response('200 OK', [
            ('DAV', ', '.join(self._get_dav_features(environ))),
            ('Allow', ', '.join(self._get_allowed_methods(environ))),
            ('Content-Length', '0')])
        return []

    def __call__(self, environ, start_response):
        method = environ['REQUEST_METHOD']
        dav = getattr(self, 'dav_' + method, None)
        if dav is not None:
            return self._send_dav_responses(start_response, dav(environ))
        do = getattr(self, 'do_' + method, None)
        if do is not None:
            return do(environ, start_response)
        return self._send_method_not_allowed(environ, start_response)
