from pathlib import Path
from subprocess import run

from fontTools.ttLib.ttFont import TTFont

from helpers import utils

def test_with_no_names(convert):
    in_file = "test/names/noname.bdf"
    font = convert(in_file)

    utils.assert_font_names(font, {
        1: "Unknown",
        2: "Regular",
        4: "Unknown",
        6: "Unknown-Regular",
    })
