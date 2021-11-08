from helpers import utils

def test_with_no_names(convert_str):
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

    utils.assert_font_names(font, {
        1: "Unknown",
        2: "Regular",
        4: "Unknown",
        6: "Unknown-Regular",
    })

def test_with_basic_styles(convert_str):
    plain_font = convert_str("""
        STARTFONT 2.1
        SIZE 1 72 72
        FONTBOUNDINGBOX 0 0 0 0
        STARTPROPERTIES 3
        FAMILY_NAME "Family Name"
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
    utils.assert_font_names(plain_font, {
        1: "Family Name",
        2: "Regular",
        4: "Family Name",
        6: "FamilyName-Regular",
    })

    regular_font = convert_str("""
        STARTFONT 2.1
        SIZE 1 72 72
        FONTBOUNDINGBOX 0 0 0 0
        STARTPROPERTIES 5
        FAMILY_NAME "Family Name"
        WEIGHT_NAME "Regular"
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
    utils.assert_font_names(regular_font, {
        1: "Family Name",
        2: "Regular",
        4: "Family Name",
        6: "FamilyName-Regular",
    })

    bold_font = convert_str("""
        STARTFONT 2.1
        SIZE 1 72 72
        FONTBOUNDINGBOX 0 0 0 0
        STARTPROPERTIES 4
        FAMILY_NAME "Family Name"
        WEIGHT_NAME "Bold"
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
    utils.assert_font_names(bold_font, {
        1: "Family Name",
        2: "Bold",
        4: "Family Name Bold",
        6: "FamilyName-Bold",
    })

    italic_font = convert_str("""
        STARTFONT 2.1
        SIZE 1 72 72
        FONTBOUNDINGBOX 0 0 0 0
        STARTPROPERTIES 5
        FAMILY_NAME "Family Name"
        WEIGHT_NAME "Medium"
        SLANT "I"
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
    utils.assert_font_names(italic_font, {
        1: "Family Name",
        2: "Italic",
        4: "Family Name Italic",
        6: "FamilyName-Italic",
    })

    bold_italic_font = convert_str("""
        STARTFONT 2.1
        SIZE 1 72 72
        FONTBOUNDINGBOX 0 0 0 0
        STARTPROPERTIES 5
        FAMILY_NAME "Family Name"
        WEIGHT_NAME "Bold"
        SLANT "I"
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
    utils.assert_font_names(bold_italic_font, {
        1: "Family Name",
        2: "Bold Italic",
        4: "Family Name Bold Italic",
        6: "FamilyName-BoldItalic",
    })

def test_with_full_styles(convert_str):
    extra_styles_font = convert_str("""
        STARTFONT 2.1
        SIZE 1 72 72
        FONTBOUNDINGBOX 0 0 0 0
        STARTPROPERTIES 5
        FAMILY_NAME "Family Name"
        SETWIDTH_NAME "Condensed"
        ADD_STYLE_NAME "Extra"
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
    utils.assert_font_names(extra_styles_font, {
        1: "Family Name Condensed Extra",
        2: "Regular",
        4: "Family Name Condensed Extra",
        6: "FamilyNameCondensedExtra-Regular",
    })

    all_styles_font = convert_str("""
        STARTFONT 2.1
        SIZE 1 72 72
        FONTBOUNDINGBOX 0 0 0 0
        STARTPROPERTIES 7
        FAMILY_NAME "Family Name"
        SETWIDTH_NAME "Condensed"
        ADD_STYLE_NAME "Extra"
        WEIGHT_NAME "Semibold"
        SLANT "RO"
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
    utils.assert_font_names(all_styles_font, {
        1: "Family Name Condensed Extra",
        2: "Semibold Reverse Oblique",
        4: "Family Name Condensed Extra Semibold Reverse Oblique",
        6: "FamilyNameCondensedExtra-SemiboldReverseOblique",
    })

def test_numeric_weight_names(convert_str):
    relative_weight_0 = convert_str("""
        STARTFONT 2.1
        SIZE 1 72 72
        FONTBOUNDINGBOX 0 0 0 0
        STARTPROPERTIES 5
        FAMILY_NAME "Family Name"
        RELATIVE_WEIGHT 0
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
    utils.assert_font_names(relative_weight_0, {
        1: "Family Name",
        2: "Regular",
        4: "Family Name",
        6: "FamilyName-Regular",
    })

    relative_weight_20 = convert_str("""
        STARTFONT 2.1
        SIZE 1 72 72
        FONTBOUNDINGBOX 0 0 0 0
        STARTPROPERTIES 5
        FAMILY_NAME "Family Name"
        RELATIVE_WEIGHT 20
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
    utils.assert_font_names(relative_weight_20, {
        1: "Family Name",
        2: "Extra Light",
        4: "Family Name Extra Light",
        6: "FamilyName-ExtraLight",
    })

    relative_weight_50 = convert_str("""
        STARTFONT 2.1
        SIZE 1 72 72
        FONTBOUNDINGBOX 0 0 0 0
        STARTPROPERTIES 5
        FAMILY_NAME "Family Name"
        RELATIVE_WEIGHT 50
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
    utils.assert_font_names(relative_weight_50, {
        1: "Family Name",
        2: "Regular",
        4: "Family Name",
        6: "FamilyName-Regular",
    })

    relative_weight_70 = convert_str("""
        STARTFONT 2.1
        SIZE 1 72 72
        FONTBOUNDINGBOX 0 0 0 0
        STARTPROPERTIES 5
        FAMILY_NAME "Family Name"
        RELATIVE_WEIGHT 70
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
    utils.assert_font_names(relative_weight_70, {
        1: "Family Name",
        2: "Bold",
        4: "Family Name Bold",
        6: "FamilyName-Bold",
    })

    relative_weight_invalid = convert_str("""
        STARTFONT 2.1
        SIZE 1 72 72
        FONTBOUNDINGBOX 0 0 0 0
        STARTPROPERTIES 5
        FAMILY_NAME "Family Name"
        RELATIVE_WEIGHT 77
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
    utils.assert_font_names(relative_weight_invalid, {
        1: "Family Name",
        2: "Regular",
        4: "Family Name",
        6: "FamilyName-Regular",
    })

    relative_weight_and_weight_name = convert_str("""
        STARTFONT 2.1
        SIZE 1 72 72
        FONTBOUNDINGBOX 0 0 0 0
        STARTPROPERTIES 6
        FAMILY_NAME "Family Name"
        RELATIVE_WEIGHT 10
        WEIGHT_NAME "Heavy"
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

    utils.assert_font_names(relative_weight_and_weight_name, {
        1: "Family Name",
        2: "Heavy",
        4: "Family Name Heavy",
        6: "FamilyName-Heavy",
    })
