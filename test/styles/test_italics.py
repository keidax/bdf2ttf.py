from helpers import utils

def test_with_no_slants(convert_str):
    font = convert_str("""
        STARTFONT 2.1
        SIZE 1 72 72
        FONTBOUNDINGBOX 0 0 0 0
        STARTPROPERTIES 2
        FONT_ASCENT 1
        FONT_DESCENT 0
        ENDPROPERTIES
        CHARS 1
        STARTCHAR space
        ENCODING 32
        DWIDTH 1 0
        BBX 0 0 0 0
        BITMAP
        ENDCHAR
        ENDFONT
        """)
    utils.assert_font_style(font, bold=False, italic=False, regular=True)


def test_with_slant_codes(convert_str):
    xlfd_slant_normal = convert_str("""
        STARTFONT 2.1
        FONT -misc-Family Name--R---1-10-72-72-C-10-ISO10646-1
        SIZE 1 72 72
        FONTBOUNDINGBOX 0 0 0 0
        STARTPROPERTIES 2
        FONT_ASCENT 1
        FONT_DESCENT 0
        ENDPROPERTIES
        CHARS 1
        STARTCHAR space
        ENCODING 32
        DWIDTH 1 0
        BBX 0 0 0 0
        BITMAP
        ENDCHAR
        ENDFONT
        """)
    utils.assert_font_style(xlfd_slant_normal, bold=False, italic=False, regular=True)

    xlfd_slant_italic = convert_str("""
        STARTFONT 2.1
        FONT -misc-Family Name--I---1-10-72-72-C-10-ISO10646-1
        SIZE 1 72 72
        FONTBOUNDINGBOX 0 0 0 0
        STARTPROPERTIES 2
        FONT_ASCENT 1
        FONT_DESCENT 0
        ENDPROPERTIES
        CHARS 1
        STARTCHAR space
        ENCODING 32
        DWIDTH 1 0
        BBX 0 0 0 0
        BITMAP
        ENDCHAR
        ENDFONT
        """)
    utils.assert_font_style(xlfd_slant_italic, bold=False, italic=True, regular=False)

    property_slant_normal = convert_str("""
        STARTFONT 2.1
        SIZE 1 72 72
        FONTBOUNDINGBOX 0 0 0 0
        STARTPROPERTIES 3
        SLANT "R"
        FONT_ASCENT 1
        FONT_DESCENT 0
        ENDPROPERTIES
        CHARS 1
        STARTCHAR space
        ENCODING 32
        DWIDTH 1 0
        BBX 0 0 0 0
        BITMAP
        ENDCHAR
        ENDFONT
        """)
    utils.assert_font_style(property_slant_normal, bold=False, italic=False, regular=True)

    property_slant_oblique = convert_str("""
        STARTFONT 2.1
        SIZE 1 72 72
        FONTBOUNDINGBOX 0 0 0 0
        STARTPROPERTIES 3
        SLANT "O"
        FONT_ASCENT 1
        FONT_DESCENT 0
        ENDPROPERTIES
        CHARS 1
        STARTCHAR space
        ENCODING 32
        DWIDTH 1 0
        BBX 0 0 0 0
        BITMAP
        ENDCHAR
        ENDFONT
        """)
    utils.assert_font_style(property_slant_oblique, bold=False, italic=True, regular=False)
