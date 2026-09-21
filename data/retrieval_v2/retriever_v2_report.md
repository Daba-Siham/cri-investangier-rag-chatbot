# Phase 4C — v2 retriever evaluation

- Timestamp UTC: `2026-09-20T21:00:12.769917+00:00`
- Collection: `cri_chunks_multilingual_e5_v2`
- Existing production retriever/collection: unchanged

## Configuration

- Candidate K: 30
- Final K: 5
- Score threshold: none
- Query language filter: none
- Same-language bonus: +0.005 maximum, soft tie-break only
- Semantic bonus: +0.004 per match, capped at +0.012; content type participates
- Temporal match bonus: +0.012
- Explicit conflicting primary/reference year penalty: -0.010
- Maximum retrieval chunks per semantic parent: 1 representative; sibling expansion deferred to context assembly
- Family diversity: soft +0.002 repeat penalty after the second result; no routine hard family cap
- Reranker: disabled
- Query embedding: `query: <user query>`, normalized E5 vector

## FR — Quels sont les coûts ou les démarches pour le branchement électrique ?

### Raw dense top 10

| Rank | Dense | Final | Lang | Family | Parent | Topic | Type | Pages | Preview |
|---:|---:|---:|---|---|---|---|---|---|---|
| 1 | 0.865279 | 0.874279 | fr | electricity_water_sanitation_connection | guide_branchement_electricite_eau_assainissement_grands_comptes_phase3f_0008 | utility_connections | procedure | 8–8 | Pour le branchement provisoire en TFZ, s’ajoutent notamment : • Autorisation de la TFZ pour l’installation du compteur provisoire ; • Décision de Monsieur le Wali de la Région. Pour le branchement définitif basse tension en TFZ, s’ajoutent  |
| 2 | 0.865155 | 0.874155 | fr | electricity_water_sanitation_connection | guide_branchement_electricite_eau_assainissement_grands_comptes_phase3f_0008 | utility_connections | procedure | 8–8 | WORKFLOW BRANCHEMENT AUX RÉSEAUX ÉLECTRIQUES Workflow de la demande de branchement au réseau d’Amendis. Types de branchement : • Branchement provisoire ; • Branchement définitif – basse tension ; • Branchement définitif – moyenne tension. É |
| 3 | 0.858569 | 0.863569 | fr | electricity_water_sanitation_connection | guide_branchement_electricite_eau_assainissement_grands_comptes_phase3f_0004 | utility_connections | service | 4–4 | VOTRE BRANCHEMENT ÉLECTRICITÉ |
| 4 | 0.849096 | 0.856096 | fr | electricity_water_sanitation_connection | guide_branchement_electricite_eau_assainissement_grands_comptes_phase3f_0007 | utility_connections | procedure | 7–7 | Client installé à la TFZ • Demande pour un branchement moyenne tension au nom du client confié à l'installateur ; • Demande pour approbation des plans du poste de transfo au nom de la société installatrice ; • Croquis de situation du projet |
| 5 | 0.847923 | 0.852923 | fr | electricity_water_sanitation_connection | guide_branchement_electricite_eau_assainissement_grands_comptes_phase3f_0006 | utility_connections | procedure | 6–6 | BRANCHEMENT DÉFINITIF EN BASSE TENSION Pour sa demande de branchement, le client doit présenter à Amendis : Client installé hors TFZ • Une demande écrite ; • La déclaration d’installation d’un nouveau branchement faite par un électricien ;  |
| 6 | 0.845789 | 0.852789 | fr | electricity_water_sanitation_connection | guide_branchement_electricite_eau_assainissement_grands_comptes_phase3f_0007 | utility_connections | procedure | 7–7 | BRANCHEMENT EN MOYENNE TENSION Pour sa demande de branchement, le client doit présenter : Client installé hors TFZ • Demande pour un branchement moyenne tension au nom du client confié à l'installateur ; • Demande pour approbation des plans |
| 7 | 0.844787 | 0.847787 | fr | electricity_water_sanitation_connection | guide_branchement_electricite_eau_assainissement_grands_comptes_phase3f_0005 | utility_connections | procedure | 5–5 | BRANCHEMENT PROVISOIRE Pour sa demande de branchement provisoire, le client doit présenter à Amendis : Client installé hors TFZ • Une demande écrite ; • La déclaration d’installation d’un nouveau branchement faite par un électricien ; • Pré |
| 8 | 0.843073 | 0.848073 | fr | production_factor_cost_guide_2024 | nv_guide_cout_facteurs_cri_2024_phase3f_0017 | production_costs | table | 28–28 | 23 Tarifs Moyenne tension HORS TFZ TFZ Redevance de consommation en DH/kWh/mois Redevance de puissance en DH/kVa/an Redevance de consommation en DH/kWh/mois Redevance de puissance en DH/kVa/an Heures Pointes 1,30486 522,31 1,19860 531,47 He |
| 9 | 0.842267 | 0.847267 | fr | production_factor_cost_guide_2024 | nv_guide_cout_facteurs_cri_2024_phase3f_0017 | production_costs | table | 27–27 | 22 Usage Tranches de consommation Redevance de consommation en DH/kWh/mois Eclairage patenté 0 - 150 kWh 1,5636 >150kWh 1,7877 Force motrice (Ascenseurs/ Piscines...) 0 - 100 kWh 1,4046 101 - 500 kWh 1,5264 >500kWh 1,7375 Redevances fixes B |
| 10 | 0.841317 | 0.844317 | fr | electricity_water_sanitation_connection | guide_branchement_electricite_eau_assainissement_grands_comptes_phase3f_0011 | utility_connections | procedure | 11–11 | BRANCHEMENT INCENDIE Pour sa demande de branchement incendie, le client doit présenter à Amendis : • Une demande écrite cachetée ; • Un justificatif d’occupation des lieux ; • Le plan indiquant le réseau incendie implanté, validé par la pro |

### Post-grouping/ranking final results

| Rank | Dense | Final | Lang | Family | Parent | Topic | Type | Pages | Preview |
|---:|---:|---:|---|---|---|---|---|---|---|
| 1 | 0.865279 | 0.874279 | fr | electricity_water_sanitation_connection | guide_branchement_electricite_eau_assainissement_grands_comptes_phase3f_0008 | utility_connections | procedure | 8–8 | Pour le branchement provisoire en TFZ, s’ajoutent notamment : • Autorisation de la TFZ pour l’installation du compteur provisoire ; • Décision de Monsieur le Wali de la Région. Pour le branchement définitif basse tension en TFZ, s’ajoutent  |
| 2 | 0.858569 | 0.863569 | fr | electricity_water_sanitation_connection | guide_branchement_electricite_eau_assainissement_grands_comptes_phase3f_0004 | utility_connections | service | 4–4 | VOTRE BRANCHEMENT ÉLECTRICITÉ |
| 3 | 0.849096 | 0.856096 | fr | electricity_water_sanitation_connection | guide_branchement_electricite_eau_assainissement_grands_comptes_phase3f_0007 | utility_connections | procedure | 7–7 | Client installé à la TFZ • Demande pour un branchement moyenne tension au nom du client confié à l'installateur ; • Demande pour approbation des plans du poste de transfo au nom de la société installatrice ; • Croquis de situation du projet |
| 4 | 0.847923 | 0.852923 | fr | electricity_water_sanitation_connection | guide_branchement_electricite_eau_assainissement_grands_comptes_phase3f_0006 | utility_connections | procedure | 6–6 | BRANCHEMENT DÉFINITIF EN BASSE TENSION Pour sa demande de branchement, le client doit présenter à Amendis : Client installé hors TFZ • Une demande écrite ; • La déclaration d’installation d’un nouveau branchement faite par un électricien ;  |
| 5 | 0.843073 | 0.848073 | fr | production_factor_cost_guide_2024 | nv_guide_cout_facteurs_cri_2024_phase3f_0017 | production_costs | table | 28–28 | 23 Tarifs Moyenne tension HORS TFZ TFZ Redevance de consommation en DH/kWh/mois Redevance de puissance en DH/kVa/an Redevance de consommation en DH/kWh/mois Redevance de puissance en DH/kVa/an Heures Pointes 1,30486 522,31 1,19860 531,47 He |

### Duplicate and diversity diagnostics

- Raw top-30 parent duplicate count: 9
- Raw top-30 family duplicate count: 25
- Siblings collapsed: 2
- Family-cap removals: 0
- Final-k cuts: 23
- Final language diversity: 1
- Final family diversity: 2
- Detected query language: fr
- Detected concepts: cost_information, procedure

## FR — Quels programmes de financement sont disponibles pour les entreprises ?

### Raw dense top 10

