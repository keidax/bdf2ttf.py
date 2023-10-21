from helpers import utils


def test_with_empty_xlfd_name(convert_str):
    font = convert_str("""
        STARTFONT 2.1
        FONT --------------
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

def test_with_invalid_xlfd_syntax(convert_str):
    almost_xlfd = convert_str("""
        STARTFONT 2.1
        FONT -misc-Family Name-Bold-I-Narrow-Extra-1-10-72-72-C-10-ISO10646
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

    utils.assert_font_names(almost_xlfd, {
        1: "Unknown",
        2: "Regular",
        4: "Unknown",
        6: "Unknown-Regular",
    })


def test_with_empty_xlfd_name_and_property_styles(convert_str):
    font = convert_str("""
        STARTFONT 2.1
        FONT --------------
        SIZE 1 72 72
        FONTBOUNDINGBOX 0 0 0 0
        STARTPROPERTIES 5
        FAMILY_NAME "Family Name 2"
        RELATIVE_WEIGHT 70
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

    utils.assert_font_names(font, {
        1: "Family Name 2",
        2: "Bold Italic",
        4: "Family Name 2 Bold Italic",
        6: "FamilyName2-BoldItalic",
    })


def test_with_only_xlfd_name(convert_str):
    font = convert_str("""
        STARTFONT 2.1
        FONT -misc-Family Name-Bold-I-Narrow-Extra-1-10-72-72-C-10-ISO10646-1
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
        1: "Family Name Narrow Extra",
        2: "Bold Italic",
        4: "Family Name Narrow Extra Bold Italic",
        6: "FamilyNameNarrowExtra-BoldItalic",
    })

def test_with_xlfd_name_and_property_styles(convert_str):
    regular_font = convert_str("""
        STARTFONT 2.1
        FONT -misc-Family Name-Bold-I-Normal--1-10-72-72-C-10-ISO10646-1
        SIZE 1 72 72
        FONTBOUNDINGBOX 0 0 0 0
        STARTPROPERTIES 5
        FAMILY_NAME "Family Name 2"
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
        1: "Family Name 2",
        2: "Regular",
        4: "Family Name 2",
        6: "FamilyName2-Regular",
    })

    font_with_bold_relative_weight = convert_str("""
        STARTFONT 2.1
        FONT -misc-Family Name-Light-I-Normal--1-10-72-72-C-10-ISO10646-1
        SIZE 1 72 72
        FONTBOUNDINGBOX 0 0 0 0
        STARTPROPERTIES 5
        FAMILY_NAME "Family Name 2"
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

    utils.assert_font_names(font_with_bold_relative_weight, {
        1: "Family Name 2",
        2: "Light",
        4: "Family Name 2 Light",
        6: "FamilyName2-Light",
    })


def test_with_xlfd_name_and_all_properties(convert_str):
    font = convert_str("""
        STARTFONT 2.1
        FONT -misc-Family Name-Bold-R-Normal--1-10-72-72-C-10-ISO10646-1
        SIZE 1 72 72
        FONTBOUNDINGBOX 0 0 0 0
        STARTPROPERTIES 7
        FAMILY_NAME "Family Name 3"
        SETWIDTH_NAME "Expanded"
        ADD_STYLE_NAME "Fancy"
        WEIGHT_NAME "Book"
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

    utils.assert_font_names(font, {
        1: "Family Name 3 Expanded Fancy",
        2: "Book Oblique",
        4: "Family Name 3 Expanded Fancy Book Oblique",
        6: "FamilyName3ExpandedFancy-BookOblique",
    })


def test_with_xlfd_name_and_overrides(convert_str):
    font = convert_str("""
        STARTFONT 2.1
        FONT -misc-Family Name-Bold-R-Normal--1-10-72-72-C-10-ISO10646-1
        SIZE 1 72 72
        FONTBOUNDINGBOX 0 0 0 0
        STARTPROPERTIES 9
        FONT_ASCENT 1
        FONT_DESCENT 0
        FAMILY_NAME "Family Name 3"
        SETWIDTH_NAME "Expanded"
        ADD_STYLE_NAME "Fancy"
        WEIGHT_NAME "Book"
        SLANT "O"
        FACE_NAME "This is the human name"
        FONT_NAME "ThisIsThePostScriptName"
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
        1: "Family Name 3 Expanded Fancy",
        2: "Book Oblique",
        4: "This is the human name",
        6: "ThisIsThePostScriptName",
    })


def test_with_xlfd_as_face_name(convert_str):
    font = convert_str("""
        STARTFONT 2.1
        FONT -misc-Family Name-Bold-R-Normal--1-10-72-72-C-10-ISO10646-1
        SIZE 1 72 72
        FONTBOUNDINGBOX 0 0 0 0
        STARTPROPERTIES 3
        FONT_ASCENT 1
        FONT_DESCENT 0
        FACE_NAME "-misc-Family Name 2-Medium-I-Condensed--1-10-72-72-C-10-ISO10646-1"
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
        1: "Family Name 2 Condensed",
        2: "Italic",
        4: "Family Name 2 Condensed Italic",
        6: "FamilyName2Condensed-Italic",
    })


def test_with_xlfd_as_face_name_and_all_properties(convert_str):
    font = convert_str("""
        STARTFONT 2.1
        FONT -misc-Family Name-Bold-R-Normal--1-10-72-72-C-10-ISO10646-1
        SIZE 1 72 72
        FONTBOUNDINGBOX 0 0 0 0
        STARTPROPERTIES 9
        FONT_ASCENT 1
        FONT_DESCENT 0
        FACE_NAME "-misc-Family Name-Bold-R-Normal--1-10-72-72-C-10-ISO10646-1"
        FONT_NAME "ThisIsThePostScriptName"
        FAMILY_NAME "Family Name 3"
        SETWIDTH_NAME "Expanded"
        ADD_STYLE_NAME "Fancy"
        WEIGHT_NAME "Book"
        SLANT "O"
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
        1: "Family Name 3 Expanded Fancy",
        2: "Book Oblique",
        4: "Family Name 3 Expanded Fancy Book Oblique",
        6: "ThisIsThePostScriptName",
    })
