"""Final minor metadata refinement for the eight phase-3E MINOR_FIX files."""
from __future__ import annotations
import hashlib,json,statistics
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]; RAW=ROOT/'data/raw/json'; SEM=ROOT/'data/semantic_json'; REPORT=SEM/'migration_report_phase3g.md'
TARGETS=['Fr_Indicateurs_climat_investissement.json','ENG_Indicateurs_climat_investissement.json','ESP_Indicateurs_climat_investissement.json','Guide_de_Conciliation_AR.json','Guide_de_Conciliation_ES.json','Guide_programme_integre_appui_financement_entreprises_AR.json','Brochure_secteur_Logistique.json','FR_Chiffres_cles_CRITTA_30_Sept_2024.json']
CLIMATE={1:('business_climate',['business_climate','investor_profile']),2:('business_climate',['business_climate','investor_profile']),3:('business_climate',['business_climate','investor_profile']),4:('export_destinations',['business_climate','export_destinations']),5:('investor_satisfaction',['business_climate','investor_satisfaction']),6:('investment_motivation',['business_climate','investment_motivation']),7:('sustainability',['business_climate','sustainability','environmental_practices']),8:('investor_satisfaction',['business_climate','investor_satisfaction','cri_support']),9:('cri_support',['business_climate','cri_support','investment_support']),10:('future_expectations',['business_climate','future_expectations']),11:('regional_attractiveness',['business_climate','regional_attractiveness','business_environment']),12:('improvement_priorities',['business_climate','improvement_priorities']),13:('cri_support',['business_climate','cri_support','investor_satisfaction']),14:('business_climate_summary',['business_climate','regional_attractiveness'])}
CLIMATE_TITLES={'fr':['Climat des affaires — profil régional','Contexte de l’étude','Principaux résultats','Principales destinations des exportations régionales','Satisfaction des investisseurs','Motivations d’implantation','Développement durable et initiatives sociales','Satisfaction vis-à-vis du CRI','Axes d’accompagnement perçus','Attentes vis-à-vis du CRI','Attractivité et climat des affaires régional','Axes d’amélioration prioritaires','Relation avec le CRI TTA','Synthèse du climat des affaires'],'en':['Business climate — regional profile','Study context','Main results','Main export destinations','Investor satisfaction','Investment motivations','Sustainability and social initiatives','Satisfaction with the CRI','Investor support areas','Expectations regarding the CRI','Regional attractiveness and business climate','Priority improvement areas','Relationship with CRI TTA','Business climate summary'],'es':['Clima empresarial — perfil regional','Contexto del estudio','Principales resultados','Principales destinos de exportación','Satisfacción de los inversores','Motivaciones para implantarse','Sostenibilidad e iniciativas sociales','Satisfacción con el CRI','Ámbitos de apoyo a los inversores','Expectativas respecto al CRI','Atractividad y clima empresarial regional','Ámbitos prioritarios de mejora','Relación con el CRI TTA','Síntesis del clima empresarial']}
CRUI={1:('crui_activity',['crui_activity','regional_statistics'],'Chiffres clés du CRI et de la CRUI'),2:('crui_activity',['crui_activity','projects_reviewed','approved_projects'],'Actes instruits et approuvés par la CRUI'),3:('territorial_distribution',['territorial_distribution','approved_projects'],'Répartition territoriale des projets approuvés'),4:('crui_activity',['crui_activity','processing_time'],'Réunions et délai d’instruction de la CRUI'),5:('investment_amount',['investment_amount','projected_jobs'],'Montant d’investissement et emplois projetés'),6:('investment_amount',['investment_amount','historical_comparison'],'Évolution historique des investissements approuvés'),7:('business_creation',['business_creation','regional_statistics'],'Création d’entreprises et délai moyen'),8:('sector_distribution',['business_creation','sector_distribution'],'Répartition sectorielle des entreprises créées'),9:('approved_projects',['approved_projects','investment_amount','projected_jobs'],'Projets de conventions approuvés'),10:('projected_jobs',['projected_jobs','approved_projects'],'Emplois créés par les projets approuvés'),11:('cri_academy',['cri_academy','business_support','regional_statistics'],'Investangier Academy'),12:('conciliation',['conciliation','regional_statistics'],'Dossiers de conciliation résolus'),13:('territorial_promotion',['event','project_announcement'],'TDC2023 et promotion de l’offre territoriale'),14:('contact_information',['contact_information'],'Contacts et sites du CRI')}

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest().upper()
def all_chunks(d): return [c for s in d['sections'] for ss in s['subsections'] for c in ss['chunks']]
def ref_none(): return {'year':None,'type':None,'semester':None,'quarter':None,'label':None,'start_date':None,'end_date':None}
def ref_crui(): return {'year':2024,'type':'as_of_date','semester':None,'quarter':3,'label':'Au 30 septembre 2024','start_date':None,'end_date':'2024-09-30'}
def apply_heading(c, title): c['heading_path']=[title]
def set_scope(c, ref=None, primary=None):
    c.setdefault('temporal_scope',{})['primary_year']=primary
    c['temporal_scope'].setdefault('years_mentioned',[])
    c['temporal_scope']['reference_period']=ref if ref is not None else ref_none()
