from helpers import utils

def test_with_no_weights(convert_str):
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
    utils.assert_font_weight(font, 400)
    utils.assert_font_style(font, bold=False, italic=False, regular=True)

def test_with_weight_names_only(convert_str):
    light_font = convert_str("""
        STARTFONT 2.1
        FONT -misc-Family Name-Light-R-Normal--1-10-72-72-C-10-ISO10646-1
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
    utils.assert_font_weight(light_font, 300)
    utils.assert_font_style(light_font, bold=False, italic=False, regular=False)

    regular_font = convert_str("""
        STARTFONT 2.1
        FONT -misc-Family Name-Regular-R-Normal--1-10-72-72-C-10-ISO10646-1
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
    utils.assert_font_weight(regular_font, 400)
    utils.assert_font_style(regular_font, bold=False, italic=False, regular=True)

    medium_font = convert_str("""
        STARTFONT 2.1
        FONT -misc-Family Name-Medium-R-Normal--1-10-72-72-C-10-ISO10646-1
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
    utils.assert_font_weight(medium_font, 500)
    utils.assert_font_style(medium_font, bold=False, italic=False, regular=True)

    bold_font = convert_str("""
        STARTFONT 2.1
        FONT -misc-Family Name-Bold-R-Normal--1-10-72-72-C-10-ISO10646-1
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
    utils.assert_font_weight(bold_font, 700)
    utils.assert_font_style(bold_font, bold=True, italic=False, regular=False)

def test_with_relative_weights_only(convert_str):
    thin_font = convert_str("""
        STARTFONT 2.1
        FONT -misc-Family Name--R-Normal--1-10-72-72-C-10-ISO10646-1
        SIZE 1 72 72
        FONTBOUNDINGBOX 0 0 0 0
        STARTPROPERTIES 3
        RELATIVE_WEIGHT 10
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
    utils.assert_font_weight(thin_font, 100)
    utils.assert_font_style(thin_font, bold=False, italic=False, regular=False)

    regular_font = convert_str("""
        STARTFONT 2.1
        FONT -misc-Family Name--R-Normal--1-10-72-72-C-10-ISO10646-1
        SIZE 1 72 72
        FONTBOUNDINGBOX 0 0 0 0
        STARTPROPERTIES 3
        RELATIVE_WEIGHT 50
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
    utils.assert_font_weight(regular_font, 400)
    utils.assert_font_style(regular_font, bold=False, italic=False, regular=True)

    extra_bold_font = convert_str("""
        STARTFONT 2.1
        FONT -misc-Family Name--R-Normal--1-10-72-72-C-10-ISO10646-1
        SIZE 1 72 72
        FONTBOUNDINGBOX 0 0 0 0
        STARTPROPERTIES 3
        RELATIVE_WEIGHT 80
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
    utils.assert_font_weight(extra_bold_font, 800)
    utils.assert_font_style(extra_bold_font, bold=True, italic=False, regular=False)

def test_with_names_and_relative_weights(convert_str):
    font = convert_str("""
        STARTFONT 2.1
        FONT -misc-Family Name-Thin-R-Normal--1-10-72-72-C-10-ISO10646-1
        SIZE 1 72 72
        FONTBOUNDINGBOX 0 0 0 0
        STARTPROPERTIES 4
        WEIGHT_NAME "Normal"
        RELATIVE_WEIGHT 90
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
    utils.assert_font_weight(font, 400)
    utils.assert_font_style(font, bold=False, italic=False, regular=True)
