import click
import re


class LinkType(click.ParamType):
    name = "Link"

    def convert(self, value, param, ctx):
        regexp = re.compile(r'\Ahttp[?s]://a.4cdn.org/(\w+)/catalog.json\Z', re.IGNORECASE)
        link_match = regexp.match(value)
        if link_match:
            return {'link': value, 'board': link_match.group(1)}
        else:
            self.fail(f"Expected a link, got {value!r} of type {type(value).__name__}", param, ctx)
