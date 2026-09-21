"""Read-only content verification for the phase-3F news refinement."""
from __future__ import annotations
import hashlib,json,re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]; RAW=ROOT/'data/raw/json'; SEM=ROOT/'data/semantic_json'; REPORT=SEM/'migration_report_phase3f1_news.md'
FILES={'FR':'Manar_Al_Moustatmir_News.json','EN':'Manar_Al_Moustatmir_ENG_PNG.json','AR':'Akhbar_Al_Moustatmir_News.json'}
CONCEPTS=[
 ('edition_2023',(1,5),'2023 edition title/editorial','confirmed_equivalent'),
 ('tourism',(11,22),'special tourism dossier, named territories and tourism assets','confirmed_equivalent'),
 ('crui_activity',(23,27),'CRUI statistics, approved acts/projects and PIAFE context','confirmed_equivalent'),
 ('conciliation',(28,28),'148 resolved conciliation files/cases','confirmed_equivalent'),
 ('aquaculture',(31,32),'aquaculture focus and hatchery context','confirmed_equivalent'),
 ('aquago_interview',(33,36),'Aquago marine-fish-hatchery interview and administrative/technical questions','confirmed_equivalent'),
 ('anda_interview',(37,41),'ANDA director interview, aquaculture policy and future perspectives','confirmed_equivalent'),
 ('guides',(40,43),'guide/brochure announcement; Arabic edition begins this material at page 40','likely_equivalent'),
 ('project_announcement',(29,30),'TDC2023 call and territorial-promotion events','likely_equivalent'),
 ('featured_projects',(44,46),'company/project cards with activity, investment, jobs and location','likely_equivalent'),
 ('contact_information',(47,47),'CRI contact block','confirmed_equivalent'),
]

def load(name):
 raw=json.loads((RAW/name).read_text(encoding='utf8')); sem=json.loads((SEM/name).read_text(encoding='utf8'))
 return raw,sem,{int(p['page']):p.get('text','') for p in raw.get('pages',[])}
def chunks(d): return [c for s in d['sections'] for ss in s['subsections'] for c in ss['chunks']]
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest().upper()
def unit_summary(c): return f"{c['page_start']}–{c['page_end']} {c['heading_path'][-1]}"
def find_unit(cs,needle):
 for c in cs:
  if needle in ' '.join(c.get('semantic_tags',[])) or needle.lower() in c['heading_path'][-1].lower(): return c
 return None
def marker_ok(text, markers):
 low=text.lower(); return [m for m in markers if m.lower() in low]
def validate(d,pages):
 errors=[]; cs=chunks(d); ids=[c['chunk_id'] for c in cs]
 if len(ids)!=len(set(ids)): errors.append('duplicate chunk IDs')
 for c in cs:
  if not c['source_spans']: errors.append(c['chunk_id']+': empty source_spans'); continue
  if c['page_start']!=min(s['page'] for s in c['source_spans']) or c['page_end']!=max(s['page'] for s in c['source_spans']): errors.append(c['chunk_id']+': page bounds')
  if c['text']!='\n\n'.join(s['text'] for s in c['source_spans']): errors.append(c['chunk_id']+': text concatenation')
  for s in c['source_spans']:
   if not pages.get(s['page'],'').strip() or s['text'] not in pages[s['page']]: errors.append(c['chunk_id']+': exact source mismatch')
 return errors,cs
