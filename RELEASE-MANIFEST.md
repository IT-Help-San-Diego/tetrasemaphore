# The Tetrasemaphore 1.0.0: release manifest

Every file of this release, with its size in bytes and its SHA-256, so that anyone can check a copy: `shasum -a 256 <file>` (or `sha256sum <file>`)
prints the hash that stands beside it here. The list covers every file except this one, `CHANGELOG.md` and `CITATION.cff`, which are written at the
push with the record's DOI. The paths are the repository's. `artwork/` holds the sealed build records of the semaphores and screens with their paths kept
as they were built, so that every reference inside their configs, READMEs and scripts resolves; `proofs/` holds the Lean proofs, their checker and
the record of their red team; `record/` holds the decision log, the exchanges, the release plan and the test register; `methods/` holds methods
note 01 in revision 1 (`tetrasemaphore-methods-note-01-rev1.md`) and, unchanged, the original it revises (`tetrasemaphore-methods-note-01.md`).
`pdf/` holds two PDFs made by `tools/generate_pdfs.py`: typeset copies of `README.md` and of revision 1. `site/` is the website as
deployed. Text and art are under CC BY 4.0 (`LICENSE`); the code is under the Apache License 2.0 (`LICENSE-CODE`; `NOTICE` says which files).

## Not included, and why
- **Five build inputs that carry a licensed stock image of an owl.** The project's licences do not cover that image, so these files stay out.
  SHA-256 (first 16 characters): ba6b89bf94983fd6, a2aba8f772f29420, 36a0633d5ae3ca0e, 46f1faa25c89350c, 53e411c36898e6c4. The note's section
  "Why we left the owl" tells the history.
