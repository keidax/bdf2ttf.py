# bdf2ttf

Utilities to turn bitmap fonts into outline "pixel" fonts, in TTF format.
Getting started

```
pip3 install bdf2ttf
```

## Usage

Two scripts are included:

### bdf2ttf

Convert bitmap fonts into TTF format.

```
bdf2ttf MyCoolFont.bdf --out MyCoolFont.ttf
```

See `bdf2ttf --help` for more details.

### yml2fea

Create an OpenType feature file from YAML shorthand syntax.

```
yml2fea interesting_stuff.yml interesting_stuff.fea
```

See full documentation for more details.

## Developing

This project uses poetry for development.

First make sure poetry is installed.

<!-- TODO -->

NOTE: If you're using a virtual environment (which poetry does by default), it's important that the `system-site-packages` is turned on.
If you're using poetry >= 1.2.0, this should be set automatically on virtual environment creation.
Otherwise, navigate to the virtual environment root, open `pyvenv.cfg`, and set `include-system-site-packages = true`.

<!-- TODO: explain why -->

## License

GNU General Public License version 3
