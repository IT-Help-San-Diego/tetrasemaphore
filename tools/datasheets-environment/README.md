# The datasheet build environment

The sheets reproduce byte for byte in two environments on macOS (Apple silicon). What decides the bytes is
Pillow's text layout engine, and since revision 1 the template names it on its one `ImageFont.truetype`
call (`layout_engine=ImageFont.Layout.BASIC`). Measured on 7 November 2026 (the record is in the outgoing
folder's evidence):

- Pillow lays text out with its basic engine unless a libfribidi library is loadable at run time, in
  which case the PyPI wheel switches to Raqm (HarfBuzz shaping with kerning and fractional advances).
  Same fonts, same strings: the 15 px line "Read the stack from the bottom up ..." measures 876.0 px
  with the basic engine and 864.52 px under Raqm; "To" 17.97 against 15.78. Every line then wraps and
  sits a little differently and 6.0 to 6.7 percent of a sheet's pixels change, all of them text; every
  quotation, value and check stays identical and the build's own checks pass either way.
- With Raqm off, the conda-forge build (python 3.11.15, pillow 12.2.0 py311hd37aea2_0, freetype 2.14.3
  hce30654_1, cairo 1.18.4 he0f2337_1, pixman 0.46.4) and the PyPI wheels of the same versions give the
  same bytes: VERIFY PASS, 13 of 13, in both.
- With the engine explicit in the template, the wheels with Raqm on also reproduce the sheets (measured,
  one configuration, this platform). `tools/build_datasheets.py` still refuses to build when Pillow reports
  Raqm on unless `--allow-raqm` is given, so the condition is never silent; and it removes a second variable,
  FREETYPE_PROPERTIES (`truetype:interpreter-version=35` shortens that line to 845.0 px on both sides),
  from the scripts' environment.
- cairosvg 2.9.1 draws no SVG filters, so the foil grain (feTurbulence) and the organic band
  displacement are absent from the layer renders; the sheets' footnote records it, and step 2 (SVG and
  vector PDF output) must measure that difference before shipping both.

## Creating the environment (macOS, Apple silicon)

Either of the following. The first is the one the 23 October 2026 sheets were made in and the one the
proof used; the lock names every package by URL and md5 (90 packages, conda-forge, osx-arm64) and
depends on conda-forge keeping those exact files available.

    micromamba create -p .venv-datasheets --override-channels -c conda-forge --no-rc \
        --file tools/datasheets-environment/conda-explicit-osx-arm64.txt
    .venv-datasheets/bin/python -m pip install --no-cache-dir -r tools/datasheets-environment/requirements-pip.txt

`requested-builds.txt` is the short list the lock was solved from (the builds that decide the bytes,
named exactly). Or, with PyPI wheels (uv or pip, Python 3.11.15):

    uv venv --python 3.11.15 .venv-datasheets
    uv pip install --python .venv-datasheets/bin/python -r tools/datasheets-environment/requirements-wheels.txt

cairosvg then needs a libcairo (Homebrew's `cairo` 1.18.4 was used). Point the loader at a folder that
holds only that library, so that no libfribidi becomes loadable alongside it:

    mkdir -p .cairo-only && ln -sf /opt/homebrew/lib/libcairo.2.dylib .cairo-only/
    DYLD_FALLBACK_LIBRARY_PATH=$PWD/.cairo-only .venv-datasheets/bin/python -I tools/build_datasheets.py --verify

Pointing it at `/opt/homebrew/lib` itself loads fribidi too and Raqm turns on; the driver then stops unless
`--allow-raqm` is passed, under which, the engine being explicit in the template, the build reproduces.

Then, from the repository root:

    .venv-datasheets/bin/python -I tools/build_datasheets.py --verify

## Other platforms

Only osx-arm64 has been run. On another platform the same package versions build the sheets and pass
every check; whether the bytes match there is not measured (the engine is explicit; that platform's
FreeType rasteriser is the remaining variable). A sheet built elsewhere is checked by its audit JSON (every quotation, value,
source and geometry check) rather than by its hash.
