"""Convert bitmap fonts into TTF format."""

import argparse
import re
import sys
import time

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


class Font:
    def __init__(self, bdf_font: bdflib.model.Font):
        self.calculate_sizes(bdf_font)
        self.build_attributes(bdf_font)
        self.build_glyphs(bdf_font)


    def calculate_sizes(self, bdf_font) -> None:
        # This *should* be the actual vertical size of our font, in pixels
        self.font_size : int = int(round(
            bdf_font[b'RESOLUTION_Y'] * bdf_font[b'POINT_SIZE'] / 72.0))

        self.ascent : int = int(bdf_font[b'FONT_ASCENT'])
        self.descent : int = int(bdf_font[b'FONT_DESCENT'])
        assert (self.ascent + self.descent) == self.font_size

        # pixel_size is the distance between pseudo-pixels in our outline font, in em
        # coordinates. Make sure it divides evenly into final em size.
        self.pixel_size : int = int(1024 / self.font_size)
        self.em_size : int = self.font_size * self.pixel_size


    def build_attributes(self, bdf_font) -> None:
        self.copyright = None
        self.version = 1.0
        self.human_name = None
        self.postscript_name = None

        base_family = None
        extra_style = None
        slant_code = None
        width = None
        weight = None

        if b'COPYRIGHT' in bdf_font:
            self.copyright = bdf_font[b'COPYRIGHT'].decode()

        if b'FONT_VERSION' in bdf_font:
            version = bdf_font[b'FONT_VERSION'].decode()
            try:
                self.version = float(version)
            except ValueError:
                # TODO: warning
                pass

        if b'FACE_NAME' in bdf_font:
            # bdflib will assign the FONT property to FACE_NAME, even if it's an
            # XLFD string. We can detect this and assign other properties based on
            # the XLFD name contents.
            face_name_property = bdf_font[b'FACE_NAME'].decode()
            xlfd_fields = self.parse_xlfd_name_fields(face_name_property)

            if xlfd_fields:
                _, base_family, weight, slant_code, width, extra_style, _, _, _, _, _, _, _, _ = xlfd_fields
            else:
                # Assume that FACE_NAME was actually specified, so we should
                # consider it as the canonical human name.
                self.human_name = face_name_property

        if b'FAMILY_NAME' in bdf_font:
            base_family = bdf_font[b'FAMILY_NAME'].decode()

        if b'WEIGHT_NAME' in bdf_font:
            weight = bdf_font[b'WEIGHT_NAME'].decode()

        if b'SLANT' in bdf_font:
            slant_code = bdf_font[b'SLANT'].decode()

        if b'SETWIDTH_NAME' in bdf_font:
            width = bdf_font[b'SETWIDTH_NAME'].decode()

        if b'ADD_STYLE_NAME' in bdf_font:
            extra_style = bdf_font[b'ADD_STYLE_NAME'].decode()

        if b'FONT_NAME' in bdf_font:
            self.postscript_name = bdf_font[b'FONT_NAME'].decode()

        self.family = self.generate_family(base_family, width, extra_style)
        self.style = self.generate_style(slant_code, weight)

        if not self.human_name:
            if self.style == "Regular":
                self.human_name = self.family
            else:
                self.human_name = f"{self.family} {self.style}"

        if not self.postscript_name:
            self.postscript_name = f"{self.family}-{self.style}".replace(" ", "")

        # if weight:
        #     font.weight = weight


    def generate_family(self, base_family, width, extra_style):
        regular_widths = {"medium", "normal", "regular"}

        family = "Unknown"

        if base_family:
            family = base_family

        if width and width.lower() not in regular_widths:
            family += f" {width}"

        if extra_style:
            family += f" {extra_style}"

        return family


    def generate_style(self, slant_code, weight):
        regular_weights = {"medium", "normal", "regular"}
        slants = {"I": "Italic", "O": "Oblique", "RI": "Reverse Italic", "RO": "Reverse Oblique"}

        weight_name = None
        if weight and weight.lower() not in regular_weights:
            weight_name = weight

        # TODO: set numeric weight and bold flag

        slant_name = None
        if slant_code and slant_code in slants:
            slant_name = slants[slant_code]
            self.is_italic = True
        else:
            self.is_italic = False

        self.is_regular = False

        if weight_name and slant_name:
            return f"{weight_name} {slant_name}"
        elif weight_name:
            return weight_name
        elif slant_name:
            return slant_name
        else:
            self.is_regular = True
            return "Regular"

    # If the string is a valid XLFD name, return a list of the fourteen XLFD properties.
    # Otherwise, return None.
    # See the XLFD specification for details:
    # https://www.x.org/releases/X11R7.6/doc/xorg-docs/specs/XLFD/xlfd.html#fontname
    def parse_xlfd_name_fields(self, name):
        if not name.startswith("-"):
            return None

        if name.count("-") != 14:
            return None

        return name.split("-")[1:]


    def build_glyphs(self, bdf_font):
        self.glyphs = OrderedDict()

        a_to_z_widths = 0
        a_to_z_count = 0

        for bdf_glyph in bdf_font.glyphs:
            codepoint = bdf_glyph.codepoint
            name = bdf_glyph.name.decode()
            advance_width = bdf_glyph.advance * self.pixel_size
            glyph = self.build_tt_glyph(bdf_glyph)

            self.glyphs[name] = (glyph, codepoint, advance_width)

            if ord("A") <= codepoint <= ord("Z"):
                a_to_z_widths += advance_width
                a_to_z_count += 1

        if ".notdef" not in self.glyphs:
            # TODO: try to provide a default shape?
            notdef_glyph = TTGlyphPen(None).glyph()

            # Try to set .notdef's advance width to the average.
            # Otherwise, just make it a square.

            if a_to_z_count > 0:
                advance_width = int(a_to_z_widths / a_to_z_count)
            else:
                advance_width = self.em_size

            self.glyphs[".notdef"] = (notdef_glyph, -1, advance_width)

        # Make sure .notdef is the first glyph
        self.glyphs.move_to_end(".notdef", last=False)

        # TODO: handle other special glyphs: .null, CR, space?


    def build_tt_glyph(self, bdf_glyph):
        pen = TTGlyphPen(None)

        # Using the example code from bdflib:
        for x in range(bdf_glyph.bbW):
            for y in range(bdf_glyph.bbH):
                if bdf_glyph.data[y] & (1 << (bdf_glyph.bbW - x - 1)):
                    # Compute the corners of our "pixel"
                    x1 = (bdf_glyph.bbX + x) * self.pixel_size
                    x2 = x1 + self.pixel_size
                    y1 = (bdf_glyph.bbY + y) * self.pixel_size
                    y2 = y1 + self.pixel_size

                    # Draw it
                    pen.moveTo((x1, y1))
                    pen.lineTo((x1, y2))
                    pen.lineTo((x2, y2))
                    pen.lineTo((x2, y1))
                    pen.closePath()

        return pen.glyph()


    def opentype_font(self):
        fb = FontBuilder(unitsPerEm=self.em_size)

        glyph_order = list(self.glyphs.keys())
        fb.setupGlyphOrder(glyph_order)

        char_map = dict()
        glyph_map = dict()
        for name, glyph_tuple in self.glyphs.items():
            glyph, codepoint, _ = glyph_tuple

            glyph_map[name] = glyph
            if codepoint >= 0:
                char_map[codepoint] = name

        fb.setupCharacterMap(char_map)
        fb.setupGlyf(glyph_map)

        metrics = {}
        glyf_table = fb.font["glyf"]
        for name, glyph_tuple in self.glyphs.items():
            advance_width = glyph_tuple[2]
            metrics[name] = (advance_width, glyf_table[name].xMin)
        fb.setupHorizontalMetrics(metrics)

        fb.setupHorizontalHeader(ascent=self.ascent * self.pixel_size, descent=(-self.descent * self.pixel_size))
        # TODO: lineGap

        fb.updateHead(fontRevision=self.version)
        # TODO: also update macStyle

        names = {
            NameID.VERSION : f"Version {self.version:.3f}",
            NameID.FONT_FAMILY : self.family,
            NameID.FONT_SUBFAMILY : self.style,
            NameID.POSTSCRIPT_NAME : self.postscript_name,
            NameID.FULL_HUMAN_NAME : self.human_name,
            NameID.UNIQUE_IDENTIFIER : f"bdf2ttf : {self.postscript_name} : {time.strftime('%Y-%m-%d')}",
        }

        if self.copyright:
            names[NameID.COPYRIGHT] = self.copyright

        fb.setupNameTable(names)

        # TODO: set fsType = 0
        # TODO: set usWeightClass
        # TODO: strikeout size & position
        # TODO: set achVendorID = None
        # TODO: set fsSelection along with macStyle
        # TODO: set ascender values here too
        # TODO: set x height and cap height
        fb.setupOS2()

        # TODO: set underline values
        # TODO: set isFixedPitch?
        fb.setupPost()

        # Merge adjacent pixel squares and reduce extra points
        removeOverlaps(fb.font)

        return fb


def convert_bdf(infile, outfile=None, feature_file=None):
    bdf = bdflib.reader.read_bdf(infile)

    font = Font(bdf)

    font_builder = font.opentype_font()

    # if feature_file != None:
    #     font.mergeFeature(feature_file.name)

    if outfile != None:
        font_filename = outfile
    else:
        # font_filename = f"{font.fontname}.ttf"
        font_filename = f"{font.postscript_name}.ttf"

    # Output the final font
    font_builder.save(font_filename)


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