- **The two typefaces used for the lettering,** cited here so that a builder can fetch and check the same files:
  - DejaVu Sans Bold, version 2.34 (`DejaVuSans-Bold.ttf`, 693,876 bytes; SHA-256 7e69e81478e233b81c3ad730f5b10abe76c792d48ec6c3e7cc3b3596a37bb3b1). Licence: the DejaVu fonts licence
    (Bitstream Vera and Arev copyrights; DejaVu's own changes are in the public domain). Source: the DejaVu fonts project, https://dejavu-fonts.github.io/;
    release 2.34 (25 August 2013) is at https://sourceforge.net/projects/dejavu/files/dejavu/2.34/.
  - STIX Two Math, version 2.13 b171 (`STIXTwoMath.otf`, 838,652 bytes; SHA-256 3a5f3f26f40d5698b3c62dd085d48d6663696a3f80825aab8b553d5097518e8c), the copy bundled with macOS.
    Licence: SIL Open Font License 1.1. Source: the STIX Fonts project, https://github.com/stipub/stixfonts, release v2.13 b171. That release's files may
    differ in bytes from the copy macOS bundles; the SHA-256 identifies the copy used.
- **Two inputs from the earlier Dose 01 work** that the screens' build records cite: the Dose 01 lock-screen master (SHA-256 first 16: 1cf8f0f9f4aa30ea),
  which carries the owl, and a text-layout helper from the same work (c197c06602351a05). The screens' build scripts read both, so the scripts are a
  record of how the screens were made; they do not run from this release alone.
- **The seven DejaVu 2.37 font files the two PDFs in `pdf/` are set in** (`DejaVuSerif.ttf`, `DejaVuSerif-Italic.ttf`, `DejaVuSerif-Bold.ttf`,
  `DejaVuSerif-BoldItalic.ttf`, `DejaVuSans.ttf`, `DejaVuSans-Bold.ttf`, `DejaVuSansMono.ttf`), each pinned by size and SHA-256 inside
  `tools/generate_pdfs.py`, which stops if one differs; the PDFs embed subsets of them. They are byte for byte the files of the DejaVu project's
  release 2.37 (`dejavu-fonts-ttf-2.37.zip`), which LibreOffice also ships. Licence: the DejaVu fonts licence (Bitstream Vera and Arev copyrights;
  DejaVu's own changes are in the public domain). Source: the DejaVu fonts project, https://dejavu-fonts.github.io/; release 2.37 is at
  https://github.com/dejavu-fonts/dejavu-fonts/releases/tag/version_2_37 and https://sourceforge.net/projects/dejavu/files/dejavu/2.37/.

## Files

| path | bytes | SHA-256 |
|---|---|---|
| `.gitignore` | 370 | c764305965f310bc922cef67e2faa810d5f2c6360e5178489d45f1c7d7ce149b |
| `LICENSE` | 18,657 | 9ba9550ad48438d0836ddab3da480b3b69ffa0aac7b7878b5a0039e7ab429411 |
| `LICENSE-CODE` | 11,358 | cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30 |
| `NOTICE` | 344 | cec827fe3863ed1c42e0e4ecccab4f9656a1e3b1d62e4a07bae3c3e7409121f4 |
| `README.md` | 23,648 | c98c3ee4a94a3daee326e7a2c41bf9af700f775132555241536c0076a6420927 |
| `artwork/finish/finish7-knobs-noflecks.txt` | 233 | f3f10832e8ae6194b9b770a64d9905dcacca36dbd0d5bf3cd46a0cc0b99622ce |
| `artwork/finish/finish7-knobs.txt` | 221 | bef0253d36e2a95983df5d8d2c4c8f2f0932aef40646db271d1e0e1277c4d74a |
| `artwork/finish/proposals/NOTE-build5-noflecks.md` | 1,402 | f91da5803384ce9ae300ddd4a072c557154a54c5a6c3de735e3721516adae9e8 |
| `artwork/finish/proposals/NOTE-build6-litedge.md` | 2,485 | 7c12d9fbe1582556a0c26db584cc4c18ee3902bf198957c15e457fd57604036b |
| `artwork/finish/proposals/NOTE-build7-litedge-guard.md` | 2,109 | 2c85d4c5a1991a74bdc32d9f02047760f0244a2e4fd3184251767dba281bdf5d |
| `artwork/finish/proposals/seam-fix/MASTER-meander-v3.1C-finalA-LEGEND-keys21-2-litedge-guard-slot820.svg` | 840,260 | 5ba62c45788b29bea98eee298da823c3a54694786b6bc0dfd8076752f9ee491b |
| `artwork/finish/proposals/seam-fix/MASTER-meander-v3.1C-finalA-LEGEND-keys21-2-litedge-slot820.svg` | 841,200 | 9af6030e1fe28c27e101f5370db81bf144df257b28a844c8408c5fa7d075f7ad |
| `artwork/finish/proposals/seam-fix/MASTER-meander-v3.1C-finalA-LEGEND-keys21-2-noflecks-slot820.svg` | 205,698 | 6086dba12965b2106ecfadaa8145a09ef406bd32fc759e0ec0dcaa84d1d2a962 |
| `artwork/finish/proposals/seam-fix/MASTER-meander-v3.1C-finalA-LEGEND-keys21-2-slot820.svg` | 205,704 | 45dafb97a8a077a18e6ebb2257ecbba531002121d4483253b451a84ba9e5e16b |
| `artwork/finish/proposals/seam-fix/MASTER-meander-v3.1C-finalA-LEGEND-keys22-1-litedge-guard-slot820.svg` | 929,267 | f20cf292bdc8113cc385aecf70e0e6a07ba5bacfb4d8ebf44cd38cc30da92c02 |
| `artwork/finish/proposals/seam-fix/MASTER-meander-v3.1C-finalA-LEGEND-keys22-1-litedge-slot820.svg` | 930,338 | b809ccf6c6784407ac401277af745384c4fdb37775bb8089e91f731eb04cb1f3 |
| `artwork/finish/proposals/seam-fix/MASTER-meander-v3.1C-finalA-LEGEND-keys22-1-noflecks-slot820.svg` | 227,497 | e0a648d4451dd7781a0d71c851b5e188eac47131895bf17c98cec7e8a830b01e |
| `artwork/finish/proposals/seam-fix/MASTER-meander-v3.1C-finalA-LEGEND-keys22-1-slot820.svg` | 227,503 | 06454b6df0e80ef49572dae59185550c9516ccd706a713018ced66eac98763f8 |
| `artwork/finish/proposals/uncut/MASTER-meander-v3.1C-finalA-UNCUT-seamfix-litedge-guard-slot820.svg` | 1,109,880 | 29af7381e53a37a640ec0ff6106516462c14a641d47ebbd4c8802ee01813eaac |
| `artwork/finish/proposals/uncut/MASTER-meander-v3.1C-finalA-UNCUT-seamfix-litedge-slot820.svg` | 1,111,145 | 91d1a01b8e1392c06f4fc70748163f15ba4e78c2cbffa32780f61927741f30ca |
| `artwork/finish/proposals/uncut/MASTER-meander-v3.1C-finalA-UNCUT-seamfix-noflecks-slot820.svg` | 271,082 | f21db7ab012500c8b72137048354b8894a45c91ed4d920132ced9fb7a065b4d2 |
| `artwork/finish/proposals/uncut/MASTER-meander-v3.1C-finalA-UNCUT-seamfix-slot820.svg` | 271,088 | 901fd319c2b7e30ab31c44856f707b960ad0075b8262a7767c430fcb6363f83a |
| `artwork/glyphs/identity_diamond_one_outline.svg` | 1,488 | e5401609bd7e1a36d3e9fca69086ef4e21d097dc121edf63b0e86dbbf775bb3a |
| `artwork/glyphs/sigma_h_twin_look2.svg` | 1,096 | 924510f313db072877abef92d27417eb26f0115c4880a4098aa7d49d38f9186d |
| `artwork/glyphs/sigma_v_twin_look2.svg` | 1,048 | 401f32832d833b478260c3e8e1e677ee044d4c9aed8c047e88428336c0227ac5 |
| `artwork/glyphs/tri_solid_A_U85_FINAL_G0.575388.svg` | 2,068 | 6a439aa605cd2098df1ceee9ddf7cd12727f40c99b73bba91162376a6d201521 |
| `artwork/master/states/proposals/layered/layered-build.json` | 8,068 | 87ed170c23ea8d052f9ab16e996236f557b5ab719aab4b592fee6a6c399faa8c |
| `artwork/master/states/proposals/layered/states-config-layered.json` | 6,420 | 3bcaf0f48459bc9712dc62dca2ba454d616672edd8f51d55ab55f66f6d7a25b9 |
| `artwork/master/states/proposals/notation/final-masters-2026-10-05/MANIFEST.json` | 44,381 | cdb83f85645e00fda7e6a8a700c489fefd09b87cf252f7e490e200f83604924c |
| `artwork/master/states/proposals/notation/final-masters-2026-10-05/MASTER-medallion-CRITICAL-notation-slot820-preview.png` | 1,106,059 | 65fd170ccac2725692f6872c2ca28f3b920785eb0650778e5372aa77673e4dae |
| `artwork/master/states/proposals/notation/final-masters-2026-10-05/MASTER-medallion-CRITICAL-notation-slot820.svg` | 2,977,502 | 33413c4af9ec838cef1252116661b9905066005b6595a3009c40dd418fd5b3a2 |
| `artwork/master/states/proposals/notation/final-masters-2026-10-05/MASTER-medallion-METACOGNITIVE-notation-slot820-preview.png` | 1,054,172 | 8d851974558f18ffe80caa59963ef0c385ac56de744775afa063e14aedc6474f |
| `artwork/master/states/proposals/notation/final-masters-2026-10-05/MASTER-medallion-METACOGNITIVE-notation-slot820.svg` | 2,802,185 | cccfcff10dc74930139864a290b62d65e0c1ef68b65f3821955206d4c5e87c8b |
| `artwork/master/states/proposals/notation/final-masters-2026-10-05/MASTER-medallion-NON-NORMATIVE-notation-slot820-preview.png` | 1,053,532 | 74bbc4559e7d8c6c33779324eff1d43e37d78575c177e976e8fa44fe0ea3c9a1 |
| `artwork/master/states/proposals/notation/final-masters-2026-10-05/MASTER-medallion-NON-NORMATIVE-notation-slot820.svg` | 2,801,300 | 4ef1de6ae126279e83c65570ba0454fef3862bb6599798bf5d6fc1dc5c100f10 |
| `artwork/master/states/proposals/notation/final-masters-2026-10-05/MASTER-medallion-NORMATIVE-notation-slot820-preview.png` | 1,108,058 | dcf7c0c6a8010123275136946c9b96229a9a9aceba9a148c8e7752bd49076c3e |
| `artwork/master/states/proposals/notation/final-masters-2026-10-05/MASTER-medallion-NORMATIVE-notation-slot820.svg` | 2,977,433 | e0b6366d5c032523dcd9b35658756570cbf0f2f09cbb1563f3885e53f0bec1e6 |
| `artwork/master/states/proposals/notation/final-masters-2026-10-05/README.md` | 34,632 | 4e0d3ff8ae34a711e2ea928c59d83d102ccdc751341b10789d059d6c67fa3cc4 |
| `artwork/master/states/proposals/notation/final-masters-2026-10-05/make_manifest.py` | 12,531 | e92cea4d4240c57e558f6d52604b82158d3d7430859edb7969f74adf75a6685f |
| `artwork/master/states/proposals/notation/final-masters-2026-10-05/notation-measurements.json` | 22,409 | 24c49d6bafacdaf581dbef05a6afac817bcac6bad7914a3d80e7fcf74373efaa |
| `artwork/master/states/proposals/notation/final-masters-2026-10-05/png/TETRASEMAPHORE-CRITICAL-en-1024.png` | 517,040 | d59377d73fccc1e6576ccf4f1a0935fe6810990ec2f7f961444746c9f56866f6 |
| `artwork/master/states/proposals/notation/final-masters-2026-10-05/png/TETRASEMAPHORE-CRITICAL-en-1214.png` | 681,745 | d7efbf891970aef009e6293c4f690cc2061696788ec235d3dcc64e695091863d |
| `artwork/master/states/proposals/notation/final-masters-2026-10-05/png/TETRASEMAPHORE-CRITICAL-en-1298.png` | 757,191 | a43da812ca3a7c885a4e688c978e6e4011c0996968b2411b6ca8a959a0ae2461 |
| `artwork/master/states/proposals/notation/final-masters-2026-10-05/png/TETRASEMAPHORE-CRITICAL-en-2460.png` | 2,150,660 | bdf43bf1db796ea098835b23b0df6f87f8d4dffe41a05902258e1d95651282e9 |
| `artwork/master/states/proposals/notation/final-masters-2026-10-05/png/TETRASEMAPHORE-CRITICAL-en-512.png` | 170,102 | 89dc35c8fcd840f0de8b75e3df094798b9a417472ffaa1ca707b2a7bac5613a3 |
| `artwork/master/states/proposals/notation/final-masters-2026-10-05/png/TETRASEMAPHORE-CRITICAL-es-1024.png` | 516,690 | 30f6b1444daa3273437c6433460a48f44aaeb86482906b4f705cd439353e2b7d |
| `artwork/master/states/proposals/notation/final-masters-2026-10-05/png/TETRASEMAPHORE-CRITICAL-es-1214.png` | 681,421 | 1d74924d9a5694e7cbb54020322ea49f0d41673f12d79fc2d32650f0c338ce82 |
| `artwork/master/states/proposals/notation/final-masters-2026-10-05/png/TETRASEMAPHORE-CRITICAL-es-1298.png` | 756,826 | 54bcc40dea8e470dc1f7e9a2ab6f5b0f5c73b258339908608e8eed38158015b7 |
| `artwork/master/states/proposals/notation/final-masters-2026-10-05/png/TETRASEMAPHORE-CRITICAL-es-2460.png` | 2,149,359 | 509297829265a0a19b2533c6ff3735c9134b46135355e9996632e1c925f61e4d |
| `artwork/master/states/proposals/notation/final-masters-2026-10-05/png/TETRASEMAPHORE-CRITICAL-es-512.png` | 170,087 | 30af4e519891b595c81ea243c7b0a87ee9fe9418bf382a7a50b29151dc98eed4 |
| `artwork/master/states/proposals/notation/final-masters-2026-10-05/png/TETRASEMAPHORE-METACOGNITIVE-en-1024.png` | 491,959 | cb29b35c8363f4afbf859e75193f942066f0079222bfbbc7e1c675a722839e1b |
| `artwork/master/states/proposals/notation/final-masters-2026-10-05/png/TETRASEMAPHORE-METACOGNITIVE-en-1214.png` | 649,119 | 54595050d3971357c219cfa5fa026f0633c45343cbaffaa4e665d45bd0c2fb3d |
| `artwork/master/states/proposals/notation/final-masters-2026-10-05/png/TETRASEMAPHORE-METACOGNITIVE-en-1298.png` | 721,125 | 0f050e240c74e952fb475211b5a31657b832e374d9587656e7f76df085cc0de0 |
| `artwork/master/states/proposals/notation/final-masters-2026-10-05/png/TETRASEMAPHORE-METACOGNITIVE-en-2460.png` | 2,047,413 | 6c5d24121f4de08c844294f6fc00e2e9ef3918e1da63e30fc1fd3eda9c697d11 |
| `artwork/master/states/proposals/notation/final-masters-2026-10-05/png/TETRASEMAPHORE-METACOGNITIVE-en-512.png` | 162,619 | 1fc5ca3480246e1277bcb56849ebb93293866dd43aa7f21d069b90f86df6e2ec |
| `artwork/master/states/proposals/notation/final-masters-2026-10-05/png/TETRASEMAPHORE-METACOGNITIVE-es-1024.png` | 491,826 | 5a75810d97e3a852a0f1b9972c3f9c8b1d51421f7e8bdcd02f1f9ee2c0738ae3 |
| `artwork/master/states/proposals/notation/final-masters-2026-10-05/png/TETRASEMAPHORE-METACOGNITIVE-es-1214.png` | 649,089 | 7ef4ddfe43c6df98eaf3af85ce9a7e4e6bcb5dbfc3ed9774e237e4de5bddab08 |
| `artwork/master/states/proposals/notation/final-masters-2026-10-05/png/TETRASEMAPHORE-METACOGNITIVE-es-1298.png` | 720,975 | 0b74d6670118923a2b15c0770c3cc123b658deee5ff7d95add1964066fe2fad4 |
| `artwork/master/states/proposals/notation/final-masters-2026-10-05/png/TETRASEMAPHORE-METACOGNITIVE-es-2460.png` | 2,047,427 | 0e59f20a7d03e8d16b62217a3d79707fc05d603be012c5d657b4b6095800e592 |
| `artwork/master/states/proposals/notation/final-masters-2026-10-05/png/TETRASEMAPHORE-METACOGNITIVE-es-512.png` | 162,481 | 289b7447e6ab663e6a96c8745815080cbaef1f731407760aa8e5f5fdb55f37be |
| `artwork/master/states/proposals/notation/final-masters-2026-10-05/png/TETRASEMAPHORE-NON-NORMATIVE-en-1024.png` | 492,172 | 83341673d1a188a24fa1c5ceca55edeebe8988df7de76c02bfa738d33f6c4878 |
| `artwork/master/states/proposals/notation/final-masters-2026-10-05/png/TETRASEMAPHORE-NON-NORMATIVE-en-1214.png` | 648,645 | 3bc24d0127c0be160237eedd4ffc1c00865eae46297119fd388da029788cc8f9 |
| `artwork/master/states/proposals/notation/final-masters-2026-10-05/png/TETRASEMAPHORE-NON-NORMATIVE-en-1298.png` | 720,684 | 658837bd2d2802b35b8a85f91fdd50d839471acf092f57e9f587589f42bc8db0 |
| `artwork/master/states/proposals/notation/final-masters-2026-10-05/png/TETRASEMAPHORE-NON-NORMATIVE-en-2460.png` | 2,047,499 | 4f430643f61b19ad705cba8dba687451a0f312f001edbd9a9b6119af23a9d25e |
| `artwork/master/states/proposals/notation/final-masters-2026-10-05/png/TETRASEMAPHORE-NON-NORMATIVE-en-512.png` | 163,398 | 9b90f014e077453b7e2446ef42c8dc0b08375ceb194c1d418ad94c162ee1d91e |
| `artwork/master/states/proposals/notation/final-masters-2026-10-05/png/TETRASEMAPHORE-NON-NORMATIVE-es-1024.png` | 489,814 | 374244c0a8e21bcb0ca1a4de2ba9bf50138f4c448c497f07dcc14485d88eaa70 |
| `artwork/master/states/proposals/notation/final-masters-2026-10-05/png/TETRASEMAPHORE-NON-NORMATIVE-es-1214.png` | 645,374 | ac2b2b6d21778c865ef92e0b706bae6baa3d8a4e7696e0caea2fce961f05303e |
| `artwork/master/states/proposals/notation/final-masters-2026-10-05/png/TETRASEMAPHORE-NON-NORMATIVE-es-1298.png` | 717,005 | a4017750741981e9ac61a99f652abd34b82bdf4aafd518e8bc2e8968fef50753 |
| `artwork/master/states/proposals/notation/final-masters-2026-10-05/png/TETRASEMAPHORE-NON-NORMATIVE-es-2460.png` | 2,038,814 | 3d148680e77d179f270311197183e833d5cb57abe0bf70be79ec22de6229e7c3 |
| `artwork/master/states/proposals/notation/final-masters-2026-10-05/png/TETRASEMAPHORE-NON-NORMATIVE-es-512.png` | 162,274 | af1236728c2dd7a64603672666a7ba264c44df16335230ca552099f39675c09d |
| `artwork/master/states/proposals/notation/final-masters-2026-10-05/png/TETRASEMAPHORE-NORMATIVE-en-1024.png` | 513,156 | 700070871d66fc0456d498b421bef8c4ba5f98da33cb219b26026edabf5f0cbc |
| `artwork/master/states/proposals/notation/final-masters-2026-10-05/png/TETRASEMAPHORE-NORMATIVE-en-1214.png` | 680,362 | bf17a636666eca1f7ab8891c38881b34daca8df2efcc797cacaed68f2e644818 |
| `artwork/master/states/proposals/notation/final-masters-2026-10-05/png/TETRASEMAPHORE-NORMATIVE-en-1298.png` | 755,820 | eacf65bc9181f649ff29d76011bc0cc759f3c9aacb01b0ab4875c764b2526438 |
| `artwork/master/states/proposals/notation/final-masters-2026-10-05/png/TETRASEMAPHORE-NORMATIVE-en-2460.png` | 2,151,407 | 7d2c42c239b403709e883b8c26725e35e52a74fabaea5123f6eba1e842985e73 |
| `artwork/master/states/proposals/notation/final-masters-2026-10-05/png/TETRASEMAPHORE-NORMATIVE-en-512.png` | 168,560 | b893c34898ab9ebc4fcd8eb2f915a30253d5afb64548aad0afe1af7b3160600d |
| `artwork/master/states/proposals/notation/final-masters-2026-10-05/png/TETRASEMAPHORE-NORMATIVE-es-1024.png` | 513,418 | ab54679ee6d54f6630b16a64dbc7ad727ee8f3921e062326f611773f0a4481e8 |
| `artwork/master/states/proposals/notation/final-masters-2026-10-05/png/TETRASEMAPHORE-NORMATIVE-es-1214.png` | 680,505 | 3250360ddf3e50f5211d9d57b913c4c71bcd172410bb553e6b968984f5040d4c |
| `artwork/master/states/proposals/notation/final-masters-2026-10-05/png/TETRASEMAPHORE-NORMATIVE-es-1298.png` | 755,972 | 077215b442760441426bd4270d844bbf16848891edeeea9a00f1b0837101b696 |
| `artwork/master/states/proposals/notation/final-masters-2026-10-05/png/TETRASEMAPHORE-NORMATIVE-es-2460.png` | 2,151,743 | 33d606f92ae91a8975a7556f79c441264fb88c6e4cab1ca1ca7dcc91dbc05efa |
| `artwork/master/states/proposals/notation/final-masters-2026-10-05/png/TETRASEMAPHORE-NORMATIVE-es-512.png` | 168,591 | 1c49f6829a561265fcd0334654ec39c81ebc37caaaf2a8b1067be57f9dbc2577 |
| `artwork/master/states/proposals/notation/final-masters-2026-10-05/proofs/TETRASEMAPHORE-BUILD3-stamp-before-after.png` | 1,234,977 | dd07fcf9a539e95e549eb7f0b288ceb9da3b878e794b4374b7dc4fc70f91b4bb |
| `artwork/master/states/proposals/notation/final-masters-2026-10-05/proofs/TETRASEMAPHORE-CRITICAL-no-legend-uncut-ring-1024.png` | 555,619 | a021f91fd50c4c3355e3211832c6876874546ce9a478c6099d5492991156c350 |
| `artwork/master/states/proposals/notation/final-masters-2026-10-05/proofs/TETRASEMAPHORE-FINAL-MASTERS-on-white.png` | 1,812,463 | 1513e2bc6b8b0cf5eeaea08b0c467006148f2c1c181336cb9eb3722fd37660c4 |
| `artwork/master/states/proposals/notation/final-masters-2026-10-05/proofs/TETRASEMAPHORE-FINAL-MASTERS-set.png` | 1,839,640 | 686a19dd8dbec954d4d5664e6f355db557352c53d7fda03a3daea7453902db38 |
| `artwork/master/states/proposals/notation/final-masters-2026-10-05/proofs/TETRASEMAPHORE-FINAL-MASTERS-spanish-and-uncut.png` | 3,320,883 | f514fb2740070ba9c71296cef10454e962c4027262ff74e30dc4e0869da9d1b1 |
| `artwork/master/states/proposals/notation/final-masters-2026-10-05/proofs/TETRASEMAPHORE-METACOGNITIVE-no-legend-uncut-ring-1024.png` | 547,506 | 2e28cf6a78c34fd81653a3f26d16ded8233d829c9dcec5ba7f6b829a02b53928 |
| `artwork/master/states/proposals/notation/final-masters-2026-10-05/proofs/TETRASEMAPHORE-NON-NORMATIVE-no-legend-uncut-ring-1024.png` | 548,132 | 6ea26e83786d491c73859f6ba1f6a252ce3772f4c6d8b55ba2135ee6af9d6c92 |
| `artwork/master/states/proposals/notation/final-masters-2026-10-05/proofs/TETRASEMAPHORE-NORMATIVE-no-legend-uncut-ring-1024.png` | 548,903 | 4bc7e620d5bd7b8ae9452c06ae49051916b43f2e4cdfd16565194b01b2d369de |
| `artwork/master/states/proposals/notation/final-masters-2026-10-05/refute/build3-first-pass-as-refuted/notation/MASTER-medallion-CRITICAL-notation-slot820.svg` | 735,274 | a8fc0bf8802a0e36cf32b0fdeabc8ed8bdb1e9f963236b7712a344841e6aef07 |
| `artwork/master/states/proposals/notation/final-masters-2026-10-05/refute/build3-first-pass-as-refuted/notation/MASTER-medallion-METACOGNITIVE-notation-slot820.svg` | 694,847 | f63747e84d9a6872f346ac8255e5f4168bc58c21b0c91f729da91fe4dc278110 |
| `artwork/master/states/proposals/notation/final-masters-2026-10-05/refute/build3-first-pass-as-refuted/notation/MASTER-medallion-NON-NORMATIVE-notation-slot820.svg` | 693,879 | bfb5652ef417c38bbf487e42a551bb396ae2beba5e3a62256378d6a5d916410b |
| `artwork/master/states/proposals/notation/final-masters-2026-10-05/refute/build3-first-pass-as-refuted/notation/MASTER-medallion-NORMATIVE-notation-slot820.svg` | 735,679 | d5532ebfafc62f21bd0c9d2878ee6b42c7ce1e6dd88043da1aef6523bb9b8426 |
| `artwork/master/states/proposals/notation/final-masters-2026-10-05/refute/labels-only-diff.py` | 3,406 | d7ebd421f7b9cd1d017983852cdbc183307899019416d8a4121dc946dca39588 |
| `artwork/master/states/proposals/notation/final-masters-2026-10-05/refute/lane-stamp-floor.json` | 3,846 | 56457475211d832ab777ef5a2de9adc17ea50a27930e32f6bc5ba1eaaef496f8 |
| `artwork/master/states/proposals/notation/final-masters-2026-10-05/refute/lane-stamp-floor.py` | 3,400 | 9364b48f698e47789367c08e983ea354fe43bea30bfb89a3002966759972272e |
| `artwork/master/states/proposals/notation/final-masters-2026-10-05/refute/lane-verify-build3.py` | 10,675 | 9c8179d7e68c713d3a6bb3d3bef34f0b9b5fb2fe0c348301c45e7cae82c6f80d |
| `artwork/master/states/proposals/notation/final-masters-2026-10-05/refute/lane-verify-build5-output.txt` | 12,257 | 40c848de02f3df558698cbd9b226157bd886076caa807bbb30b09ab526b21070 |
| `artwork/master/states/proposals/notation/final-masters-2026-10-05/refute/lane-verify-build5.py` | 13,234 | e77b057ef15ad5a5e2c08f4a7f8bb7875da0954464b7e800972e6171ff79d8ee |
| `artwork/master/states/proposals/notation/final-masters-2026-10-05/refute/lane-verify-build6-output.txt` | 14,368 | f8083571e24cd0667a30c52f5fbd66a899a6f623208bf52485aa59454f8dc006 |
| `artwork/master/states/proposals/notation/final-masters-2026-10-05/refute/lane-verify-build6.py` | 11,998 | 315f92d66f160565af6b80905f18bb4d6c8c70f5132ca3e6ad3c704a92a5d4d9 |
| `artwork/master/states/proposals/notation/final-masters-2026-10-05/refute/lane-verify-build7-output.txt` | 21,824 | a6e7bbec3cae0117746a941c02f7d3fd86b6159ccbf8361d7f07ed71ceff3393 |
| `artwork/master/states/proposals/notation/final-masters-2026-10-05/refute/lane-verify-build7-report.json` | 4,255 | 7a0966e4ec9536adbfa881b40da5b3240c1a6c4e52a960aaf7e9ea702817bc7c |
| `artwork/master/states/proposals/notation/final-masters-2026-10-05/refute/lane-verify-build7.py` | 19,015 | e92013aa300356c963065ea24c9c8d4a453dbdf1b6fe8986b97061057d8a014a |
| `artwork/master/states/proposals/notation/final-masters-2026-10-05/refute/lane-verify-final-masters.py` | 10,466 | 33a718d0029f3dc53f3cc1cfdbecda3880d39a93088538a13c21e18b9f0e6f24 |
| `artwork/master/states/proposals/notation/final-masters-2026-10-05/refute/refute-build3.json` | 152,522 | a17def0f9e07d7818912c2d95815a73265b662521e5328815d5b0237a879e82c |
| `artwork/master/states/proposals/notation/final-masters-2026-10-05/refute/window-end-METACOGNITIVE-left-inkscape.png` | 718,357 | 302ea6e6b74a95f7f5bce7c58882d639a9a65f5fa7f1d26094528fb33955d3d3 |
| `artwork/master/states/proposals/notation/final-masters-2026-10-05/refute/window-ends-build3-resvg-4920.png` | 910,196 | f9b7b6a64721d5cfbf6eab429bb5503c45123efe3c5a81a42db92a83ccfbd786 |
| `artwork/master/states/proposals/notation/final-masters-2026-10-05/research/spanish-terms-raw.json` | 69,456 | 6232d380c6ecb12c5bd13fba2a70dc1dca6c7275e18a18fbe0c4a4fb32c995f0 |
| `artwork/master/states/proposals/notation/final-masters-2026-10-05/scan-cards/SCAN-CRITICAL-readable-half.png` | 200,033 | f0b37156b196386fb4398c4caaaaddb317784e2000c5164ab7247fbcf6d45ba7 |
| `artwork/master/states/proposals/notation/final-masters-2026-10-05/scan-cards/SCAN-CRITICAL-whole-coin.png` | 1,525,398 | 719af68267e1901d4af5a488a7d08ba1b4f5af24413241636cd51a58ce072fcd |
| `artwork/master/states/proposals/notation/final-masters-2026-10-05/scan-cards/SCAN-METACOGNITIVE-readable-half.png` | 97,036 | 58f9dee0274acaa89067766c13868f7049bc920955d7024c6193448d09fc7ad5 |
| `artwork/master/states/proposals/notation/final-masters-2026-10-05/scan-cards/SCAN-METACOGNITIVE-whole-coin.png` | 1,452,778 | 7a5499b403187e289b6c03f091d5f5016a586264ab6b24b881149e640277194b |
| `artwork/master/states/proposals/notation/final-masters-2026-10-05/scan-cards/SCAN-NON-NORMATIVE-readable-half.png` | 106,071 | 66fdbf504bc4f492f89bd736a8273a7530f3b9935dfe35d33ae3d4f612de6042 |
| `artwork/master/states/proposals/notation/final-masters-2026-10-05/scan-cards/SCAN-NON-NORMATIVE-whole-coin.png` | 1,452,223 | dc3680aeacc01047a077beccd3a672c0ede2fa4e5eab28a306c628e7e397fe26 |
| `artwork/master/states/proposals/notation/final-masters-2026-10-05/scan-cards/SCAN-NORMATIVE-readable-half.png` | 114,547 | 0f6af13e3f92cbbebc928c6dc562488011f89911b9c0040e2f561be378114a24 |
| `artwork/master/states/proposals/notation/final-masters-2026-10-05/scan-cards/SCAN-NORMATIVE-whole-coin.png` | 1,529,025 | 1ba54fc377883665eb5819e5a7b707bd49bb9c3ce3aa8a39b35bbe8d3116eea9 |
| `artwork/master/states/proposals/notation/notation-config-final-masters.json` | 5,839 | fa8a842b07fdd9d69bcb1c3221a803481c365b7c439acc281a4b2ffcb869b334 |
| `artwork/master/states/states-config.json` | 1,635 | 3550aab519bbd09163db445e7306fec4f4fa9496c157875f04b5ff1162d0cc88 |
| `artwork/tools/build_notation.py` | 36,667 | f3b70c3a422a93ed1d7402ef98b3a534cb955cc638feee9662cb843cc8e4516d |
| `artwork/tools/build_states.py` | 3,352 | b80ca81e7c446b296e7216f373c1d3d2ceaf86fcba2115d406f1b9ce974f1e08 |
| `artwork/tools/build_states_layered.py` | 24,833 | fdd9f8d9efe3e335e445eb9c6f74a010ea228f09f590164be0d484b4b9e5cd6b |
| `artwork/tools/compose.py` | 915 | 551a3e326c3f031ff071b46534ad01dff4e6b9f47da71825c57ae099bb446fe8 |
| `artwork/tools/export_set.py` | 8,693 | ff39844baa06cb9993636a7263cc0843c9d3a533c7c6fd51c83bceb51a74392a |
| `artwork/tools/finish7.js` | 23,379 | 90055af236a795d594e52830b73c25b383b4922a3afa8568e1b3861d57608c79 |
| `artwork/tools/legend.js` | 8,901 | 3a0711ab56cc4ac4d2dadd612214cc2aac7a9c6931b14049c9eb7deac6113c60 |
| `artwork/tools/litedge.js` | 9,861 | 88bfd9d7787af720a415b6715b4fd001185526c4bb9551aac791435553e011a3 |
| `artwork/tools/meander3.js` | 10,455 | a95717a5f7481c4716f5e1f30e05eef63361746231a26c304b07962561109586 |
| `artwork/tools/png_tag.py` | 2,982 | a690beca6b7d1c14126c714009345de938afc23f402c6639eefe3d91e6a84b8c |
| `artwork/tools/render.js` | 430 | f8cc0e08bc3c626c678a3d98f4e2b2ab65e144ee547b5cefbd45e37243bb60a2 |
| `artwork/tools/ring_build.js` | 2,598 | dfc9c721f46fe3a8fbc8f6bc90b56ae997685d6cb0c9c8c223bfc9d08a3fb3a2 |
| `artwork/tools/sealed/build_states_layered.py.before-cut-in-9ecd029d3f637b44` | 12,182 | 9ecd029d3f637b442fc499ed6de97411c711bf03465c32e153f175bb4634a9c8 |
| `artwork/tools/sealed/litedge.js.build6-d1082feb366e17b7` | 9,173 | d1082feb366e17b7d26b8bd068be21d1e6cacbfce29c41011350f8df52f49b80 |
| `artwork/vector-masters/tetrasemaphore-build7-allfour-lockscreen-halfway/README.md` | 7,416 | 5596f22fa2e22011098bcaac523429e238d5da6790ed4dd0a54ac7d1f8e0e7e3 |
| `artwork/vector-masters/tetrasemaphore-build7-allfour-lockscreen-halfway/SHA256.txt` | 528 | 023605c9720cf33d0ccecaaebc5aab0bde92c90bee1f148ce1aaf06840440fbc |
| `artwork/vector-masters/tetrasemaphore-build7-allfour-lockscreen-halfway/dose-01-iphone-17-pro-1206x2622-TETRASEMAPHORE-ALL-FOUR-lockscreen-halfway-MASTER.svg` | 11,582,793 | c102093af228eb727e0f797e8217dca3b40a5e3bab37b87d0f5e87874954a780 |
| `artwork/vector-masters/tetrasemaphore-build7-allfour-lockscreen-halfway/dose-01-iphone-17-pro-1206x2622-TETRASEMAPHORE-ALL-FOUR-lockscreen-halfway.png` | 524,788 | 98539d7457697edb14f2ca3d79b4b606b9ac23274df3da9f15b2df8c6e04663b |
| `artwork/vector-masters/tetrasemaphore-build7-allfour-lockscreen-halfway/proofs/TETRASEMAPHORE-ALL-FOUR-lockscreen-halfway-preview.png` | 456,626 | c4723f982adf7bc64de5c315daa57fc7532c46d1f0b650953c62eb49b4bbdec2 |
| `artwork/vector-masters/tetrasemaphore-build7-allfour-lockscreen-halfway/work/build-lock-rev6.js` | 25,570 | df04b2ee0c4c7cb62d21f3777e80b390d3c2d7d56b451fcf1c25d9f2582a51eb |
| `artwork/vector-masters/tetrasemaphore-build7-allfour-lockscreen-halfway/work/layout_report.json` | 10,233 | a12bd752de955a0ce0f4664fa89ad592c9fab2f11e8583a39c301b00ffd90001 |
| `artwork/vector-masters/tetrasemaphore-build7-allfour-lockscreen-halfway/work/spec-rev6/FINISH-TODAY-update-19.md` | 1,024 | 645fbdab25c36d579b840a0c27f24d10653d26e7c10aea20ca4247abb89d61ee |
| `artwork/vector-masters/tetrasemaphore-build7-allfour-lockscreen-halfway/work/verify-lock-rev6.py` | 9,303 | 0d8fc51b92cae9411cf3c37226491981ae91bff724f290dd41fc49666410fe97 |
| `artwork/vector-masters/tetrasemaphore-build7-allfour-lockscreen-halfway/work/verify_report.json` | 5,039 | 3b6c7a19bff0a5ade6a0ba6ec2733dc134393e3474c9d75dfc1f9a568c4d15d5 |
| `artwork/vector-masters/tetrasemaphore-build7-j4-screens/README.md` | 8,954 | 5b79c860a9ce331e41fda4ce336417220ade93411f91d0b52653ffee64b8d961 |
| `artwork/vector-masters/tetrasemaphore-build7-j4-screens/SHA256.txt` | 1,396 | 26b01bc8b3f6c42c62179c31a9e4adf9aa4b6d43ab5177be9c7649873d06940b |
| `artwork/vector-masters/tetrasemaphore-build7-j4-screens/dose-01-iphone-17-pro-1206x2622-TETRASEMAPHORE-ALL-FOUR-flashcard-MASTER.svg` | 11,582,136 | 0b83fba14b3c08d6324b966be665de838071398f118282b4d9d19a974c2ca3b4 |
| `artwork/vector-masters/tetrasemaphore-build7-j4-screens/dose-01-iphone-17-pro-1206x2622-TETRASEMAPHORE-ALL-FOUR-flashcard.png` | 469,029 | 9da7baacc29fdd0a03b23628c1053a66cbca6e9d75c5d1c42b19ed7e5495f568 |
| `artwork/vector-masters/tetrasemaphore-build7-j4-screens/dose-01-iphone-17-pro-1206x2622-TETRASEMAPHORE-ALL-FOUR-lockscreen-MASTER.svg` | 11,582,194 | d551d3c339cdd915d680e9f5f7c017cb8e183a85d923cbfc4a2cce2915cacf68 |
| `artwork/vector-masters/tetrasemaphore-build7-j4-screens/dose-01-iphone-17-pro-1206x2622-TETRASEMAPHORE-ALL-FOUR-lockscreen.png` | 652,332 | c5026f044c48c0590926893bf54a8e125e6bdf848cfd6b667672f7678dd75cf1 |
| `artwork/vector-masters/tetrasemaphore-build7-j4-screens/dose-01-iphone-17-pro-1206x2622-TETRASEMAPHORE-CRITICAL-flashcard-MASTER.svg` | 3,012,247 | 7ef95fb6e0aee46e239ee0f4ba0737559bff24d11aa62e2a9878ca77c4bbed7d |
| `artwork/vector-masters/tetrasemaphore-build7-j4-screens/dose-01-iphone-17-pro-1206x2622-TETRASEMAPHORE-CRITICAL-flashcard.png` | 274,281 | 9762a175f02cb36490b622193e215997e47b25b5953eed23c4b92cb91d6b780a |
| `artwork/vector-masters/tetrasemaphore-build7-j4-screens/dose-01-iphone-17-pro-1206x2622-TETRASEMAPHORE-NON-NORMATIVE-flashcard-MASTER.svg` | 2,830,346 | 06c8b13bc205a1246b9a56cb6ed53452b21f0a389c3232b358b73aca4f268c43 |
| `artwork/vector-masters/tetrasemaphore-build7-j4-screens/dose-01-iphone-17-pro-1206x2622-TETRASEMAPHORE-NON-NORMATIVE-flashcard.png` | 261,595 | 1ff196ef5092f3aef9d2952d1c5e018a6dded7ff3ec5b4089c16f3f5771bdc11 |
| `artwork/vector-masters/tetrasemaphore-build7-j4-screens/dose-01-iphone-17-pro-1206x2622-TETRASEMAPHORE-NORMATIVE-flashcard-MASTER.svg` | 3,013,376 | 26c5648afbf9d3f89602f76712c6d74c8808243bab551fd736fe89fb1454958e |
| `artwork/vector-masters/tetrasemaphore-build7-j4-screens/dose-01-iphone-17-pro-1206x2622-TETRASEMAPHORE-NORMATIVE-flashcard.png` | 275,105 | b8e04fd9ad63be7b14d03abaf9f24a650d167cf921068770eb152d220728f0d9 |
| `artwork/vector-masters/tetrasemaphore-build7-j4-screens/proofs/TETRASEMAPHORE-J4-FIVE-SCREENS-preview.png` | 582,878 | d7de5512907a52d5b5d1de91ef0a8c90b2c7d0ef013e806ec275ac3108a81ec8 |
| `artwork/vector-masters/tetrasemaphore-build7-j4-screens/work/build-five.js` | 33,316 | af3ab4e85e5b1c1c2783742c0123a06829bf558e18ff1e0774fc553f6b60131c |
| `artwork/vector-masters/tetrasemaphore-build7-j4-screens/work/lane-check-five-out.txt` | 4,559 | ba05a8f0aabe5927de7a3d1fdf02a8b2d6103858b173225bf780f687a347db34 |
| `artwork/vector-masters/tetrasemaphore-build7-j4-screens/work/lane-check-five-run.json` | 14,172 | 30020941075ccfe41df06dd57dff1d11f4ea726ab087d5dbad27d72b0d9988ec |
| `artwork/vector-masters/tetrasemaphore-build7-j4-screens/work/lane-check-five.py` | 15,144 | ddf686707892d49574439d5204055787a924f277da9716a6b3bf15b10f3ef6b8 |
| `artwork/vector-masters/tetrasemaphore-build7-j4-screens/work/lane-check-paths.js` | 699 | 386c3d04a674000c97e5a7f28295b3e001b239d5b9cb17bcd810c0f754967408 |
| `artwork/vector-masters/tetrasemaphore-build7-j4-screens/work/layout_report.json` | 37,338 | 1a9760c6eeb3975e222ccb2463acd9d61b43d13000249350bd6a52f3c2d5862a |
| `artwork/vector-masters/tetrasemaphore-build7-j4-screens/work/render-five.sh` | 938 | 5811c4973101563eba24f85630fa12e6ea7f4f6c731b617245baff68b680081b |
| `artwork/vector-masters/tetrasemaphore-build7-j4-screens/work/verify-five-out.txt` | 14,652 | 72daadc1f9c762bff3a791806dd5a76f4cd4cb764eb79d6b39345432a7b14685 |
| `artwork/vector-masters/tetrasemaphore-build7-j4-screens/work/verify-five.py` | 35,920 | 9655a55f827ea1eb135004cd0806342b0ac527ad9db8d1805cec8de6437cba64 |
| `artwork/vector-masters/tetrasemaphore-build7-j4-screens/work/verify_report.json` | 31,125 | 0242e03613fcfeaa5271716bcdfcfa3b1fac824245ce1502f176e7a9a6b86506 |
| `artwork/vector-masters/tetrasemaphore-build7-og-card/README.md` | 4,192 | 97c6995344aa3a2dcbc39cfb2818fb3d978249d2e56e93dabef954243aa6f61d |
| `artwork/vector-masters/tetrasemaphore-build7-og-card/SHA256.txt` | 326 | 4f0bd98ec821ff28d0c654aa72065dc8e61dc649cfe3ce5888399b7f81a29e27 |
| `artwork/vector-masters/tetrasemaphore-build7-og-card/og-card-MASTER.svg` | 11,547,869 | 0660fd91c299902384cefa4bede42cc70a3a05a556911186d5cc61fdb7b1b49f |
| `artwork/vector-masters/tetrasemaphore-build7-og-card/og-card.jpg` | 183,315 | a175dc759f3a2fd950ff2710ea94eb4e8f8bcc0a5590ee7a89344615d1066573 |
| `artwork/vector-masters/tetrasemaphore-build7-og-card/og-card.png` | 217,921 | 0cf08ac9028fc22dcc3c927cabd64dd3ec22234a168f4af2f23c912885aa4ce3 |
| `artwork/vector-masters/tetrasemaphore-build7-og-card/proofs/og-card-preview.png` | 104,134 | 5b1af9480016f6d5e3a58ba1f7822425cfd4cc4dd5554e43b9e4d94b70a1516b |
| `artwork/vector-masters/tetrasemaphore-build7-og-card/work/build-og-card.js` | 14,967 | addb1e5a77834cc0a07a68e79750cf7b47cc76335c0958bb3eec51757eb9e4a8 |
| `artwork/vector-masters/tetrasemaphore-build7-og-card/work/layout_report.json` | 3,716 | be7ad7a92cdb3889d4b8f3b0628e6ebb06fb8609fcd28e5702fafb6e9bae77c3 |
| `artwork/vector-masters/tetrasemaphore-build7-og-card/work/verify-og-card.py` | 7,145 | f79ebe66dfa896cebebaa9fd1f6c2a9a4d7c14ee7693c220222a856583bc1b02 |
| `artwork/vector-masters/tetrasemaphore-build7-og-card/work/verify_report.json` | 2,420 | 646a741e36dcb86a9701f8a962fae9c2987b932e3b172643b368cc9efc197210 |
| `artwork/vector-masters/tetrasemaphore-build7/README.md` | 3,809 | f0fb41b00306a09a0e0b74e94c72e599603ae3396b8425989dd404e28751d3c5 |
| `artwork/vector-masters/tetrasemaphore-build7/SHA256.txt` | 520 | 320f5ae098ac04c26c5154c92e2ada144f6ce30a12463c9b82c6e6bdcf0b1943 |
| `artwork/vector-masters/tetrasemaphore-build7/dose-01-iphone-17-pro-lockscreen-1206x2622-TETRASEMAPHORE-METACOGNITIVE-MASTER.svg` | 2,836,894 | a62a3dd18508996054f89c302bc36323cc88bbe185e008ebdcdec2322f3285ed |
| `artwork/vector-masters/tetrasemaphore-build7/dose-01-iphone-17-pro-lockscreen-1206x2622-TETRASEMAPHORE-METACOGNITIVE.png` | 272,507 | f2e7dee3412f5b92bd8b78bad1b0222d0e06107e16ffc67281e7e48dbc85600b |
| `artwork/vector-masters/tetrasemaphore-build7/proofs/TETRASEMAPHORE-LOCKSCREEN-METACOGNITIVE-build6-vs-build7-1206.png` | 272,113 | 4a61fba145951dcc7c6aa87f860ff493a3d8a60513da8e2a71e7b952202d617a |
| `artwork/vector-masters/tetrasemaphore-build7/proofs/TETRASEMAPHORE-LOCKSCREEN-METACOGNITIVE-build7-coin-and-row-3x.png` | 1,002,274 | 6f5f1471540d84bcc72052e9b8f120f0d274d4b58178b9e49edb67bd24d26f36 |
| `artwork/vector-masters/tetrasemaphore-build7/work/build-meta7.js` | 8,277 | b64cd9df95b18b8fdce95304598a363c107c16e3fb982cbd76588257466c3408 |
| `artwork/vector-masters/tetrasemaphore-build7/work/verify-meta7-run.json` | 676 | 77aa2ab9541ca99649562b35af04837bcbeb65693f6d138d3a8e7b6f6d5c2f9f |
| `artwork/vector-masters/tetrasemaphore-build7/work/verify-meta7.py` | 5,357 | b575632ea6f451151bfb458eb7f5f88d63141cb87737ba115d62f3b8f2a40165 |
| `methods/tetrasemaphore-methods-note-01-rev1.md` | 15,308 | 46f436d9ef3a35ceceec395a4f86009e8bfa094fcf786fbb1e9da468b518cb05 |
| `methods/tetrasemaphore-methods-note-01.md` | 7,829 | 10a216a4cf8861c0ab04b5faca8ec529eaf6cfea76838c3fd2e7d091d420e536 |
| `pdf/TETRASEMAPHORE-METHODS-NOTE-01.pdf` | 2,796,025 | 3bf981b258544cf15c2c2c22ef9aad1433a8a32bea2bff79e6d6fd601191ad36 |
| `pdf/TETRASEMAPHORE-PUBLIC-NOTE.pdf` | 2,802,582 | 7e4f0e52986dcf2fc02f33c7c19a4bb31abdc1c06059bb2912c8b932ba3266cd |
| `proofs/ANSWERS_v2.2_SECOND_OPINION.md` | 30,607 | b7897400e7b9bbe492c816da063d6596a70c9eff0a08a995ef258baad0b18297 |
| `proofs/ANSWERS_v2.3_SECOND_OPINION.md` | 25,086 | 8e0180103468f93d0049cca9a3382dc3d4873fe0ccaa061b1c4693a631da808b |
| `proofs/CHANGES_v2.2_to_v2.3.md` | 19,783 | b7d8c2031cd20aacce6a98d7f9f39d3afdcfe9f4aaece574e31928bcb59be94d |
| `proofs/CHANGES_v2.3_to_v2.4.md` | 9,872 | 9d523a8e2bfa9291ab5ae172227c2757b927038ae128fdf10ef106f825a5e4c5 |
| `proofs/CHANGES_v2.4.1_to_v2.4.2.md` | 9,570 | 5c438f85113eb693d49d04a50dd92b914c2e568f383db5acb8a1531895a3a5f3 |
| `proofs/CHANGES_v2.4_to_v2.4.1.md` | 13,224 | 62695593df4c3a14fb2baf5dacd0ed909d4675da3c038ec140c1537d1cb43f0f |
| `proofs/README_LEAN.md` | 52,081 | eb930febe5fec749b1fecfcf56f70a61b5c2d28b2414c3b8cdcffccffa700984 |
| `proofs/RED_TEAM_LEAN.md` | 110,747 | 89bde723a74f58db5896a554c2f7466b95104afe937cda36675e8e2a29609b14 |
| `proofs/RUN_INDEX.tsv` | 220,637 | 6fb36722a6513bf25c706fcb0b15412414a58055278b0ff64c9cfc7eda081fae |
| `proofs/SCIENCE_CHECK_v2.3.md` | 13,786 | bfc7327d83519c30b8fc0a50366f4b01ab7fb157b9b754cb7ddb82c03be74df3 |
| `proofs/SCIENCE_CHECK_v2.4.1.md` | 13,426 | 6b17554ff591947f75b09d0f214a22fb6d54ee358f7f7080c9858918ef9dcd2d |
| `proofs/SCIENCE_CHECK_v2.4.2.md` | 5,664 | 504e02e9b807df518968c95c5aab3a748107ac458c6945f7b70ce2d574d3d4a6 |
| `proofs/STATEMENTS.md` | 287,840 | 12b11a5e6651b38651a0b537b32c7d9f60aa82fcdb6d8d982e516f824ddadd86 |
| `proofs/TetrasemaphoreAlgebra.lean` | 61,638 | f066faf6595d22e94d6d7507b07e28a1993fe5d56e13d9a6512b9dcf9a30cd2a |
| `proofs/attack_matrix.json` | 417,388 | 0d24cf58b1438ee40692fc225ecd3198aa7c807a300fcac49e22966d29aafafa |
| `proofs/attacks/ABBREV16/TetrasemaphoreAlgebra.lean` | 61,725 | 394f4265b65d9a7fb39bdd354402ea1829536683d4c9c10813f86a01376bccd0 |
| `proofs/attacks/ABBREV16_AUX/TetrasemaphoreAlgebra.lean` | 61,739 | 679346bd4f734bee5adc7f323ac6d923f0d17c0a0a91dac0f8d8c8ab53d4837d |
| `proofs/attacks/ABBREVFALSE/TetrasemaphoreAlgebra.lean` | 61,858 | 2a0a7218f1fa50fe185de9d11db91a04983c042fb09030ea68d188cfffc66da6 |
| `proofs/attacks/ABBREVFALSE_AUX/TetrasemaphoreAlgebra.lean` | 61,878 | a5d9ad3ad702a7949af198218faba6798f8da2bb886089aaea4a69928e6f2a42 |
| `proofs/attacks/ATTACKS.tsv` | 6,433 | a165a7928217ce630081f085cda804beefd7e3b84e577a76c8eeb6f913e72046 |
| `proofs/attacks/AUXNAME_DEF/TetrasemaphoreAlgebra.lean` | 61,672 | 421628fb75a2408f6d4482d4b1ce5212c625439f160ab38a9ddd321ca6fe3f8d |
| `proofs/attacks/Comm_tamper_dangling_print/TetrasemaphoreAlgebra.lean` | 61,622 | 7c01faa6f2a1a45f32d329dbabf8a4450f66a7112ec064774427ace67283f57a |
| `proofs/attacks/DESYNC_EOF/TetrasemaphoreAlgebra.lean` | 61,713 | 84b28ac9093273a0fd1dc78f8695020aa342332d40437e4a9cd5ba373eafb925 |
| `proofs/attacks/DESYNC_EVAL/TetrasemaphoreAlgebra.lean` | 61,775 | 2f05dbb2e1ea6d8937a2b690a5be2f313e4c89868e48f679141fe37c94a6332c |
| `proofs/attacks/DESYNC_RAWSTRING/TetrasemaphoreAlgebra.lean` | 61,782 | 66a2e64cff7acaad208cfc786c876cc21a4e5497b91d304f8d92eb40e090e290 |
| `proofs/attacks/F1_honest_variants/TetrasemaphoreAlgebra.lean` | 61,965 | b99e16987e4d24eed2f57e268e96a13ff4db834632c3d074db8b593bd51cbf1a |
| `proofs/attacks/F2_string_sorry/TetrasemaphoreAlgebra.lean` | 61,715 | d7a7dae718f8c45d56f036be0a6dee754fd823ceae795146469e2bf918295c12 |
| `proofs/attacks/K1d_proofN_name/TetrasemaphoreAlgebra.lean` | 61,689 | 3a445f6045d55e9ab9e5e48164b7ca618bc3e25ba1717bd6e15cfcd2300ba1dd |
| `proofs/attacks/LTSWAP/TetrasemaphoreAlgebra.lean` | 61,822 | 479e787a4b37131f52e214296254a3fbd47c4ba82dd7d088ec850dfbf698082d |
| `proofs/attacks/M1a_holds_arm_swap/TetrasemaphoreAlgebra.lean` | 61,638 | 3f467c422bea414861890d53e08c6f19b1c552b770247ae19ddbb4bcd8ccbcbc |
| `proofs/attacks/M1b_holds_rhs_swap/TetrasemaphoreAlgebra.lean` | 61,638 | e81fb7991e16cf83d64114a2c08971f48511bb780991a9ff8c0dcb6217c26793 |
| `proofs/attacks/N1_hidden_instance/TetrasemaphoreAlgebra.lean` | 61,684 | 865a0adbc58f41068bb440709cf3e50e5938e0e0ec4aad62a8c3e92760002519 |
| `proofs/attacks/N1b_false_row_hidden_instance/TetrasemaphoreAlgebra.lean` | 61,811 | d55a180f17526376929572913379554d9a77eb7fd591c41ff3c38a70cb89c1f4 |
| `proofs/attacks/N1c_visible_instance/TetrasemaphoreAlgebra.lean` | 61,691 | 972f4f7eb24e6488330cfe2df43f703acf5a6519946c4dc99e67e06231b46655 |
| `proofs/attacks/N1e_aux_named_instance/TetrasemaphoreAlgebra.lean` | 61,693 | cb6455d67334203a62f1e19a6d019539cfce7c9061255ae0627b7b40162091bf |
| `proofs/attacks/N3b_extern_existing_def/TetrasemaphoreAlgebra.lean` | 61,671 | b4dc1f092d72de75edc26004ed0e41f0a10cd15bce53ff35226bd21d74f03fea |
| `proofs/attacks/N3b_extern_sameline/TetrasemaphoreAlgebra.lean` | 61,671 | 16b0a1a01689568825b7376e8fa3d3250b8431dc78aa35294e2f757133c92d11 |
| `proofs/attacks/N6_eval_sees_wrapper/TetrasemaphoreAlgebra.lean` | 61,750 | c4f501246159fe5760cdd2704ba1a5fd0039c236924feb1cc2c0155534ec8641 |
| `proofs/attacks/N6b_indented_eval/TetrasemaphoreAlgebra.lean` | 61,745 | ea9b849369758a261b1ee1c5a682fa13d050d8f53ed422713597bbc6a2cd41f6 |
| `proofs/attacks/NEGFALSE/TetrasemaphoreAlgebra.lean` | 61,796 | e3c7083d713059d7ff6453b2359ea52e90a5e342c05d8f36081c2c163d7d87e6 |
| `proofs/attacks/NEGFALSE_VISIBLE/TetrasemaphoreAlgebra.lean` | 61,798 | 696a370cca6327c51da32349c393bcf32c6d48bf30a02b8294df006236693750 |
| `proofs/attacks/NEG_LOCAL_SECTION/TetrasemaphoreAlgebra.lean` | 61,816 | 9397021b1b684739ac1362b06ee39f78f62fd4ef895facc37d78bb10ecfb1edc |
| `proofs/attacks/PRIVATE_DEF/TetrasemaphoreAlgebra.lean` | 61,675 | f4f8e15bd0f18a226c57ed7f7f1f3c3174d7e65cd1e42e77f01775e271eef2b2 |
| `proofs/attacks/README.md` | 3,569 | 3f9f453bb37a7928eb5898cd485c15d848d0e7b68d1d8e8360cd4cfa68bcbf3f |
| `proofs/attacks/S5_22_attr_newline_axiom/TetrasemaphoreAlgebra.lean` | 61,681 | 9684c2bbc806842c03943b011f82e1f77af5ef760e02ae942b2cb0b2c8dd2489 |
| `proofs/attacks/S5_24_exit/TetrasemaphoreAlgebra.lean` | 61,645 | f56319b02ebdc211bf7316cd13321ddaa53c65a51f7d8f6eacf53c3306eb1d54 |
| `proofs/attacks/S5_31_keyword_split_newline/TetrasemaphoreAlgebra.lean` | 61,678 | bb5e162fda4f1a01dc3991285ec0947fd4e47c9b73fd0dbfb9c2a75986962f48 |
| `proofs/attacks/a10_macro_command/TetrasemaphoreAlgebra.lean` | 61,716 | e1b99bba9b1a174f01d592f7e449e6ee3bbb641238087af8a54b4d6f01b4dba2 |
| `proofs/attacks/a13_extern_space/TetrasemaphoreAlgebra.lean` | 61,721 | 7a7595d1cebebb2685a033b30a5951d6133bb241ac1c19cb94b6b42dd8a4e377 |
| `proofs/attacks/a15_full_chain/TetrasemaphoreAlgebra.lean` | 61,790 | dd23dc149475cce572e01925975152553c11666304c90ef83c5d4d740755b5af |
| `proofs/attacks/a16_macro_sorry/TetrasemaphoreAlgebra.lean` | 61,685 | 0281e64041280278ae4c4d34ddc4a949c77b68daa62ed14508971a06a8c06e32 |
| `proofs/attacks/a17_poison_audit/TetrasemaphoreAlgebra.lean` | 61,704 | f4fd92eaef1225136759edb652a1823556aafff145abb5860adcbb29bb45516e |
| `proofs/attacks/a2_guard_msgs_printaxioms/TetrasemaphoreAlgebra.lean` | 61,664 | 29afe0ce95005872f5719a8cfec92e76d4b5f0e22f7cbc08a2bd834f521e975e |
| `proofs/attacks/a5_macro_decide_native/TetrasemaphoreAlgebra.lean` | 61,702 | 9c6abfd37a11a8d21daca36e0b9f62a70647362736fbba24e4520fa15d745ca3 |
| `proofs/attacks/a9_quoted_sorryAx/TetrasemaphoreAlgebra.lean` | 61,649 | c6638fe44c222a47a9bc4853085e00c60f4b5a68ec363ad115b056c1f5f83594 |
| `proofs/attacks/build_attacks.py` | 10,097 | 99fd88333c8885e0a8ff8dcf1c1761f9e6c2d38fcdbeb4649b09f6a40f4068fa |
| `proofs/attacks/build_attacks_v24.py` | 6,850 | 82d45ebb0b0e9ce91206d0548759881c3d6efb2fed8fb261c21184fa4e17d83f |
| `proofs/check.sh` | 102,794 | ab6f55d3216e1f193678e94eeb6c780572163906cd389188a17332850655b626 |
| `proofs/check_output.txt` | 14,484 | df2f24dc4e5e38521b9fd3e0dca57fd76986047ae1eec46b0628e374804242e0 |
| `proofs/lean-toolchain` | 25 | 302cd63c54178885b89e669f33b38f12f4dd7ae7e5cac537b3203e3768d8fb2b |
| `record/decision-log.md` | 74,854 | 612cc1da69b448c0cee547e3eba0dbf4461cab9fce2769e679db9cdbc04b9ac0 |
| `record/exchanges.md` | 9,013 | b2185f5bd07e8b20268790fe875edd16047b6823f8170192a481d95c5e0063fa |
| `record/release-plan.md` | 25,667 | 07cb7d0457baa3c9533b9a97abc032a9c6462ec2bb5d20a1cc3b70f8baad0471 |
| `record/test-register.md` | 23,076 | 23b34fb2164f1da4ed07a9ac54178dbe3be4bd9cefb3a1ab615b5bbb756648d2 |
| `site/.well-known/security.txt` | 159 | e6955225abbdb95fde382ff4607f42c6a0512f02ff592e9b311985216dec9b47 |
| `site/404.html` | 12,175 | d80a2e8a50c933351069b59609af44affa787518957c4b40658a1a678db1d8a7 |
| `site/Makefile` | 2,198 | bc1d5d2e00bab8ccf8d5169074add3817f57a512b3fde56840965a2b818e5dd5 |
| `site/assets/TETRASEMAPHORE-CRITICAL-en-1298.png` | 757,191 | a43da812ca3a7c885a4e688c978e6e4011c0996968b2411b6ca8a959a0ae2461 |
| `site/assets/TETRASEMAPHORE-CRITICAL-en-512.png` | 170,102 | 89dc35c8fcd840f0de8b75e3df094798b9a417472ffaa1ca707b2a7bac5613a3 |
| `site/assets/TETRASEMAPHORE-CRITICAL-es-1298.png` | 756,826 | 54bcc40dea8e470dc1f7e9a2ab6f5b0f5c73b258339908608e8eed38158015b7 |
| `site/assets/TETRASEMAPHORE-CRITICAL-es-512.png` | 170,087 | 30af4e519891b595c81ea243c7b0a87ee9fe9418bf382a7a50b29151dc98eed4 |
| `site/assets/TETRASEMAPHORE-METACOGNITIVE-en-1298.png` | 721,125 | 0f050e240c74e952fb475211b5a31657b832e374d9587656e7f76df085cc0de0 |
| `site/assets/TETRASEMAPHORE-METACOGNITIVE-en-512.png` | 162,619 | 1fc5ca3480246e1277bcb56849ebb93293866dd43aa7f21d069b90f86df6e2ec |
| `site/assets/TETRASEMAPHORE-METACOGNITIVE-es-1298.png` | 720,975 | 0b74d6670118923a2b15c0770c3cc123b658deee5ff7d95add1964066fe2fad4 |
| `site/assets/TETRASEMAPHORE-METACOGNITIVE-es-512.png` | 162,481 | 289b7447e6ab663e6a96c8745815080cbaef1f731407760aa8e5f5fdb55f37be |
| `site/assets/TETRASEMAPHORE-NON-NORMATIVE-en-1298.png` | 720,684 | 658837bd2d2802b35b8a85f91fdd50d839471acf092f57e9f587589f42bc8db0 |
| `site/assets/TETRASEMAPHORE-NON-NORMATIVE-en-512.png` | 163,398 | 9b90f014e077453b7e2446ef42c8dc0b08375ceb194c1d418ad94c162ee1d91e |
| `site/assets/TETRASEMAPHORE-NON-NORMATIVE-es-1298.png` | 717,005 | a4017750741981e9ac61a99f652abd34b82bdf4aafd518e8bc2e8968fef50753 |
| `site/assets/TETRASEMAPHORE-NON-NORMATIVE-es-512.png` | 162,274 | af1236728c2dd7a64603672666a7ba264c44df16335230ca552099f39675c09d |
| `site/assets/TETRASEMAPHORE-NORMATIVE-en-1298.png` | 755,820 | eacf65bc9181f649ff29d76011bc0cc759f3c9aacb01b0ab4875c764b2526438 |
| `site/assets/TETRASEMAPHORE-NORMATIVE-en-512.png` | 168,560 | b893c34898ab9ebc4fcd8eb2f915a30253d5afb64548aad0afe1af7b3160600d |
| `site/assets/TETRASEMAPHORE-NORMATIVE-es-1298.png` | 755,972 | 077215b442760441426bd4270d844bbf16848891edeeea9a00f1b0837101b696 |
| `site/assets/TETRASEMAPHORE-NORMATIVE-es-512.png` | 168,591 | 1c49f6829a561265fcd0334654ec39c81ebc37caaaf2a8b1067be57f9dbc2577 |
| `site/assets/og-card.jpg` | 183,315 | a175dc759f3a2fd950ff2710ea94eb4e8f8bcc0a5590ee7a89344615d1066573 |
| `site/index.html` | 24,917 | 9cefa8b1bcaaa572390a7b361df925b3566b607fcd374580672563521991bbe5 |
| `site/infra/cloudfront/README.md` | 919 | 264cacf2b4beca9bf81d67d9139c66c9a181854d1a928b7474dbb9d258cf181a |
| `site/infra/cloudfront/assets-headers.json` | 2,472 | 8720263cee6486bfc79a288b17ebffedd93e6d86b53caea5bafc95c97914cb74 |
| `site/infra/cloudfront/security-headers.json` | 2,540 | b1db1cc42b2ca247f098d5050a731fccfc1f83ac9af59daf47130a1aef14d0a4 |
| `site/llms.txt` | 731 | da4c8e0c64396e80d105a8324bc25c0853fc4ee118fb943c2c199bdbe0807971 |
| `site/method.html` | 23,836 | 410b96764ff72659a3b748843998184640dba23d83d13aaf43001bc7d6897f5a |
| `site/note.html` | 40,336 | 425ddf1074af7775e341ed89af60ca1a8f5bc05bf711adc3bdb14ee5f3a056bd |
| `site/robots.txt` | 76 | 2a3a3eb6c8c64a268097fd3fc989b7ee7caac07785f4c4fa3a71ad70dbb69089 |
| `site/sitemap.xml` | 424 | 86c9471d3f7fe9bc345ef2497e4a599d2d064489374a781bde713a76ba35a9a9 |
| `site/verify.sh` | 9,501 | 9c1d072fb53aa3b11ddd33b1002046ce7133944bcdf0b96f24b0377302b66811 |
| `tools/generate_pdfs.py` | 20,070 | 3e6eea4933a83d6191b412616df6e33a8ecdb679806e055112cfc433a9469a32 |