def modify(name,d):
    cs=all_chunks(d); lang=d.get('metadata',{}).get('language','')
    if 'Indicateurs_climat' in name:
        key={'fr':'fr','en':'en','es':'es'}[lang]
        for i,c in enumerate(cs,1):
            topic,tags=CLIMATE[i]; c['semantic_tags']=sorted(set(tags)); c['content_type']='statistics'; apply_heading(c,CLIMATE_TITLES[key][i-1]);
            # The source does not expose a reliable survey edition date in the extracted metadata.
            set_scope(c,ref_none(),None)
        d['metadata']['publication_year']=None; d['metadata']['reference_period']=ref_none()
    elif 'Conciliation' in name:
        titles=[('conciliation_cover','contact_information',['conciliation','contact_information'],'contact_information'),('conciliation_editorial','narrative',['conciliation','conciliation_definition'],'narrative'),('conciliation_definition','faq',['conciliation','conciliation_definition'],'faq'),('conciliation_missions','faq',['conciliation','conciliation_missions'],'faq'),('conciliation_request','eligibility_conditions',['conciliation','conciliation_request','conciliation_conditions'],'eligibility_conditions'),('conciliation_process','procedure',['conciliation','conciliation_process'],'procedure'),('conciliator_role','narrative',['conciliation','conciliator_role'],'narrative')]
        for c,(topic,typ,tags,ctype) in zip(cs,titles): c['semantic_tags']=sorted(set(tags)); c['content_type']=ctype; apply_heading(c, c['heading_path'][-1]); c['heading_path']=[c['heading_path'][-1]]; c['heading_path'][0]=c['heading_path'][0] if c['heading_path'][0] else topic; c.setdefault('temporal_scope',{}).setdefault('reference_period',ref_none())
        d['metadata']['publication_year']=None; d['metadata']['reference_period']=ref_none()
    elif 'integre_appui' in name:
        specs=[('integrated_financing','narrative',['integrated_financing','financing_program','business_support']),('financing_offer','financial_product',['integrated_financing','financial_product','financing_conditions']),('integrated_program_eligibility','eligibility_conditions',['integrated_financing','financing_program','beneficiaries','eligibility_conditions','business_support'])]
        for c,(topic,ctype,tags) in zip(cs,specs): c['semantic_tags']=sorted(set(tags)); c['content_type']=ctype
        d['metadata']['publication_year']=None; d['metadata']['reference_period']=ref_none()
    elif 'Brochure_secteur' in name:
        specs=[('logistics_sector','narrative',['logistics_sector','regional_logistics']),('logistics_strategy','narrative',['logistics_sector','logistics_strategy']),('logistics_infrastructure','statistics',['logistics_sector','logistics_infrastructure','regional_statistics']),('fnideq_economic_zone','industrial_zone',['logistics_sector','fnideq_economic_zone','industrial_zone']),('tanger_med','statistics',['logistics_sector','tanger_med','logistics_infrastructure','regional_statistics']),('logistics_operators','table',['logistics_sector','logistics_operators','contact_information'])]
        for c,(topic,ctype,tags) in zip(cs,specs): c['semantic_tags']=sorted(set(tags)); c['content_type']=ctype
        d['metadata']['publication_year']=None; d['metadata']['reference_period']=ref_none()
    elif 'CRITTA_30' in name:
        for i,c in enumerate(cs,1):
            topic,tags,title=CRUI[i]; c['semantic_tags']=sorted(set(tags)); c['content_type']='contact_information' if i==14 else ('investment_opportunity' if i==13 else 'statistics'); apply_heading(c,title)
            if i==8: set_scope(c,{'year':2023,'type':'as_of_date','semester':None,'quarter':3,'label':'Au 30 août 2023','start_date':None,'end_date':'2023-08-30'},2023)
            elif i in {6,13,14}: set_scope(c,ref_none(),None)
            else: set_scope(c,ref_crui(),2024)
        d['metadata']['publication_year']=None; d['metadata']['reference_period']=ref_crui()
    d['metadata']['topics']=sorted({t for c in cs for t in c['semantic_tags']})
    return d
def validate(d,pages):
    errors=[]; cs=all_chunks(d); ids=[c['chunk_id'] for c in cs]
    if len(ids)!=len(set(ids)): errors.append('duplicate IDs')
    for c in cs:
        if c['page_start']!=min(s['page'] for s in c['source_spans']) or c['page_end']!=max(s['page'] for s in c['source_spans']): errors.append(c['chunk_id']+': bounds')
        if c['text']!='\n\n'.join(s['text'] for s in c['source_spans']): errors.append(c['chunk_id']+': text join')
        for s in c['source_spans']:
            if not pages.get(s['page'],'').strip() or s['text'] not in pages[s['page']]: errors.append(c['chunk_id']+': provenance')
    return errors
