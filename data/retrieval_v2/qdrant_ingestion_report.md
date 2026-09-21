# Phase 4B — Qdrant v2 ingestion report

- Status: **PASS**
- Timestamp UTC: `2026-09-20T15:22:28.568324+00:00`
- Failure reason: `none`

## Configuration

- Collection: `cri_chunks_multilingual_e5_v2`
- Existing production collection: `cri_chunks_multilingual_e5_base` (never modified)
- Qdrant endpoint: `http://localhost:6333`
- Model: `intfloat/multilingual-e5-base`
- Local model source used: `C:\Users\siham\.cache\huggingface\hub\models--intfloat--multilingual-e5-base\snapshots\d128750597153bb5987e10b1c3493a34e5a4502a`
- Tokenizer: `intfloat/multilingual-e5-base`
- Vector dimension: 768
- Distance: COSINE
- Device: `cpu`
- Batch size: 128
- Normalization: `normalize_embeddings=True`

## Artifact validation

- JSONL SHA-256: `5062E2135C8856EB5BE03D68F0D065C8460825B6899F52E839487FD0519011F2`
- Source records: 1901
- Indexable records: 1894
- Skipped non-indexable records: 7

## Exact token validation

- Stored maximum token count: 499
- Exact final maximum token count: 499
- Exact inputs over 500: 0
- Records with stored/exact count differences: 1159
- Maximum absolute difference: 2

## Ingestion

- Expected point count: 1894
- Inserted point count: 1894
- Deterministic point IDs: UUID5 with fixed namespace, derived from `retrieval_chunk_id`
- Payload indexes: [{"field": "document_id", "schema": "keyword"}, {"field": "document_family_id", "schema": "keyword"}, {"field": "language", "schema": "keyword"}, {"field": "content_type", "schema": "keyword"}, {"field": "topic_id", "schema": "keyword"}, {"field": "semantic_tags", "schema": "keyword"}, {"field": "primary_year", "schema": "integer"}, {"field": "reference_period_year", "schema": "integer"}]
- Full `source_spans` stored in Qdrant: **no**
- `embedding_text` stored in Qdrant: **no**

## Vector sanity

- Dimension check: PASS
- Finite values: PASS
- Norm min/median/max: 0.9999998910150015 / 1.0000000305356544 / 1.0000001458027494

## Collection protection

- Base collection before: `{"exists": true, "name": "cri_chunks_multilingual_e5_base", "points": 1893, "vectors": {"size": 768, "distance": "Cosine"}}`
- Base collection after: `{"exists": true, "name": "cri_chunks_multilingual_e5_base", "points": 1893, "vectors": {"size": 768, "distance": "Cosine"}}`
- Base collection unchanged: **True**

## Multilingual dense-vector smoke searches

### French — Quels sont les coûts de branchement ou les démarches pour l'électricité ?

| Rank | Score | Language | Filename | Parent | Topic | Type | Pages | Preview |
|---:|---:|---|---|---|---|---|---|---|
| 1 | 0.858722 | fr | Guide_branchement_electricite_eau_assainissement.json | guide_branchement_electricite_eau_assainissement_grands_comptes_phase3f_0004 | utility_connections | service | 4–4 | VOTRE BRANCHEMENT ÉLECTRICITÉ |
| 2 | 0.853996 | fr | Guide_branchement_electricite_eau_assainissement.json | guide_branchement_electricite_eau_assainissement_grands_comptes_phase3f_0008 | utility_connections | procedure | 8–8 | WORKFLOW BRANCHEMENT AUX RÉSEAUX ÉLECTRIQUES Workflow de la demande de branchement au réseau d’Amendis. Types de branchement : • Branchement provisoire ; • Branchement définitif –  |
| 3 | 0.853618 | fr | Guide_branchement_electricite_eau_assainissement.json | guide_branchement_electricite_eau_assainissement_grands_comptes_phase3f_0008 | utility_connections | procedure | 8–8 | Pour le branchement provisoire en TFZ, s’ajoutent notamment : • Autorisation de la TFZ pour l’installation du compteur provisoire ; • Décision de Monsieur le Wali de la Région. Pou |
| 4 | 0.847895 | fr | Nv_Guide_Cout_facteurs_CRI_2024.json | nv_guide_cout_facteurs_cri_2024_phase3f_0017 | production_costs | table | 28–28 | 23 Tarifs Moyenne tension HORS TFZ TFZ Redevance de consommation en DH/kWh/mois Redevance de puissance en DH/kVa/an Redevance de consommation en DH/kWh/mois Redevance de puissance  |
| 5 | 0.846923 | fr | Nv_Guide_Cout_facteurs_CRI_2024.json | nv_guide_cout_facteurs_cri_2024_phase3f_0017 | production_costs | table | 27–27 | 22 Usage Tranches de consommation Redevance de consommation en DH/kWh/mois Eclairage patenté 0 - 150 kWh 1,5636 >150kWh 1,7877 Force motrice (Ascenseurs/ Piscines...) 0 - 100 kWh 1 |

