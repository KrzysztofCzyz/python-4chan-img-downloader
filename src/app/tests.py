from click.testing import CliRunner
from pytest import skip


class DownloadTests:

    def test_one(self):
        assert 1 == 1

    def test_skipped(self):
        skip('No test me plox }:-{{')