| Rank | Dense | Final | Lang | Family | Parent | Topic | Type | Pages | Preview |
|---:|---:|---:|---|---|---|---|---|---|---|
| 1 | 0.856610 | 0.861610 | fr | financing_guide | guide_du_financement_des_entreprises_piafe_index | bank_financing | narrative | 31–31 | LE FINANCEMENT PAR LE PROGRAMME INTÉGRÉ D’APPUI ET DE FINANCEMENT DES ENTREPRISES BANQUES INTELAK.............................................................................................................................32 INTELAK AL MOST |
| 2 | 0.856226 | 0.865226 | fr | financing_guide | guide_du_financement_des_entreprises_green_invest | public_financing | financial_product | 85–85 | des autres partenaires financiers. O Un business plan reprenant le détail du projet à financer. e Plafond de financement Les programmes d’investissement seront financés par les fonds propres et/ou l’autofinancement et par le crédit conjoin |
| 3 | 0.853792 | 0.856792 | fr | financing_guide | guide_du_financement_des_entreprises_partner_messages | guide_overview | narrative | 8–8 | Parallèlement aux efforts d’orientation, Bank Al-Maghrib entreprend également une panoplie de mesures pour soutenir l’accès des petites et moyennes entreprises aux financements bancaires. On peut en citer notamment, la mise en place d’un mé |
| 4 | 0.848098 | 0.849098 | fr | financing_guide | guide_du_financement_des_entreprises_ebrd_advice | international_financing | service | 133–133 | grâce a un soutien technique et financier accordé aux PME marocaines O 10 domaines de conseil concernés (stratégie, marketing, opérations, TIC, finance, organisation, gestion environne- mentale, solution d’ingénierie, management de la quali |
| 5 | 0.845727 | 0.850727 | fr | chiffres_cles_2025 | fr_chiffres_cles_annee_2025_p11_c01 | business_support | statistics | 11–11 | Accompagnement des entreprises (2/4) Bilan du PIAFE* au niveau de la région TTA 4 672 Dossiers financés ~1,14 M MAD de financement * Programme Intégré d’Appui et de Financement des Entreprises www.investangier.com 11 |
| 6 | 0.844954 | 0.845954 | fr | financing_guide | guide_du_financement_des_entreprises_industrial_fund_index | public_financing | narrative | 109–109 | LE FINANCEMENT PAR LES ORGANISMES PUBLICS LE FINANCEMENT PAR LE FONDS DE DÉVELOPPEMENT INDUSTRIEL ET DE L‘INVESTISSEMENT AIDES DIRECTES ACCORDÉES AUX ÉCOSYSTÈMES INDUSTRIELS........110 AIDES DIRECTES ACCORDÉES DANS LE CADRE DE LA CHARTE DE  |
| 7 | 0.843104 | 0.848104 | fr | financing_guide | guide_du_financement_des_entreprises_intelak | bank_financing | financial_product | 32–32 | 32 Programme de financement couvrant les besoins d’investissement et de fonctionne- ment à des conditions préférentielles, destiné aux entreprises, personnes physiques ou morales, de droit marocain, remplissant les conditions d’éligibilité. |
| 8 | 0.841833 | 0.846833 | fr | financing_guide | guide_du_financement_des_entreprises_industrial_ecosystem_aid | public_financing | financial_product | 110–110 | 110 L Description Le Fonds de Développement Industriel et des Investis- sements (FDII) a été créé pour le financement des program- mes relevant du Plan d’Accélération Industrielle (PAI). Le FDII permet au tissu industriel de se consolider, |
| 9 | 0.841393 | 0.842393 | fr | financing_guide | guide_du_financement_des_entreprises_vision_preamble | guide_overview | narrative | 6–6 | PREAMBULE Dans un environnement marqué par des mutations économiques permanentes et continues, l’entreprise est confrontée à de nombreux défis. Elle doit exister, survivre, croître et se développer, dans un marché fortement concurrentiel. D |
| 10 | 0.841270 | 0.846270 | fr | financing_guide | guide_du_financement_des_entreprises_intelak_al_moustatmir_qarawi | bank_financing | financial_product | 33–33 | 33 Crédits d’investissement et des crédits d’exploitation de 1,2 MDhs maximum accordés aux entreprises éligibles. L Description Financement des dépenses d’investissement relatives aux projets de création et d’extension (acquisition de loca |

### Post-grouping/ranking final results

| Rank | Dense | Final | Lang | Family | Parent | Topic | Type | Pages | Preview |
|---:|---:|---:|---|---|---|---|---|---|---|
| 1 | 0.856226 | 0.865226 | fr | financing_guide | guide_du_financement_des_entreprises_green_invest | public_financing | financial_product | 85–85 | des autres partenaires financiers. O Un business plan reprenant le détail du projet à financer. e Plafond de financement Les programmes d’investissement seront financés par les fonds propres et/ou l’autofinancement et par le crédit conjoin |
| 2 | 0.856610 | 0.861610 | fr | financing_guide | guide_du_financement_des_entreprises_piafe_index | bank_financing | narrative | 31–31 | LE FINANCEMENT PAR LE PROGRAMME INTÉGRÉ D’APPUI ET DE FINANCEMENT DES ENTREPRISES BANQUES INTELAK.............................................................................................................................32 INTELAK AL MOST |
| 3 | 0.853792 | 0.856792 | fr | financing_guide | guide_du_financement_des_entreprises_partner_messages | guide_overview | narrative | 8–8 | Parallèlement aux efforts d’orientation, Bank Al-Maghrib entreprend également une panoplie de mesures pour soutenir l’accès des petites et moyennes entreprises aux financements bancaires. On peut en citer notamment, la mise en place d’un mé |
| 4 | 0.845727 | 0.850727 | fr | chiffres_cles_2025 | fr_chiffres_cles_annee_2025_p11_c01 | business_support | statistics | 11–11 | Accompagnement des entreprises (2/4) Bilan du PIAFE* au niveau de la région TTA 4 672 Dossiers financés ~1,14 M MAD de financement * Programme Intégré d’Appui et de Financement des Entreprises www.investangier.com 11 |
| 5 | 0.848098 | 0.849098 | fr | financing_guide | guide_du_financement_des_entreprises_ebrd_advice | international_financing | service | 133–133 | grâce a un soutien technique et financier accordé aux PME marocaines O 10 domaines de conseil concernés (stratégie, marketing, opérations, TIC, finance, organisation, gestion environne- mentale, solution d’ingénierie, management de la quali |

### Duplicate and diversity diagnostics

- Raw top-30 parent duplicate count: 8
- Raw top-30 family duplicate count: 25
- Siblings collapsed: 1
- Family-cap removals: 0
- Final-k cuts: 24
- Final language diversity: 1
- Final family diversity: 2
- Detected query language: fr
- Detected concepts: financial_product

## FR — Quelles opportunités d'investissement existent dans le secteur automobile ?

### Raw dense top 10

| Rank | Dense | Final | Lang | Family | Parent | Topic | Type | Pages | Preview |
|---:|---:|---:|---|---|---|---|---|---|---|
| 1 | 0.874807 | 0.891807 | fr | investors_guide_territorial_opportunities | investors_guide_territorial_opportunities_fr_chunk_0020 | investment_opportunity | investment_opportunity | 87–87 | INDICATEURS FINANCIERS DE L’INVESTISSEMENT Coût potentiel de l’investissement Des prévisions de croissance pour le secteurautomobile marocain estimées à 17,5% offrant de réelles opportunités pour les équipementiers. Croissance de 6 % du par |
| 2 | 0.851091 | 0.868091 | fr | investors_guide_territorial_opportunities | investors_guide_territorial_opportunities_fr_chunk_0032 | investment_opportunity | investment_opportunity | 134–135 | Le Royaume a élaboré des stratégies et des plans sectoriels visant l’amélioration des niveaux de services de transport et de la logistique ainsi que le développement d’infrastructures de transport, tel que le Plan nationale portuaire 2030 e |
| 3 | 0.850961 | 0.867961 | fr | investors_guide_territorial_opportunities | investors_guide_territorial_opportunities_fr_chunk_0032 | investment_opportunity | investment_opportunity | 135–135 | Parc automobile équipé d’informatique embarquée permettant de géo localiser l’ensemble des véhicules actifs. Système d’information pour assurer un suivi en temps réel. Entrepôts pour le stockage. Personnel qualifié et formé. Formalités admi |
| 4 | 0.849998 | 0.866998 | fr | investors_guide_territorial_opportunities | investors_guide_territorial_opportunities_fr_chunk_0020 | investment_opportunity | investment_opportunity | 88–88 | Programme « IDMAJ » / Programme « TAEHIL » Casablanca / Kenitra / Tanger Risques exogènes: Crises sanitaires, ... Institut de Formation aux Métiers de l‘Industrie Automobile PRINCIPAUX INSTITUTS DE FORMATIONS AUX MÉTIERS DE L’INDUSTRIE AUTO |
| 5 | 0.849476 | 0.864476 | fr | investors_guide_territorial_opportunities | investors_guide_territorial_opportunities_fr_chunk_0009 | investment_opportunity | investment_opportunity | 46–46 | Un climat régional favorable aux cultures de cannabis (intrant de l’industrie) et proximité avec les producteurs. Chaîne de valeur existante et taux d’intégration national de l’industrie automobile élevé. Des normes strictes à respecter, re |
| 6 | 0.848976 | 0.847976 | fr | investors_guide_territorial_opportunities | investors_guide_territorial_opportunities_fr_chunk_0067 | territorial_overview | narrative | 41–41 | AUTOMOBILE 34 38 41 44 47 Unité de transformation de cannabis pour l'industrie automobile Unité industrielle d'amortisseurs Unité industrielle de filtres Unité industrielle de plaquettes de freins Projet de Vélo / Moto électriques 32 |
| 7 | 0.847490 | 0.862490 | fr | investors_guide_territorial_opportunities | investors_guide_territorial_opportunities_fr_chunk_0009 | investment_opportunity | investment_opportunity | 43–43 | Ecosystème réglementé en amont et en aval (avec des dispositions en vigueur notamment pour l’approvisionnement de plants et semences étrangères et de commercialisation). Climat régional favorable à la culture du cannabis et proximité avec l |
| 8 | 0.847365 | 0.860365 | fr | investors_guide_territorial_opportunities | investors_guide_territorial_opportunities_fr_chunk_0011 | investment_opportunity | investment_opportunity | 50–50 | à une forte demande locale. Augmentation de la demande du fait d’une accentuation et d’un renforcement des normes de sécurité. Indice de complexité pour les produits** L’automobile est un secteur structurant de la région de TTA. Une filière |
| 9 | 0.846294 | 0.857294 | fr | investors_guide_territorial_opportunities | investors_guide_territorial_opportunities_fr_chunk_0012 | investment_opportunity | investment_opportunity | 55–55 | Unité Industrielle De Plaquettes De Freins Concurrents sur le territoire Concurrents internationaux Allemagne Chine Mexique MATRICE SWOT DE L’OPPORTUNITÉ D’INVESTISSEMENT Forces Faiblesses Manque d’expertise en matière de R&D et de la Pièce |
| 10 | 0.845227 | 0.858227 | fr | investors_guide_territorial_opportunities | investors_guide_territorial_opportunities_fr_chunk_0011 | investment_opportunity | investment_opportunity | 52–52 | Unité industrielle de filtres automobiles Concurrents sur le territoire Concurrents internationaux Allemagne Chine USA *Non exhaustif MATRICE SWOT DE L’OPPORTUNITÉ D’INVESTISSEMENT Forces Faiblesses Pièce indispensable s’insérant dans la ch |

### Post-grouping/ranking final results

| Rank | Dense | Final | Lang | Family | Parent | Topic | Type | Pages | Preview |
|---:|---:|---:|---|---|---|---|---|---|---|
| 1 | 0.874807 | 0.891807 | fr | investors_guide_territorial_opportunities | investors_guide_territorial_opportunities_fr_chunk_0020 | investment_opportunity | investment_opportunity | 87–87 | INDICATEURS FINANCIERS DE L’INVESTISSEMENT Coût potentiel de l’investissement Des prévisions de croissance pour le secteurautomobile marocain estimées à 17,5% offrant de réelles opportunités pour les équipementiers. Croissance de 6 % du par |
| 2 | 0.851091 | 0.868091 | fr | investors_guide_territorial_opportunities | investors_guide_territorial_opportunities_fr_chunk_0032 | investment_opportunity | investment_opportunity | 134–135 | Le Royaume a élaboré des stratégies et des plans sectoriels visant l’amélioration des niveaux de services de transport et de la logistique ainsi que le développement d’infrastructures de transport, tel que le Plan nationale portuaire 2030 e |
| 3 | 0.849476 | 0.864476 | fr | investors_guide_territorial_opportunities | investors_guide_territorial_opportunities_fr_chunk_0009 | investment_opportunity | investment_opportunity | 46–46 | Un climat régional favorable aux cultures de cannabis (intrant de l’industrie) et proximité avec les producteurs. Chaîne de valeur existante et taux d’intégration national de l’industrie automobile élevé. Des normes strictes à respecter, re |
| 4 | 0.847365 | 0.860365 | fr | investors_guide_territorial_opportunities | investors_guide_territorial_opportunities_fr_chunk_0011 | investment_opportunity | investment_opportunity | 50–50 | à une forte demande locale. Augmentation de la demande du fait d’une accentuation et d’un renforcement des normes de sécurité. Indice de complexité pour les produits** L’automobile est un secteur structurant de la région de TTA. Une filière |
| 5 | 0.846294 | 0.857294 | fr | investors_guide_territorial_opportunities | investors_guide_territorial_opportunities_fr_chunk_0012 | investment_opportunity | investment_opportunity | 55–55 | Unité Industrielle De Plaquettes De Freins Concurrents sur le territoire Concurrents internationaux Allemagne Chine Mexique MATRICE SWOT DE L’OPPORTUNITÉ D’INVESTISSEMENT Forces Faiblesses Manque d’expertise en matière de R&D et de la Pièce |

### Duplicate and diversity diagnostics

- Raw top-30 parent duplicate count: 11
- Raw top-30 family duplicate count: 26
- Siblings collapsed: 9
- Family-cap removals: 0
- Final-k cuts: 16
- Final language diversity: 1
- Final family diversity: 1
- Detected query language: fr
- Detected concepts: automotive, investment_opportunity

## FR — Quels projets ont été approuvés par la CRUI en 2024 ?

### Raw dense top 10

| Rank | Dense | Final | Lang | Family | Parent | Topic | Type | Pages | Preview |
|---:|---:|---:|---|---|---|---|---|---|---|
| 1 | 0.875096 | 0.880096 | fr | manar_al_moustatmir_news_2023 | manar_al_moustatmir_news_phase3f_0020 | crui_activity | statistics | 25–26 | 19 Durant l’année 2023, la CRUI a instruit 972 actes lors de ses 230 réunions et pour lesquels la Commission Régionale Unifiée d’Investissement a approuvé 709 demandes, soit 73% des actes soumis, et ce dans un délai ne dépassant la moyenne  |
| 2 | 0.859987 | 0.876987 | fr | cri_presentation | fr_presentation_cri_tta_vf_semantic_029 | crui | statistics | 40–41 | a _ és si El = Une fois vous êtes ici, vous êtes partout ! ANR Bilan Une croissance soutenue des dossiers d'investissement approuvés en CRUI CRUI 2024 — 737 Evolution du nombre 508 Evolution du montant 2022 des dossiers approuvés CHUTE ï ss |
| 3 | 0.857622 | 0.882622 | fr | crui_key_figures_2024_09_30 | fr_chiffres_cles_critta_30_sept_2024_chunk_002 | crui_activity | statistics | 2–2 | Une fois vous êtes ici, vous êtes partout ! 693 actes instruits par la CRUI au 30 septembre 2024 615 actes approuvés par la CRUI au 30 septembre 2024 Évolution de la part des actes examinés favorablement par la CRUI 2021 au 30 septembre 202 |
| 4 | 0.852554 | 0.849554 | fr | manar_al_moustatmir_news_2023 | manar_al_moustatmir_news_phase3f_0002 | investment_news | narrative | 5–5 | www.investangier.com Par ailleurs, depuis l’entrée 2023 de la nouvelle charte de l’investissement, la CRUI a également joué un rôle crucial en approuvant 44 projets de convention d'investissement d'une valeur d'environ 18 milliards de dirha |
| 5 | 0.850459 | 0.863459 | fr | chiffres_cles_2025 | fr_chiffres_cles_annee_2025_p06_c01 | crui_activity | table | 6–6 | Bilan de la CRUI (3/6) Répartition sectorielle des dossiers d’investissement approuvés en CRUI Secteurs : Énergie Industrie Tourisme Services Autres Par nombre de projets : 487 dossiers d’investissement Énergie : 67% Industrie : 15% Tourism |
| 6 | 0.849753 | 0.866753 | fr | crui_key_figures_2024_h1 | chiffres_cles_crui_1er_semestre_2024_francais_chunk_002 | projects_reviewed | statistics | 2–2 | Une fois vous êtes ici, vous êtes partout ! 433 Nombre de projets instruits par la CRUI avec avis définitif 379 Projets approuvés soit 87,5% des projets statués en CRUI 40,76 Milliards MAD d’investissement soit +72% par rapport au 1er semes |
| 7 | 0.848063 | 0.843063 | fr | chiffres_cles_2025 | fr_chiffres_cles_annee_2025_p09_c01 | sector_investment | statistics | 9–9 | Bilan de la CRUI (6/6) Une région pionnière en énergie, moteur de compétitivité et durabilité à l’export 11 projets approuvés ~22,4 milliards de dirhams projetés +770 emplois à terme 2,4 GW de puissance installée 2 projets solaires approuvé |
| 8 | 0.843870 | 0.855870 | es | crui_key_figures_2024_h1 | chiffres_cles_crui_1er_semestre_2024_espagnol_chunk_002 | projects_reviewed | statistics | 2–2 | ¡Una vez aquí, está en todas partes! 433 proyectos examinados por la Comisión Regional Unificada de Inversiones (CRUI) 379 proyectos aprobados, el 87,5% de los proyectos examinados por la CRUI 40,76 mil millones de dirhams de inversión, un  |
| 9 | 0.842559 | 0.859559 | fr | crui_key_figures_2024_h1 | chiffres_cles_crui_1er_semestre_2024_francais_chunk_006 | approved_projects | statistics | 6–6 | Une fois vous êtes ici, vous êtes partout ! 16 Projets de conventions d’investissement approuvés 9,54 milliards MAD d’investissement 6 525 emplois directs projetés Ventilation sectorielle des montants d’investissement des conventions approu |
| 10 | 0.841703 | 0.862703 | fr | crui_key_figures_2024_09_30 | fr_chiffres_cles_critta_30_sept_2024_chunk_006 | crui_activity | statistics | 6–6 | Une fois vous êtes ici, vous êtes partout ! ÉVOLUTION DES MONTANTS D’INVESTISSEMENT APPROUVÉS EN CRUI 2021-2023 (EN MILLIARDS MAD) 2021 : 36,6 2022 : 52 2023 : ~73,4 2024 au 30 septembre 2024 : ~68,8 Évolution indiquée : +41% ÉVOLUTION DU N |

### Post-grouping/ranking final results

| Rank | Dense | Final | Lang | Family | Parent | Topic | Type | Pages | Preview |
|---:|---:|---:|---|---|---|---|---|---|---|
| 1 | 0.857622 | 0.882622 | fr | crui_key_figures_2024_09_30 | fr_chiffres_cles_critta_30_sept_2024_chunk_002 | crui_activity | statistics | 2–2 | Une fois vous êtes ici, vous êtes partout ! 693 actes instruits par la CRUI au 30 septembre 2024 615 actes approuvés par la CRUI au 30 septembre 2024 Évolution de la part des actes examinés favorablement par la CRUI 2021 au 30 septembre 202 |
| 2 | 0.875096 | 0.880096 | fr | manar_al_moustatmir_news_2023 | manar_al_moustatmir_news_phase3f_0020 | crui_activity | statistics | 25–26 | 19 Durant l’année 2023, la CRUI a instruit 972 actes lors de ses 230 réunions et pour lesquels la Commission Régionale Unifiée d’Investissement a approuvé 709 demandes, soit 73% des actes soumis, et ce dans un délai ne dépassant la moyenne  |
| 3 | 0.859987 | 0.876987 | fr | cri_presentation | fr_presentation_cri_tta_vf_semantic_029 | crui | statistics | 40–41 | a _ és si El = Une fois vous êtes ici, vous êtes partout ! ANR Bilan Une croissance soutenue des dossiers d'investissement approuvés en CRUI CRUI 2024 — 737 Evolution du nombre 508 Evolution du montant 2022 des dossiers approuvés CHUTE ï ss |
| 4 | 0.849753 | 0.866753 | fr | crui_key_figures_2024_h1 | chiffres_cles_crui_1er_semestre_2024_francais_chunk_002 | projects_reviewed | statistics | 2–2 | Une fois vous êtes ici, vous êtes partout ! 433 Nombre de projets instruits par la CRUI avec avis définitif 379 Projets approuvés soit 87,5% des projets statués en CRUI 40,76 Milliards MAD d’investissement soit +72% par rapport au 1er semes |
| 5 | 0.850459 | 0.863459 | fr | chiffres_cles_2025 | fr_chiffres_cles_annee_2025_p06_c01 | crui_activity | table | 6–6 | Bilan de la CRUI (3/6) Répartition sectorielle des dossiers d’investissement approuvés en CRUI Secteurs : Énergie Industrie Tourisme Services Autres Par nombre de projets : 487 dossiers d’investissement Énergie : 67% Industrie : 15% Tourism |

### Duplicate and diversity diagnostics

- Raw top-30 parent duplicate count: 4
- Raw top-30 family duplicate count: 24
- Siblings collapsed: 2
- Family-cap removals: 0
- Final-k cuts: 23
- Final language diversity: 1
- Final family diversity: 5
- Detected query language: fr
- Detected concepts: crui_activity, investment_opportunity

## EN — What investment opportunities exist in the automotive sector?

### Raw dense top 10

| Rank | Dense | Final | Lang | Family | Parent | Topic | Type | Pages | Preview |
|---:|---:|---:|---|---|---|---|---|---|---|
| 1 | 0.839548 | 0.856548 | en | investors_guide_territorial_opportunities | investors_guide_territorial_opportunities_en_chunk_0012 | investment_opportunity | investment_opportunity | 54–54 | (+Essential parts integrating into the value chain of the first Moroccan export sector and high national industry integration rate in the automotive industry. (Economic and trade liberalization policy (free trade agreements) (¿Sector suppor |
| 2 | 0.832911 | 0.849911 | en | investors_guide_territorial_opportunities | investors_guide_territorial_opportunities_en_chunk_0020 | investment_opportunity | investment_opportunity | 87–88 | (2) Existence of investment benefits. * Depending on the location chosen, investors can also benefit from various advantages (EAZ, lAZ, IZ). ** For more information on funding mechanisms, consult the CRI Funding Guide. PAL INVESTANGIER ELEC |
| 3 | 0.832402 | 0.842402 | fr | investors_guide_territorial_opportunities | investors_guide_territorial_opportunities_fr_chunk_0020 | investment_opportunity | investment_opportunity | 87–87 | INDICATEURS FINANCIERS DE L’INVESTISSEMENT Coût potentiel de l’investissement Des prévisions de croissance pour le secteurautomobile marocain estimées à 17,5% offrant de réelles opportunités pour les équipementiers. Croissance de 6 % du par |
| 4 | 0.828176 | 0.827176 | en | investors_guide_territorial_opportunities | investors_guide_territorial_opportunities_en_phase3d1_chunk_0005 | investment_methodology | narrative | 12–12 | TERRITORIAL OFFER OF INVESTMENT OPPORTUNITIES 2 4 |
| 5 | 0.826496 | 0.843496 | en | investors_guide_territorial_opportunities | investors_guide_territorial_opportunities_en_chunk_0020 | investment_opportunity | investment_opportunity | 89–89 | ELECTRICAL-ELECTRONICS SECTOR WITH HIGH POTENTIAL AT THE REGIONAL LEVEL AND STRONG There are 5 industrial zones dedicated to activities in this sector: Tanger Automotive City, TFZ, Tanger Tech, ZAE Ait Kamra, and Tétouan Park. The prefectur |
| 6 | 0.825803 | 0.842803 | en | investors_guide_territorial_opportunities | investors_guide_territorial_opportunities_en_chunk_0020 | investment_opportunity | investment_opportunity | 86–87 | Potential partnerships with operators in the sector and/or other national and international establishments. FINANCIAL INDICATORS OF THE INVESTMENT Potential investment cost e - from 15 million MAD CENTRE RÉGIONAL D'INVESTISSEMENT TANGER - T |
| 7 | 0.816913 | 0.829913 | en | investors_guide_territorial_opportunities | investors_guide_territorial_opportunities_en_chunk_0009 | investment_opportunity | investment_opportunity | 42–42 | The regional climate is favorable to cannabis cultivation, and proximity to farmers favors supply. Hemp fiber, representing 30% of the plant's composition, has been increasingly used in the automotive industry for nearly 10 years, enabling  |
| 8 | 0.812516 | 0.829516 | en | investors_guide_territorial_opportunities | investors_guide_territorial_opportunities_en_chunk_0020 | investment_opportunity | investment_opportunity | 89–89 | 81 ELECTRICAL-ELECTRONICS They have trusted us SECTOR WITH HIGH POTENTIAL AT THE REGIONAL LEVEL AND STRONG INTERSECTORAL SYNERGIES The electrical-electronics sector is a highpotential industry, capitalizing on its various applications upstr |
| 9 | 0.810644 | 0.821644 | en | investors_guide_territorial_opportunities | investors_guide_territorial_opportunities_en_chunk_0011 | investment_opportunity | investment_opportunity | 51–51 | 43 Competitors in the territory International competitors Germany China USA *Non exhaustif Opportunities Strengths Weaknesses Threats Indispensable part in the value of the Moroccan automotive sector. Proximity to the assembly plants of the |
| 10 | 0.810001 | 0.821001 | en | investors_guide_territorial_opportunities | investors_guide_territorial_opportunities_en_chunk_0011 | investment_opportunity | investment_opportunity | 51–51 | Industrial unit for automotive filters MAIN COMPETITORS* Competitors in the territory International competitors Germany China USA *Non exhaustif Strengths Weaknesses Indispensable part in the value of the Moroccan Need to respond to the spe |

### Post-grouping/ranking final results

| Rank | Dense | Final | Lang | Family | Parent | Topic | Type | Pages | Preview |
|---:|---:|---:|---|---|---|---|---|---|---|
| 1 | 0.839548 | 0.856548 | en | investors_guide_territorial_opportunities | investors_guide_territorial_opportunities_en_chunk_0012 | investment_opportunity | investment_opportunity | 54–54 | (+Essential parts integrating into the value chain of the first Moroccan export sector and high national industry integration rate in the automotive industry. (Economic and trade liberalization policy (free trade agreements) (¿Sector suppor |
| 2 | 0.832911 | 0.849911 | en | investors_guide_territorial_opportunities | investors_guide_territorial_opportunities_en_chunk_0020 | investment_opportunity | investment_opportunity | 87–88 | (2) Existence of investment benefits. * Depending on the location chosen, investors can also benefit from various advantages (EAZ, lAZ, IZ). ** For more information on funding mechanisms, consult the CRI Funding Guide. PAL INVESTANGIER ELEC |
| 3 | 0.832402 | 0.842402 | fr | investors_guide_territorial_opportunities | investors_guide_territorial_opportunities_fr_chunk_0020 | investment_opportunity | investment_opportunity | 87–87 | INDICATEURS FINANCIERS DE L’INVESTISSEMENT Coût potentiel de l’investissement Des prévisions de croissance pour le secteurautomobile marocain estimées à 17,5% offrant de réelles opportunités pour les équipementiers. Croissance de 6 % du par |
| 4 | 0.816913 | 0.829913 | en | investors_guide_territorial_opportunities | investors_guide_territorial_opportunities_en_chunk_0009 | investment_opportunity | investment_opportunity | 42–42 | The regional climate is favorable to cannabis cultivation, and proximity to farmers favors supply. Hemp fiber, representing 30% of the plant's composition, has been increasingly used in the automotive industry for nearly 10 years, enabling  |
| 5 | 0.828176 | 0.827176 | en | investors_guide_territorial_opportunities | investors_guide_territorial_opportunities_en_phase3d1_chunk_0005 | investment_methodology | narrative | 12–12 | TERRITORIAL OFFER OF INVESTMENT OPPORTUNITIES 2 4 |

### Duplicate and diversity diagnostics

- Raw top-30 parent duplicate count: 17
- Raw top-30 family duplicate count: 28
- Siblings collapsed: 13
- Family-cap removals: 0
- Final-k cuts: 12
- Final language diversity: 2
- Final family diversity: 1
- Detected query language: en
- Detected concepts: automotive, investment_opportunity

## EN — What support services does the CRI provide to investors?

### Raw dense top 10

| Rank | Dense | Final | Lang | Family | Parent | Topic | Type | Pages | Preview |
|---:|---:|---:|---|---|---|---|---|---|---|
| 1 | 0.866111 | 0.871111 | en | investors_guide_territorial_opportunities | investors_guide_territorial_opportunities_en_phase3d1_chunk_0002 | director_message | narrative | 5–5 | It aims to direct investors towards new investment niches and to facilitate access for project holders to information relating to the support services provided by the specialized bodies in the field, each according to its scope of intervent |
| 2 | 0.840745 | 0.845745 | en | investment_climate_indicators | eng_indicateurs_climat_dinvestissement_chunk_013 | business_climate | statistics | 25–26 | PERCEPTION OF THE RELATIONSHIP WITH CRI TTA 100% of all stakeholders interviewed maintain a very good and close relationship with CRI. All stakeholders interviewed are aware of the crucial and central role of CRI in the development of inves |
| 3 | 0.831610 | 0.831610 | es | conciliation_guide | guide_de_conciliation_es_chunk_004 | conciliation | faq | 4–4 | ¿Cuáles son las misiones de la Conciliación? • Recepción e instrucción de solicitudes de conciliación. • Contribuir a facilitar un acercamiento de puntos de vista entre inversiones y la administración o la entidad pública. • Manejar quejas, |
| 4 | 0.826971 | 0.831971 | en | investment_climate_indicators | eng_indicateurs_climat_dinvestissement_chunk_010 | business_climate | statistics | 19–20 | 6. Expectations Regarding the CRI Strengthening support for companies: 9% Giving more weight to assistance in finding land solutions: 6% Assisting in finding financial/subsidy solutions: 6% Strengthening the availability and ease of contact |
| 5 | 0.825916 | 0.842916 | en | investors_guide_territorial_opportunities | investors_guide_territorial_opportunities_en_phase3d1_chunk_0004 | business_support | service | 10–10 | INVESTORS MANAR AL MOUSTATMIR As part of its missions related to contributing to the implementation of the State policy on development, incentives, promotion, and attraction of investments at the regional level, as well as comprehensive sup |
| 6 | 0.820998 | 0.823998 | en | investment_climate_indicators | eng_indicateurs_climat_dinvestissement_chunk_009 | business_climate | statistics | 17–18 | Main Support axis Perceived by Investors Promotion of investment opportunities: 67% Proactive support for the development of your company's ecosystem: 29% Pre-investment assistance: 12% Provision of services related to starting your busines |
| 7 | 0.820155 | 0.824155 | es | cri_presentation | esp_presentation_cri_tta_vf_semantic_003 | cri_missions | service | 3–3 | is ¿a Pared a lara) PITT A ¡Una vez aquí, está en todas partes! a INNEETAMZS El Centro Regional de Inversiones se encarga de contribuir a la aplicación de la política del Estado en materia de desarrollo, fomento, promoción y atracción de in |
| 8 | 0.818974 | 0.821974 | en | investment_climate_indicators | eng_indicateurs_climat_dinvestissement_chunk_014 | business_climate | statistics | 27–28 | Summary Business climate The Tangier-Tetouan-Al Hoceima region is widely perceived as offering a very favorable business climate for investment, with potential mainly concentrated in industry, tourism, and agriculture. The region strongly a |
| 9 | 0.817210 | 0.829210 | fr | investment_business_support_single_window | investment_business_support_single_window_fr_phase3f_0002 | business_support | service | 3–3 | LE CRI TANGER-TÉTOUAN-AL HOCEIMA AU SERVICE DES INVESTISSEURS Conformément aux Hautes Orientations Royales, la réforme des Centres Régionaux d’Investissement (CRI), portée par la loi 47-18, est entrée en vigueur en décembre 2019. Elle a ass |
| 10 | 0.815585 | 0.818585 | en | investment_climate_indicators | eng_indicateurs_climat_dinvestissement_chunk_008 | business_climate | statistics | 15–16 | Overall satisfaction level regarding the experience with the CRI 90% of companies revealed being satisfied with their relationship with CRI TTA. Legend: Very satified / Satified / Dissatisfied Ease of contacting CRI TTA: 80% / 16% / 4% Avai |

### Post-grouping/ranking final results

| Rank | Dense | Final | Lang | Family | Parent | Topic | Type | Pages | Preview |
|---:|---:|---:|---|---|---|---|---|---|---|
| 1 | 0.866111 | 0.871111 | en | investors_guide_territorial_opportunities | investors_guide_territorial_opportunities_en_phase3d1_chunk_0002 | director_message | narrative | 5–5 | It aims to direct investors towards new investment niches and to facilitate access for project holders to information relating to the support services provided by the specialized bodies in the field, each according to its scope of intervent |
| 2 | 0.840745 | 0.845745 | en | investment_climate_indicators | eng_indicateurs_climat_dinvestissement_chunk_013 | business_climate | statistics | 25–26 | PERCEPTION OF THE RELATIONSHIP WITH CRI TTA 100% of all stakeholders interviewed maintain a very good and close relationship with CRI. All stakeholders interviewed are aware of the crucial and central role of CRI in the development of inves |
| 3 | 0.825916 | 0.842916 | en | investors_guide_territorial_opportunities | investors_guide_territorial_opportunities_en_phase3d1_chunk_0004 | business_support | service | 10–10 | INVESTORS MANAR AL MOUSTATMIR As part of its missions related to contributing to the implementation of the State policy on development, incentives, promotion, and attraction of investments at the regional level, as well as comprehensive sup |
| 4 | 0.826971 | 0.831971 | en | investment_climate_indicators | eng_indicateurs_climat_dinvestissement_chunk_010 | business_climate | statistics | 19–20 | 6. Expectations Regarding the CRI Strengthening support for companies: 9% Giving more weight to assistance in finding land solutions: 6% Assisting in finding financial/subsidy solutions: 6% Strengthening the availability and ease of contact |
| 5 | 0.831610 | 0.831610 | es | conciliation_guide | guide_de_conciliation_es_chunk_004 | conciliation | faq | 4–4 | ¿Cuáles son las misiones de la Conciliación? • Recepción e instrucción de solicitudes de conciliación. • Contribuir a facilitar un acercamiento de puntos de vista entre inversiones y la administración o la entidad pública. • Manejar quejas, |

### Duplicate and diversity diagnostics

- Raw top-30 parent duplicate count: 2
- Raw top-30 family duplicate count: 23
- Siblings collapsed: 1
- Family-cap removals: 0
- Final-k cuts: 24
- Final language diversity: 2
- Final family diversity: 3
- Detected query language: en
- Detected concepts: business_support

## EN — What are the requirements for financing programs?

### Raw dense top 10

| Rank | Dense | Final | Lang | Family | Parent | Topic | Type | Pages | Preview |
|---:|---:|---:|---|---|---|---|---|---|---|
| 1 | 0.823169 | 0.831169 | ar | integrated_business_support_financing | guide_programme_integre_appui_financement_entreprises_ar_chunk_002 | integrated_financing | financial_product | 4–4 | إلى البنوك الشريكة التي تعرض التمويلات المحددة في إطار هذا البرنامج وهي: • CFG BANK • CIH بنك • BMCI — Groupe BNP Paribas • Société Générale • Al Amal Bank • Arab Bank • Banque Populaire • Bank of Africa — BMCE Group • البريد بنك • Crédit d |
| 2 | 0.819376 | 0.823376 | fr | financing_guide | guide_du_financement_des_entreprises_intelak | bank_financing | financial_product | 32–32 | 32 Programme de financement couvrant les besoins d’investissement et de fonctionne- ment à des conditions préférentielles, destiné aux entreprises, personnes physiques ou morales, de droit marocain, remplissant les conditions d’éligibilité. |
| 3 | 0.813681 | 0.818681 | en | investors_guide_territorial_opportunities | investors_guide_territorial_opportunities_en_chunk_0033 | investment_opportunity | investment_opportunity | 140–140 | • List of permanent medical staff and their qualifications. • Any document related to the legal form of the proposed establishment. • Internal regulations of the establishment • If the clinic is operated by an association, a partnership agr |
| 4 | 0.810130 | 0.808130 | fr | financing_guide | guide_du_financement_des_entreprises_youth_inclusion | equity_financing | service | 21–21 | 21 Inclusion économique des jeunes L Description Un programme constitué de 3 axes : O Appui à l’Entrepreneuriat O Appui à l’économie sociale et solidaire O Aide à l’employabilité. a Cible O Axe 1 : Coopérative, IGE, SARL, Auto-entrepreneu |
| 5 | 0.809908 | 0.813908 | fr | financing_guide | guide_du_financement_des_entreprises_intelak_al_moustatmir_qarawi | bank_financing | financial_product | 33–33 | 33 Crédits d’investissement et des crédits d’exploitation de 1,2 MDhs maximum accordés aux entreprises éligibles. L Description Financement des dépenses d’investissement relatives aux projets de création et d’extension (acquisition de loca |
| 6 | 0.809382 | 0.811382 | fr | financing_guide | guide_du_financement_des_entreprises_green_invest | public_financing | financial_product | 85–85 | des autres partenaires financiers. O Un business plan reprenant le détail du projet à financer. e Plafond de financement Les programmes d’investissement seront financés par les fonds propres et/ou l’autofinancement et par le crédit conjoin |
| 7 | 0.808937 | 0.806937 | fr | financing_guide | guide_du_financement_des_entreprises_piafe_index | bank_financing | narrative | 31–31 | LE FINANCEMENT PAR LE PROGRAMME INTÉGRÉ D’APPUI ET DE FINANCEMENT DES ENTREPRISES BANQUES INTELAK.............................................................................................................................32 INTELAK AL MOST |
| 8 | 0.808410 | 0.810410 | fr | financing_guide | guide_du_financement_des_entreprises_agricultural_development_fund | public_financing | financial_product | 119–119 | Les modèles des documents à télécharger pour constitution du dossier suivant le type du projet sont accessibles via |
| 9 | 0.806897 | 0.811897 | en | cri_presentation | eng_presentation_cri_tta_vf_semantic_039 | infrastructure | narrative | 54–54 | Investment The 4 investment support mechanism |
| 10 | 0.806651 | 0.811651 | en | investors_guide_territorial_opportunities | investors_guide_territorial_opportunities_en_chunk_0014 | investment_opportunity | investment_opportunity | 61–61 | 53 Requirement INVESTMENT-RELATED ADVANTAGES FINANCIAL INDICATORS OF THE INVESTMENT *Depending on the chosen location, the investor may also benefit from various advantages (Special Economic Zones, Industrial Zones, Free Zones). Furthermore |

### Post-grouping/ranking final results

| Rank | Dense | Final | Lang | Family | Parent | Topic | Type | Pages | Preview |
|---:|---:|---:|---|---|---|---|---|---|---|
| 1 | 0.823169 | 0.831169 | ar | integrated_business_support_financing | guide_programme_integre_appui_financement_entreprises_ar_chunk_002 | integrated_financing | financial_product | 4–4 | إلى البنوك الشريكة التي تعرض التمويلات المحددة في إطار هذا البرنامج وهي: • CFG BANK • CIH بنك • BMCI — Groupe BNP Paribas • Société Générale • Al Amal Bank • Arab Bank • Banque Populaire • Bank of Africa — BMCE Group • البريد بنك • Crédit d |
| 2 | 0.819376 | 0.823376 | fr | financing_guide | guide_du_financement_des_entreprises_intelak | bank_financing | financial_product | 32–32 | 32 Programme de financement couvrant les besoins d’investissement et de fonctionne- ment à des conditions préférentielles, destiné aux entreprises, personnes physiques ou morales, de droit marocain, remplissant les conditions d’éligibilité. |
| 3 | 0.813681 | 0.818681 | en | investors_guide_territorial_opportunities | investors_guide_territorial_opportunities_en_chunk_0033 | investment_opportunity | investment_opportunity | 140–140 | • List of permanent medical staff and their qualifications. • Any document related to the legal form of the proposed establishment. • Internal regulations of the establishment • If the clinic is operated by an association, a partnership agr |
| 4 | 0.809908 | 0.813908 | fr | financing_guide | guide_du_financement_des_entreprises_intelak_al_moustatmir_qarawi | bank_financing | financial_product | 33–33 | 33 Crédits d’investissement et des crédits d’exploitation de 1,2 MDhs maximum accordés aux entreprises éligibles. L Description Financement des dépenses d’investissement relatives aux projets de création et d’extension (acquisition de loca |
| 5 | 0.806897 | 0.811897 | en | cri_presentation | eng_presentation_cri_tta_vf_semantic_039 | infrastructure | narrative | 54–54 | Investment The 4 investment support mechanism |

### Duplicate and diversity diagnostics

- Raw top-30 parent duplicate count: 3
- Raw top-30 family duplicate count: 26
- Siblings collapsed: 0
- Family-cap removals: 0
- Final-k cuts: 25
- Final language diversity: 3
- Final family diversity: 4
- Detected query language: en
- Detected concepts: financial_product

## AR — ما هي شروط الاستفادة من برامج التمويل؟

### Raw dense top 10

| Rank | Dense | Final | Lang | Family | Parent | Topic | Type | Pages | Preview |
|---:|---:|---:|---|---|---|---|---|---|---|
| 1 | 0.856851 | 0.869851 | ar | integrated_business_support_financing | guide_programme_integre_appui_financement_entreprises_ar_chunk_002 | integrated_financing | financial_product | 4–4 | إلى البنوك الشريكة التي تعرض التمويلات المحددة في إطار هذا البرنامج وهي: • CFG BANK • CIH بنك • BMCI — Groupe BNP Paribas • Société Générale • Al Amal Bank • Arab Bank • Banque Populaire • Bank of Africa — BMCE Group • البريد بنك • Crédit d |
| 2 | 0.841591 | 0.854591 | ar | integrated_business_support_financing | guide_programme_integre_appui_financement_entreprises_ar_chunk_002 | integrated_financing | financial_product | 3–3 | ما المقصود بعرض التمويل؟ يقصد بعرض التمويل مجموعة من القروض قابلة للتسديد تهدف إلى تمويل: • نفقات الاستثمار • نفقات التشغيل ماهي منتجات التمويل المتاحة؟ يتكون العرض من مجموعة من منتجات التمويل التي تمثل مجموعة من الخصائص المشتركة وتشمل 3 فئ |
| 3 | 0.840583 | 0.853583 | ar | integrated_business_support_financing | guide_programme_integre_appui_financement_entreprises_ar_chunk_002 | integrated_financing | financial_product | 3–4 | المنتج: START-TPE تعريف: قرض تكميلي يمنح إلى جانب القرض الاستثماري ويمكن من تمويل الحاجة إلى متطلبات رأس المال المتداول المرتبط بالاستثمار. مبلغ التمويل: يمكن أن يصل إلى 20% من المبلغ في حدود 50.000 درهم. الضمانات اللازمة: لا تشترط أية ضمان |
| 4 | 0.818655 | 0.823655 | ar | cri_presentation | ar_pr_sentation_cri_tta_vf_semantic_035 | regional_positioning | narrative | 59–60 | شروط الإستفادة برامج الاستثمار الجديدة فى الاحداث او توسيع التي تبلغ تكلفتها مليون درهم على الاقل .إن كنتم هناء فأنتم في كل مكان؟؟ تثزواا مايرا كيف يتم تمويل المشاريع الأموال الذاتية لحصة المغربي المقيم بالخارج صندوق دعم الاستثمار الخاص بال |
| 5 | 0.818247 | 0.826247 | fr | financing_guide | guide_du_financement_des_entreprises_intelak | bank_financing | financial_product | 32–32 | 32 Programme de financement couvrant les besoins d’investissement et de fonctionne- ment à des conditions préférentielles, destiné aux entreprises, personnes physiques ou morales, de droit marocain, remplissant les conditions d’éligibilité. |
| 6 | 0.816936 | 0.821936 | ar | cri_presentation | ar_pr_sentation_cri_tta_vf_semantic_033 | regional_positioning | narrative | 53–54 | و ا عد ف سد ا 01 م فس 0 202010 8 لو ا ا ميثاق الاستئمار المحور الثاني: نظام خاص يطبق على مشاريع الاستثمار ذات الطابع الاستراتيجي الجديد (1/11) مشاريع يبلغ حجم استثمارها 2 مليار درهم أو أكثر وتستوفي على الأقل أحد الشروط التالية » أن يكون لها |
| 7 | 0.814345 | 0.819345 | ar | integrated_business_support_financing | guide_programme_integre_appui_financement_entreprises_ar_chunk_001 | integrated_financing | narrative | 1–2 | المركز الجهوي للاستثمار طنجة - تطوان - الحسيمة Centre Régional d’Investissement Tanger - Tétouan - Al Hoceima البرنامج المندمج لدعم وتمويل المقاولات «انطلاقة» ما المقصود بعرض المواكبة؟ هي الخدمات المقدمة إلى حاملي المشاريع من أجل مساعدتهم ع |
| 8 | 0.813303 | 0.821303 | fr | financing_guide | guide_du_financement_des_entreprises_intelak_al_moustatmir_qarawi | bank_financing | financial_product | 33–33 | 33 Crédits d’investissement et des crédits d’exploitation de 1,2 MDhs maximum accordés aux entreprises éligibles. L Description Financement des dépenses d’investissement relatives aux projets de création et d’extension (acquisition de loca |
| 9 | 0.812064 | 0.815064 | ar | cri_presentation | ar_pr_sentation_cri_tta_vf_semantic_022 | regional_positioning | narrative | 38–39 | ٠ 4 -المقاولات الكبرى آليات تحفيز الاستثمار الإنتاجي والمستدام والمبتكر على الصعيد الجهوي 2 \| ماله802 < (ملاملزة 1 لاذللاه على المستوى الوطني إطار شفاف ومحفز لتشجيع الاستثمار]0 ماله [اعا/ل[كع]ااا 607 طااناء ال/0711ا بميزانية تبلغ مليار درهم |
| 10 | 0.812029 | 0.815029 | ar | cri_presentation | ar_pr_sentation_cri_tta_vf_semantic_002 | human_capital | narrative | 5–5 | ع7غروعع-ع همومه تسوية النزاعات الرأسمال البشري التمويل بشكل ودي ععصم اام برامج التمويل مكتب التكوين المهني و إنعاش الشغل دعم في التعامل مع الأبناك الجامعات ل © التراخيص التعمبيرية تراخيص الاستغلال رخصة البناء تصنيف مؤسسات الديواء السياحي تر |

### Post-grouping/ranking final results

| Rank | Dense | Final | Lang | Family | Parent | Topic | Type | Pages | Preview |
|---:|---:|---:|---|---|---|---|---|---|---|
| 1 | 0.856851 | 0.869851 | ar | integrated_business_support_financing | guide_programme_integre_appui_financement_entreprises_ar_chunk_002 | integrated_financing | financial_product | 4–4 | إلى البنوك الشريكة التي تعرض التمويلات المحددة في إطار هذا البرنامج وهي: • CFG BANK • CIH بنك • BMCI — Groupe BNP Paribas • Société Générale • Al Amal Bank • Arab Bank • Banque Populaire • Bank of Africa — BMCE Group • البريد بنك • Crédit d |
| 2 | 0.818247 | 0.826247 | fr | financing_guide | guide_du_financement_des_entreprises_intelak | bank_financing | financial_product | 32–32 | 32 Programme de financement couvrant les besoins d’investissement et de fonctionne- ment à des conditions préférentielles, destiné aux entreprises, personnes physiques ou morales, de droit marocain, remplissant les conditions d’éligibilité. |
| 3 | 0.818655 | 0.823655 | ar | cri_presentation | ar_pr_sentation_cri_tta_vf_semantic_035 | regional_positioning | narrative | 59–60 | شروط الإستفادة برامج الاستثمار الجديدة فى الاحداث او توسيع التي تبلغ تكلفتها مليون درهم على الاقل .إن كنتم هناء فأنتم في كل مكان؟؟ تثزواا مايرا كيف يتم تمويل المشاريع الأموال الذاتية لحصة المغربي المقيم بالخارج صندوق دعم الاستثمار الخاص بال |
| 4 | 0.816936 | 0.821936 | ar | cri_presentation | ar_pr_sentation_cri_tta_vf_semantic_033 | regional_positioning | narrative | 53–54 | و ا عد ف سد ا 01 م فس 0 202010 8 لو ا ا ميثاق الاستئمار المحور الثاني: نظام خاص يطبق على مشاريع الاستثمار ذات الطابع الاستراتيجي الجديد (1/11) مشاريع يبلغ حجم استثمارها 2 مليار درهم أو أكثر وتستوفي على الأقل أحد الشروط التالية » أن يكون لها |
| 5 | 0.813303 | 0.821303 | fr | financing_guide | guide_du_financement_des_entreprises_intelak_al_moustatmir_qarawi | bank_financing | financial_product | 33–33 | 33 Crédits d’investissement et des crédits d’exploitation de 1,2 MDhs maximum accordés aux entreprises éligibles. L Description Financement des dépenses d’investissement relatives aux projets de création et d’extension (acquisition de loca |

### Duplicate and diversity diagnostics

- Raw top-30 parent duplicate count: 6
- Raw top-30 family duplicate count: 25
- Siblings collapsed: 3
- Family-cap removals: 0
- Final-k cuts: 22
- Final language diversity: 2
- Final family diversity: 3
- Detected query language: ar
- Detected concepts: eligibility_conditions, financial_product

## AR — ما هي خدمات المركز الجهوي للاستثمار للمستثمرين؟

### Raw dense top 10

| Rank | Dense | Final | Lang | Family | Parent | Topic | Type | Pages | Preview |
|---:|---:|---:|---|---|---|---|---|---|---|
| 1 | 0.839865 | 0.844865 | ar | cri_presentation | ar_pr_sentation_cri_tta_vf_semantic_001 | regional_positioning | narrative | 1–3 | المملكة المغربية رئيس الحكومة وزارة الاستثمار والالتقائية وتقييم السياسات العمومية INVESTANGIER المركز الجهوي للاستثمار طنجة - تطوان - الحسيمة طنجة تطوان الحسيمة وجهة استثمارية عند مفترق الطرق والأسواق العالمية www.investangier.com 1210: 0  |
| 2 | 0.838459 | 0.843459 | ar | conciliation_guide | guide_de_conciliation_ar_chunk_002 | conciliation | narrative | 2–2 | ديباجة تنزيلا للخطاب الملكي السامي بمناسبة افتتاح الدورة الأولى من السنة التشريعية الثانية من الولاية التشريعية الحادية عشرة، وتفعيلا لمقتضيات المادة 4 من القانون 47-18 المتعلق بإصلاح المراكز الجهوية للاستثمار وإحداث اللجن الجهوية الموحدة ل |
| 3 | 0.827967 | 0.832967 | ar | conciliation_guide | guide_de_conciliation_ar_chunk_004 | conciliation | faq | 4–4 | ماهي مهمة مصلحة المصالحة؟ • استقبال طلبات التوفيق والتحقيق فيها. • المساهمة في إجراء توفيق وتقريب وجهات النظر بين المستثمرين والإدارة أو الهيئات العامة المعنية. • التعامل مع الشكاوى وتحليل أسبابها والتوصية بحلول عادلة. • تسهيل جلسات التوفيق |
| 4 | 0.827287 | 0.836287 | ar | integrated_business_support_financing | guide_programme_integre_appui_financement_entreprises_ar_chunk_001 | integrated_financing | narrative | 1–2 | المركز الجهوي للاستثمار طنجة - تطوان - الحسيمة Centre Régional d’Investissement Tanger - Tétouan - Al Hoceima البرنامج المندمج لدعم وتمويل المقاولات «انطلاقة» ما المقصود بعرض المواكبة؟ هي الخدمات المقدمة إلى حاملي المشاريع من أجل مساعدتهم ع |
| 5 | 0.827114 | 0.832114 | ar | cri_presentation | ar_pr_sentation_cri_tta_vf_semantic_029 | regional_positioning | narrative | 47–47 | ميثاق الاستثمار المحور الأول: نظام دعم أساسي الجديد (5/11) آلية الدعم الرئيسية 5 منح للاستثمار تماشياً مع التوجيهات الملكية السامية. وأهداف النموذج التنموي الجديد. وبرنامج الحكومة 5 1< 59 عدد مناصب الشغل المحدثة/ مبلغ الاستثمار 5 1,5 < ص7 ( |
| 6 | 0.823256 | 0.840256 | ar | manar_al_moustatmir_news_2023 | akhbar_al_moustatmir_news_phase3f_0005 | business_support | service | 8–8 | 02 www.investangier.com :اختتام الدورة التكوينية لخبراء الاستثمار : دورة تكوينية Investangier Experts مصممة خصيصا أطلقها المركز الجهوي للاستثمار بجهة طنجة تطوان الحسيمة بشراكة مع برنامج فرصتي التابع للوكالة ونفذتها الدولية، للتنمية الأمريكي |
| 7 | 0.823049 | 0.828049 | ar | chiffres_cles_2025 | arabe_chiffres_cles_2025_chunk_015 | territorial_promotion | statistics | 15–15 | الترويج والشراكات (2/4) من التعبئة إلى المواكبة من أجل استثمار مغاربة العالم – من 11 إلى 15 غشت 2025 مقاربة 360 تضم 3 محاور رئيسية: • حملة تواصلية مندمجة على المستوى الجهوي، بما في ذلك الإعلانات على مستوى المحاور الطرقية الكبرى للأقاليم وال |
| 8 | 0.822153 | 0.827153 | ar | conciliation_guide | guide_de_conciliation_ar_chunk_001 | conciliation | contact_information | 1–1 | Once you are here, you are everywhere! دليل المصالحة عن طريق المركز الجهوي للاستثمار لجهة طنجة-تطوان-الحسيمة Avenue Omar Ibn El Khattab (Près du siège de la Wilaya de Tanger - Tétouan - Al Hoceima) support@investangier.com Tel: +(212) 0539  |
| 9 | 0.819823 | 0.828823 | ar | integrated_business_support_financing | guide_programme_integre_appui_financement_entreprises_ar_chunk_003 | integrated_financing | eligibility_conditions | 5–6 | ما هو البرنامج المندمج لدعم وتمويل المقاولات؟ هو برنامج مكون من عرض تمويل ومواكبة بشروط جد تفضيلية. من هي الفئة المستهدفة من هذا البرنامج؟ • الشباب حاملي الشهادات/ المؤهلين وحاملي المشاريع. • المقاولين الذاتيين المسجلين في السجل الوطني. • ا |
| 10 | 0.817619 | 0.822619 | ar | conciliation_guide | guide_de_conciliation_ar_chunk_005 | conciliation | eligibility_conditions | 5–5 | يتضمن الطلب • اسم ومقر الشركة ورقم القيد في السجل التجاري وعنوان المستثمر • الحالة المدنية للممثل القانوني للأطراف • ملخص موضوع النزاع • أي مستند يبرر النزاع مباشرة مسطرة المصالحة • يتم فتح مسطرة التوفيق مباشرة عند إيداع المستثمر لطلب التوف |

### Post-grouping/ranking final results

| Rank | Dense | Final | Lang | Family | Parent | Topic | Type | Pages | Preview |
|---:|---:|---:|---|---|---|---|---|---|---|
| 1 | 0.839865 | 0.844865 | ar | cri_presentation | ar_pr_sentation_cri_tta_vf_semantic_001 | regional_positioning | narrative | 1–3 | المملكة المغربية رئيس الحكومة وزارة الاستثمار والالتقائية وتقييم السياسات العمومية INVESTANGIER المركز الجهوي للاستثمار طنجة - تطوان - الحسيمة طنجة تطوان الحسيمة وجهة استثمارية عند مفترق الطرق والأسواق العالمية www.investangier.com 1210: 0  |
| 2 | 0.838459 | 0.843459 | ar | conciliation_guide | guide_de_conciliation_ar_chunk_002 | conciliation | narrative | 2–2 | ديباجة تنزيلا للخطاب الملكي السامي بمناسبة افتتاح الدورة الأولى من السنة التشريعية الثانية من الولاية التشريعية الحادية عشرة، وتفعيلا لمقتضيات المادة 4 من القانون 47-18 المتعلق بإصلاح المراكز الجهوية للاستثمار وإحداث اللجن الجهوية الموحدة ل |
| 3 | 0.823256 | 0.840256 | ar | manar_al_moustatmir_news_2023 | akhbar_al_moustatmir_news_phase3f_0005 | business_support | service | 8–8 | 02 www.investangier.com :اختتام الدورة التكوينية لخبراء الاستثمار : دورة تكوينية Investangier Experts مصممة خصيصا أطلقها المركز الجهوي للاستثمار بجهة طنجة تطوان الحسيمة بشراكة مع برنامج فرصتي التابع للوكالة ونفذتها الدولية، للتنمية الأمريكي |
| 4 | 0.827287 | 0.836287 | ar | integrated_business_support_financing | guide_programme_integre_appui_financement_entreprises_ar_chunk_001 | integrated_financing | narrative | 1–2 | المركز الجهوي للاستثمار طنجة - تطوان - الحسيمة Centre Régional d’Investissement Tanger - Tétouan - Al Hoceima البرنامج المندمج لدعم وتمويل المقاولات «انطلاقة» ما المقصود بعرض المواكبة؟ هي الخدمات المقدمة إلى حاملي المشاريع من أجل مساعدتهم ع |
| 5 | 0.827967 | 0.832967 | ar | conciliation_guide | guide_de_conciliation_ar_chunk_004 | conciliation | faq | 4–4 | ماهي مهمة مصلحة المصالحة؟ • استقبال طلبات التوفيق والتحقيق فيها. • المساهمة في إجراء توفيق وتقريب وجهات النظر بين المستثمرين والإدارة أو الهيئات العامة المعنية. • التعامل مع الشكاوى وتحليل أسبابها والتوصية بحلول عادلة. • تسهيل جلسات التوفيق |

### Duplicate and diversity diagnostics

- Raw top-30 parent duplicate count: 0
- Raw top-30 family duplicate count: 23
- Siblings collapsed: 0
- Family-cap removals: 0
- Final-k cuts: 25
- Final language diversity: 1
- Final family diversity: 4
- Detected query language: ar
- Detected concepts: business_support

## AR — ما هي فرص الاستثمار في قطاع السياحة؟

### Raw dense top 10

| Rank | Dense | Final | Lang | Family | Parent | Topic | Type | Pages | Preview |
|---:|---:|---:|---|---|---|---|---|---|---|
| 1 | 0.839125 | 0.844125 | ar | crui_key_figures_2024_h1 | chiffres_cles_crui_1er_semestre_2024_arabe_chunk_003 | sector_distribution | statistics | 3–3 | إن كنتم هنا، فأنتم في كل مكان توزيع حجم الاستثمارات حسب القطاع يواصل القطاع الصناعي نموه الاستثنائي بأكثر من نصف الاستثمارات التي تمت المصادقة عليها إجمالي الاستثمارات: 40,76 مليار درهم الصناعة: 54% السياحة: 22% الطاقة والمناجم: 15% قطاعات  |
| 2 | 0.838534 | 0.843534 | ar | crui_key_figures_2024_h1 | chiffres_cles_crui_1er_semestre_2024_arabe_chunk_004 | industrial_investment | statistics | 4–4 | إن كنتم هنا، فأنتم في كل مكان تشكل الصناعة القطاع الرائد في توفير فرص شغل على المدى المتوسط والبعيد، بحصة تقدر بـ 83% الصناعة: 83% السياحة: 7% قطاعات أخرى: 10% www.investangier.com |
| 3 | 0.834453 | 0.839453 | ar | chiffres_cles_2025 | arabe_chiffres_cles_2025_chunk_008 | sector_investment | statistics | 8–8 | حصيلة اللجنة الجهوية الموحدة للاستثمار (5/6) دينامية قوية للاستثمار السياحي مدعومة برؤية واعدة لقد اختاروا الجهة سنة 2025 7 مؤسسات مفتوحة سنة 2025 +300 غرفة 194 مليون درهم من الاستثمارات 31 مؤسسة في طور الإنجاز 2 036 غرفة إضافية منها 1 220  |
| 4 | 0.833021 | 0.836021 | ar | crui_key_figures_2024_h1 | chiffres_cles_crui_1er_semestre_2024_arabe_chunk_006 | approved_projects | statistics | 6–6 | إن كنتم هنا، فأنتم في كل مكان 16 اتفاقية استثمار 9,54 مليار درهم من الاستثمار 6 525 منصب شغل مباشر توزيع مبالغ الاستثمارات المبرمجة في إطار اتفاقيات الاستثمار المصادق عليها من طرف اللجنة الجهوية الموحدة للاستثمار: السياحة والترفيه: 78% الصن |
| 5 | 0.832188 | 0.835188 | ar | manar_al_moustatmir_news_2023 | akhbar_al_moustatmir_news_phase3f_0001 | investment_news | statistics | 1–1 | حقائق علامات بارومتر الإستثمار قضية السياحة الخاصة LES CHIFFRES CLÉS DE L'INVESTISSEMENT ET DE L'ENTREPRENEURIAT de l’année 2023 1 أخبـار منارالمستثمر رقم 2024 لسنة مؤشرات الاستثمار وريادة الأعمال بارزة الاستثمار مقياس خاص بالسياحة ملف أحدا |
| 6 | 0.831273 | 0.834273 | ar | manar_al_moustatmir_news_2023 | akhbar_al_moustatmir_news_phase3f_0020 | crui_activity | statistics | 25–26 | 19 www.investangier.com . 230 طلبا إثر اجتماعاتها ال972 CRUI ، درست2023 »خلال سنة 709 ومن بين هذه الطلبات، وافقت اللجنة الجهوية الموحدة للاستثمار على من الطلبات المقدمة، وكل ذلك في غضون فترة زمنية 73% طلبا، تمثل أيام".4،9 متوسطة لا تزيد عن  |
| 7 | 0.826463 | 0.839463 | ar | manar_al_moustatmir_news_2023 | akhbar_al_moustatmir_news_phase3f_0029 | investment_news | investment_opportunity | 42–42 | 36 www.investangier.com TIERRA BENDITA HOUARA GESTION ROMANTICO CO LTD اليابان الدولية للتبغ النشاط الاستثمار العدد المتوقع للوظائف المكان إنتاج التبغ مليون درهم 170 تطوان بارك 930 شركة طاقة المغربیة للرياح النشاط الاستثمار العدد المتوقع لل |
| 8 | 0.823040 | 0.828040 | ar | cri_presentation | ar_pr_sentation_cri_tta_vf_semantic_032 | strategic_sectors | narrative | 52–52 | حي ال ا د وفيس الهسو للاستتبار 5 50 ثزاء كوه 8 م ا 5 إن كنتم هناء فالتم مي كل مكان 58 لجس 1 اساي لقع تنا ا لم ع ا ل ميثاق الاستثمار المحور الأول: نظام دعم أساسى الجديد (0/11) منحة قطاعية لتحفيز الاستثمار فى القطاعات ذات الأولوية 9 النقل و ا |
| 9 | 0.822499 | 0.829499 | ar | manar_al_moustatmir_news_2023 | akhbar_al_moustatmir_news_phase3f_0018 | investment_news | statistics | 22–22 | 16 www.investangier.com ممیزات القطاع العلامات التجارية السياحية الموجودة في الجهة الانفتاح على جبھتین بحريتین: ساحل المحیط الأطلسي )الریاضة، الریاضات اللوحیة، ركوب الأمواج( وساحل البحر الأبیض المتوسط )السباحة، الإبحار(. ثراء وتنوع المناظر  |
| 10 | 0.822486 | 0.839486 | ar | manar_al_moustatmir_news_2023 | akhbar_al_moustatmir_news_phase3f_0007 | investment_news | investment_opportunity | 10–10 | 04 www.investangier.com تعزیز العرض العقاري المخصص لقطاع السیاحة من خلال إتاحة فرص عقاریة متر مربع لبناء 2949 للمستثمرین بمساحة نجوم أو أكثر في أصیلة.4 فندق بعد انتھاء ھذا الإعلان عن الاستثمار، تم ملفات، تم اختیار مشروع واحد لبناء 3 تقدیم غ |

### Post-grouping/ranking final results

| Rank | Dense | Final | Lang | Family | Parent | Topic | Type | Pages | Preview |
|---:|---:|---:|---|---|---|---|---|---|---|
| 1 | 0.839125 | 0.844125 | ar | crui_key_figures_2024_h1 | chiffres_cles_crui_1er_semestre_2024_arabe_chunk_003 | sector_distribution | statistics | 3–3 | إن كنتم هنا، فأنتم في كل مكان توزيع حجم الاستثمارات حسب القطاع يواصل القطاع الصناعي نموه الاستثنائي بأكثر من نصف الاستثمارات التي تمت المصادقة عليها إجمالي الاستثمارات: 40,76 مليار درهم الصناعة: 54% السياحة: 22% الطاقة والمناجم: 15% قطاعات  |
| 2 | 0.838534 | 0.843534 | ar | crui_key_figures_2024_h1 | chiffres_cles_crui_1er_semestre_2024_arabe_chunk_004 | industrial_investment | statistics | 4–4 | إن كنتم هنا، فأنتم في كل مكان تشكل الصناعة القطاع الرائد في توفير فرص شغل على المدى المتوسط والبعيد، بحصة تقدر بـ 83% الصناعة: 83% السياحة: 7% قطاعات أخرى: 10% www.investangier.com |
| 3 | 0.822486 | 0.839486 | ar | manar_al_moustatmir_news_2023 | akhbar_al_moustatmir_news_phase3f_0007 | investment_news | investment_opportunity | 10–10 | 04 www.investangier.com تعزیز العرض العقاري المخصص لقطاع السیاحة من خلال إتاحة فرص عقاریة متر مربع لبناء 2949 للمستثمرین بمساحة نجوم أو أكثر في أصیلة.4 فندق بعد انتھاء ھذا الإعلان عن الاستثمار، تم ملفات، تم اختیار مشروع واحد لبناء 3 تقدیم غ |
| 4 | 0.826463 | 0.839463 | ar | manar_al_moustatmir_news_2023 | akhbar_al_moustatmir_news_phase3f_0029 | investment_news | investment_opportunity | 42–42 | 36 www.investangier.com TIERRA BENDITA HOUARA GESTION ROMANTICO CO LTD اليابان الدولية للتبغ النشاط الاستثمار العدد المتوقع للوظائف المكان إنتاج التبغ مليون درهم 170 تطوان بارك 930 شركة طاقة المغربیة للرياح النشاط الاستثمار العدد المتوقع لل |
| 5 | 0.834453 | 0.839453 | ar | chiffres_cles_2025 | arabe_chiffres_cles_2025_chunk_008 | sector_investment | statistics | 8–8 | حصيلة اللجنة الجهوية الموحدة للاستثمار (5/6) دينامية قوية للاستثمار السياحي مدعومة برؤية واعدة لقد اختاروا الجهة سنة 2025 7 مؤسسات مفتوحة سنة 2025 +300 غرفة 194 مليون درهم من الاستثمارات 31 مؤسسة في طور الإنجاز 2 036 غرفة إضافية منها 1 220  |

### Duplicate and diversity diagnostics

- Raw top-30 parent duplicate count: 1
- Raw top-30 family duplicate count: 25
- Siblings collapsed: 0
- Family-cap removals: 0
- Final-k cuts: 25
- Final language diversity: 1
- Final family diversity: 3
- Detected query language: ar
- Detected concepts: investment_opportunity, tourism

## ES — ¿Qué servicios ofrece el CRI a los inversores?

### Raw dense top 10

| Rank | Dense | Final | Lang | Family | Parent | Topic | Type | Pages | Preview |
|---:|---:|---:|---|---|---|---|---|---|---|
| 1 | 0.875684 | 0.880684 | es | conciliation_guide | guide_de_conciliation_es_chunk_004 | conciliation | faq | 4–4 | ¿Cuáles son las misiones de la Conciliación? • Recepción e instrucción de solicitudes de conciliación. • Contribuir a facilitar un acercamiento de puntos de vista entre inversiones y la administración o la entidad pública. • Manejar quejas, |
| 2 | 0.863187 | 0.880187 | es | investment_business_support_single_window | investment_business_support_single_window_es_phase3f_0002 | business_support | service | 3–3 | EL CRI DE LA REGIÓN TÁNGER-TETUÁN-ALHUCEMAS AL SERVICIO DE LOS INVERSORES De acuerdo con las Altas Orientaciones Reales, la reforma de los Centros Regionales de Inversión (CRI), impulsada por la ley 47-18, entró en vigor en diciembre de 201 |
| 3 | 0.853282 | 0.862282 | es | cri_presentation | esp_presentation_cri_tta_vf_semantic_003 | cri_missions | service | 3–3 | is ¿a Pared a lara) PITT A ¡Una vez aquí, está en todas partes! a INNEETAMZS El Centro Regional de Inversiones se encarga de contribuir a la aplicación de la política del Estado en materia de desarrollo, fomento, promoción y atracción de in |
| 4 | 0.851299 | 0.868299 | es | investment_business_support_single_window | investment_business_support_single_window_es_phase3f_0003 | business_support | service | 4–4 | NUESTRA OFERTA DE SERVICIOS El CRI TTA también interviene ahora en la intermediación y conciliación para la resolución amistosa de disputas entre inversores y administraciones. Además, contribuye a la elaboración y despliegue de estrategias |
| 5 | 0.847961 | 0.862961 | es | investment_business_support_single_window | investment_business_support_single_window_es_phase3f_0010 | business_support | service | 11–11 | MANAR AL MOUSTATMIR Primera ventanilla única comunitaria virtual de asesoramiento a los inversores • Estructura la acción colectiva, optimiza el proceso de asesoramiento y mejora la experiencia del inversor en la región. • Agrupa todos los  |
| 6 | 0.845527 | 0.850527 | es | investment_climate_indicators | esp_indicateurs_climat_dinvestissement_chunk_013 | business_climate | statistics | 25–26 | PERCEPCIÓN DE LA RELACIÓN CON EL CRI TTA 100% de todas las partes interesadas encontradas mantienen una relación muy buena y estrecha con el CRI. Todos los actores interrogados son conscientes del papel crucial y central del CRI en el desar |
| 7 | 0.843921 | 0.848921 | es | conciliation_guide | guide_de_conciliation_es_chunk_002 | conciliation | narrative | 2–2 | EDITORIAL De acuerdo con el Discurso Real pronunciado durante la ceremonia de apertura de la primera sesión del segundo año legislativo de la undécima legislatura, y de acuerdo con el artículo 4 de la Ley n.º 18-47, que reforma los Centros  |
| 8 | 0.837970 | 0.842970 | es | investment_climate_indicators | esp_indicateurs_climat_dinvestissement_chunk_009 | business_climate | statistics | 17–18 | Principales áreas de asesoramiento percibidas por los inversores Promoción de oportunidades de inversión: 67% Acompañamiento proactivo para el desarrollo del ecosistema de su empresa: 29% Asistencia previa a la inversión: 12% Provisión de s |
| 9 | 0.836769 | 0.841769 | es | conciliation_guide | guide_de_conciliation_es_chunk_005 | conciliation | eligibility_conditions | 5–5 | ¿Cómo se abre un proceso de conciliación? • El proceso de conciliación se inicia tan pronto como el CRI recibe la solicitud de conciliación por parte del inversor. • Cuando el Centro Regional de Inversiones (CRI) recibe una solicitud de con |
| 10 | 0.832936 | 0.840936 | fr | investment_business_support_single_window | investment_business_support_single_window_fr_phase3f_0002 | business_support | service | 3–3 | LE CRI TANGER-TÉTOUAN-AL HOCEIMA AU SERVICE DES INVESTISSEURS Conformément aux Hautes Orientations Royales, la réforme des Centres Régionaux d’Investissement (CRI), portée par la loi 47-18, est entrée en vigueur en décembre 2019. Elle a ass |

### Post-grouping/ranking final results

| Rank | Dense | Final | Lang | Family | Parent | Topic | Type | Pages | Preview |
|---:|---:|---:|---|---|---|---|---|---|---|
| 1 | 0.875684 | 0.880684 | es | conciliation_guide | guide_de_conciliation_es_chunk_004 | conciliation | faq | 4–4 | ¿Cuáles son las misiones de la Conciliación? • Recepción e instrucción de solicitudes de conciliación. • Contribuir a facilitar un acercamiento de puntos de vista entre inversiones y la administración o la entidad pública. • Manejar quejas, |
| 2 | 0.863187 | 0.880187 | es | investment_business_support_single_window | investment_business_support_single_window_es_phase3f_0002 | business_support | service | 3–3 | EL CRI DE LA REGIÓN TÁNGER-TETUÁN-ALHUCEMAS AL SERVICIO DE LOS INVERSORES De acuerdo con las Altas Orientaciones Reales, la reforma de los Centros Regionales de Inversión (CRI), impulsada por la ley 47-18, entró en vigor en diciembre de 201 |
| 3 | 0.851299 | 0.868299 | es | investment_business_support_single_window | investment_business_support_single_window_es_phase3f_0003 | business_support | service | 4–4 | NUESTRA OFERTA DE SERVICIOS El CRI TTA también interviene ahora en la intermediación y conciliación para la resolución amistosa de disputas entre inversores y administraciones. Además, contribuye a la elaboración y despliegue de estrategias |
| 4 | 0.847961 | 0.862961 | es | investment_business_support_single_window | investment_business_support_single_window_es_phase3f_0010 | business_support | service | 11–11 | MANAR AL MOUSTATMIR Primera ventanilla única comunitaria virtual de asesoramiento a los inversores • Estructura la acción colectiva, optimiza el proceso de asesoramiento y mejora la experiencia del inversor en la región. • Agrupa todos los  |
| 5 | 0.853282 | 0.862282 | es | cri_presentation | esp_presentation_cri_tta_vf_semantic_003 | cri_missions | service | 3–3 | is ¿a Pared a lara) PITT A ¡Una vez aquí, está en todas partes! a INNEETAMZS El Centro Regional de Inversiones se encarga de contribuir a la aplicación de la política del Estado en materia de desarrollo, fomento, promoción y atracción de in |

### Duplicate and diversity diagnostics

- Raw top-30 parent duplicate count: 0
- Raw top-30 family duplicate count: 21
- Siblings collapsed: 0
- Family-cap removals: 0
- Final-k cuts: 25
- Final language diversity: 1
- Final family diversity: 3
- Detected query language: es
- Detected concepts: business_support

## ES — ¿Qué oportunidades de inversión existen en el sector turístico?

### Raw dense top 10

| Rank | Dense | Final | Lang | Family | Parent | Topic | Type | Pages | Preview |
|---:|---:|---:|---|---|---|---|---|---|---|
| 1 | 0.844380 | 0.849380 | es | crui_key_figures_2024_h1 | chiffres_cles_crui_1er_semestre_2024_espagnol_chunk_004 | industrial_investment | statistics | 4–4 | ¡Una vez aquí, está en todas partes! El sector industrial continúa su excepcional crecimiento con más de la mitad de las inversiones aprobadas. Industria: 83% Turismo: 7% Otros sectores: 10% www.investangier.com |
| 2 | 0.835787 | 0.840787 | es | crui_key_figures_2024_h1 | chiffres_cles_crui_1er_semestre_2024_espagnol_chunk_003 | sector_distribution | statistics | 3–3 | ¡Una vez aquí, está en todas partes! Desglose del volumen de inversión por sector El sector industrial continúa su excepcional crecimiento con más de la mitad de las inversiones aprobadas. Total de inversiones: 40,76 mil millones MAD Indust |
| 3 | 0.834596 | 0.839596 | es | investment_business_support_single_window | investment_business_support_single_window_es_phase3f_0011 | business_support | service | 12–12 | GUÍA DE LA OFERTA TERRITORIAL DE LAS OPORTUNIDADES DE INVERSIÓN Y ASESORAMIENTO El Centro Regional de Inversiones de la región Tánger-Tetuán-Alhucemas lanzó una nueva guía sobre “La oferta territorial de las oportunidades de inversión y ase |
| 4 | 0.834588 | 0.839588 | es | chiffres_cles_2025 | esp_chiffres_cles_annee_2025_chunk_008 | sector_investment | statistics | 8–8 | Balance de la CRUI (5/6) Una fuerte dinámica de inversión turística respaldada por una visión ambiciosa Proyectos operacionales: 7 establecimientos abiertos en 2025 +300 habitaciones 194 millones MAD de inversión Proyectos en curso: 31 esta |
| 5 | 0.834583 | 0.839583 | es | cri_presentation | esp_presentation_cri_tta_vf_semantic_007 | territorial_offer | narrative | 7–7 | sl ¿al ¡Una vez aquí, está en todas partes! E A INVESTANGIER CeNmEneOCHAL reason Monografía Atractivos de la Región Tánger-Tetuán-Alhucemas Sectores clave de la Región Oferta territorial para la inversión |
| 6 | 0.834309 | 0.839309 | es | investment_climate_indicators | esp_indicateurs_climat_dinvestissement_chunk_005 | business_climate | statistics | 9–10 | 92% de las empresas están satisfechas de su implantación en la región Tánger-Tetuán-Alhucemas. 7 Motivaciones para implantarse en la región TTA 1. Situación geográfica y madurez del ecosistema Soy originario de la región: 51% Cercanía a los |
| 7 | 0.833835 | 0.838835 | es | cri_presentation | esp_presentation_cri_tta_vf_semantic_022 | territorial_offer | narrative | 29–29 | ¡Una vez aquí, está en todas partes! Monografía Atractivos de la Región Tánger-Tetuán-Alhucemas Sectores clave de la Región Oferta territorial para la inversión |
| 8 | 0.833278 | 0.838278 | es | cri_presentation | esp_presentation_cri_tta_vf_semantic_010 | territorial_offer | narrative | 10–10 | ¡Una vez aquí, está en todas partes! E A Monografía Atractivos de la Región Tánger-Tetuán-Alhucemas Sectores clave de la Región Oferta territorial para la inversión |
| 9 | 0.833021 | 0.836021 | es | crui_key_figures_2024_h1 | chiffres_cles_crui_1er_semestre_2024_espagnol_chunk_006 | approved_projects | statistics | 6–6 | ¡Una vez aquí, está en todas partes! 16 convenios de inversión aprobados 9.540 millones de dirhams de inversión 6 525 empleos directos a medio y largo plazo Desglose sectorial de los importes de las inversiones de los convenios aprobados po |
| 10 | 0.830121 | 0.835121 | es | chiffres_cles_2025 | esp_chiffres_cles_annee_2025_chunk_006 | crui_activity | statistics | 6–6 | Balance de la CRUI (3/6) Distribución sectorial de los expedientes de inversión aprobados en la CRUI Sectores: Energía Industria Turismo Servicios Otros Por número de proyectos: 487 expedientes de inversión Energía: 67% Industria: 15% Turis |

### Post-grouping/ranking final results

| Rank | Dense | Final | Lang | Family | Parent | Topic | Type | Pages | Preview |
|---:|---:|---:|---|---|---|---|---|---|---|
| 1 | 0.844380 | 0.849380 | es | crui_key_figures_2024_h1 | chiffres_cles_crui_1er_semestre_2024_espagnol_chunk_004 | industrial_investment | statistics | 4–4 | ¡Una vez aquí, está en todas partes! El sector industrial continúa su excepcional crecimiento con más de la mitad de las inversiones aprobadas. Industria: 83% Turismo: 7% Otros sectores: 10% www.investangier.com |
| 2 | 0.835787 | 0.840787 | es | crui_key_figures_2024_h1 | chiffres_cles_crui_1er_semestre_2024_espagnol_chunk_003 | sector_distribution | statistics | 3–3 | ¡Una vez aquí, está en todas partes! Desglose del volumen de inversión por sector El sector industrial continúa su excepcional crecimiento con más de la mitad de las inversiones aprobadas. Total de inversiones: 40,76 mil millones MAD Indust |
| 3 | 0.834596 | 0.839596 | es | investment_business_support_single_window | investment_business_support_single_window_es_phase3f_0011 | business_support | service | 12–12 | GUÍA DE LA OFERTA TERRITORIAL DE LAS OPORTUNIDADES DE INVERSIÓN Y ASESORAMIENTO El Centro Regional de Inversiones de la región Tánger-Tetuán-Alhucemas lanzó una nueva guía sobre “La oferta territorial de las oportunidades de inversión y ase |
| 4 | 0.834588 | 0.839588 | es | chiffres_cles_2025 | esp_chiffres_cles_annee_2025_chunk_008 | sector_investment | statistics | 8–8 | Balance de la CRUI (5/6) Una fuerte dinámica de inversión turística respaldada por una visión ambiciosa Proyectos operacionales: 7 establecimientos abiertos en 2025 +300 habitaciones 194 millones MAD de inversión Proyectos en curso: 31 esta |
| 5 | 0.834583 | 0.839583 | es | cri_presentation | esp_presentation_cri_tta_vf_semantic_007 | territorial_offer | narrative | 7–7 | sl ¿al ¡Una vez aquí, está en todas partes! E A INVESTANGIER CeNmEneOCHAL reason Monografía Atractivos de la Región Tánger-Tetuán-Alhucemas Sectores clave de la Región Oferta territorial para la inversión |

### Duplicate and diversity diagnostics

- Raw top-30 parent duplicate count: 0
- Raw top-30 family duplicate count: 23
- Siblings collapsed: 0
- Family-cap removals: 0
- Final-k cuts: 25
- Final language diversity: 1
- Final family diversity: 4
- Detected query language: es
- Detected concepts: investment_opportunity, tourism

## ES — ¿Cuáles son las condiciones para beneficiarse de los programas de financiación؟

### Raw dense top 10

| Rank | Dense | Final | Lang | Family | Parent | Topic | Type | Pages | Preview |
|---:|---:|---:|---|---|---|---|---|---|---|
| 1 | 0.820977 | 0.825977 | es | investment_business_support_single_window | investment_business_support_single_window_es_phase3f_0005 | business_support | service | 6–6 | Incentivos Ponemos a su disposición todas las ofertas de incentivos, así como soluciones de financiamiento y ayuda financiera ofrecidas por nuestros socios públicos y privados a nivel nacional y regional, en un enfoque de convergencia de pr |
| 2 | 0.820098 | 0.825098 | es | chiffres_cles_2025 | esp_chiffres_cles_annee_2025_chunk_017 | territorial_promotion | statistics | 17–17 | Promoción y alianzas (4/4) Alianzas estratégicas para la proyección y el desarrollo económico de la Región Nuevo acuerdo de alianza CRI–IFC El objetivo de la alianza IFC – CRI TTA es incrementar las inversiones privadas respetuosas con el c |
| 3 | 0.819008 | 0.823008 | fr | financing_guide | guide_du_financement_des_entreprises_contractual_regime | public_financing | financial_product | 128–128 | à 250 o assurer un transfert de technologie o contribuer à la protection de l’environnement. Seuls les projets d’investissements dans les secteurs de l’Immobilier et de l’Agriculture, ne sont pas éligibles à la subvention FDII sous réserve  |
| 4 | 0.816202 | 0.821202 | es | chiffres_cles_2025 | esp_chiffres_cles_annee_2025_chunk_010 | business_support | statistics | 10–10 | Acompañamiento a las empresas (1/4) 5 500 empresas / promotores de proyectos acompañados 3 223 beneficiarios Ejes de acompañamiento: Facilitación del acceso a la financiación Refuerzo de las capacidades empresariales de los promotores de pr |
| 5 | 0.814717 | 0.819717 | es | cri_presentation | esp_presentation_cri_tta_vf_semantic_028 | infrastructure | statistics | 38–39 | Las empresas elegibles para Los requisitos ¿Cuáles son los criterios de elegibilidad para poder beneficiar del apoyo beneficiar del apoyo? Cifra de negocios / Número de años de Importe total de la actividad Tasa prevista de inversion empleo |
| 6 | 0.813844 | 0.816844 | es | chiffres_cles_2025 | esp_chiffres_cles_annee_2025_chunk_011 | business_support | statistics | 11–11 | Acompañamiento a las empresas (2/4) Balance del PIAFE* a nivel de la región TTA 4 672 expedientes financiados ~1,14 mil millones MAD de financiación * PIAFE: Programa Integrado de Apoyo y Financiación de las Empresas www.investangier.com 11 |
| 7 | 0.813634 | 0.817634 | fr | financing_guide | guide_du_financement_des_entreprises_agricultural_development_fund | public_financing | financial_product | 119–119 | Les modèles des documents à télécharger pour constitution du dossier suivant le type du projet sont accessibles via |
| 8 | 0.813582 | 0.818582 | es | investment_climate_indicators | esp_indicateurs_climat_dinvestissement_chunk_009 | business_climate | statistics | 17–18 | Principales áreas de asesoramiento percibidas por los inversores Promoción de oportunidades de inversión: 67% Acompañamiento proactivo para el desarrollo del ecosistema de su empresa: 29% Asistencia previa a la inversión: 12% Provisión de s |
| 9 | 0.812263 | 0.816263 | fr | financing_guide | guide_du_financement_des_entreprises_tpe_agr_support | equity_financing | financial_product | 20–20 | Dossier de candidature constitué des pièces suivantes fournies lors de la séance de sensibilisation : O Copie de la CIN légalisée O Dossier médical handicap O Carte RAMED (en cas de besoin) O Certificat de résidence (en cas de besoin) A l’i |
| 10 | 0.812175 | 0.817175 | es | investment_climate_indicators | esp_indicateurs_climat_dinvestissement_chunk_006 | business_climate | statistics | 11–11 | Motivaciones para implantarse en la región TTA Leyenda: Muy importante Moderadamente importante No importante 2. Economía / Coste Acceso a fuentes de financiamiento nacionales: Muy importante 74% — Moderadamente importante 9% — No important |

### Post-grouping/ranking final results

| Rank | Dense | Final | Lang | Family | Parent | Topic | Type | Pages | Preview |
|---:|---:|---:|---|---|---|---|---|---|---|
| 1 | 0.820977 | 0.825977 | es | investment_business_support_single_window | investment_business_support_single_window_es_phase3f_0005 | business_support | service | 6–6 | Incentivos Ponemos a su disposición todas las ofertas de incentivos, así como soluciones de financiamiento y ayuda financiera ofrecidas por nuestros socios públicos y privados a nivel nacional y regional, en un enfoque de convergencia de pr |
| 2 | 0.820098 | 0.825098 | es | chiffres_cles_2025 | esp_chiffres_cles_annee_2025_chunk_017 | territorial_promotion | statistics | 17–17 | Promoción y alianzas (4/4) Alianzas estratégicas para la proyección y el desarrollo económico de la Región Nuevo acuerdo de alianza CRI–IFC El objetivo de la alianza IFC – CRI TTA es incrementar las inversiones privadas respetuosas con el c |
| 3 | 0.819008 | 0.823008 | fr | financing_guide | guide_du_financement_des_entreprises_contractual_regime | public_financing | financial_product | 128–128 | à 250 o assurer un transfert de technologie o contribuer à la protection de l’environnement. Seuls les projets d’investissements dans les secteurs de l’Immobilier et de l’Agriculture, ne sont pas éligibles à la subvention FDII sous réserve  |
| 4 | 0.816202 | 0.821202 | es | chiffres_cles_2025 | esp_chiffres_cles_annee_2025_chunk_010 | business_support | statistics | 10–10 | Acompañamiento a las empresas (1/4) 5 500 empresas / promotores de proyectos acompañados 3 223 beneficiarios Ejes de acompañamiento: Facilitación del acceso a la financiación Refuerzo de las capacidades empresariales de los promotores de pr |
| 5 | 0.811719 | 0.819719 | fr | financing_guide | guide_du_financement_des_entreprises_intelak | bank_financing | financial_product | 32–32 | 32 Programme de financement couvrant les besoins d’investissement et de fonctionne- ment à des conditions préférentielles, destiné aux entreprises, personnes physiques ou morales, de droit marocain, remplissant les conditions d’éligibilité. |

### Duplicate and diversity diagnostics

- Raw top-30 parent duplicate count: 5
- Raw top-30 family duplicate count: 23
- Siblings collapsed: 0
- Family-cap removals: 0
- Final-k cuts: 25
- Final language diversity: 2
- Final family diversity: 3
- Detected query language: es
- Detected concepts: eligibility_conditions, financial_product

## ES — ¿Cuáles son las condiciones para beneficiarse de los programas de financiación?

### Raw dense top 10

| Rank | Dense | Final | Lang | Family | Parent | Topic | Type | Pages | Preview |
|---:|---:|---:|---|---|---|---|---|---|---|
| 1 | 0.822966 | 0.827966 | es | investment_business_support_single_window | investment_business_support_single_window_es_phase3f_0005 | business_support | service | 6–6 | Incentivos Ponemos a su disposición todas las ofertas de incentivos, así como soluciones de financiamiento y ayuda financiera ofrecidas por nuestros socios públicos y privados a nivel nacional y regional, en un enfoque de convergencia de pr |
| 2 | 0.821667 | 0.826667 | es | chiffres_cles_2025 | esp_chiffres_cles_annee_2025_chunk_017 | territorial_promotion | statistics | 17–17 | Promoción y alianzas (4/4) Alianzas estratégicas para la proyección y el desarrollo económico de la Región Nuevo acuerdo de alianza CRI–IFC El objetivo de la alianza IFC – CRI TTA es incrementar las inversiones privadas respetuosas con el c |
| 3 | 0.820284 | 0.824284 | fr | financing_guide | guide_du_financement_des_entreprises_contractual_regime | public_financing | financial_product | 128–128 | à 250 o assurer un transfert de technologie o contribuer à la protection de l’environnement. Seuls les projets d’investissements dans les secteurs de l’Immobilier et de l’Agriculture, ne sont pas éligibles à la subvention FDII sous réserve  |
| 4 | 0.818151 | 0.823151 | es | chiffres_cles_2025 | esp_chiffres_cles_annee_2025_chunk_010 | business_support | statistics | 10–10 | Acompañamiento a las empresas (1/4) 5 500 empresas / promotores de proyectos acompañados 3 223 beneficiarios Ejes de acompañamiento: Facilitación del acceso a la financiación Refuerzo de las capacidades empresariales de los promotores de pr |
| 5 | 0.817154 | 0.822154 | es | cri_presentation | esp_presentation_cri_tta_vf_semantic_028 | infrastructure | statistics | 38–39 | Las empresas elegibles para Los requisitos ¿Cuáles son los criterios de elegibilidad para poder beneficiar del apoyo beneficiar del apoyo? Cifra de negocios / Número de años de Importe total de la actividad Tasa prevista de inversion empleo |
| 6 | 0.816229 | 0.821229 | es | investment_climate_indicators | esp_indicateurs_climat_dinvestissement_chunk_009 | business_climate | statistics | 17–18 | Principales áreas de asesoramiento percibidas por los inversores Promoción de oportunidades de inversión: 67% Acompañamiento proactivo para el desarrollo del ecosistema de su empresa: 29% Asistencia previa a la inversión: 12% Provisión de s |
| 7 | 0.815681 | 0.818681 | es | chiffres_cles_2025 | esp_chiffres_cles_annee_2025_chunk_011 | business_support | statistics | 11–11 | Acompañamiento a las empresas (2/4) Balance del PIAFE* a nivel de la región TTA 4 672 expedientes financiados ~1,14 mil millones MAD de financiación * PIAFE: Programa Integrado de Apoyo y Financiación de las Empresas www.investangier.com 11 |
| 8 | 0.814512 | 0.818512 | fr | financing_guide | guide_du_financement_des_entreprises_agricultural_development_fund | public_financing | financial_product | 119–119 | Les modèles des documents à télécharger pour constitution du dossier suivant le type du projet sont accessibles via |
| 9 | 0.813842 | 0.817842 | fr | financing_guide | guide_du_financement_des_entreprises_tpe_agr_support | equity_financing | financial_product | 20–20 | Dossier de candidature constitué des pièces suivantes fournies lors de la séance de sensibilisation : O Copie de la CIN légalisée O Dossier médical handicap O Carte RAMED (en cas de besoin) O Certificat de résidence (en cas de besoin) A l’i |
| 10 | 0.813728 | 0.818728 | es | investment_climate_indicators | esp_indicateurs_climat_dinvestissement_chunk_006 | business_climate | statistics | 11–11 | Motivaciones para implantarse en la región TTA Leyenda: Muy importante Moderadamente importante No importante 2. Economía / Coste Acceso a fuentes de financiamiento nacionales: Muy importante 74% — Moderadamente importante 9% — No important |

### Post-grouping/ranking final results

| Rank | Dense | Final | Lang | Family | Parent | Topic | Type | Pages | Preview |
|---:|---:|---:|---|---|---|---|---|---|---|
| 1 | 0.822966 | 0.827966 | es | investment_business_support_single_window | investment_business_support_single_window_es_phase3f_0005 | business_support | service | 6–6 | Incentivos Ponemos a su disposición todas las ofertas de incentivos, así como soluciones de financiamiento y ayuda financiera ofrecidas por nuestros socios públicos y privados a nivel nacional y regional, en un enfoque de convergencia de pr |
| 2 | 0.821667 | 0.826667 | es | chiffres_cles_2025 | esp_chiffres_cles_annee_2025_chunk_017 | territorial_promotion | statistics | 17–17 | Promoción y alianzas (4/4) Alianzas estratégicas para la proyección y el desarrollo económico de la Región Nuevo acuerdo de alianza CRI–IFC El objetivo de la alianza IFC – CRI TTA es incrementar las inversiones privadas respetuosas con el c |
| 3 | 0.820284 | 0.824284 | fr | financing_guide | guide_du_financement_des_entreprises_contractual_regime | public_financing | financial_product | 128–128 | à 250 o assurer un transfert de technologie o contribuer à la protection de l’environnement. Seuls les projets d’investissements dans les secteurs de l’Immobilier et de l’Agriculture, ne sont pas éligibles à la subvention FDII sous réserve  |
| 4 | 0.818151 | 0.823151 | es | chiffres_cles_2025 | esp_chiffres_cles_annee_2025_chunk_010 | business_support | statistics | 10–10 | Acompañamiento a las empresas (1/4) 5 500 empresas / promotores de proyectos acompañados 3 223 beneficiarios Ejes de acompañamiento: Facilitación del acceso a la financiación Refuerzo de las capacidades empresariales de los promotores de pr |
| 5 | 0.817154 | 0.822154 | es | cri_presentation | esp_presentation_cri_tta_vf_semantic_028 | infrastructure | statistics | 38–39 | Las empresas elegibles para Los requisitos ¿Cuáles son los criterios de elegibilidad para poder beneficiar del apoyo beneficiar del apoyo? Cifra de negocios / Número de años de Importe total de la actividad Tasa prevista de inversion empleo |

### Duplicate and diversity diagnostics

- Raw top-30 parent duplicate count: 4
- Raw top-30 family duplicate count: 22
- Siblings collapsed: 0
- Family-cap removals: 0
- Final-k cuts: 25
- Final language diversity: 2
- Final family diversity: 4
- Detected query language: es
- Detected concepts: eligibility_conditions, financial_product

## ES — ¿Cuáles son las condiciones para beneficiarse de los programas de financiación؟

### Raw dense top 10

| Rank | Dense | Final | Lang | Family | Parent | Topic | Type | Pages | Preview |
|---:|---:|---:|---|---|---|---|---|---|---|
| 1 | 0.820977 | 0.825977 | es | investment_business_support_single_window | investment_business_support_single_window_es_phase3f_0005 | business_support | service | 6–6 | Incentivos Ponemos a su disposición todas las ofertas de incentivos, así como soluciones de financiamiento y ayuda financiera ofrecidas por nuestros socios públicos y privados a nivel nacional y regional, en un enfoque de convergencia de pr |
| 2 | 0.820098 | 0.825098 | es | chiffres_cles_2025 | esp_chiffres_cles_annee_2025_chunk_017 | territorial_promotion | statistics | 17–17 | Promoción y alianzas (4/4) Alianzas estratégicas para la proyección y el desarrollo económico de la Región Nuevo acuerdo de alianza CRI–IFC El objetivo de la alianza IFC – CRI TTA es incrementar las inversiones privadas respetuosas con el c |
| 3 | 0.819008 | 0.823008 | fr | financing_guide | guide_du_financement_des_entreprises_contractual_regime | public_financing | financial_product | 128–128 | à 250 o assurer un transfert de technologie o contribuer à la protection de l’environnement. Seuls les projets d’investissements dans les secteurs de l’Immobilier et de l’Agriculture, ne sont pas éligibles à la subvention FDII sous réserve  |
| 4 | 0.816202 | 0.821202 | es | chiffres_cles_2025 | esp_chiffres_cles_annee_2025_chunk_010 | business_support | statistics | 10–10 | Acompañamiento a las empresas (1/4) 5 500 empresas / promotores de proyectos acompañados 3 223 beneficiarios Ejes de acompañamiento: Facilitación del acceso a la financiación Refuerzo de las capacidades empresariales de los promotores de pr |
| 5 | 0.814717 | 0.819717 | es | cri_presentation | esp_presentation_cri_tta_vf_semantic_028 | infrastructure | statistics | 38–39 | Las empresas elegibles para Los requisitos ¿Cuáles son los criterios de elegibilidad para poder beneficiar del apoyo beneficiar del apoyo? Cifra de negocios / Número de años de Importe total de la actividad Tasa prevista de inversion empleo |
| 6 | 0.813844 | 0.816844 | es | chiffres_cles_2025 | esp_chiffres_cles_annee_2025_chunk_011 | business_support | statistics | 11–11 | Acompañamiento a las empresas (2/4) Balance del PIAFE* a nivel de la región TTA 4 672 expedientes financiados ~1,14 mil millones MAD de financiación * PIAFE: Programa Integrado de Apoyo y Financiación de las Empresas www.investangier.com 11 |
| 7 | 0.813634 | 0.817634 | fr | financing_guide | guide_du_financement_des_entreprises_agricultural_development_fund | public_financing | financial_product | 119–119 | Les modèles des documents à télécharger pour constitution du dossier suivant le type du projet sont accessibles via |
| 8 | 0.813582 | 0.818582 | es | investment_climate_indicators | esp_indicateurs_climat_dinvestissement_chunk_009 | business_climate | statistics | 17–18 | Principales áreas de asesoramiento percibidas por los inversores Promoción de oportunidades de inversión: 67% Acompañamiento proactivo para el desarrollo del ecosistema de su empresa: 29% Asistencia previa a la inversión: 12% Provisión de s |
| 9 | 0.812263 | 0.816263 | fr | financing_guide | guide_du_financement_des_entreprises_tpe_agr_support | equity_financing | financial_product | 20–20 | Dossier de candidature constitué des pièces suivantes fournies lors de la séance de sensibilisation : O Copie de la CIN légalisée O Dossier médical handicap O Carte RAMED (en cas de besoin) O Certificat de résidence (en cas de besoin) A l’i |
| 10 | 0.812175 | 0.817175 | es | investment_climate_indicators | esp_indicateurs_climat_dinvestissement_chunk_006 | business_climate | statistics | 11–11 | Motivaciones para implantarse en la región TTA Leyenda: Muy importante Moderadamente importante No importante 2. Economía / Coste Acceso a fuentes de financiamiento nacionales: Muy importante 74% — Moderadamente importante 9% — No important |

### Post-grouping/ranking final results

| Rank | Dense | Final | Lang | Family | Parent | Topic | Type | Pages | Preview |
|---:|---:|---:|---|---|---|---|---|---|---|
| 1 | 0.820977 | 0.825977 | es | investment_business_support_single_window | investment_business_support_single_window_es_phase3f_0005 | business_support | service | 6–6 | Incentivos Ponemos a su disposición todas las ofertas de incentivos, así como soluciones de financiamiento y ayuda financiera ofrecidas por nuestros socios públicos y privados a nivel nacional y regional, en un enfoque de convergencia de pr |
| 2 | 0.820098 | 0.825098 | es | chiffres_cles_2025 | esp_chiffres_cles_annee_2025_chunk_017 | territorial_promotion | statistics | 17–17 | Promoción y alianzas (4/4) Alianzas estratégicas para la proyección y el desarrollo económico de la Región Nuevo acuerdo de alianza CRI–IFC El objetivo de la alianza IFC – CRI TTA es incrementar las inversiones privadas respetuosas con el c |
| 3 | 0.819008 | 0.823008 | fr | financing_guide | guide_du_financement_des_entreprises_contractual_regime | public_financing | financial_product | 128–128 | à 250 o assurer un transfert de technologie o contribuer à la protection de l’environnement. Seuls les projets d’investissements dans les secteurs de l’Immobilier et de l’Agriculture, ne sont pas éligibles à la subvention FDII sous réserve  |
| 4 | 0.816202 | 0.821202 | es | chiffres_cles_2025 | esp_chiffres_cles_annee_2025_chunk_010 | business_support | statistics | 10–10 | Acompañamiento a las empresas (1/4) 5 500 empresas / promotores de proyectos acompañados 3 223 beneficiarios Ejes de acompañamiento: Facilitación del acceso a la financiación Refuerzo de las capacidades empresariales de los promotores de pr |
| 5 | 0.811719 | 0.819719 | fr | financing_guide | guide_du_financement_des_entreprises_intelak | bank_financing | financial_product | 32–32 | 32 Programme de financement couvrant les besoins d’investissement et de fonctionne- ment à des conditions préférentielles, destiné aux entreprises, personnes physiques ou morales, de droit marocain, remplissant les conditions d’éligibilité. |

### Duplicate and diversity diagnostics

- Raw top-30 parent duplicate count: 5
- Raw top-30 family duplicate count: 23
- Siblings collapsed: 0
- Family-cap removals: 0
- Final-k cuts: 25
- Final language diversity: 2
- Final family diversity: 3
- Detected query language: es
- Detected concepts: eligibility_conditions, financial_product

## FR — Quels projets ont été approuvés par la CRUI en 2024 ?

### Raw dense top 10

| Rank | Dense | Final | Lang | Family | Parent | Topic | Type | Pages | Preview |
|---:|---:|---:|---|---|---|---|---|---|---|
| 1 | 0.875096 | 0.880096 | fr | manar_al_moustatmir_news_2023 | manar_al_moustatmir_news_phase3f_0020 | crui_activity | statistics | 25–26 | 19 Durant l’année 2023, la CRUI a instruit 972 actes lors de ses 230 réunions et pour lesquels la Commission Régionale Unifiée d’Investissement a approuvé 709 demandes, soit 73% des actes soumis, et ce dans un délai ne dépassant la moyenne  |
| 2 | 0.859987 | 0.876987 | fr | cri_presentation | fr_presentation_cri_tta_vf_semantic_029 | crui | statistics | 40–41 | a _ és si El = Une fois vous êtes ici, vous êtes partout ! ANR Bilan Une croissance soutenue des dossiers d'investissement approuvés en CRUI CRUI 2024 — 737 Evolution du nombre 508 Evolution du montant 2022 des dossiers approuvés CHUTE ï ss |
| 3 | 0.857622 | 0.882622 | fr | crui_key_figures_2024_09_30 | fr_chiffres_cles_critta_30_sept_2024_chunk_002 | crui_activity | statistics | 2–2 | Une fois vous êtes ici, vous êtes partout ! 693 actes instruits par la CRUI au 30 septembre 2024 615 actes approuvés par la CRUI au 30 septembre 2024 Évolution de la part des actes examinés favorablement par la CRUI 2021 au 30 septembre 202 |
| 4 | 0.852554 | 0.849554 | fr | manar_al_moustatmir_news_2023 | manar_al_moustatmir_news_phase3f_0002 | investment_news | narrative | 5–5 | www.investangier.com Par ailleurs, depuis l’entrée 2023 de la nouvelle charte de l’investissement, la CRUI a également joué un rôle crucial en approuvant 44 projets de convention d'investissement d'une valeur d'environ 18 milliards de dirha |
| 5 | 0.850459 | 0.863459 | fr | chiffres_cles_2025 | fr_chiffres_cles_annee_2025_p06_c01 | crui_activity | table | 6–6 | Bilan de la CRUI (3/6) Répartition sectorielle des dossiers d’investissement approuvés en CRUI Secteurs : Énergie Industrie Tourisme Services Autres Par nombre de projets : 487 dossiers d’investissement Énergie : 67% Industrie : 15% Tourism |
| 6 | 0.849753 | 0.866753 | fr | crui_key_figures_2024_h1 | chiffres_cles_crui_1er_semestre_2024_francais_chunk_002 | projects_reviewed | statistics | 2–2 | Une fois vous êtes ici, vous êtes partout ! 433 Nombre de projets instruits par la CRUI avec avis définitif 379 Projets approuvés soit 87,5% des projets statués en CRUI 40,76 Milliards MAD d’investissement soit +72% par rapport au 1er semes |
| 7 | 0.848063 | 0.843063 | fr | chiffres_cles_2025 | fr_chiffres_cles_annee_2025_p09_c01 | sector_investment | statistics | 9–9 | Bilan de la CRUI (6/6) Une région pionnière en énergie, moteur de compétitivité et durabilité à l’export 11 projets approuvés ~22,4 milliards de dirhams projetés +770 emplois à terme 2,4 GW de puissance installée 2 projets solaires approuvé |
| 8 | 0.843870 | 0.855870 | es | crui_key_figures_2024_h1 | chiffres_cles_crui_1er_semestre_2024_espagnol_chunk_002 | projects_reviewed | statistics | 2–2 | ¡Una vez aquí, está en todas partes! 433 proyectos examinados por la Comisión Regional Unificada de Inversiones (CRUI) 379 proyectos aprobados, el 87,5% de los proyectos examinados por la CRUI 40,76 mil millones de dirhams de inversión, un  |
| 9 | 0.842559 | 0.859559 | fr | crui_key_figures_2024_h1 | chiffres_cles_crui_1er_semestre_2024_francais_chunk_006 | approved_projects | statistics | 6–6 | Une fois vous êtes ici, vous êtes partout ! 16 Projets de conventions d’investissement approuvés 9,54 milliards MAD d’investissement 6 525 emplois directs projetés Ventilation sectorielle des montants d’investissement des conventions approu |
| 10 | 0.841703 | 0.862703 | fr | crui_key_figures_2024_09_30 | fr_chiffres_cles_critta_30_sept_2024_chunk_006 | crui_activity | statistics | 6–6 | Une fois vous êtes ici, vous êtes partout ! ÉVOLUTION DES MONTANTS D’INVESTISSEMENT APPROUVÉS EN CRUI 2021-2023 (EN MILLIARDS MAD) 2021 : 36,6 2022 : 52 2023 : ~73,4 2024 au 30 septembre 2024 : ~68,8 Évolution indiquée : +41% ÉVOLUTION DU N |

### Post-grouping/ranking final results

| Rank | Dense | Final | Lang | Family | Parent | Topic | Type | Pages | Preview |
|---:|---:|---:|---|---|---|---|---|---|---|
| 1 | 0.857622 | 0.882622 | fr | crui_key_figures_2024_09_30 | fr_chiffres_cles_critta_30_sept_2024_chunk_002 | crui_activity | statistics | 2–2 | Une fois vous êtes ici, vous êtes partout ! 693 actes instruits par la CRUI au 30 septembre 2024 615 actes approuvés par la CRUI au 30 septembre 2024 Évolution de la part des actes examinés favorablement par la CRUI 2021 au 30 septembre 202 |
| 2 | 0.875096 | 0.880096 | fr | manar_al_moustatmir_news_2023 | manar_al_moustatmir_news_phase3f_0020 | crui_activity | statistics | 25–26 | 19 Durant l’année 2023, la CRUI a instruit 972 actes lors de ses 230 réunions et pour lesquels la Commission Régionale Unifiée d’Investissement a approuvé 709 demandes, soit 73% des actes soumis, et ce dans un délai ne dépassant la moyenne  |
| 3 | 0.859987 | 0.876987 | fr | cri_presentation | fr_presentation_cri_tta_vf_semantic_029 | crui | statistics | 40–41 | a _ és si El = Une fois vous êtes ici, vous êtes partout ! ANR Bilan Une croissance soutenue des dossiers d'investissement approuvés en CRUI CRUI 2024 — 737 Evolution du nombre 508 Evolution du montant 2022 des dossiers approuvés CHUTE ï ss |
| 4 | 0.849753 | 0.866753 | fr | crui_key_figures_2024_h1 | chiffres_cles_crui_1er_semestre_2024_francais_chunk_002 | projects_reviewed | statistics | 2–2 | Une fois vous êtes ici, vous êtes partout ! 433 Nombre de projets instruits par la CRUI avec avis définitif 379 Projets approuvés soit 87,5% des projets statués en CRUI 40,76 Milliards MAD d’investissement soit +72% par rapport au 1er semes |
| 5 | 0.850459 | 0.863459 | fr | chiffres_cles_2025 | fr_chiffres_cles_annee_2025_p06_c01 | crui_activity | table | 6–6 | Bilan de la CRUI (3/6) Répartition sectorielle des dossiers d’investissement approuvés en CRUI Secteurs : Énergie Industrie Tourisme Services Autres Par nombre de projets : 487 dossiers d’investissement Énergie : 67% Industrie : 15% Tourism |

### Duplicate and diversity diagnostics

- Raw top-30 parent duplicate count: 4
- Raw top-30 family duplicate count: 24
- Siblings collapsed: 2
- Family-cap removals: 0
- Final-k cuts: 23
- Final language diversity: 1
- Final family diversity: 5
- Detected query language: fr
- Detected concepts: crui_activity, investment_opportunity

## FR — Quelles opportunités d'investissement existent dans le secteur automobile ?

### Raw dense top 10

| Rank | Dense | Final | Lang | Family | Parent | Topic | Type | Pages | Preview |
|---:|---:|---:|---|---|---|---|---|---|---|
| 1 | 0.874807 | 0.891807 | fr | investors_guide_territorial_opportunities | investors_guide_territorial_opportunities_fr_chunk_0020 | investment_opportunity | investment_opportunity | 87–87 | INDICATEURS FINANCIERS DE L’INVESTISSEMENT Coût potentiel de l’investissement Des prévisions de croissance pour le secteurautomobile marocain estimées à 17,5% offrant de réelles opportunités pour les équipementiers. Croissance de 6 % du par |
| 2 | 0.851091 | 0.868091 | fr | investors_guide_territorial_opportunities | investors_guide_territorial_opportunities_fr_chunk_0032 | investment_opportunity | investment_opportunity | 134–135 | Le Royaume a élaboré des stratégies et des plans sectoriels visant l’amélioration des niveaux de services de transport et de la logistique ainsi que le développement d’infrastructures de transport, tel que le Plan nationale portuaire 2030 e |
| 3 | 0.850961 | 0.867961 | fr | investors_guide_territorial_opportunities | investors_guide_territorial_opportunities_fr_chunk_0032 | investment_opportunity | investment_opportunity | 135–135 | Parc automobile équipé d’informatique embarquée permettant de géo localiser l’ensemble des véhicules actifs. Système d’information pour assurer un suivi en temps réel. Entrepôts pour le stockage. Personnel qualifié et formé. Formalités admi |
| 4 | 0.849998 | 0.866998 | fr | investors_guide_territorial_opportunities | investors_guide_territorial_opportunities_fr_chunk_0020 | investment_opportunity | investment_opportunity | 88–88 | Programme « IDMAJ » / Programme « TAEHIL » Casablanca / Kenitra / Tanger Risques exogènes: Crises sanitaires, ... Institut de Formation aux Métiers de l‘Industrie Automobile PRINCIPAUX INSTITUTS DE FORMATIONS AUX MÉTIERS DE L’INDUSTRIE AUTO |
| 5 | 0.849476 | 0.864476 | fr | investors_guide_territorial_opportunities | investors_guide_territorial_opportunities_fr_chunk_0009 | investment_opportunity | investment_opportunity | 46–46 | Un climat régional favorable aux cultures de cannabis (intrant de l’industrie) et proximité avec les producteurs. Chaîne de valeur existante et taux d’intégration national de l’industrie automobile élevé. Des normes strictes à respecter, re |
| 6 | 0.848976 | 0.847976 | fr | investors_guide_territorial_opportunities | investors_guide_territorial_opportunities_fr_chunk_0067 | territorial_overview | narrative | 41–41 | AUTOMOBILE 34 38 41 44 47 Unité de transformation de cannabis pour l'industrie automobile Unité industrielle d'amortisseurs Unité industrielle de filtres Unité industrielle de plaquettes de freins Projet de Vélo / Moto électriques 32 |
| 7 | 0.847490 | 0.862490 | fr | investors_guide_territorial_opportunities | investors_guide_territorial_opportunities_fr_chunk_0009 | investment_opportunity | investment_opportunity | 43–43 | Ecosystème réglementé en amont et en aval (avec des dispositions en vigueur notamment pour l’approvisionnement de plants et semences étrangères et de commercialisation). Climat régional favorable à la culture du cannabis et proximité avec l |
| 8 | 0.847365 | 0.860365 | fr | investors_guide_territorial_opportunities | investors_guide_territorial_opportunities_fr_chunk_0011 | investment_opportunity | investment_opportunity | 50–50 | à une forte demande locale. Augmentation de la demande du fait d’une accentuation et d’un renforcement des normes de sécurité. Indice de complexité pour les produits** L’automobile est un secteur structurant de la région de TTA. Une filière |
| 9 | 0.846294 | 0.857294 | fr | investors_guide_territorial_opportunities | investors_guide_territorial_opportunities_fr_chunk_0012 | investment_opportunity | investment_opportunity | 55–55 | Unité Industrielle De Plaquettes De Freins Concurrents sur le territoire Concurrents internationaux Allemagne Chine Mexique MATRICE SWOT DE L’OPPORTUNITÉ D’INVESTISSEMENT Forces Faiblesses Manque d’expertise en matière de R&D et de la Pièce |
| 10 | 0.845227 | 0.858227 | fr | investors_guide_territorial_opportunities | investors_guide_territorial_opportunities_fr_chunk_0011 | investment_opportunity | investment_opportunity | 52–52 | Unité industrielle de filtres automobiles Concurrents sur le territoire Concurrents internationaux Allemagne Chine USA *Non exhaustif MATRICE SWOT DE L’OPPORTUNITÉ D’INVESTISSEMENT Forces Faiblesses Pièce indispensable s’insérant dans la ch |

### Post-grouping/ranking final results

| Rank | Dense | Final | Lang | Family | Parent | Topic | Type | Pages | Preview |
|---:|---:|---:|---|---|---|---|---|---|---|
| 1 | 0.874807 | 0.891807 | fr | investors_guide_territorial_opportunities | investors_guide_territorial_opportunities_fr_chunk_0020 | investment_opportunity | investment_opportunity | 87–87 | INDICATEURS FINANCIERS DE L’INVESTISSEMENT Coût potentiel de l’investissement Des prévisions de croissance pour le secteurautomobile marocain estimées à 17,5% offrant de réelles opportunités pour les équipementiers. Croissance de 6 % du par |
| 2 | 0.851091 | 0.868091 | fr | investors_guide_territorial_opportunities | investors_guide_territorial_opportunities_fr_chunk_0032 | investment_opportunity | investment_opportunity | 134–135 | Le Royaume a élaboré des stratégies et des plans sectoriels visant l’amélioration des niveaux de services de transport et de la logistique ainsi que le développement d’infrastructures de transport, tel que le Plan nationale portuaire 2030 e |
| 3 | 0.849476 | 0.864476 | fr | investors_guide_territorial_opportunities | investors_guide_territorial_opportunities_fr_chunk_0009 | investment_opportunity | investment_opportunity | 46–46 | Un climat régional favorable aux cultures de cannabis (intrant de l’industrie) et proximité avec les producteurs. Chaîne de valeur existante et taux d’intégration national de l’industrie automobile élevé. Des normes strictes à respecter, re |
| 4 | 0.847365 | 0.860365 | fr | investors_guide_territorial_opportunities | investors_guide_territorial_opportunities_fr_chunk_0011 | investment_opportunity | investment_opportunity | 50–50 | à une forte demande locale. Augmentation de la demande du fait d’une accentuation et d’un renforcement des normes de sécurité. Indice de complexité pour les produits** L’automobile est un secteur structurant de la région de TTA. Une filière |
| 5 | 0.846294 | 0.857294 | fr | investors_guide_territorial_opportunities | investors_guide_territorial_opportunities_fr_chunk_0012 | investment_opportunity | investment_opportunity | 55–55 | Unité Industrielle De Plaquettes De Freins Concurrents sur le territoire Concurrents internationaux Allemagne Chine Mexique MATRICE SWOT DE L’OPPORTUNITÉ D’INVESTISSEMENT Forces Faiblesses Manque d’expertise en matière de R&D et de la Pièce |

### Duplicate and diversity diagnostics

- Raw top-30 parent duplicate count: 11
- Raw top-30 family duplicate count: 26
- Siblings collapsed: 9
- Family-cap removals: 0
- Final-k cuts: 16
- Final language diversity: 1
- Final family diversity: 1
- Detected query language: fr
- Detected concepts: automotive, investment_opportunity

## Aggregate diagnostics

- Queries evaluated: 17
- Raw top-30 parent duplicates: 90
- Raw top-30 family duplicates: 412
- Siblings collapsed: 42
- Family soft penalties applied: 158
- Total family soft penalty: 0.584000
- Hard family removals: 0
- Strong temporal conflicts applied: 12
- Weak temporal conflicts applied: 16
- Temporal match bonuses applied: 22
- Final results returned: 85

## Targeted regression checks

- Spanish normal punctuation: PASS
- Spanish stray Arabic punctuation: PASS
- Automotive rich-family unique parents: 5
- Automotive rich-family results retained: 5
- CRUI 2024 ranking: 2024-supported evidence is reported with temporal match bonuses; explicit historical-only candidates receive weak penalties.

## Cross-language policy

No hard language filter is applied. Same-language preference is a small auditable adjustment; stronger cross-language evidence can outrank weaker same-language evidence. Translated document families remain independently retrievable and are not routinely capped.

## Recommendation

Use this retriever only for Phase 4D/4E evaluation until score calibration and answer-level evaluation are complete. Do not switch production routing yet.
