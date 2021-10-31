"""Convert bitmap fonts into TTF format."""

import argparse
import re
import sys

from collections import OrderedDict
from enum import IntEnum

import bdflib.model
import bdflib.reader

from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib.removeOverlaps import removeOverlaps

class NameID(IntEnum):
    COPYRIGHT = 0
    FONT_FAMILY = 1
    FONT_SUBFAMILY = 2
    UNIQUE_IDENTIFIER = 3
    FULL_HUMAN_NAME = 4
    VERSION = 5
    POSTSCRIPT_NAME = 6

try:
    # bdflib will ignore the FACE_NAME property, which we don't want
    bdflib.model.IGNORABLE_PROPERTIES.remove(b'FACE_NAME')
except ValueError:
    pass

# Map BDF properties to OpenType names
def map_attributes(bdf):
    base_family = None
    slant_code = None
    weight = None
    width = None
    extra_style = None
    human_name = None
    postscript_name = None

    names = {}

    if b'COPYRIGHT' in bdf:
        names[NameID.COPYRIGHT] = bdf[b'COPYRIGHT'].decode()

    if b'FONT_VERSION' in bdf:
        names[NameID.VERSION] = bdf[b'FONT_VERSION'].decode()

    if b'FACE_NAME' in bdf:
        # bdflib will assign the FONT property to FACE_NAME, even if it's an
        # XLFD string. We can detect this and assign other properties based on
        # the XLFD name contents.
        face_name_property = bdf[b'FACE_NAME'].decode()
        xlfd_fields = parse_xlfd_name_fields(face_name_property)

        if xlfd_fields:
            _, base_family, weight, slant_code, width, extra_style, _, _, _, _, _, _, _, _ = xlfd_fields
        else:
            # Assume that FACE_NAME was actually specified, so we should
            # consider it as the canonical human name.
            human_name = face_name_property

    if b'FAMILY_NAME' in bdf:
        base_family = bdf[b'FAMILY_NAME'].decode()

    if b'WEIGHT_NAME' in bdf:
        weight = bdf[b'WEIGHT_NAME'].decode()

    if b'SLANT' in bdf:
        slant_code = bdf[b'SLANT'].decode()

    if b'SETWIDTH_NAME' in bdf:
        width = bdf[b'SETWIDTH_NAME'].decode()

    if b'ADD_STYLE_NAME' in bdf:
        extra_style = bdf[b'ADD_STYLE_NAME'].decode()

    if b'FONT_NAME' in bdf:
        postscript_name = bdf[b'FONT_NAME'].decode()

    family = generate_family(base_family, width, extra_style)
    style = generate_style(slant_code, weight)

    if not human_name:
        if style == "Regular":
            human_name = family
        else:
            human_name = f"{family} {style}"

    if not postscript_name:
        postscript_name = f"{family}-{style}".replace(" ", "")

    names[NameID.FULL_HUMAN_NAME] = human_name
    names[NameID.POSTSCRIPT_NAME] = postscript_name
    names[NameID.FONT_FAMILY] = family
    names[NameID.FONT_SUBFAMILY] = style

    # TODO: set weight

    # if weight:
    #     font.weight = weight
    return names


def generate_family(base_family, width, extra_style):
    regular_widths = {"medium", "normal", "regular"}

    family = "Unknown"

    if base_family:
        family = base_family

    if width and width.lower() not in regular_widths:
        family += f" {width}"

    if extra_style:
        family += f" {extra_style}"

    return family


def generate_style(slant_code, weight):
    regular_weights = {"medium", "normal", "regular"}
    slants = {"I": "Italic", "O": "Oblique", "RI": "Reverse Italic", "RO": "Reverse Oblique"}

    weight_name = None
    if weight and weight.lower() not in regular_weights:
        weight_name = weight

    slant_name = None
    if slant_code and slant_code in slants:
        slant_name = slants[slant_code]

    if weight_name and slant_name:
        return f"{weight_name} {slant_name}"
    elif weight_name:
        return weight_name
    elif slant_name:
        return slant_name
    else:
        return "Regular"

# If the string is a valid XLFD name, return a list of the fourteen XLFD properties.
# Otherwise, return None.
# See the XLFD specification for details:
# https://www.x.org/releases/X11R7.6/doc/xorg-docs/specs/XLFD/xlfd.html#fontname
def parse_xlfd_name_fields(name):
    if not name.startswith("-"):
        return None

    if name.count("-") != 14:
        return None

    return name.split("-")[1:]


