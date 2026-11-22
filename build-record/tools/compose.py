#!/usr/bin/env python3
"""compose.py <finish-slot820.svg> <existing-master.svg> <out.svg> — keep everything before the finish's owl-slot element from the new finish,
and everything from the existing master's owl block (pupils defs / owl-placement / owl group) to the end."""
import sys, re
fin, old, out = sys.argv[1:4]
F=open(fin).read(); M=open(old).read()
m=re.search(r'<g id="owl-slot"[^>]*/>\s*', F); assert m, 'no owl-slot in finish'
head=F[:m.start()]
# keep the master's own <title>
t_old=re.search(r'<title>.*?</title>', M, re.S); t_new=re.search(r'<title>.*?</title>', head, re.S)
if t_old and t_new: head=head[:t_new.start()]+t_old.group(0)+head[t_new.end():]
starts=[k for k in (M.find('<defs><mask id="pupils"'), M.find('<g id="owl-pupils-open"'), M.find('<g id="owl-placement"'), M.find('<g id="owl" ')) if k>=0]
tail=M[min(starts):]
open(out,'w').write(head+tail); print(out, len(head), len(tail))
