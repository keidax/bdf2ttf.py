import subprocess

import pytest

from fontTools.ttLib.ttFont import TTFont

# convert is a fixture that returns a function for converting files.
@pytest.fixture
def convert(tmp_path, capfd):
    def _convert(filename):
        out_file = tmp_path / "converted_file.ttf"

        process = subprocess.run(
            f"python -m bdf2ttf.convert {filename} -o {out_file}",
            shell=True,
            stderr=subprocess.STDOUT
        )

        __tracebackhide__ = True
        if process.returncode:
            pytest.fail(f"failed to convert:\n{capfd.readouterr().out}")

        assert out_file.exists()

        return TTFont(out_file)

    return _convert
