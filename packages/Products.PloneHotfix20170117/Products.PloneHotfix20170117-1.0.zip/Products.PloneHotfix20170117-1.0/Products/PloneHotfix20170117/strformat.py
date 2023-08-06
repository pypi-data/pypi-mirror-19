from AccessControl import allow_type
from AccessControl.ZopeGuards import guarded_getattr
from collections import Mapping
from urlparse import urlparse
from zope.component import getMultiAdapter

import string

try:
    # The Less config was introduced in Plone 5.
    from Products.CMFPlone.resources.browser.mixins import lessconfig
    from Products.CMFPlone.resources.browser.mixins import LessConfiguration
    from Products.CMFPlone.resources.browser.mixins import lessmodify
    from Products.CMFPlone.resources.browser.mixins import (
        LessModifyConfiguration)
except ImportError:
    # Plone 3 or 4.
    lessconfig = lessmodify = None
    LessConfiguration = LessModifyConfiguration = None


class _MagicFormatMapping(Mapping):
    """
    Pulled from Jinja2

    This class implements a dummy wrapper to fix a bug in the Python
    standard library for string formatting.

    See http://bugs.python.org/issue13598 for information about why
    this is necessary.
    """

    def __init__(self, args, kwargs):
        self._args = args
        self._kwargs = kwargs
        self._last_index = 0

    def __getitem__(self, key):
        if key == '':
            idx = self._last_index
            self._last_index += 1
            try:
                return self._args[idx]
            except LookupError:
                pass
            key = str(idx)
        return self._kwargs[key]

    def __iter__(self):
        return iter(self._kwargs)

    def __len__(self):
        return len(self._kwargs)


class SafeFormatter(string.Formatter):

    def __init__(self, value):
        self.value = value
        super(SafeFormatter, self).__init__()

    def get_field(self, field_name, args, kwargs):
        """
        Here we're overridding so we can use guarded_getattr instead of
        regular getattr
        """
        first, rest = field_name._formatter_field_name_split()

        obj = self.get_value(first, args, kwargs)

        # loop through the rest of the field_name, doing
        #  getattr or getitem as needed
        for is_attr, i in rest:
            if is_attr:
                obj = guarded_getattr(obj, i)
            else:
                obj = obj[i]

        return obj, first

    def safe_format(self, *args, **kwargs):
        kwargs = _MagicFormatMapping(args, kwargs)
        return self.vformat(self.value, args, kwargs)


def safe_format(inst, method):
    """
    Use our SafeFormatter that uses guarded_getattr for attribute access
    """
    return SafeFormatter(inst).safe_format


# we want to allow all methods on string type except "format"
rules = dict([(m, True) for m in dir(str) if not m.startswith('_')])
rules['format'] = safe_format
allow_type(str, rules)

# Same for unicode instead of str.
rules = dict([(m, True) for m in dir(unicode) if not m.startswith('_')])
rules['format'] = safe_format
allow_type(unicode, rules)


def LessConfiguration__call__(self):
    registry = self.registry()
    portal_state = getMultiAdapter((self.context, self.request),
                                   name=u'plone_portal_state')
    site_url = portal_state.portal_url()
    result = ""
    result += "sitePath: '\"%s\"',\n" % site_url
    result += "isPlone: true,\n"
    result += "isMockup: false,\n"
    result += "staticPath: '\"%s/++plone++static\"',\n" % site_url
    result += "barcelonetaPath: '\"%s/++theme++barceloneta\"',\n" % site_url

    less_vars_params = {
        'site_url': site_url,
    }

    # Storing variables to use them on further vars
    for name, value in registry.items():
        less_vars_params[name] = value

    for name, value in registry.items():
        t = SafeFormatter(value).safe_format(**less_vars_params)
        result += "'%s': \"%s\",\n" % (name, t)

    # Adding all plone.resource entries css values as less vars
    for name, value in self.resource_registry().items():
        for css in value.css:

            url = urlparse(css)
            if url.netloc == '':
                # Local
                src = "%s/%s" % (site_url, css)
            else:
                src = "%s" % (css)
            # less vars can't have dots on it
            result += "'%s': '\"%s\"',\n" % (name.replace('.', '_'), src)

    self.request.response.setHeader("Content-Type",
                                    "application/javascript")

    try:
        debug_level = int(self.request.get('debug', 2))
    except:
        debug_level = 2
    return lessconfig % (debug_level, result, result)


if LessConfiguration is not None:
    LessConfiguration.__call__ = LessConfiguration__call__


def LessModifyConfiguration__call__(self):
    registry = self.registry()
    portal_state = getMultiAdapter((self.context, self.request),
                                   name=u'plone_portal_state')
    site_url = portal_state.portal_url()
    result2 = ""
    result2 += "'@sitePath': '\"%s\"',\n" % site_url
    result2 += "'@isPlone': true,\n"
    result2 += "'@isMockup': false,\n"
    result2 += "'@staticPath: '\"%s/++plone++static\"',\n" % site_url
    result2 += "'@barcelonetaPath: '\"%s/++theme++barceloneta\"',\n" % site_url

    less_vars_params = {
        'site_url': site_url,
    }

    # Storing variables to use them on further vars
    for name, value in registry.items():
        less_vars_params[name] = value

    for name, value in registry.items():
        t = SafeFormatter(value).safe_format(**less_vars_params)
        result2 += "'@%s': \"%s\",\n" % (name, t)

    self.request.response.setHeader("Content-Type",
                                    "application/javascript")

    return lessmodify % (result2)


if LessModifyConfiguration is not None:
    LessModifyConfiguration.__call__ = LessModifyConfiguration__call__
