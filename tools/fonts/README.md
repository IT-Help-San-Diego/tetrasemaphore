# Fonts the datasheets are set in

| file | family and version | sha256 (first 16) | origin of this copy |
|---|---|---|---|
| DejaVuSans.ttf | DejaVu Sans 2.37 | 7da195a74c55bef9 | LibreOffice's bundled fonts, as the 23 October 2026 build read them |
| DejaVuSansMono.ttf | DejaVu Sans Mono 2.37 | b4a6c3e4faab8773 | LibreOffice's bundled fonts, as the 23 October 2026 build read them |
| DejaVuSans-Bold.ttf | DejaVu Sans Bold 2.34 | 7e69e81478e233b8 | the Dose 01 design folder's copy (05-DejaVuSans-Bold.ttf), as the 23 October 2026 build read it |

The Bold is version 2.34 while the other two are 2.37: that is what the sheets were built
with, and the byte-for-byte proof needs these exact files. Changing any of them changes
text metrics and therefore the sheets.

Licence: `LICENSE-DejaVu.txt`, the text embedded in the fonts themselves (name table entry
13): Bitstream Vera Fonts Copyright, with the DejaVu changes in the public domain and the
Arev glyphs under their own notice. It permits bundling and redistribution.

Science's ruling of 7 November 2026 (decision item 92): leave the Bold at 2.34 for 1.1 and carry the
unification to 2.37 as a 1.2 candidate, with its consequence stated: it changes text metrics and therefore
every sheet's bytes, so it forces a rebuild and a new hash set.