def build_glyphs(bdf_font, pixel_size):
    glyphs = OrderedDict()

    for bdf_glyph in bdf_font.glyphs:
        codepoint = bdf_glyph.codepoint
        name = bdf_glyph.name.decode()
        advance_width = bdf_glyph.advance * pixel_size
        glyph = build_tt_glyph(bdf_glyph, pixel_size)

        glyphs[name] = (glyph, codepoint, advance_width)

        # TODO: handle special names?

    return glyphs


def build_tt_glyph(bdf_glyph, pixel_size):
    pen = TTGlyphPen(None)

    # Using the example code from bdflib:
    for x in range(bdf_glyph.bbW):
        for y in range(bdf_glyph.bbH):
            if bdf_glyph.data[y] & (1 << (bdf_glyph.bbW - x - 1)):
                # Compute the corners of our "pixel"
                x1 = (bdf_glyph.bbX + x) * pixel_size
                x2 = x1 + pixel_size
                y1 = (bdf_glyph.bbY + y) * pixel_size
                y2 = y1 + pixel_size

                # Draw it
                pen.moveTo((x1, y1))
                pen.lineTo((x1, y2))
                pen.lineTo((x2, y2))
                pen.lineTo((x2, y1))
                pen.closePath()

    return pen.glyph()


def convert_bdf(infile, outfile=None, feature_file=None):
    bdf = bdflib.reader.read_bdf(infile)

    # This *should* be the actual vertical size of our font, in pixels
    font_size = int(round(
        bdf[b'RESOLUTION_Y'] * bdf[b'POINT_SIZE'] / 72.0))

    ascent = int(bdf[b'FONT_ASCENT'])
    descent = int(bdf[b'FONT_DESCENT'])
    assert (ascent + descent) == font_size

    # pixel_size is the distance between pseudo-pixels in our outline font, in em
    # coordinates. Make sure it divides evenly into final em size.
    pixel_size = int(1024 / font_size)
    em_size = font_size * pixel_size

    fb = FontBuilder(unitsPerEm=em_size)

    glyphs = build_glyphs(bdf_font=bdf, pixel_size=pixel_size)

    glyph_order = list(glyphs.keys())
    fb.setupGlyphOrder(glyph_order)

    char_map = dict()
    for name, glyph_tuple in glyphs.items():
        codepoint = glyph_tuple[1]
        if codepoint >= 0:
            char_map[codepoint] = name
    fb.setupCharacterMap(char_map)

    glyph_map = dict()
    for name, glyph_tuple in glyphs.items():
        glyph = glyph_tuple[0]
        glyph_map[name] = glyph
    fb.setupGlyf(glyph_map)

    metrics = {}
    glyf_table = fb.font["glyf"]
    for name, glyph_tuple in glyphs.items():
        advance_width = glyph_tuple[2]
        metrics[name] = (advance_width, glyf_table[name].xMin)
    fb.setupHorizontalMetrics(metrics)

    fb.setupHorizontalHeader(ascent=ascent * pixel_size, descent=(-descent * pixel_size))

    names = map_attributes(bdf)

    version_string = "1.0"
    version_float = 1.0
    if NameID.VERSION in names:
        version_string = names[NameID.VERSION]
        try:
            version_float = float(version_string)
        except ValueError:
            # TODO: warning
            pass

    names[NameID.VERSION] = f"Version {version_string}"
    fb.setupNameTable(names)
    fb.updateHead(fontRevision=version_float)

    fb.setupOS2()
    fb.setupPost()

    # Merge adjacent pixel squares and reduce extra points
    removeOverlaps(fb.font)

    # if feature_file != None:
    #     font.mergeFeature(feature_file.name)

    if outfile != None:
        font_filename = outfile
    else:
        # font_filename = f"{font.fontname}.ttf"
        font_filename = f"{'asdf'}.ttf"

    # Output the final font
    fb.save(font_filename)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("infile", type=argparse.FileType("rb"), help="""
            The bitmap font to convert. Must be either a BDF font file, or an
            SFD file containing a bitmap font.
            """)
    parser.add_argument("-o", "--out", help="""
            The TTF font file to output. If not specified, will be generated
            based on the font name and weight.
            """)
    parser.add_argument("-f", "--feature-file", type=argparse.FileType("rb"), help="""
            Include feature information from an OpenType feature file in the
            final font.
            """)

    args = parser.parse_args()
    convert_bdf(args.infile, outfile=args.out, feature_file=args.feature_file)


if __name__ == '__main__':
    main()
