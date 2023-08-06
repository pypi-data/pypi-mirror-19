from click.testing import CliRunner
import tempfile

from imagefactory.cli import main


def test_commands():
    runner = CliRunner()
    with tempfile.TemporaryDirectory() as tmpdir:
        result = runner.invoke(main, ['--savedir', tmpdir])
    assert result.exit_code == 0
    assert result.output == ''