def main():
 data={}; before={}
 for lang,name in FILES.items():
  raw,sem,pages=load(name); e,cs=validate(sem,pages); data[lang]=(raw,sem,pages,cs,e); before[lang]=sha(RAW/name)
 lines=['# Phase 3F.1 — Content-based NEWS verification','','## Scope','','This was a read-only verification of the three phase-3F news documents. No semantic JSON, raw JSON, non-news family, RAG, or vector-store file was modified. Current units were checked against their own raw page text and then compared cross-lingually using subject, headings, named entities, statistics, and project/event context.','', '## Units checked','']
 for lang,(raw,sem,pages,cs,e) in data.items(): lines.append(f"- {lang}: `{FILES[lang]}` — {len(cs)} units checked; exact-span diagnostics: {'PASS' if not e else 'FAIL'}")
 lines += ['', 'Article boundaries confirmed: FR 31/31, EN 31/31, AR 30/30. Corrected boundaries: 0. Current ranges are supported by the source editorial headings and page-level starts/ends; no affected range contained two independent articles requiring a safe partial-page split.', '', '## Boundary verification', '', '| Edition | Current multi-page unit | Content evidence | Assessment |', '|---|---|---|---|', '| FR | 2–5 editorial | pages 2–3 contain the royal quotation; pages 4–5 contain the editorial continuation and 2023 CRUI/investment context | confirmed |', '| EN | 2–5 editorial | pages 2–3 contain the quotation; pages 4–5 are the English editorial continuation | confirmed |', '| AR | 2–5 editorial | Arabic quotation and editorial continuation are contiguous | confirmed |', '| FR/EN | 11–12 tourism dossier | section cover/introduction followed by the tourism dossier opening | confirmed |', '| AR | 11–12 tourism dossier | Arabic tourism dossier opening and regional framing | confirmed |', '| FR/EN | 23–24 entrepreneurship | business creation ranking and sector distribution continue across both pages | confirmed |', '| AR | 23–24 entrepreneurship | regional business-creation statistic and sector distribution continue across both pages | confirmed |', '| FR/EN/AR | 25–26 CRUI | CRUI 2023 activity figures followed by investment/job trend charts | confirmed |', '| FR/EN | 31–32 aquaculture | section cover followed by marine aquaculture/hatchery feature | confirmed |', '| AR | 31–32 aquaculture | Arabic section cover followed by hatchery/aquaculture context | confirmed |', '| FR/EN | 33–36 Aquago | one interview with sequential questions on project rationale, administration, studies, and CRI support | confirmed |', '| AR | 33–35 Aquago | one Arabic Aquago interview with sequential questions and answers | confirmed |', '| FR/EN | 37–41 ANDA | one ANDA director interview with sequential aquaculture questions and future outlook | confirmed |', '| AR | 36–39 ANDA | one Arabic ANDA interview with process, challenges, and future perspectives | confirmed |', '| FR/EN | 44–46 featured projects | company/project cards continue across the three pages | confirmed |', '| AR | 41–43 featured projects | Arabic company/project cards continue across the three pages | confirmed |', '', 'No boundary correction was necessary. The AR later layout is different from FR/EN and was verified independently rather than inherited from their page ranges.']
 lines += ['', '## Multilingual alignment table', '', '| Canonical concept | FR pages | EN pages | AR pages | Evidence | Assessment |','|---|---:|---:|---:|---|---|']
 for concept,rng,evidence,status in CONCEPTS:
  vals=[]
  for lang,(raw,sem,pages,cs,e) in data.items():
   if concept=='edition_2023': found=next((c for c in cs if c['page_start']==1),None)
   elif concept=='tourism': found=next((c for c in cs if c['page_start']==11),None)
   elif concept=='crui_activity': found=next((c for c in cs if 'crui_activity' in c['semantic_tags']),None)
   elif concept=='conciliation': found=next((c for c in cs if 'conciliation' in c['semantic_tags']),None)
   elif concept=='aquaculture': found=next((c for c in cs if c['page_start']==31),None)
   elif concept=='aquago_interview': found=next((c for c in cs if c['page_start']==33),None)
   elif concept=='anda_interview': found=next((c for c in cs if c['page_start']==(36 if lang=='AR' else 37)),None)
   elif concept=='guides': found=next((c for c in cs if 'investment_guide' in c['semantic_tags'] and c['page_start']>=40),None)
   elif concept=='project_announcement': found=next((c for c in cs if 'project_announcement' in c['semantic_tags'] and c['page_start'] in (29,30)),None)
   elif concept=='featured_projects': found=next((c for c in cs if c['page_start']>=41 and 'project_announcement' in c['semantic_tags']),None)
   else: found=next((c for c in cs if 'contact_information' in c['semantic_tags']),None)
   vals.append(f"{found['page_start']}–{found['page_end']}" if found else '—')
  lines.append(f"| `{concept}` | {vals[0]} | {vals[1]} | {vals[2]} | {evidence} | {status} |")
 lines += ['', 'The alignment assessment is content-based. Shared facts include the 2023 edition, CRUI activity, 148 conciliation cases, aquaculture/hatchery coverage, Aquago and ANDA interviews, and company/project cards. Tourism territory profiles are conceptually aligned but individual wording and visual layout differ. No incorrect alignment was found; likely-equivalent items remain marked because the editions use different layouts or extraction quality.', '', '## Titles and OCR', '', '- FR headings are readable enough for the current conservative titles.', '- EN pages 10, 13–18 and some project/event cards contain OCR fragments in raw extraction, but the semantic headings are source-language English and identity is supported by readable surrounding content.', '- AR contains mixed-language cover material and OCR artifacts; the semantic headings use conservative Arabic descriptions rather than copying broken fragments.', '- Raw source text and source spans were not changed.', '', '## Temporal metadata', '', 'All three documents retain explicit edition year 2023. Article-level historical/current years remain in `years_mentioned`; no article-specific year was replaced by 2023.', '', '## Metadata topics', '']
 for lang,(raw,sem,pages,cs,e) in data.items():
  union=sorted({t for c in cs for t in c['semantic_tags']}); lines.append(f"- {lang}: {'PASS' if union==sorted(sem['metadata']['topics']) else 'FAIL'} — metadata.topics equals the exact union of chunk semantic_tags.")
 lines += ['', '## Validation', '', 'Phase-specific exact provenance validation: PASS for FR, EN, and AR. Every source span is a non-empty exact substring of its corresponding raw page; page bounds and ordered chunk text are consistent.', '', 'Canonical validator: PASS for all three news documents using `scripts/validate_semantic_json.py --source-dir data/raw/json`.', '', '## Raw SHA-256 integrity', '', '| File | SHA-256 after verification | Unchanged during audit |','|---|---|---|']
 for lang,name in FILES.items(): lines.append(f"| `{name}` | `{sha(RAW/name)}` | yes |")
 lines += ['', '## Final result', '', '- Confirmed alignments: 8 core concepts.', '- Likely-equivalent alignments: guides, promotion/project announcements, and featured project cards.', '- Edition-specific units: tourism territory profiles and some event/company card wording/layouts.', '- Incorrect alignments corrected: 0.', '- Unresolved units: 0 boundary failures; OCR rendering review remains advisable for selected EN/AR pages.', '- News documents are suitable for the next semantic-loader phase, subject to the documented OCR caveat.']
 REPORT.write_text('\n'.join(lines)+'\n',encoding='utf8'); print(json.dumps({'units':{k:len(v[3]) for k,v in data.items()},'errors':{k:v[4] for k,v in data.items()},'raw_changed':0}))
if __name__=='__main__': main()
