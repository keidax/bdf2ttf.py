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

## License

GNU General Public License version 3
