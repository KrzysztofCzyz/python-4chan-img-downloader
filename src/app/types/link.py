import click
import re


class LinkType(click.ParamType):
    name = "Link"

    def convert(self, value, param, ctx):
        # http://a.4cdn.org/BOARD/catalog.json
        regexp = re.compile(r'\A(?:http[?s]://)?a.4cdn.org/(\w+)/catalog.json\Z', re.IGNORECASE)
        # https://boards.4chan.org/BOARD/catalog
        regexp2 = re.compile(r'\A(?:http[?s]://)?boards.4chan(?:nel)?.org/(\w+)/catalog')
        link_match = regexp.match(value)
        link_match2 = regexp2.match(value)
        if link_match:
            return {'link': "http://a.4cdn.org/" + link_match.group(1) + "/catalog.json", 'board': link_match.group(1)}
        elif link_match2:
            return {'link': "http://a.4cdn.org/" + link_match2.group(1)
                            + "/catalog.json", 'board': link_match2.group(1)}
        else:
            self.fail(f"Expected a link, got {value!r} of type {type(value).__name__}", param, ctx)
