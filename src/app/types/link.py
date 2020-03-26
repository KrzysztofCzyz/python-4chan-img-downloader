import click
import re


class CatalogLinkType(click.ParamType):
    name = "Link"
    # cloud define it as 1 regexp

    def convert(self, value, param, ctx):
        # matches catalog.json links e.g. http://a.4cdn.org/BOARD/catalog.json
        regexp = re.compile(r'\A(?:http[?s]://)?a.4cdn.org/(\w+)/catalog.json\Z', re.IGNORECASE)
        # matches direct Board links e.g. https://boards.4chan.org/BOARD/catalog
        regexp2 = re.compile(r'\A(?:http[?s]://)?boards.4chan(?:nel)?.org/(\w+)/catalog')
        link_match = regexp.match(value)
        link_match2 = regexp2.match(value)
        if link_match:
            return {'link': "http://a.4cdn.org/" + link_match.group(1)
                            + "/catalog.json", 'board': link_match.group(1)}
        elif link_match2:
            return {'link': "http://a.4cdn.org/" + link_match2.group(1)
                            + "/catalog.json", 'board': link_match2.group(1)}
        else:
            self.fail(f"Expected a link, got {value!r}", param, ctx)


class ThreadLinkType(click.ParamType):
    name = "Link"

    def convert(self, value, param, ctx):
        # matches direct thread links e.g. https://boards.4chan.org/BOARD/thread/TH_NUM(.json)
        regexp = re.compile(r'\A(?:http[?s]://)?boards.4chan(?:nel)?.org/(\w+)/thread/([0-9]+)(?:.json)?\Z'
                            , re.IGNORECASE)
        link_match = regexp.match(value)
        if link_match:
            return {'link': "http://boards.4chan.org/" + link_match.group(1)
                            + "/thread/" + link_match.group(2) + ".json", 'board': link_match.group(1)}
        else:
            self.fail(f"Expected a link, got {value!r}", param, ctx)
