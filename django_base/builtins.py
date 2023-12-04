from urllib.parse import quote, urljoin

import django.db.models
from django import template
from django.apps import apps
from django.template.base import Node
from django.templatetags.static import PrefixNode
from django.utils.datastructures import ImmutableList
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()


def doc(obj) -> str:
    if obj == '':
        return mark_safe('<!-- no obj -->')
    if not hasattr(obj, '__doc__'):
        return mark_safe('<!-- no doc -->')
    if hasattr(obj, '__bases__'):
        this = [f'{obj.__name__}: {obj.__doc__}']
        bases = [
            f'{x.__name__}: {x.__doc__}'
            for x in obj.__bases__ if hasattr(x, '__doc__')
        ]
        return '\n\n'.join(this + bases)
    return obj.__doc__


def fields(obj: django.db.models.Model) -> ImmutableList:
    return obj._meta.get_fields()


def name_(obj) -> str:
    return str(getattr(obj, '__name__', ''))


register.filter('doc', doc)
register.filter('fields', fields)
register.filter('name', name_)


class AssetNode(template.Node):
    def __init__(self, varname: str = None, path=None):
        if path is None:
            raise template.TemplateSyntaxError(
                "Asset template nodes must be given a path to return."
            )
        self.path = path
        self.varname = varname

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(varname={self.varname!r}, path={self.path!r})"
        )

    def url(self, context):
        path = self.path.resolve(context)
        return self.handle_simple(path)

    def render(self, context) -> str:
        url = self.url(context)
        if context.autoescape:
            url = conditional_escape(url)
        if self.varname is None:
            return url
        context[self.varname] = url
        return ""

    @classmethod
    def handle_simple(cls, path):
        # if apps.is_installed('django.contrib.staticfiles'):
        #     from django.contrib.staticfiles.storage import staticfiles_storage
        #     return staticfiles_storage.url(path)
        # else:
        print(path)
        print(PrefixNode.handle_simple('ASSET_URL'))
        print(urljoin(PrefixNode.handle_simple('ASSET_URL'), quote(path)))
        return urljoin(PrefixNode.handle_simple('ASSET_URL'), quote(path))

    @classmethod
    def handle_token(
            cls,
            parser: django.template.base.Parser,
            token: django.template.base.Token):
        bits = token.split_contents()
        if len(bits) < 2:
            raise template.TemplateSyntaxError(
                "'%s' takes at least one argument (path to file)" % bits[0]
            )
        path = parser.compile_filter(bits[1])
        if len(bits) >= 2 and bits[-2] == 'as':
            varname = bits[3]
        else:
            varname = None
        return cls(varname, path)


@register.tag("asset")
def do_asset(
        parser: django.template.base.Parser,
        token: django.template.base.Token):
    return AssetNode.handle_token(parser, token)


class ViteNode(Node):
    def render(self, context):
        from django.conf import settings
        return getattr(settings, 'VITE_CLIENT_URL', '')


@register.tag("vite")
def do_vite(_parser, _token):
    return ViteNode()
