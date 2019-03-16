"""Convert bitmap fonts into TTF format."""

import argparse
import sys

import bdflib.reader
try:
    import fontforge
except ImportError as e:
    print("\033[1;31mCould not import fontforge!\nMake sure the FontForge"
            " Python extension is properly installed.\033[0m",
            file=sys.stderr)
    raise e

# Map BDF properties to fontforge settings
def map_attributes(bdf, font):
    attr_map = {
        b'FACE_NAME': "fullname",
        b'FAMILY_NAME': "familyname",
        b'WEIGHT_NAME': "weight",
        b'FONT_VERSION': "version",
        b'COPYRIGHT': "copyright",
    }

    for attr_name in attr_map:
        attr_value = bdf[attr_name]
        if attr_value is not None:
            setattr(font, attr_map[attr_name], attr_value)

    fontname = compute_fontname(bdf)
    font.fontname = fontname


# Build the final font name
def compute_fontname(bdf):
    return (bdf[b'FAMILY_NAME'] + bdf[b'WEIGHT_NAME']).replace(b' ', b'')


# Build the final file name
def compute_filename(bdf):
    return "{}-{}.ttf".format(
        compute_fontname(bdf).decode(),
        bdf[b'FONT_VERSION'].decode()
    )


def trace_outlines(bdf_font, outline_font, pixel_size):
    for bdf_glyph in bdf_font.glyphs:
        # Add a new outline glyph
        outline_glyph = outline_font.createChar(bdf_glyph.codepoint,
                bdf_glyph.name.decode())

        trace_outline(bdf_glyph, outline_glyph, pixel_size)

        # The fontforge glyphs seem to start as squares, we want them to be
        # proportional. For some reason, this has to be set *after* we do the
        # drawing.
        outline_glyph.width = bdf_glyph.advance * pixel_size


def trace_outline(bdf_glyph, outline_glyph, pixel_size):
    pen = outline_glyph.glyphPen()

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
                pen.lineTo((x2, y1))
                pen.lineTo((x2, y2))
                pen.lineTo((x1, y2))
                pen.closePath()


def convert_bdf(infile, outfile=None, feature_file=None):
    font = fontforge.font()
    bdf = bdflib.reader.read_bdf(infile)

    map_attributes(bdf, font)

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

    # Apply metrics to the font
    font.ascent = ascent * pixel_size
    font.descent = descent * pixel_size
    assert font.em == em_size

    trace_outlines(bdf, font, pixel_size)

    if feature_file != None:
        font.mergeFeature(feature_file.name)

    # Merge adjacent pixel squares and reduce extra points
    font.selection.all()
    font.removeOverlap()
    font.simplify()

    if outfile != None:
        font_filename = outfile
    else:
        font_filename = compute_filename(bdf)

    # Output the final font
    font.generate(font_filename)


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
