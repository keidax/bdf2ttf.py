import subprocess
from inspect import cleandoc

import pytest

from fontTools.ttLib.ttFont import TTFont

# convert is a fixture that returns a function for converting BDF files.
@pytest.fixture
def convert(tmp_path, capfd):
    def _convert(filename, feature_filename=None):
        out_file = tmp_path / "converted_file.ttf"

        command = f"python -m bdf2ttf.convert {filename} -o {out_file}"

        if feature_filename:
            command += f" -f {feature_filename}"

        process = subprocess.run(
            command,
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
    def _convert_str(bdf_contents, feature_contents=None):
        in_file = tmp_path / "in_file.bdf"
        in_file.write_text(cleandoc(bdf_contents))

        feature_file = None
        if feature_contents:
            feature_file = tmp_path / "in.fea"
            feature_file.write_text(cleandoc(feature_contents))

        return convert(in_file, feature_file)

    return _convert_str