### English — What investment opportunities exist in the automotive sector?

| Rank | Score | Language | Filename | Parent | Topic | Type | Pages | Preview |
|---:|---:|---|---|---|---|---|---|---|
| 1 | 0.839548 | en | Investors_Guide_territorial_opportunities_EN.json | investors_guide_territorial_opportunities_en_chunk_0012 | investment_opportunity | investment_opportunity | 54–54 | (+Essential parts integrating into the value chain of the first Moroccan export sector and high national industry integration rate in the automotive industry. (Economic and trade l |
| 2 | 0.832911 | en | Investors_Guide_territorial_opportunities_EN.json | investors_guide_territorial_opportunities_en_chunk_0020 | investment_opportunity | investment_opportunity | 87–88 | (2) Existence of investment benefits. * Depending on the location chosen, investors can also benefit from various advantages (EAZ, lAZ, IZ). ** For more information on funding mech |
| 3 | 0.832402 | fr | Investors_Guide_territorial_opportunities_FR.json | investors_guide_territorial_opportunities_fr_chunk_0020 | investment_opportunity | investment_opportunity | 87–87 | INDICATEURS FINANCIERS DE L’INVESTISSEMENT Coût potentiel de l’investissement Des prévisions de croissance pour le secteurautomobile marocain estimées à 17,5% offrant de réelles op |
| 4 | 0.828176 | en | Investors_Guide_territorial_opportunities_EN.json | investors_guide_territorial_opportunities_en_phase3d1_chunk_0005 | investment_methodology | narrative | 12–12 | TERRITORIAL OFFER OF INVESTMENT OPPORTUNITIES 2 4 |
| 5 | 0.826496 | en | Investors_Guide_territorial_opportunities_EN.json | investors_guide_territorial_opportunities_en_chunk_0020 | investment_opportunity | investment_opportunity | 89–89 | ELECTRICAL-ELECTRONICS SECTOR WITH HIGH POTENTIAL AT THE REGIONAL LEVEL AND STRONG There are 5 industrial zones dedicated to activities in this sector: Tanger Automotive City, TFZ, |

### Arabic — ما هي شروط الاستفادة من برامج التمويل؟

| Rank | Score | Language | Filename | Parent | Topic | Type | Pages | Preview |
|---:|---:|---|---|---|---|---|---|---|
| 1 | 0.856851 | ar | Guide_programme_integre_appui_financement_entreprises_AR.json | guide_programme_integre_appui_financement_entreprises_ar_chunk_002 | integrated_financing | financial_product | 4–4 | إلى البنوك الشريكة التي تعرض التمويلات المحددة في إطار هذا البرنامج وهي: • CFG BANK • CIH بنك • BMCI — Groupe BNP Paribas • Société Générale • Al Amal Bank • Arab Bank • Banque Pop |
| 2 | 0.841591 | ar | Guide_programme_integre_appui_financement_entreprises_AR.json | guide_programme_integre_appui_financement_entreprises_ar_chunk_002 | integrated_financing | financial_product | 3–3 | ما المقصود بعرض التمويل؟ يقصد بعرض التمويل مجموعة من القروض قابلة للتسديد تهدف إلى تمويل: • نفقات الاستثمار • نفقات التشغيل ماهي منتجات التمويل المتاحة؟ يتكون العرض من مجموعة من من |
| 3 | 0.840583 | ar | Guide_programme_integre_appui_financement_entreprises_AR.json | guide_programme_integre_appui_financement_entreprises_ar_chunk_002 | integrated_financing | financial_product | 3–4 | المنتج: START-TPE تعريف: قرض تكميلي يمنح إلى جانب القرض الاستثماري ويمكن من تمويل الحاجة إلى متطلبات رأس المال المتداول المرتبط بالاستثمار. مبلغ التمويل: يمكن أن يصل إلى 20% من الم |
| 4 | 0.818655 | ar | AR_Presentation_CRI_TTA.json | ar_pr_sentation_cri_tta_vf_semantic_035 | regional_positioning | narrative | 59–60 | شروط الإستفادة برامج الاستثمار الجديدة فى الاحداث او توسيع التي تبلغ تكلفتها مليون درهم على الاقل .إن كنتم هناء فأنتم في كل مكان؟؟ تثزواا مايرا كيف يتم تمويل المشاريع الأموال الذات |
| 5 | 0.818247 | fr | Guide du financement des entreprises.pdf | guide_du_financement_des_entreprises_intelak | bank_financing | financial_product | 32–32 | 32 Programme de financement couvrant les besoins d’investissement et de fonctionne- ment à des conditions préférentielles, destiné aux entreprises, personnes physiques ou morales,  |

### Spanish — ¿Qué servicios ofrece el CRI a los inversores?

| Rank | Score | Language | Filename | Parent | Topic | Type | Pages | Preview |
|---:|---:|---|---|---|---|---|---|---|
| 1 | 0.875684 | es | Guide_de_Conciliation_ES.json | guide_de_conciliation_es_chunk_004 | conciliation | faq | 4–4 | ¿Cuáles son las misiones de la Conciliación? • Recepción e instrucción de solicitudes de conciliación. • Contribuir a facilitar un acercamiento de puntos de vista entre inversiones |
| 2 | 0.863187 | es | Investment_Business_Support_Single_Window_ES.json | investment_business_support_single_window_es_phase3f_0002 | business_support | service | 3–3 | EL CRI DE LA REGIÓN TÁNGER-TETUÁN-ALHUCEMAS AL SERVICIO DE LOS INVERSORES De acuerdo con las Altas Orientaciones Reales, la reforma de los Centros Regionales de Inversión (CRI), im |
| 3 | 0.853282 | es | ESP_Presentation_CRI_TTA.json | esp_presentation_cri_tta_vf_semantic_003 | cri_missions | service | 3–3 | is ¿a Pared a lara) PITT A ¡Una vez aquí, está en todas partes! a INNEETAMZS El Centro Regional de Inversiones se encarga de contribuir a la aplicación de la política del Estado en |
| 4 | 0.851299 | es | Investment_Business_Support_Single_Window_ES.json | investment_business_support_single_window_es_phase3f_0003 | business_support | service | 4–4 | NUESTRA OFERTA DE SERVICIOS El CRI TTA también interviene ahora en la intermediación y conciliación para la resolución amistosa de disputas entre inversores y administraciones. Ade |
| 5 | 0.847961 | es | Investment_Business_Support_Single_Window_ES.json | investment_business_support_single_window_es_phase3f_0010 | business_support | service | 11–11 | MANAR AL MOUSTATMIR Primera ventanilla única comunitaria virtual de asesoramiento a los inversores • Estructura la acción colectiva, optimiza el proceso de asesoramiento y mejora l |

## Package versions

- `sentence-transformers`: 6.0.0
- `transformers`: 5.15.1
- `qdrant-client`: 1.19.0
- `torch`: 2.13.0
