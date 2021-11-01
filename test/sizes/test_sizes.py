from helpers import utils
from fontTools.pens.recordingPen import RecordingPen

def test_with_simple_glyph(convert_str):
    font = convert_str("""
        STARTFONT 2.1
        FONT --------------
        SIZE 3 72 72
        FONTBOUNDINGBOX 0 0 0 0
        STARTPROPERTIES 2
        FONT_ASCENT 3
        FONT_DESCENT 0
        ENDPROPERTIES
        CHARS 1
        STARTCHAR bar
        ENCODING 124
        SWIDTH 120 0
        DWIDTH 3 0
        BBX 1 3 1 0
        BITMAP
        8
        8
        8
        ENDCHAR
        ENDFONT
        """)

    head = font["head"]
    assert head.unitsPerEm == 1023

    glyphs = font.getGlyphSet()
    bar = glyphs["bar"]
    assert bar.width == 1023
    assert bar.lsb == 341

    pen = RecordingPen()
    bar.draw(pen)

    # Glyph is drawn as a rectangle in clockwise order
    assert pen.value == [
        ('moveTo', ((341, 0),)),
        ('lineTo', ((341, 1023),)),
        ('lineTo', ((682, 1023),)),
        ('lineTo', ((682, 0),)),
        ('closePath', ())
    ]
