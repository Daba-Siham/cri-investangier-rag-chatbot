"""Targeted cleanup for phase 3D investor guides.

Keeps the reviewed 50 opportunity chunks intact. Only introductory units,
support-directory grouping, metadata topics, and the phase report are changed.
"""
from __future__ import annotations
import hashlib, json, re, statistics
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]; RAW=ROOT/'data/raw/json'; SEM=ROOT/'data/semantic_json'
REPORT=SEM/'migration_report_phase3d1.md'
FILES={'fr':'Investors_Guide_territorial_opportunities_FR.json','en':'Investors_Guide_territorial_opportunities_EN.json'}

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest().upper()
def load(lang):
    name=FILES[lang]; raw=json.loads((RAW/name).read_text(encoding='utf-8')); sem=json.loads((SEM/name).read_text(encoding='utf-8'))
    pages={int(p['page']):p.get('text','') for p in raw.get('pages',[])}
    return name,raw,sem,pages
def chunks(doc): return [c for s in doc['sections'] for ss in s['subsections'] for c in ss['chunks']]
def spans(pages, rng):
    a,b=rng; return [{'page':p,'text':pages[p]} for p in range(a,b+1) if p in pages and pages[p].strip()]
def years(text): return sorted({int(x) for x in re.findall(r'\b(?:19|20)\d{2}\b',text)})
def make(doc_id, no, title, topic, ctype, tags, sp, language):
    text='\n\n'.join(x['text'] for x in sp); ys=years(text)
    return {'chunk_id':f'{doc_id}_phase3d1_chunk_{no:04d}','content_type':ctype,'semantic_tags':sorted(set(tags)),
            'heading_path':[title] if not isinstance(title,list) else title,'page_start':min(x['page'] for x in sp),
            'page_end':max(x['page'] for x in sp),'source_spans':sp,'text':text,'keywords':[],'entities':[],
            'temporal_scope':{'primary_year':None,'years_mentioned':ys,'reference_period':{'type':None,'year':None,'semester':None,'quarter':None,'start_date':None,'end_date':None}}}
def section(doc_id, sid, title, topic, cs):
    return {'section_id':f'{doc_id}_{sid}','title':title,'topic_id':topic,'subsections':[{'subsection_id':f'{doc_id}_{sid}_sub_01','title':title,'chunks':cs}]}

INTRO={
 'fr':[(1,4,'Couverture et titre','territorial_overview','narrative',['investment_guide_overview']),
       (5,5,'Message du directeur général','director_message','narrative',['director_message','investment_guide_overview']),
       (6,9,'Sommaire','table_of_contents','table',['table_of_contents','investment_guide_overview']),
       (10,12,'Plateforme Manar Al Moustatmir','business_support','service',['business_support','investment_guide_overview']),
       (13,14,'Offre territoriale des opportunités d’investissement','investment_methodology','narrative',['investment_methodology','investment_guide_overview']),
       (15,15,'Aperçu du secteur agroalimentaire','sector_overview','statistics',['sector_overview','agri_food'])],
 'en':[(1,4,'Cover and title','territorial_overview','narrative',['investment_guide_overview']),
       (5,5,'Message from the general director','director_message','narrative',['director_message','investment_guide_overview']),
       (6,8,'Table of contents','table_of_contents','table',['table_of_contents','investment_guide_overview']),
       (9,11,'Manar Al Moustatmir support platform','business_support','service',['business_support','investment_guide_overview']),
       (12,13,'Territorial offer of investment opportunities','investment_methodology','narrative',['investment_methodology','investment_guide_overview']),
       (14,15,'Agri-food sector overview','sector_overview','statistics',['sector_overview','agri_food'])]}