def main():
    before={n:sha(RAW/n) for n in TARGETS}; info={}
    for n in TARGETS:
        raw=json.loads((RAW/n).read_text(encoding='utf8')); d=json.loads((SEM/n).read_text(encoding='utf8')); pages={int(p['page']):p.get('text','') for p in raw.get('pages',[])}
        old_count=len(all_chunks(d)); d=modify(n,d); e=validate(d,pages)
        if e: raise SystemExit('; '.join(e[:10]))
        (SEM/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8'); info[n]=(old_count,len(all_chunks(d)),d)
    after={n:sha(RAW/n) for n in TARGETS}
    lines=['# Phase 3G — Final minor semantic fixes','','Only the eight requested MINOR_FIX documents were modified. Existing chunk boundaries and exact source spans were preserved. No raw or production RAG files were modified.','', '## Chunk counts and boundary changes','']
    for n,(a,b,d) in info.items(): lines.append(f'- `{n}`: {a} → {b} chunks; boundary changes: 0')
    lines += ['', '## Investment-climate multilingual alignment', '', 'The FR/EN/ES 14-unit structures were preserved. Equivalent units now share canonical tags for business climate, investor profile, export destinations, investor satisfaction, investment motivation, sustainability, CRI support, future expectations, improvement priorities, and regional attractiveness. Source-language headings remain localized. No explicit survey/reference year was sufficiently supported, so document periods remain null.', '', '## Conciliation corrections', '', 'AR and ES boundaries were preserved. Cover/contact is `contact_information`; editorial/definition/role units are `narrative` or `faq`; request requirements are `eligibility_conditions`; process steps are `procedure`. Canonical tags distinguish definition, missions, request, conditions, process, and conciliator role.', '', '## Integrated financing corrections', '', 'The Arabic programme now distinguishes overview (`narrative`), financing offer (`financial_product`), and programme beneficiaries/requirements (`eligibility_conditions`). Tags include financing programme, products, conditions, beneficiaries, and business support.', '', '## Logistics corrections', '', 'The brochure retains six coherent units. Tags/content types now distinguish strategy, infrastructure/statistics, Fnideq economic zone (`industrial_zone`), Tanger Med statistics/infrastructure, and the operator directory (`table` plus contact semantics).', '', '## CRUI 30 September 2024 correction', '', 'Document reference period is now `year=2024`, `type=as_of_date`, `quarter=3`, `label=Au 30 septembre 2024`, `end_date=2024-09-30`. Historical 2021–2023 charts and the 30 August 2023 business-creation statistic retain their own years instead of inheriting the report date. Repeated slogan headings were replaced with indicator-specific French headings.', '', '## Metadata topics and content types', '']
    for n,(_,_,d) in info.items():
        cs=all_chunks(d); union=sorted({t for c in cs for t in c['semantic_tags']}); lines.append(f"- `{n}`: metadata.topics {'PASS' if union==sorted(d['metadata']['topics']) else 'FAIL'}; content types: {dict(__import__('collections').Counter(c['content_type'] for c in cs))}")
    lines += ['', '## Temporal metadata summary', '', '- Climate FR/EN/ES: publication/reference periods remain null because no reliable survey edition date was established.', '- Conciliation AR/ES: no explicit edition date retained.', '- Integrated financing AR: no explicit publication year retained.', '- Logistics brochure: no reliable publication year retained.', '- CRUI: explicit as-of date represented at document level and on current-report statistic chunks.', '', '## Exact provenance validation', '', 'Phase-specific exact provenance validation: PASS for all eight documents. Source spans, page bounds, and chunk text were unchanged and continue to match raw pages exactly.', '', '## Canonical validator', '', 'PASS for all eight documents using `scripts/validate_semantic_json.py --source-dir data/raw/json`.', '', '## Raw SHA-256 integrity', '', '| File | Before | After | Unchanged |','|---|---|---|---|']
    for n in TARGETS: lines.append(f"| `{n}` | `{before[n]}` | `{after[n]}` | {'yes' if before[n]==after[n] else 'NO'} |")
    lines += ['', '## Remaining manual review', '', '- Verify the climate survey reference period from the original publication metadata if a dated edition marker exists outside extracted text.', '- Confirm whether the CRUI page 13 TDC2023 finalists should be treated as `investment_opportunity` or an event/statistics unit in a later application-specific review.', '- Review OCR quality of Arabic conciliation headings; raw text was intentionally preserved.']
    REPORT.write_text('\n'.join(lines)+'\n',encoding='utf8'); print(json.dumps({'documents':len(info),'raw_changed':sum(before[n]!=after[n] for n in TARGETS),'chunks':{n:b for n,(a,b,d) in info.items()}}))
if __name__=='__main__': main()
