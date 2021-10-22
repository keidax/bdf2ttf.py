import subprocess
from inspect import cleandoc

import pytest

from fontTools.ttLib.ttFont import TTFont

# convert is a fixture that returns a function for converting BDF files.
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

# convert_str is the same as convert, but takes the contents of a file as a string.
@pytest.fixture
def convert_str(tmp_path, convert):
    def _convert_str(bdf_contents):
        in_file = tmp_path / "in_file.bdf"
        in_file.write_text(cleandoc(bdf_contents))

        return convert(in_file)

    return _convert_str