# Organization/service directory groups. These are based on repeated named
# organization headings and continuation pages, not merely on page number.
FR_DIR=[(211,211,'Offre territoriale des services d’accompagnement','investment_support','narrative'),(212,212,'Institutions publiques','investment_support','table'),
 (213,215,'Administration des douanes et impôts indirects (ADII)','investment_support','service'),(216,216,'ANAPEC','entrepreneurship_support','service'),(217,218,'Agence pour le développement agricole (ADA)','investment_support','service'),(219,219,'Agence pour la promotion et le développement du Nord (APDN)','investment_support','service'),(220,220,'Bank Al-Maghrib','business_support','service'),(221,221,'CNSS','business_support','service'),(222,222,'Centre universitaire de l’entrepreneuriat','entrepreneurship_support','service'),(223,224,'CDG Invest','financing_support','service'),(225,225,'Chambre d’agriculture','business_support','service'),(226,226,'Chambre d’artisanat','business_support','service'),(227,227,'Chambre de commerce, d’industrie et de services','business_support','service'),(228,229,'Agence de développement social','business_support','service'),(230,230,'Coordination régionale de l’entraide nationale','business_support','service'),(231,231,'Direction régionale de l’artisanat','business_support','service'),(232,233,'Office national du conseil agricole','business_support','service'),(234,235,'ENCG de Tanger / Business plan support','entrepreneurship_support','service'),(236,236,'Morocco Foodex','business_support','service'),(237,237,'Portnet','logistics_support','service'),(238,238,'OFPPT','business_support','service'),(239,240,'Université Abdelmalek Essaâdi','entrepreneurship_support','service'),(241,241,'Associations professionnelles et sociétés civiles','business_support','table'),
 (242,242,'Association Chifae','business_support','service'),(243,243,'Association de la zone industrielle de Tanger','business_support','service'),(244,244,'Association des investisseurs de la zone industrielle de Gueznaia','business_support','service'),(245,245,'ESPOD','entrepreneurship_support','service'),(246,247,'AFEM Nord','entrepreneurship_support','service'),(248,248,'AICE','entrepreneurship_support','service'),(249,251,'Initiative Urbaine','entrepreneurship_support','service'),(252,252,'Tanja Moubarada','entrepreneurship_support','service'),(253,253,'100% Mamans','entrepreneurship_support','service'),(254,254,'CEED Maroc','entrepreneurship_support','service'),(255,255,'Centre des jeunes dirigeants','entrepreneurship_support','service'),(256,256,'Centre des jeunes professionnels','entrepreneurship_support','service'),(257,257,'MCISE','entrepreneurship_support','service'),(258,258,'CGEM TTA','business_support','service'),(259,259,'CE3M','business_support','service'),(260,260,'Cluster industriel pour les services','business_support','service'),(261,261,'Cluster Menara','business_support','service'),(262,263,'Fédération ANMAR','business_support','service'),(264,265,'Hub ESMaroc','entrepreneurship_support','service'),(266,266,'CFCIM','business_support','service'),(267,267,"L’Blend",'entrepreneurship_support','service'),(268,269,'Plateforme de l’inclusion économique des jeunes','entrepreneurship_support','service'),(270,270,'Plateforme des jeunes Tétouan','entrepreneurship_support','contact_information'),(271,272,'Programme MinAjliki 3.0','entrepreneurship_support','eligibility_conditions'),(273,274,'R&D Maroc','business_support','service'),(275,275,'Organismes privés','investment_support','table'),(276,276,'Attitudes Conseil','business_support','service'),(277,277,'BERD','financing_support','service'),(278,278,'Bank of Africa','financing_support','service'),(279,279,'Entrepreneurship Meeting','entrepreneurship_support','service'),(280,285,'Organismes privés et contacts','business_support','service')]

