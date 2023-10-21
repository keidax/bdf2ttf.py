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
from fontTools.feaLib.builder import addOpenTypeFeatures


class NameID(IntEnum):
    COPYRIGHT = 0
    FONT_FAMILY = 1
    FONT_SUBFAMILY = 2
    UNIQUE_IDENTIFIER = 3
    FULL_HUMAN_NAME = 4
    VERSION = 5
    POSTSCRIPT_NAME = 6
    TRADEMARK = 7


class Font:
    def __init__(self, bdf_font: bdflib.model.Font):
        self.calculate_sizes(bdf_font)
        self.build_attributes(bdf_font)
        self.build_glyphs(bdf_font)


    def calculate_sizes(self, bdf_font) -> None:
        # This *should* be the actual vertical size of our font, in pixels
        self.font_size : int = int(round(bdf_font.ydpi * bdf_font.ptSize / 72.0))

        self.ascent : int = int(bdf_font[b'FONT_ASCENT'])
        self.descent : int = int(bdf_font[b'FONT_DESCENT'])
        assert (self.ascent + self.descent) == self.font_size

        self.x_height : int = 0
        self.cap_height : int = 0
        self.underline_position : int = round(self.descent / 2)
        self.underline_thickness : int = 1

        if b'X_HEIGHT' in bdf_font:
            self.x_height = int(bdf_font[b'X_HEIGHT'])

        if b'CAP_HEIGHT' in bdf_font:
            self.cap_height = int(bdf_font[b'CAP_HEIGHT'])

        if b'UNDERLINE_POSITION' in bdf_font:
            # XLFD documentation says an underline position below the baseline
            # should be a positive number, but most existing BDF fonts seem to
            # use negative numbers. We assume underline is always under the
            # baseline, so treat this as a positive number.
            self.underline_position = abs(int(bdf_font[b'UNDERLINE_POSITION']))

        if b'UNDERLINE_THICKNESS' in bdf_font:
            self.underline_thickness = int(bdf_font[b'UNDERLINE_THICKNESS'])


        # pixel_size is the distance between pseudo-pixels in our outline font, in em
        # coordinates. Make sure it divides evenly into final em size.
        self.pixel_size : int = int(1024 / self.font_size)
        self.em_size : int = self.font_size * self.pixel_size


    def build_attributes(self, bdf_font) -> None:
        self.copyright = None
        self.trademark_notice = None
        self.version = 1.0
        self.human_name = None
        self.postscript_name = None

        base_family = None
        extra_style = None
        slant_code = None
        width = None
        weight_name = None
        relative_weight = None
        spacing = None

        if b'COPYRIGHT' in bdf_font:
            self.copyright = bdf_font[b'COPYRIGHT'].decode()

        if b'NOTICE' in bdf_font:
            self.trademark_notice = bdf_font[b'NOTICE'].decode()

        if b'FONT_VERSION' in bdf_font:
            version = bdf_font[b'FONT_VERSION'].decode()
            try:
                self.version = float(version)
            except ValueError:
                # TODO: warning
                pass

        # This is the name specified with the FONT keyword, which is usually but not always in XLFD format.
        if bdf_font.name:
            font_name = bdf_font.name.decode()
            xlfd_fields = self.parse_xlfd_name_fields(font_name)

            if xlfd_fields:
                _, base_family, weight_name, slant_code, width, extra_style, _, _, _, _, spacing, _, _, _ = xlfd_fields
            else:
                # TODO: warning
                pass

        if b'FACE_NAME' in bdf_font:
            # Check if FACE_NAME was specified as an XLFD string
            face_name_property = bdf_font[b'FACE_NAME'].decode()
            xlfd_fields = self.parse_xlfd_name_fields(face_name_property)

            if xlfd_fields:
                _, base_family, weight_name, slant_code, width, extra_style, _, _, _, _, spacing, _, _, _ = xlfd_fields
            else:
                # FACE_NAME was specified as the canonical human name
                self.human_name = face_name_property

        if b'FAMILY_NAME' in bdf_font:
            base_family = bdf_font[b'FAMILY_NAME'].decode()

        if b'WEIGHT_NAME' in bdf_font:
            weight_name = bdf_font[b'WEIGHT_NAME'].decode()

        if b'RELATIVE_WEIGHT' in bdf_font:
            relative_weight = int(bdf_font[b'RELATIVE_WEIGHT'])

        if b'SLANT' in bdf_font:
            slant_code = bdf_font[b'SLANT'].decode()

        if b'SETWIDTH_NAME' in bdf_font:
            width = bdf_font[b'SETWIDTH_NAME'].decode()

        if b'ADD_STYLE_NAME' in bdf_font:
            extra_style = bdf_font[b'ADD_STYLE_NAME'].decode()

        if b'FONT_NAME' in bdf_font:
            self.postscript_name = bdf_font[b'FONT_NAME'].decode()

        if b'SPACING' in bdf_font:
            spacing = bdf_font[b'SPACING'].decode()

        self.family = self.generate_family(base_family, width, extra_style)
        self.style = self.generate_style(slant_code, weight_name, relative_weight)

        if not self.human_name:
            if self.style == "Regular":
                self.human_name = self.family
            else:
                self.human_name = f"{self.family} {self.style}"

        if not self.postscript_name:
            self.postscript_name = f"{self.family}-{self.style}".replace(" ", "")

        if spacing and spacing.upper() in {"M", "C"}:
            self.is_monospace = True
        else:
            self.is_monospace = False

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


    def generate_style(self, slant_code, weight_name, relative_weight):
        style_weight_name = self.calculate_weight_name(weight_name, relative_weight)
        style_slant_name = self.calculate_slant_name(slant_code)

        self.is_regular = False
        if style_weight_name and style_slant_name:
            return f"{style_weight_name} {style_slant_name}"
        elif style_weight_name:
            return style_weight_name
        elif style_slant_name:
            return style_slant_name
        else:
            self.is_regular = True
            return "Regular"


    # Calculate the slant of the font.
    # Return an appropriate slant name for the font style.
    # TODO: we could also come up with the italic angle for the font
    def calculate_slant_name(self, slant_code):
        slants = {"I": "Italic", "O": "Oblique", "RI": "Reverse Italic", "RO": "Reverse Oblique"}

        slant_name = None
        if slant_code and slant_code in slants:
            slant_name = slants[slant_code]
            self.is_italic = True
        else:
            self.is_italic = False

        return slant_name


    # Calculate a numeric weight and a weight name based on the inputs.
    # Return an appropriate weight name for the font style.
    def calculate_weight_name(self, weight_name, relative_weight):
        weight_name_mapping = {
            ("thin", "extrathin", "ultrathin", "hairline"): 100,
            ("extralight", "ultralight"): 200,
            ("light", "semilight", "demilight"): 300,
            ("regular", "normal", "book"): 400,
            ("medium",): 500,
            ("semibold", "demibold"): 600,
            ("bold",): 700,
            ("extrabold", "ultrabold"): 800,
            ("black", "extrablack", "ultrablack", "heavy") : 900,
        }
        relative_weight_mapping = {
            10: 100,
            20: 200,
            30: 300,
            40: 300,
            50: 400,
            60: 600,
            70: 700,
            80: 800,
            90: 900
        }
        canonical_weight_names = {
            100: "Thin",
            200: "Extra Light",
            300: "Light",
            400: "Regular",
            500: "Medium",
            600: "Semi Bold",
            700: "Bold",
            800: "Extra Bold",
            900: "Black",
        }
        regular_weight_names = {"medium", "normal", "regular"}

        self.weight_value = None
        if weight_name:
            for names, value in weight_name_mapping.items():
                if weight_name.lower().replace(" ", "").replace("-", "") in names:
                    self.weight_value = value
        elif relative_weight and relative_weight in relative_weight_mapping:
            self.weight_value = relative_weight_mapping[relative_weight]

        if not self.weight_value:
            self.weight_value = 400

        if self.weight_value > 600:
            self.is_bold = True
        else:
            self.is_bold = False

        self.weight_name = None
        if weight_name:
            self.weight_name = weight_name
        else:
            self.weight_name = canonical_weight_names[self.weight_value]

        if self.weight_name.lower() in regular_weight_names:
            # The weight is "regular", so it should not be part of the font's style name.
            return None
        else:
            return self.weight_name


    # If the string is a valid XLFD name, return a list of the fourteen XLFD properties.
    # Otherwise, return None.
    # See the XLFD specification for details:
    # https://www.x.org/releases/X11R7.6/doc/xorg-docs/specs/XLFD/xlfd.html#fontname
    def parse_xlfd_name_fields(self, name):
        if not name.startswith("-"):
            return None

        if name.count("-") != 14:
            return None

        fields = name.split("-")[1:]
        return fields


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


    def mac_style(self):
        mac_style = 0
        if self.is_bold:
            mac_style |= 1 << 0
        if self.is_italic:
            mac_style |= 1 << 1

        return mac_style


    def fs_selection(self):
        fs_selection = 0
        if self.is_italic:
            fs_selection |= 1 << 0
        if self.is_bold:
            fs_selection |= 1 << 5
        if self.is_regular:
            fs_selection |= 1 << 6

        # Should always be set for new fonts
        fs_selection |= 1 << 7

        return fs_selection


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

        font_ascent = self.ascent * self.pixel_size
        font_descent = -self.descent * self.pixel_size # specified as a negative value
        line_gap = 0

        fb.setupHorizontalHeader(
            ascent=font_ascent,
            descent=font_descent,
            lineGap=line_gap,
        )

        fb.updateHead(
            fontRevision=self.version,
            lowestRecPPEM=self.font_size,
            macStyle=self.mac_style(),
        )

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
        if self.trademark_notice:
            names[NameID.TRADEMARK] = self.trademark_notice

        fb.setupNameTable(names)

        x_height = self.x_height * self.pixel_size
        cap_height = self.cap_height * self.pixel_size
        underline_position = -self.underline_position * self.pixel_size
        underline_thickness = self.underline_thickness * self.pixel_size

        # TODO: set win metrics to max bounding box?
        fb.setupOS2(
            version=4,

            fsType=0,
            usWeightClass=self.weight_value,
            fsSelection=self.fs_selection(),

            sTypoAscender=font_ascent,
            sTypoDescender=font_descent,
            sTypoLineGap=line_gap,

            usWinAscent=font_ascent,
            usWinDescent=-font_descent,

            sxHeight=x_height,
            sCapHeight=cap_height,

            # We can't infer strikeout position from BDF properties, but
            # thickness can be matched with the underline thickness.
            # TODO: should we still try to generate a reasonable value for
            # yStrikeoutPosition?
            yStrikeoutSize=underline_thickness,
        )

        fixed_pitch = 1 if self.is_monospace else 0
        fb.setupPost(
            isFixedPitch=fixed_pitch,
            underlineThickness=underline_thickness,
            underlinePosition=underline_position,
        )

        # Merge adjacent pixel squares and reduce extra points
        removeOverlaps(fb.font)

        return fb


def convert_bdf(infile, outfile=None, feature_file=None):
    bdf = bdflib.reader.read_bdf(infile)

    font = Font(bdf)

    font_builder = font.opentype_font()

    if feature_file != None:
        addOpenTypeFeatures(font_builder.font, feature_file)

    if outfile != None:
        font_filename = outfile
    else:
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
    parser.add_argument("-f", "--feature-file", type=argparse.FileType("r"), help="""
            Include feature information from an OpenType feature file in the
            final font.
            """)

    args = parser.parse_args()
    convert_bdf(args.infile, outfile=args.out, feature_file=args.feature_file)


if __name__ == '__main__':
    main()
