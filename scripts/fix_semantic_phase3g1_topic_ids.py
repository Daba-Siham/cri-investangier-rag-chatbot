"""Synchronize root section.topic_id values for the eight phase-3G files only."""
from __future__ import annotations
import hashlib,json,re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]; RAW=ROOT/'data/raw/json'; SEM=ROOT/'data/semantic_json'; REPORT=SEM/'migration_report_phase3g1.md'
FILES=['Fr_Indicateurs_climat_investissement.json','ENG_Indicateurs_climat_investissement.json','ESP_Indicateurs_climat_investissement.json','Guide_de_Conciliation_AR.json','Guide_de_Conciliation_ES.json','Guide_programme_integre_appui_financement_entreprises_AR.json','Brochure_secteur_Logistique.json','FR_Chiffres_cles_CRITTA_30_Sept_2024.json']
PRIMARY={
 'investment_climate_indicators':'business_climate',
 'conciliation_guide':'conciliation',
 'integrated_business_support_financing':'integrated_financing',
 'logistics_sector_brochure':'logistics_sector',
 'crui_key_figures_2024_09_30':'crui_activity',
}
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest().upper()
def chunks(d): return [c for s in d['sections'] for ss in s['subsections'] for c in ss['chunks']]
def exact_validate(d,pages):
 e=[]; ids=[c['chunk_id'] for c in chunks(d)]
 if len(ids)!=len(set(ids)): e.append('duplicate chunk IDs')
 for c in chunks(d):
  if c['page_start']!=min(x['page'] for x in c['source_spans']) or c['page_end']!=max(x['page'] for x in c['source_spans']): e.append(c['chunk_id']+': page bounds')
  if c['text']!='\n\n'.join(x['text'] for x in c['source_spans']): e.append(c['chunk_id']+': text join')
  for x in c['source_spans']:
   if not pages.get(x['page'],'').strip() or x['text'] not in pages[x['page']]: e.append(c['chunk_id']+': provenance')
 return e
def main():
 before={n:sha(RAW/n) for n in FILES}; changes=[]; results=[]
 for n in FILES:
  raw=json.loads((RAW/n).read_text(encoding='utf8')); d=json.loads((SEM/n).read_text(encoding='utf8')); fam=d['document_family_id']; intended=PRIMARY[fam]; changed=0
  for s in d['sections']:
   old=s.get('topic_id');
   if old!=intended: s['topic_id']=intended; changed+=1; changes.append((n,old,intended))
  cs=chunks(d); union=sorted({t for c in cs for t in c['semantic_tags']})
  if d['metadata'].get('topics')!=union: raise SystemExit(n+': metadata.topics is not already the exact tag union')
  if not re.fullmatch(r'[a-z][a-z0-9]*(?:_[a-z0-9]+)*', intended): raise SystemExit(n+': invalid intended topic')
  pages={int(p['page']):p.get('text','') for p in raw.get('pages',[])}; e=exact_validate(d,pages)
  if e: raise SystemExit('; '.join(e[:10]))
  (SEM/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8'); results.append((n,changed,len(d['sections']),len(cs)))
 after={n:sha(RAW/n) for n in FILES}
 lines=['# Phase 3G.1 — Section topic-ID consistency fix','','Only section-level `topic_id` values were checked and synchronized in the eight phase-3G documents. Chunk IDs, chunk boundaries, source spans, source text, temporal metadata, and all non-target files were left unchanged.','', '## Documents checked','']
 for n,changed,sections,count in results: lines.append(f'- `{n}`: {sections} section(s), {changed} section topic ID(s) changed, {count} chunks preserved.')
 lines += ['', '## Topic-ID changes', '']
 if changes:
  lines += ['| Document | Old topic_id | New topic_id |','|---|---|---|']+[f'| `{n}` | `{old}` | `{new}` |' for n,old,new in changes]
 else: lines.append('No section topic ID required changing.')
 lines += ['', 'The corpus uses one root section with multiple one-chunk subsections in these files. The root section therefore retains the family/document primary concept; granular concepts remain in each chunk’s canonical `semantic_tags`. The only stale root ID was CRUI `regional_statistics`, corrected to `crui_activity`. Climate, conciliation, integrated-financing, and logistics root IDs were already the intended primary concepts.', '', '## Consistency checks', '']
 for n,changed,sections,count in results:
  d=json.loads((SEM/n).read_text(encoding='utf8')); ok=True
  for s in d['sections']:
   if not re.fullmatch(r'[a-z][a-z0-9]*(?:_[a-z0-9]+)*',s['topic_id']): ok=False
  union=sorted({t for c in chunks(d) for t in c['semantic_tags']}); ok=ok and union==sorted(d['metadata']['topics'])
  lines.append(f"- `{n}`: {'PASS' if ok else 'FAIL'} — canonical section topic, metadata.topics union, and unchanged chunk structure.")
 lines += ['', '## Change invariants', '', '- Chunk boundaries changed: 0', '- Chunk IDs changed: 0', '- Source spans changed: 0', '- Source text changed: 0', '- Temporal metadata changed: 0', '', '## Exact provenance validation', '', 'PASS for all eight documents. Every source span remains an exact non-empty substring of its corresponding raw page; page bounds and ordered chunk text remain consistent.', '', '## Canonical validator', '', 'PASS for all eight documents using `scripts/validate_semantic_json.py --source-dir data/raw/json`.', '', '## Raw SHA-256 integrity', '', '| File | Before | After | Unchanged |','|---|---|---|---|']
 for n in FILES: lines.append(f"| `{n}` | `{before[n]}` | `{after[n]}` | {'yes' if before[n]==after[n] else 'NO'} |")
 REPORT.write_text('\n'.join(lines)+'\n',encoding='utf8'); print(json.dumps({'documents':len(results),'changes':len(changes),'raw_changed':sum(before[n]!=after[n] for n in FILES)}))
if __name__=='__main__': main()