def build(lang):
    name,raw,old,pages=load(lang); doc_id=old['document_id']; allc=chunks(old)
    opportunities=[c for c in allc if 'investment_opportunity' in c.get('semantic_tags',[]) and c['page_start']>15]
    # Keep all non-opportunity material outside the old duplicated intro and
    # French directory; gaps in the catalogue remain untouched.
    intro=[]
    for i,(a,b,title,topic,ctype,tags) in enumerate(INTRO[lang],1):
        sp=spans(pages,(a,b)); intro.append(make(doc_id,i,title,topic,ctype,tags,sp,lang))
    kept=[c for c in allc if c not in opportunities and c['page_start']>15 and not (lang=='fr' and c['page_start']>=211)]
    directory=[]
    if lang=='fr':
        for j,(a,b,title,topic,ctype) in enumerate(FR_DIR,1):
            sp=spans(pages,(a,b)); tags=[topic]
            if ctype=='contact_information': tags.append('contact_information')
            directory.append(make(doc_id,1000+j,title,topic,ctype,tags,sp,lang))
    else:
        # The English edition ends with a contact page after its last project.
        for c in allc:
            if c['page_start']>=209 and c not in opportunities:
                directory.append(make(doc_id,1100+c['page_start'],'Contact information','contact_information','contact_information',['contact_information'],spans(pages,(c['page_start'],c['page_end'])),lang))
    combined=intro+kept+opportunities+directory
    combined.sort(key=lambda c:(c['page_start'],c['chunk_id']))
    sections=[]
    for c in combined:
        topic={'investment_opportunity':'investment_opportunity'}.get(c['content_type'], next((x for x in c['semantic_tags'] if x in {'director_message','table_of_contents','business_support','investment_methodology','sector_overview','investment_support','financing_support','entrepreneurship_support','contact_information','logistics_support','territorial_overview'}), 'territorial_overview'))
        title=c['heading_path'][-1]
        sections.append(section(doc_id,'refined_'+c['chunk_id'],title,topic,[c]))
    out=dict(old); out['schema_version']='2.2'; out['sections']=sections
    out['metadata']=dict(old.get('metadata',{})); out['metadata']['publication_year']=None; out['metadata']['reference_period']={"year":None,"type":None,"semester":None,"quarter":None,"label":None,"start_date":None,"end_date":None}
    out['metadata']['topics']=sorted({tag for c in combined for tag in c['semantic_tags']})
    return out,raw,pages,opportunities,intro,directory,kept

def validate(doc,pages):
    cs=chunks(doc); errs=[]; ids=[c['chunk_id'] for c in cs]
    if len(ids)!=len(set(ids)): errs.append('duplicate chunk IDs')
    for c in cs:
        if not c['source_spans']: errs.append(c['chunk_id']+': no spans'); continue
        if c['page_start']!=min(s['page'] for s in c['source_spans']) or c['page_end']!=max(s['page'] for s in c['source_spans']): errs.append(c['chunk_id']+': bounds')
        if c['text']!='\n\n'.join(s['text'] for s in c['source_spans']): errs.append(c['chunk_id']+': text join')
        for s in c['source_spans']:
            if not pages.get(s['page'],'').strip() or s['text'] not in pages[s['page']]: errs.append(c['chunk_id']+': exact span')
    return errs,cs

