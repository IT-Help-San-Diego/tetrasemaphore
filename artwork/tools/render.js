const {Resvg}=require('/private/tmp/claude-501/-Users-careybalboa-Downloads/f53c0528-5366-4b21-a083-f42921c4609f/scratchpad/meander/node_modules/@resvg/resvg-js');const fs=require('fs');
const [,,inp,out,w,bg]=process.argv; const opts={fitTo:{mode:'width',value:parseInt(w)}}; if(bg&&bg!=='none') opts.background=bg;
fs.writeFileSync(out,new Resvg(fs.readFileSync(inp,'utf8'),opts).render().asPng()); console.log('rendered',out);
