from click.testing import CliRunner
from app.download import thread, catalog
import os
from pytest import skip

cli_runner = CliRunner()


def dry_run(fun, link):
    result = cli_runner.invoke(fun, ["--test-run", "--link", link])
    return result


class ThreadTests:

    # checking malformed http(s) link on http conditional match
    def thread_malformed_link_http_test(self):
        result = dry_run(thread, "htps://boards.4channel.org/po/thread/570368")
        assert result.exit_code != 0

    # passes if no link fails
    def thread_no_link_test(self):
        result = dry_run(thread, "")
        assert result.exit_code != 0

    # checking (nel)? conditional match
    def thread_malformed_link_nel_test(self):
        result = dry_run(thread, "https://boards.4channel.org/po/thread/570368")
        assert result.exit_code == 0

    # checking .json conditional match
    def thread_malformed_link_json_test(self):
        result = dry_run(thread, "https://boards.4channel.org/po/thread/570368.json")
        assert result.exit_code == 0

    # lack of http(s) pattern check
    def thread_malformed_link_neg_https_test(self):
        result = dry_run(thread, "boards.4channel.org/po/thread/570368")
        assert result.exit_code == 0

    # final download check, sticky thread, might fail in the future
    def thread_with_link_test(self):
        with cli_runner.isolated_filesystem():
            cli_runner.invoke(thread, ["--link", "https://boards.4channel.org/po/thread/570368"])
            download_dir = "Downloads"
            assert len([name for name in os.listdir(download_dir) if os.path.isfile(os.path.join(download_dir,
                                                                                                 name))]) == 3


# for comments refer to ThreadTests class
class CatalogTests:

    # http://
    def catalog_malformed_link_no_http_check_test(self):
        result = dry_run(catalog, "a.4cdn.org/BOARD/catalog.json")
        assert result.exit_code == 0

    # lack of link test
    def catalog_no_link_test(self):
        result = dry_run(catalog, "")
        assert result.exit_code != 0

    # omitted .json - should be implemented to pass == test
    def catalog_malformed_link_json_test(self):
        result = dry_run(catalog, "a.4cdn.org/BOARD/catalog")
        assert result.exit_code != 0