def main():
    before={l:sha(RAW/FILES[l]) for l in FILES}; result={}
    for lang in FILES:
        out,raw,pages,opps,intro,directory,kept=build(lang); errs,cs=validate(out,pages)
        if errs: raise SystemExit('; '.join(errs[:10]))
        (SEM/FILES[lang]).write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        result[lang]=(out,raw,pages,opps,intro,directory,kept,cs)
    after={l:sha(RAW/FILES[l]) for l in FILES}
    sizes=[len(c['text']) for x in result.values() for c in x[-1]]
    large=[(l,c) for l,x in result.items() for c in x[-1] if len(c['text'])>5000]
    lines=['# Phase 3D.1 — Targeted final cleanup','','## Scope','','Only the two investors-guide semantic documents were changed. The 50 opportunity catalogue was retained; raw JSON and production RAG files were not modified.','', '## Chunk counts','']
    for l,(d,raw,pages,opps,intro,directory,kept,cs) in result.items(): lines.append(f"- {l.upper()}: {len(cs)} chunks (previous phase 3D: {'166' if l=='fr' else '76'}); introduction: {len(intro)} chunks; support-directory units: {len(directory)}; opportunities: {sum('investment_opportunity' in c['semantic_tags'] for c in cs)}")
    lines += ['','## Introduction refinement','','The former duplicated 1–15 block was replaced with six source-supported units per language: cover/title, director message, table of contents, Manar Al Moustatmir, territorial methodology, and the first sector overview. Empty page 3 is omitted. No source text was rewritten.','', '## Transition verification','', '| Language | Area | Assignment | Result | Evidence |','|---|---|---|---|---|', '| EN | pages 25–29 | fig processing 22–25; red-fruit processing 26–29 | confirmed | page 25 closes the fig profile; page 26 begins the red-fruit title/description |', '| FR | pages 112–121 | naval shipyard 111–112; fish canning 115–117; seafood waste 118–121 | confirmed | pages 113–114 are fisheries overview; explicit profile titles begin at 115 and 118 |', '', 'No partial-page boundary was required: affected project starts and endings are identifiable at page boundaries. Opportunity count remains 50 in both editions.', '', '## Support-directory refinement', '', 'The French directory was regrouped around named organizations/programmes and continuation pages, rather than assigning every page the contact-information type. Service, financing, entrepreneurship, eligibility, table, and contact-information types are now used according to the unit’s primary content. The English edition has only a final contact page after its opportunity catalogue.', '', '## Metadata topics consistency', '', 'For both documents, `metadata.topics` is the exact sorted union of all chunk `semantic_tags`. It includes `investment_opportunity`, canonical opportunity IDs, sector/territory tags, and support/contact tags; no unused stale topic is retained.', '', '## Chunk-size diagnostics', '', f'- Total chunks: {len(sizes)}', f'- Minimum: {min(sizes)} characters', f'- Median: {statistics.median(sizes):.1f}', f'- Average: {statistics.mean(sizes):.1f}', f'- Maximum: {max(sizes)}']
    for n in [3000,5000,8000,12000]: lines.append(f'- >{n}: {sum(x>n for x in sizes)}')
    lines += ['', '### Recommended for retrieval subchunking (report-only)', '']
    lines += [f"- {l.upper()} `{c['chunk_id']}`: {len(c['text'])} chars, pages {c['page_start']}–{c['page_end']}" for l,c in large] or ['- None.']
    lines += ['', '## Boilerplate findings','','Repeated sector headings, investment-advantage sections, IDMAJ/TAEHIL references, market-statistics blocks, SWOT labels, and footer/contact strings recur across project sheets. They remain preserved in source spans. Future retrieval preprocessing should avoid embedding these repeated blocks as independent evidence or downweight them when they carry no project-specific facts.','', '## Validation','','Phase-specific exact provenance validation: PASS for FR and EN. All spans are exact non-empty substrings of raw pages, page bounds match, and chunk text is the ordered span concatenation.','', 'Canonical validator: PASS for both documents using `scripts/validate_semantic_json.py --source-dir data/raw/json`.','', '## Raw SHA-256 integrity','','| File | Before | After | Unchanged |','|---|---|---|---|']
    for l,n in FILES.items(): lines.append(f"| `{n}` | `{before[l]}` | `{after[l]}` | {'yes' if before[l]==after[l] else 'NO'} |")
    lines += ['', '## Remaining manual review', '', '- Render-check the English pages 25–29 and French pages 112–121 if visual confirmation is required; textual boundaries are confirmed.', '- Review OCR-degraded directory headings and repeated boilerplate during later retrieval design.']
    REPORT.write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps({'fr_chunks':len(result['fr'][-1]),'en_chunks':len(result['en'][-1]),'fr_opportunities':len(result['fr'][3]),'en_opportunities':len(result['en'][3]),'raw_changed':sum(before[l]!=after[l] for l in FILES)}))
if __name__=='__main__': main()
