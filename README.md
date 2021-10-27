# bdf2ttf

Utilities to turn bitmap fonts into outline "pixel" fonts, in TTF format.

## Getting started

```
pip install bdf2ttf
```

This package also has a dependency on [FontForge](https://github.com/fontforge/fontforge)

Note that FontForge will typically install its Python module only in the system Python's `site-packages` directory.
This means `bdf2ttf` may not work inside a virtual environment.


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

This project uses [poetry](https://python-poetry.org/) for development.

```
poetry install
poetry run bdf2ttf
poetry run pytest
```

NOTE: If you're using a virtual environment (which poetry does by default), it's important that the `system-site-packages` is turned on.
This is necessary for the `fontforge` module to be imported.
If you're using poetry >= 1.2.0, this should be set automatically on virtual environment creation.
Otherwise, navigate to the virtual environment root, open `pyvenv.cfg`, and set `include-system-site-packages = true`.

## License

GNU General Public License version 3
