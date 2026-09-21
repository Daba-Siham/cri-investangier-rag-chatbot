# Phase 4E.1 — isolated abstention, temporal, and generation evaluation

- Timestamp UTC: `2026-09-20T22:00:26.278393+00:00`
- Frozen Phase-4E artifacts were read-only inputs and were not overwritten.

# Phase 4E.1 report

## Frozen Phase-4E baseline

- Baseline results SHA-256: `A2F82E251AE7316BCEF59EDEA55D8EE65C675BB2A6C4125F2E12E30998127097`
- Baseline dataset SHA-256: `229FD5097CD5643CFDCFC440D24E7DFECB5123857BEA339650841F500A1B1A4C`
- Frozen v1 family Recall@5: `0.64`
- Frozen v2 family Recall@5: `0.86`
- Frozen baseline gate: `V2_NOT_READY`

## Expanded abstention benchmark

- Total queries: 70
- Answerable: 50
- No-answer: 20

## Dense versus ranking threshold analysis

- Recommended evaluation-only policy: `top1_dense`
- Policy evidence: `{"policy_type": "top1_dense", "dense_threshold": 0.83, "minimum_margin": null, "evidence": {"best_dense": {"threshold": 0.83, "answerable_acceptance_recall": 0.7, "no_answer_rejection": 1.0, "false_acceptance_rate": 0.0, "false_rejection_rate": 0.30000000000000004, "balanced_accuracy": 0.85, "precision_answerable": 1.0, "f1": 0.8235294117647058}, "best_margin": {"threshold": 0.83, "minimum_margin": 0.0, "answerable_recall": 0.7, "no_answer_rejection": 1.0, "balanced_accuracy": 0.85}}}`
- Threshold 0.82 dense: `{"threshold": 0.82, "answerable_acceptance_recall": 0.84, "no_answer_rejection": 0.7, "false_acceptance_rate": 0.3, "false_rejection_rate": 0.16000000000000003, "balanced_accuracy": 0.77, "precision_answerable": 0.875, "f1": 0.8571428571428572}`
- Threshold 0.82 ranking: `{"threshold": 0.82, "answerable_acceptance_recall": 0.88, "no_answer_rejection": 0.7, "false_acceptance_rate": 0.3, "false_rejection_rate": 0.12, "balanced_accuracy": 0.79, "precision_answerable": 0.88, "f1": 0.88}`
- Full threshold tables are stored in the machine-readable results artifact.

## Margin analysis

- Best margin policy: `{"threshold": 0.83, "minimum_margin": 0.0, "answerable_recall": 0.7, "no_answer_rejection": 1.0, "balanced_accuracy": 0.85}`

## Temporal strict-year experiment

{
  "strict_query_count": 10,
  "frozen": {
    "requested_year_context_rate": 0.9,
    "conflicting_year_context_rate": 0.8,
    "family_recall_at_5": 0.7
  },
  "experimental": {
    "requested_year_context_rate": 0.9,
    "conflicting_year_context_rate": 0.1,
    "family_recall_at_5": 0.7
  }
}

- The experimental policy changes only final context selection; vector retrieval and Phase-4C ranking are unchanged.

## Known regression cases

{
  "v1_better": [
    "Q019",
    "Q024",
    "Q032"
  ],
  "both_missed": [
    "Q027",
    "Q029",
    "Q036",
    "Q048"
  ],
  "details": {
    "Q019": {
      "query": {
        "query_id": "Q019",
        "language": "en",
        "question": "What are the logistics infrastructure assets of the region?",
        "category": "infrastructure",
        "explicit_year": null,
        "expected_topics": [
          "logistics_infrastructure",
          "logistics_sector",
          "tanger_med"
        ],
        "expected_document_families": [
          "logistics_sector_brochure",
          "industrial_zones_panorama"
        ],
        "acceptable_languages": [
          "en",
          "fr"
        ]
      },
      "baseline_v1": [
        {
          "chunk_id": "investors_guide_territorial_opportunities_en_p133_c1",
          "document_id": "investors_guide_territorial_opportunities_en",
          "document_family_id": "investors_guide_territorial_opportunities",
          "filename": "Investors Guide to territorial opportunities_EN.pdf",
          "language": "en",
          "page": 133,
          "page_start": 133,
          "page_end": 133,
          "source_pages": [
            133
          ],
          "dense_score": 0.843789,
          "ranking_score": 0.843789,
          "retrieval_score": 0.843789,
          "final_score": 0.843789,
          "text": "Distribution Company\nLogistics\n• Fahs Anjra Province (Med Hub)\n• Tanger-Assilah Prefecture\n• Tetouan Province\nPROJECT DESCRIPTION\nBenefiting from the dynamism of its trade, the TTA region has significant\nadvantages for the establishment of a distribution company and a high -\nquality road, port, and airport network, particularly on its main axes.\nFurthermore, the region's proximity to Europe and the cities of Ceuta and\nMellilia, as well as the presence of free zones (such as Med Hub Logistics), further\nstrengthens this potential.\nCharacteristics of the Industry\nGeneral characteristics of the\nenvironment\nStrong\nnational\nand\nregional\ninvestment\ndynamics\nin\ninfrastructure,\nparticularly\nmaritime,\nroad,\nand\nrail,\nto\nprovide\ninterconnection between ports, airports, and\nlogistics zones.\nA geostrategic positioning of the TTA region and\nstrong proximity to Europe and the cities of\nCeuta and Mellilia.\nThanks to the positive evolution of Moroccan\nlogistics\nservices,\nseveral\ninternational\noperators have established themselves in\nMorocco,\nand\ndomestic\noperators\nare\nbeginning\nto\nposition\nthemselves\ninternationally,\nparticularly\nin\nthe\nAfrican\nmarket.\nWell -developed transportation infrastructure in\nthe region, including a high -quality road, rail,\nport, and airport network, demonstrating efforts\nto improve territorial accessibility and enhance\nthe quality of travel and trade.\nA national road network facilitating the flow of\ngoods,\nexcluding\nphosphate\n(which\nis\nExistence of dedicated free zones (notably Med\nHub in the Fahs Anjra province) offering various\ncustoms and fiscal benefits, reinforcing regional\nattractiveness.\nProximity to the Tanger -Med port, the largest\ncontainer port in the Mediterranean basin,\nconnected to over 180 ports worldwide and\nmore than 70 countries.\nA New Development Model that aims to make\nthe Kingdom a multisectoral platform anchored\nin international value chains, proposing a\nlogistics\nsector\nreform\nthrough\nthe\nestablishment of new governance to promote\nmultimodality and the structuring of logistics\nflows around logistics zones.\nNearly 7.5% of companies established in the TTA\nregion operate in the transportation sector. The\ncity of Tangier accounts for over 69% of regional\ntransportation companies.\nA high concentration of industries in the region\n(numerous industrial zones, logistics zones, etc.)\npresents an opportunity for sector operators.\nThe Kingdom has developed strategies and\nsectoral plans aimed at improving transport\nand logistics services levels, as well as the\ndevelopment of transport infrastructure, such\nNational\nLogistics\nCompetitiveness\n125"
        },
        {
          "chunk_id": "eng_panorama_des_zi_p32_c1",
          "document_id": "eng_panorama_des_zi",
          "document_family_id": "industrial_zones_panorama",
          "filename": "ENG_ Panorama des ZI.pdf",
          "language": "en",
          "page": 32,
          "page_start": 32,
          "page_end": 32,
          "source_pages": [
            32
          ],
          "dense_score": 0.82482857,
          "ranking_score": 0.82482857,
          "retrieval_score": 0.82482857,
          "final_score": 0.82482857,
          "text": "PROVINCE OF FAHS-ANJRA\n\nLocated on the western Mediterranean coast of Morocco, the province of Fahs-Anjra is a predominantly rural area characterized by remarkable landscapes. Fahs-Anjra has experienced spectacular economic growth in recent years. This coastal zone enjoys a strategic position, hosting the Tangier-Med port, logistics and industrial complex, which facilitates commercial exchanges with over 180 international ports.\n\nIn order to encourage economic growth, numerous other investments have been launched in the province, including the construction of roads, railways, ports and other infrastructure facilities. This commitment has attracted many foreign companies seeking to establish high-value-added activities in the region.\n\nBy hosting the Renault factory on 300 hectares, revolutionizing the automotive industry by being both carbon-neutral and zero industrial liquid discharge, the province has become the cradle of the automotive ecosystem. It already houses 40 multinational companies in the Tangier Automotive City industrial acceleration zone, offering direct access to Tangier Med Port.\n\nThe province also houses a logistics zone adjacent to the Med Hub port, a platform dedicated to establishing logistics bases covering Europe, the Mediterranean and Africa. It brings together logistics operators and distributors offering services such as order preparation, warehousing, packaging, labeling and quality control.\n\nIn parallel with its economic development, the province aims to become an urban center with the creation of a new city called Chrafate, located 18 km from Tangier, covering nearly 770 hectares. This city is designed to accommodate around 150,000 inhabitants and will be equipped with clean energy, public transportation, tourist areas, green spaces and a diverse range of housing options."
        },
        {
          "chunk_id": "eng_indicateurs_climat_dinvestissement_p23_c1",
          "document_id": "eng_indicateurs_climat_dinvestissement",
          "document_family_id": "investment_climate_indicators",
          "filename": "ENG_Indicateurs-climat-dinvestissement.pdf",
          "language": "en",
          "page": 23,
          "page_start": 23,
          "page_end": 23,
          "source_pages": [
            23
          ],
          "dense_score": 0.82046837,
          "ranking_score": 0.82046837,
          "retrieval_score": 0.82046837,
          "final_score": 0.82046837,
          "text": "3. Main improvement areas to activate to further enhance the business climate of the region and attract more FDI\n\nAdministrative:\n• Continuing the simplification of administrative procedures, especially those related to urban planning authorizations\n• Continuing the dematerialization of procedures\n• Urban planning that is more favorable to investment\n\nCommunication:\n• Mobilizing more resources for the promotion of territorial offerings at regional, national, and international levels\n\nLogistics:\n• Strengthening the supply of land for industrial, tourism, and economic use, especially in Tangier\n• Improving mobility and traffic management\n• Reducing logistics costs (road, maritime transport, etc.)\n\nSupport:\n• Consolidation & convergence of programs supporting young entrepreneurs\n\nTraining & HR:\n• Strengthening the offer of professional training\n• Implementation of an incentive framework for research and development\n\n21"
        },
        {
          "chunk_id": "eng_presentation_cri_tta_vf_p36_c1",
          "document_id": "eng_presentation_cri_tta_vf",
          "document_family_id": "cri_presentation",
          "filename": "ENG_Présentation CRI TTA VF.pdf",
          "language": "en",
          "page": 36,
          "page_start": 36,
          "page_end": 36,
          "source_pages": [
            36
          ],
          "dense_score": 0.81516105,
          "ranking_score": 0.81516105,
          "retrieval_score": 0.81516105,
          "final_score": 0.81516105,
          "text": "Territoriaioner Lever of the region's economic development\nmultisectoral hosting — and ee ei support offer"
        },
        {
          "chunk_id": "investors_guide_territorial_opportunities_en_p135_c1",
          "document_id": "investors_guide_territorial_opportunities_en",
          "document_family_id": "investors_guide_territorial_opportunities",
          "filename": "Investors Guide to territorial opportunities_EN.pdf",
          "language": "en",
          "page": 135,
          "page_start": 135,
          "page_end": 135,
          "source_pages": [
            135
          ],
          "dense_score": 0.81303716,
          "ranking_score": 0.81303716,
          "retrieval_score": 0.81303716,
          "final_score": 0.81303716,
          "text": "Distribution Company\nFOCUS: MED HUB\nFOCUS: TTA REGION'S\nINFRASTRUCTURE\nzones under development, and 2 planned zones.\nThe Free Trade Logistics Zone (FTLZ) of the Tanger\nMed complex was opened for commercialization\nsingle-window principle and offers investors\nwishing\nto\nestablish\nthemselves\nthere\na\nmultitude of customs and fiscal benefits.\nMed Hub is dedicated to value-added logistics\nactivities such as consolidation, distribution, and\nsupply. It operates in the distribution to other free\nzones in Morocco as well as the consumption of\nproducts in the Moroccan market (preparation,\nstorage, packaging, labelling, assembly, and\nquality control).\nIt benefits from its strategic location within the\nTanger Med port area and provides operators\nwith direct access to North Africa and Western\nEurope.\nProductive activities are mainly developed\naround the Tanger Med complex, confirming its\nquality\nand\ncompetitiveness\n(global\nconnectivity, significant processing capacities,\nvarious certifications and recognitions, etc.).\nTanger Med is the first container port in Africa\nand the Mediterranean and contributes strongly\nto regional and national commercial dynamics.\nst\nImport/Export Platform in Morocco\nIncluding the Tanger Med complex\nAirports\nof railway lines\n300 hectares\nincluding a complete range of warehouses, offices, or developed\nvacant land\nLocated in immediate proximity to the port\nthrough a single customs zone, the zone\ndedicated to valueadded logistics activities is in\nthe heart of the region's business centres,\nenabling rapid and efficient distribution to a\nmarket of over 1 billion consumers.\nPlatform is a global logistics, industrial, and\ncommercial hub.\nLocated at the Strait of Gibraltar, the platform\nbenefits from connectivity with 186 global ports\nand hosts 1,100 active companies operating\nmainly\nin\nthe\nautomotive,\naerospace,\nelectronics,\ntextile,\nagri-food,\nservices\nsectors.\n127"
        }
      ],
      "baseline_v2": [
        {
          "retrieval_chunk_id": "eng_presentation_cri_tta_vf_semantic_026__r001",
          "document_id": "eng_presentation_cri_tta_vf",
          "document_family_id": "cri_presentation",
          "filename": "ENG_Presentation_CRI_TTA.json",
          "language": "en",
          "topic_id": "infrastructure",
          "content_type": "narrative",
          "page_start": 36,
          "page_end": 36,
          "source_pages": [
            36
          ],
          "dense_score": 0.8507682,
          "ranking_score": 0.8557682,
          "text": "Territoriaioner Lever of the region's economic development\nmultisectoral hosting — and ee ei support offer"
        },
        {
          "retrieval_chunk_id": "investors_guide_territorial_opportunities_en_chunk_0032__r001a",
          "document_id": "investors_guide_territorial_opportunities_en",
          "document_family_id": "investors_guide_territorial_opportunities",
          "filename": "Investors_Guide_territorial_opportunities_EN.json",
          "language": "en",
          "topic_id": "investment_opportunity",
          "content_type": "investment_opportunity",
          "page_start": 133,
          "page_end": 133,
          "source_pages": [
            133
          ],
          "dense_score": 0.8448098,
          "ranking_score": 0.8498098000000001,
          "text": "Distribution Company\nLogistics\n• Fahs Anjra Province (Med Hub)\n• Tanger-Assilah Prefecture\n• Tetouan Province\nPROJECT DESCRIPTION\nBenefiting from the dynamism of its trade, the TTA region has significant\nadvantages for the establishment of a distribution company and a high -\nquality road, port, and airport network, particularly on its main axes.\nFurthermore, the region's proximity to Europe and the cities of Ceuta and\nMellilia, as well as the presence of free zones (such as Med Hub Logistics), further\nstrengthens this potential.\nCharacteristics of the Industry\nGeneral characteristics of the\nenvironment\nStrong\nnational\nand\nregional\ninvestment\ndynamics\nin\ninfrastructure,\nparticularly\nmaritime,\nroad,\nand\nrail,\nto\nprovide\ninterconnection between ports, airports, and\nlogistics zones.\nA geostrategic positioning of the TTA region and\nstrong proximity to Europe and the cities of\nCeuta and Mellilia.\nThanks to the positive evolution of Moroccan\nlogistics\nservices,\nseveral\ninternational\noperators have established themselves in\nMorocco,\nand\ndomestic\noperators\nare\nbeginning\nto\nposition\nthemselves\ninternationally,\nparticularly\nin\nthe\nAfrican\nmarket.\nWell -developed transportation infrastructure in\nthe region, including a high -quality road, rail,\nport, and airport network, demonstrating efforts\nto improve territorial accessibility and enhance\nthe quality of travel and trade.\nA national road network facilitating the flow of\ngoods,\nexcluding\nphosphate\n(which\nis\nExistence of dedicated free zones (notably Med\nHub in the Fahs Anjra province) offering various\ncustoms and fiscal benefits, reinforcing regional\nattractiveness."
        },
        {
          "retrieval_chunk_id": "eng_presentation_cri_tta_vf_semantic_043__r001",
          "document_id": "eng_presentation_cri_tta_vf",
          "document_family_id": "cri_presentation",
          "filename": "ENG_Presentation_CRI_TTA.json",
          "language": "en",
          "topic_id": "infrastructure",
          "content_type": "statistics",
          "page_start": 60,
          "page_end": 60,
          "source_pages": [
            60
          ],
          "dense_score": 0.82460123,
          "ranking_score": 0.82960123,
          "text": "porn slr Once you are here, you are everywhere! en See:\n° ° °\nTeritoriaioter A favorable business climate for investors\nfor investment ———\n92% OF COMPANIES ARE SATISFIED WITH\n° THEIR LOCATION IN THE TTA REGION.\nMain reasons to set up in the region Business trends and growth outlook in the region.\nof respondents consider the current situation\n\nQuality of life 82% of their companies satisfactory, with optimistic\n—— EEE 95% © growth prospects at all levels.\nGeographical location\n— 94% Bi Chet = bo\n\n- ro] ae Oe\nInfrastructure and a next-generation support structure fas | pass |\n84% tx | } sox |\nAvailability of skilled labor\n== Ss 81°, 69%\nMaturity of the ecosystem\n——— EE 78%\nCompetitive production costs Turnover Number Export Investment\n— EEE 74%, fours’ ereprcmwess flume vose\n\n@ Optimistic outlook @ Stable. @ Pessimistic outlook\nSource: Perception survey conducted by the IFC and the World Bank Group in 2023."
        },
        {
          "retrieval_chunk_id": "eng_presentation_cri_tta_vf_semantic_028__r001",
          "document_id": "eng_presentation_cri_tta_vf",
          "document_family_id": "cri_presentation",
          "filename": "ENG_Presentation_CRI_TTA.json",
          "language": "en",
          "topic_id": "infrastructure",
          "content_type": "narrative",
          "page_start": 39,
          "page_end": 39,
          "source_pages": [
            39
          ],
          "dense_score": 0.8227323,
          "ranking_score": 0.8257323,
          "text": "Once you are here, you are everywhere! one te\neT n eroe INVESTANGIER —ommtzonpe geepamnoe\nTerritoriaiorer Lever of the region's economic development\nmultisectoral hosting Skilled & qual ified ali aig support offer"
        },
        {
          "retrieval_chunk_id": "investors_guide_territorial_opportunities_en_chunk_0031__r001b",
          "document_id": "investors_guide_territorial_opportunities_en",
          "document_family_id": "investors_guide_territorial_opportunities",
          "filename": "Investors_Guide_territorial_opportunities_EN.json",
          "language": "en",
          "topic_id": "investment_opportunity",
          "content_type": "investment_opportunity",
          "page_start": 130,
          "page_end": 130,
          "source_pages": [
            130
          ],
          "dense_score": 0.81772494,
          "ranking_score": 0.82272494,
          "text": "PROJECT CHARACTERISTICS\nRegional geostrategic positioning close to\nEurope,\nfacilitating\nthe\ntransportation\nof\ncannabis not only at the national level but also\ninternationally.\nService Characteristics\nExistence of logistic zones in the region offering\nvarious advantages for investors.\nThe project involves handling the transportation\nof cannabis in its various forms and throughout\nthe entire process, from the supply phases of\nbasic inputs to the commercialization of the\nfinished product, including the transformation\nphases.\nStorage and handling dimensions may need to\nbe considered in addition to the transportation\naspect.\nPrerequisites\nDeveloped\nregional\ntransportation\ninfrastructure\n(Tanger\n-Med\nport,\nroads,\nairports, etc.) facilitating the transportation of\nproducts throughout their entire production\nprocess\n(supply,\ncultivation,\nprocessing,\nmarketing). However, some disparities related\nto the condition of the infrastructure are\nobserved, particularly in the most remote rural\ncommunities. Existence of a regulatory agency\nfor cannabis -related activities: the National\nAgency for Regulating Cannabis - Related\nActivities (ANRAC).\nCharacteristics of the Industry\nIndustry\nwith\nhigh\npotential\nbut\nstill\nunderdeveloped in terms of activities. The\nRegulatory Requirements\nBeing established as a company or other legal\nentity governed by Moroccan law.\nHaving qualified and sufficient material and\nhuman resources to carry out these activities.\nObtaining the approval issued by the Ministry of\nTransport and Logistics in accordance with the\napplicable legislation and regulations.\n122"
        }
      ],
      "experimental_v2": [
        {
          "evidence_id": "E1",
          "retrieval_chunk_id": "eng_presentation_cri_tta_vf_semantic_026__r001",
          "parent_semantic_chunk_id": "eng_presentation_cri_tta_vf_semantic_026",
          "document_id": "eng_presentation_cri_tta_vf",
          "document_family_id": "cri_presentation",
          "filename": "ENG_Presentation_CRI_TTA.json",
          "document_title": "Presentation of the Regional Investment Center",
          "language": "en",
          "topic_id": "infrastructure",
          "content_type": "narrative",
          "semantic_tags": [
            "infrastructure"
          ],
          "heading_path": [
            "Infrastructure and logistics"
          ],
          "page_start": 36,
          "page_end": 36,
          "source_pages": [
            36
          ],
          "text": "Territoriaioner Lever of the region's economic development\nmultisectoral hosting — and ee ei support offer",
          "source_spans": [
            {
              "page": 36,
              "text": "Territoriaioner Lever of the region's economic development\nmultisectoral hosting — and ee ei support offer"
            }
          ],
          "dense_score": 0.8507682,
          "ranking_score": 0.8557682,
          "expanded_from_sibling": false,
          "retrieval_chunk_index": 0,
          "retrieval_chunk_count": 1,
          "temporal_scope": {
            "primary_year": null,
            "years_mentioned": [],
            "reference_period": {
              "type": null,
              "year": null,
              "semester": null,
              "quarter": null,
              "start_date": null,
              "end_date": null
            }
          }
        },
        {
          "evidence_id": "E2",
          "retrieval_chunk_id": "investors_guide_territorial_opportunities_en_chunk_0032__r001a",
          "parent_semantic_chunk_id": "investors_guide_territorial_opportunities_en_chunk_0032",
          "document_id": "investors_guide_territorial_opportunities_en",
          "document_family_id": "investors_guide_territorial_opportunities",
          "filename": "Investors_Guide_territorial_opportunities_EN.json",
          "document_title": "Investors Guide to Territorial Opportunities",
          "language": "en",
          "topic_id": "investment_opportunity",
          "content_type": "investment_opportunity",
          "semantic_tags": [
            "distribution_company",
            "fahs_anjra",
            "investment_opportunity",
            "logistics",
            "tanger_assilah",
            "tetouan"
          ],
          "heading_path": [
            "Investors Guide to Territorial Opportunities",
            "Distribution Company"
          ],
          "page_start": 133,
          "page_end": 133,
          "source_pages": [
            133
          ],
          "text": "Distribution Company\nLogistics\n• Fahs Anjra Province (Med Hub)\n• Tanger-Assilah Prefecture\n• Tetouan Province\nPROJECT DESCRIPTION\nBenefiting from the dynamism of its trade, the TTA region has significant\nadvantages for the establishment of a distribution company and a high -\nquality road, port, and airport network, particularly on its main axes.\nFurthermore, the region's proximity to Europe and the cities of Ceuta and\nMellilia, as well as the presence of free zones (such as Med Hub Logistics), further\nstrengthens this potential.\nCharacteristics of the Industry\nGeneral characteristics of the\nenvironment\nStrong\nnational\nand\nregional\ninvestment\ndynamics\nin\ninfrastructure,\nparticularly\nmaritime,\nroad,\nand\nrail,\nto\nprovide\ninterconnection between ports, airports, and\nlogistics zones.\nA geostrategic positioning of the TTA region and\nstrong proximity to Europe and the cities of\nCeuta and Mellilia.\nThanks to the positive evolution of Moroccan\nlogistics\nservices,\nseveral\ninternational\noperators have established themselves in\nMorocco,\nand\ndomestic\noperators\nare\nbeginning\nto\nposition\nthemselves\ninternationally,\nparticularly\nin\nthe\nAfrican\nmarket.\nWell -developed transportation infrastructure in\nthe region, including a high -quality road, rail,\nport, and airport network, demonstrating efforts\nto improve territorial accessibility and enhance\nthe quality of travel and trade.\nA national road network facilitating the flow of\ngoods,\nexcluding\nphosphate\n(which\nis\nExistence of dedicated free zones (notably Med\nHub in the Fahs Anjra province) offering various\ncustoms and fiscal benefits, reinforcing regional\nattractiveness.",
          "source_spans": [
            {
              "page": 133,
              "text": "Distribution Company\nLogistics\n• Fahs Anjra Province (Med Hub)\n• Tanger-Assilah Prefecture\n• Tetouan Province\nPROJECT DESCRIPTION\nBenefiting from the dynamism of its trade, the TTA region has significant\nadvantages for the establishment of a distribution company and a high -\nquality road, port, and airport network, particularly on its main axes.\nFurthermore, the region's proximity to Europe and the cities of Ceuta and\nMellilia, as well as the presence of free zones (such as Med Hub Logistics), further\nstrengthens this potential.\nCharacteristics of the Industry\nGeneral characteristics of the\nenvironment\nStrong\nnational\nand\nregional\ninvestment\ndynamics\nin\ninfrastructure,\nparticularly\nmaritime,\nroad,\nand\nrail,\nto\nprovide\ninterconnection between ports, airports, and\nlogistics zones.\nA geostrategic positioning of the TTA region and\nstrong proximity to Europe and the cities of\nCeuta and Mellilia.\nThanks to the positive evolution of Moroccan\nlogistics\nservices,\nseveral\ninternational\noperators have established themselves in\nMorocco,\nand\ndomestic\noperators\nare\nbeginning\nto\nposition\nthemselves\ninternationally,\nparticularly\nin\nthe\nAfrican\nmarket.\nWell -developed transportation infrastructure in\nthe region, including a high -quality road, rail,\nport, and airport network, demonstrating efforts\nto improve territorial accessibility and enhance\nthe quality of travel and trade.\nA national road network facilitating the flow of\ngoods,\nexcluding\nphosphate\n(which\nis\nExistence of dedicated free zones (notably Med\nHub in the Fahs Anjra province) offering various\ncustoms and fiscal benefits, reinforcing regional\nattractiveness."
            }
          ],
          "dense_score": 0.8448098,
          "ranking_score": 0.8498098000000001,
          "expanded_from_sibling": false,
          "retrieval_chunk_index": 0,
          "retrieval_chunk_count": 9,
          "temporal_scope": {
            "primary_year": null,
            "years_mentioned": [
              2008,
              2009,
              2020
            ],
            "reference_period": {
              "type": null,
              "year": null,
              "semester": null,
              "quarter": null,
              "start_date": null,
              "end_date": null
            }
          }
        },
        {
          "evidence_id": "E3",
          "retrieval_chunk_id": "eng_presentation_cri_tta_vf_semantic_043__r001",
          "parent_semantic_chunk_id": "eng_presentation_cri_tta_vf_semantic_043",
          "document_id": "eng_presentation_cri_tta_vf",
          "document_family_id": "cri_presentation",
          "filename": "ENG_Presentation_CRI_TTA.json",
          "document_title": "Presentation of the Regional Investment Center",
          "language": "en",
          "topic_id": "infrastructure",
          "content_type": "statistics",
          "semantic_tags": [
            "infrastructure",
            "regional_indicators"
          ],
          "heading_path": [
            "Infrastructure and logistics"
          ],
          "page_start": 60,
          "page_end": 60,
          "source_pages": [
            60
          ],
          "text": "porn slr Once you are here, you are everywhere! en See:\n° ° °\nTeritoriaioter A favorable business climate for investors\nfor investment ———\n92% OF COMPANIES ARE SATISFIED WITH\n° THEIR LOCATION IN THE TTA REGION.\nMain reasons to set up in the region Business trends and growth outlook in the region.\nof respondents consider the current situation\n\nQuality of life 82% of their companies satisfactory, with optimistic\n—— EEE 95% © growth prospects at all levels.\nGeographical location\n— 94% Bi Chet = bo\n\n- ro] ae Oe\nInfrastructure and a next-generation support structure fas | pass |\n84% tx | } sox |\nAvailability of skilled labor\n== Ss 81°, 69%\nMaturity of the ecosystem\n——— EE 78%\nCompetitive production costs Turnover Number Export Investment\n— EEE 74%, fours’ ereprcmwess flume vose\n\n@ Optimistic outlook @ Stable. @ Pessimistic outlook\nSource: Perception survey conducted by the IFC and the World Bank Group in 2023.",
          "source_spans": [
            {
              "page": 60,
              "text": "porn slr Once you are here, you are everywhere! en See:\n° ° °\nTeritoriaioter A favorable business climate for investors\nfor investment ———\n92% OF COMPANIES ARE SATISFIED WITH\n° THEIR LOCATION IN THE TTA REGION.\nMain reasons to set up in the region Business trends and growth outlook in the region.\nof respondents consider the current situation\n\nQuality of life 82% of their companies satisfactory, with optimistic\n—— EEE 95% © growth prospects at all levels.\nGeographical location\n— 94% Bi Chet = bo\n\n- ro] ae Oe\nInfrastructure and a next-generation support structure fas | pass |\n84% tx | } sox |\nAvailability of skilled labor\n== Ss 81°, 69%\nMaturity of the ecosystem\n——— EE 78%\nCompetitive production costs Turnover Number Export Investment\n— EEE 74%, fours’ ereprcmwess flume vose\n\n@ Optimistic outlook @ Stable. @ Pessimistic outlook\nSource: Perception survey conducted by the IFC and the World Bank Group in 2023."
            }
          ],
          "dense_score": 0.82460123,
          "ranking_score": 0.82960123,
          "expanded_from_sibling": false,
          "retrieval_chunk_index": 0,
          "retrieval_chunk_count": 1,
          "temporal_scope": {
            "primary_year": null,
            "years_mentioned": [
              2023
            ],
            "reference_period": {
              "type": null,
              "year": null,
              "semester": null,
              "quarter": null,
              "start_date": null,
              "end_date": null
            }
          }
        },
        {
          "evidence_id": "E4",
          "retrieval_chunk_id": "eng_presentation_cri_tta_vf_semantic_028__r001",
          "parent_semantic_chunk_id": "eng_presentation_cri_tta_vf_semantic_028",
          "document_id": "eng_presentation_cri_tta_vf",
          "document_family_id": "cri_presentation",
          "filename": "ENG_Presentation_CRI_TTA.json",
          "document_title": "Presentation of the Regional Investment Center",
          "language": "en",
          "topic_id": "infrastructure",
          "content_type": "narrative",
          "semantic_tags": [
            "infrastructure"
          ],
          "heading_path": [
            "Infrastructure and logistics"
          ],
          "page_start": 39,
          "page_end": 39,
          "source_pages": [
            39
          ],
          "text": "Once you are here, you are everywhere! one te\neT n eroe INVESTANGIER —ommtzonpe geepamnoe\nTerritoriaiorer Lever of the region's economic development\nmultisectoral hosting Skilled & qual ified ali aig support offer",
          "source_spans": [
            {
              "page": 39,
              "text": "Once you are here, you are everywhere! one te\neT n eroe INVESTANGIER —ommtzonpe geepamnoe\nTerritoriaiorer Lever of the region's economic development\nmultisectoral hosting Skilled & qual ified ali aig support offer"
            }
          ],
          "dense_score": 0.8227323,
          "ranking_score": 0.8257323,
          "expanded_from_sibling": false,
          "retrieval_chunk_index": 0,
          "retrieval_chunk_count": 1,
          "temporal_scope": {
            "primary_year": null,
            "years_mentioned": [],
            "reference_period": {
              "type": null,
              "year": null,
              "semester": null,
              "quarter": null,
              "start_date": null,
              "end_date": null
            }
          }
        },
        {
          "evidence_id": "E5",
          "retrieval_chunk_id": "investors_guide_territorial_opportunities_en_chunk_0031__r001b",
          "parent_semantic_chunk_id": "investors_guide_territorial_opportunities_en_chunk_0031",
          "document_id": "investors_guide_territorial_opportunities_en",
          "document_family_id": "investors_guide_territorial_opportunities",
          "filename": "Investors_Guide_territorial_opportunities_EN.json",
          "document_title": "Investors Guide to Territorial Opportunities",
          "language": "en",
          "topic_id": "investment_opportunity",
          "content_type": "investment_opportunity",
          "semantic_tags": [
            "al_hoceima",
            "cannabis_transport",
            "chefchaouen",
            "investment_opportunity",
            "larache",
            "logistics",
            "tanger_assilah"
          ],
          "heading_path": [
            "Investors Guide to Territorial Opportunities",
            "Transportation of Cannabis"
          ],
          "page_start": 130,
          "page_end": 130,
          "source_pages": [
            130
          ],
          "text": "PROJECT CHARACTERISTICS\nRegional geostrategic positioning close to\nEurope,\nfacilitating\nthe\ntransportation\nof\ncannabis not only at the national level but also\ninternationally.\nService Characteristics\nExistence of logistic zones in the region offering\nvarious advantages for investors.\nThe project involves handling the transportation\nof cannabis in its various forms and throughout\nthe entire process, from the supply phases of\nbasic inputs to the commercialization of the\nfinished product, including the transformation\nphases.\nStorage and handling dimensions may need to\nbe considered in addition to the transportation\naspect.\nPrerequisites\nDeveloped\nregional\ntransportation\ninfrastructure\n(Tanger\n-Med\nport,\nroads,\nairports, etc.) facilitating the transportation of\nproducts throughout their entire production\nprocess\n(supply,\ncultivation,\nprocessing,\nmarketing). However, some disparities related\nto the condition of the infrastructure are\nobserved, particularly in the most remote rural\ncommunities. Existence of a regulatory agency\nfor cannabis -related activities: the National\nAgency for Regulating Cannabis - Related\nActivities (ANRAC).\nCharacteristics of the Industry\nIndustry\nwith\nhigh\npotential\nbut\nstill\nunderdeveloped in terms of activities. The\nRegulatory Requirements\nBeing established as a company or other legal\nentity governed by Moroccan law.\nHaving qualified and sufficient material and\nhuman resources to carry out these activities.\nObtaining the approval issued by the Ministry of\nTransport and Logistics in accordance with the\napplicable legislation and regulations.\n122",
          "source_spans": [
            {
              "page": 130,
              "text": "PROJECT CHARACTERISTICS\nRegional geostrategic positioning close to\nEurope,\nfacilitating\nthe\ntransportation\nof\ncannabis not only at the national level but also\ninternationally.\nService Characteristics\nExistence of logistic zones in the region offering\nvarious advantages for investors.\nThe project involves handling the transportation\nof cannabis in its various forms and throughout\nthe entire process, from the supply phases of\nbasic inputs to the commercialization of the\nfinished product, including the transformation\nphases.\nStorage and handling dimensions may need to\nbe considered in addition to the transportation\naspect.\nPrerequisites\nDeveloped\nregional\ntransportation\ninfrastructure\n(Tanger\n-Med\nport,\nroads,\nairports, etc.) facilitating the transportation of\nproducts throughout their entire production\nprocess\n(supply,\ncultivation,\nprocessing,\nmarketing). However, some disparities related\nto the condition of the infrastructure are\nobserved, particularly in the most remote rural\ncommunities. Existence of a regulatory agency\nfor cannabis -related activities: the National\nAgency for Regulating Cannabis - Related\nActivities (ANRAC).\nCharacteristics of the Industry\nIndustry\nwith\nhigh\npotential\nbut\nstill\nunderdeveloped in terms of activities. The\nRegulatory Requirements\nBeing established as a company or other legal\nentity governed by Moroccan law.\nHaving qualified and sufficient material and\nhuman resources to carry out these activities.\nObtaining the approval issued by the Ministry of\nTransport and Logistics in accordance with the\napplicable legislation and regulations.\n122"
            }
          ],
          "dense_score": 0.81772494,
          "ranking_score": 0.82272494,
          "expanded_from_sibling": false,
          "retrieval_chunk_index": 1,
          "retrieval_chunk_count": 6,
          "temporal_scope": {
            "primary_year": null,
            "years_mentioned": [],
            "reference_period": {
              "type": null,
              "year": null,
              "semester": null,
              "quarter": null,
              "start_date": null,
              "end_date": null
            }
          }
        }
      ],
      "status": "review_required"
    },
    "Q024": {
      "query": {
        "query_id": "Q024",
        "language": "en",
        "question": "What is the cost of industrial land?",
        "category": "cost",
        "explicit_year": 2024,
        "expected_topics": [
          "industrial_land_cost"
        ],
        "expected_document_families": [
          "production_factor_cost_guide_2024"
        ],
        "acceptable_languages": [
          "en",
          "fr"
        ]
      },
      "baseline_v1": [
        {
          "chunk_id": "manar_al_moustatmir_eng_png_p9_c1",
          "document_id": "manar_al_moustatmir_eng_png",
          "document_family_id": "manar_al_moustatmir_news_2023",
          "filename": "Manar Al Moustatmir ENG PNG Latest version.pdf",
          "language": "en",
          "page": 9,
          "page_start": 9,
          "page_end": 9,
          "source_pages": [
            9
          ],
          "dense_score": 0.8364601,
          "ranking_score": 0.8364601,
          "retrieval_score": 0.8364601,
          "final_score": 0.8364601,
          "text": "= Allocation of plots at the first phase (SO hectares) of the Loukkos Agropole\nin Larache.\n\n—\n\na Poh = @Fnideq\n2 | \\~ Tanger @\n(@ Maiq\nSurface area Global Tetouan\nat term cost .\nAssileh (@)\n150 ha 457 MDH aiecsing\nCompanies in Long-term abgrepote\nprocess of set up employment Ouszza0e\n47 8000\n\nm Launch of a land leasing offer at Tetouan Park under the partnership\nagreement related to land mobilization within the industrial and logistics park\nTETOUAN PARK signed on June 10, 2022: 9 industrial lots.\"\n\nTotal surface Valid industrial Investment Long-term\narea projects amount employment\n8 ha 8 350 MMAD 1000\n\nThe start of the commissioning of the Tanja Balia economic activities zone: 117\npremises allocated.\n\nwww.investangier.com\n\nLoukkos Agropole: 150 ha; global cost 457 MDH; 47 companies in process of set up; 8,000 long-term jobs.\nTetouan Park land leasing offer: 8 ha; 8 valid industrial projects; investment amount 350 MMAD; 1,000 long-term jobs.\nTanja Balia economic activities zone: 117 premises allocated."
        },
        {
          "chunk_id": "eng_presentation_cri_tta_vf_p37_c1",
          "document_id": "eng_presentation_cri_tta_vf",
          "document_family_id": "cri_presentation",
          "filename": "ENG_Présentation CRI TTA VF.pdf",
          "language": "en",
          "page": 37,
          "page_start": 37,
          "page_end": 37,
          "source_pages": [
            37
          ],
          "dense_score": 0.8174325,
          "ranking_score": 0.8174325,
          "retrieval_score": 0.8174325,
          "final_score": 0.8174325,
          "text": "Sere aeirt seca Once you are here, you are everywhere! 4 fee,\nSala ‘mares = SE\n° e e °\nCompetitive Varied land offer aimed at productive investment\n& multisectoral ——=— Legend\nhosting platforms —\nic) 2\nf Fahs-Anjra = (2) Fishing port\n23 Operational economic | ZIGTENAYA a a > A FNIDEG | eer\nA and industrial zones 2 Commercial zones 2 Tanger a gaan Fridoq platform TS tonger mea port\ncovering an area Zilighogha, a ae, e oo 8 iw\nof 150 ha asjer LEON ar\nNat a oe | a i [) zMartit\nS »} Tetouan Shor\n+3900 1 Agro-pole covering sesaeex : ange DUAN a\nha an area of 150 ha mere i pap omegenrns\noun |\nZAE Assilah~_ AM\n4 industrial acceleration 1 Offshoring zone 2 ie) f\nzones covering an area (P21) covering 20 ha [ LARACHE F@ Bd vecua | &\nof 2,500 ha ZHostal As\n8 Muttisectoral industrial 5 Zones in the Leracne Aare >, moe\nzones covering an FF process of being di\narea of 700 ha developed 2\n6 Economic activity\nzones covering an area of 53 ha 1\napproximately 160 ha\n1 Free logistics zone\ncovering ee ~400 millon MaD\nof 250ha"
        },
        {
          "chunk_id": "nv_guide_cout_facteurs_cri_2024_p12_c1",
          "document_id": "nv_guide_cout_facteurs_cri_2024",
          "document_family_id": "production_factor_cost_guide_2024",
          "filename": "Nv Guide Cout de facteurs CRI V13032025.pdf",
          "language": "fr",
          "page": 12,
          "page_start": 12,
          "page_end": 12,
          "source_pages": [
            12
          ],
          "dense_score": 0.81007516,
          "ranking_score": 0.81007516,
          "retrieval_score": 0.81007516,
          "final_score": 0.81007516,
          "text": "PRIX DES MATÉRIAUX DE CONSTRUCTION"
        },
        {
          "chunk_id": "eng_presentation_cri_tta_vf_p30_c1",
          "document_id": "eng_presentation_cri_tta_vf",
          "document_family_id": "cri_presentation",
          "filename": "ENG_Présentation CRI TTA VF.pdf",
          "language": "en",
          "page": 30,
          "page_start": 30,
          "page_end": 30,
          "source_pages": [
            30
          ],
          "dense_score": 0.80864453,
          "ranking_score": 0.80864453,
          "retrieval_score": 0.80864453,
          "final_score": 0.80864453,
          "text": "Engine of the regional economy, in continuous development\n© SAU: 730,000 ha © 18 fishing ports & landing @ 2 identified areas:\n© 80% of the national @ Total area: 795 ha, of which\nagricultural added value“ (2% of the national tonnage)\nWith a value of 722 million MAD\n© 34 million workdays (75% of the national value) ®"
        },
        {
          "chunk_id": "manar_al_moustatmir_news_p9_c1",
          "document_id": "manar_al_moustatmir_news",
          "document_family_id": "manar_al_moustatmir_news_2023",
          "filename": "Manar Al Moustatmir News.pdf",
          "language": "fr",
          "page": 9,
          "page_start": 9,
          "page_end": 9,
          "source_pages": [
            9
          ],
          "dense_score": 0.80810213,
          "ranking_score": 0.80810213,
          "retrieval_score": 0.80810213,
          "final_score": 0.80810213,
          "text": "03\nwww.investangier.com\nLancement d’une offre foncière en location à Tétouan Park en vertu de la \nconvention de partenariat relative à la mobilisation foncière relevant du parc \nindustriel et logistique TETOUAN PARK signée le 10 juin 2022 : 9 lots industriels\n8 ha\nSurface\ntotale\n8\nProjets\nindustriels\nvalidés\n350 MMAD\nMontant\nd’investissement\n1 000\nEmplois\nà terme\nAttribution des lots au niveau de la première tranche (50 Ha) de l'agropole \nLoukkos de Larache.\n47\nCoût\nglobal\n457 MDH\nEntreprises\nen cours\nd’installation\n8 000\nEmplois\nà terme\n150 ha\nSurface\nà termes\nAssilah\nLarache\nAl Hoceima\nChefchaouen\nOuezzane\nKsar\nEl Kebir\nTetouan\nM’diq\nFnideq\nTanger\nAgropole\nde Loukkos\nDébut de la mise en service de la zone d’activités économiques Tanja Balia : \n117 locaux attribués"
        }
      ],
      "baseline_v2": [
        {
          "retrieval_chunk_id": "manar_al_moustatmir_eng_png_phase3f_0006__r001",
          "document_id": "manar_al_moustatmir_eng_png",
          "document_family_id": "manar_al_moustatmir_news_2023",
          "filename": "Manar_Al_Moustatmir_ENG_PNG.json",
          "language": "en",
          "topic_id": "investment_news",
          "content_type": "investment_opportunity",
          "page_start": 9,
          "page_end": 9,
          "source_pages": [
            9
          ],
          "dense_score": 0.83712626,
          "ranking_score": 0.84212626,
          "text": "= Allocation of plots at the first phase (SO hectares) of the Loukkos Agropole\nin Larache.\n\n—\n\na Poh = @Fnideq\n2 | \\~ Tanger @\n(@ Maiq\nSurface area Global Tetouan\nat term cost .\nAssileh (@)\n150 ha 457 MDH aiecsing\nCompanies in Long-term abgrepote\nprocess of set up employment Ouszza0e\n47 8000\n\nm Launch of a land leasing offer at Tetouan Park under the partnership\nagreement related to land mobilization within the industrial and logistics park\nTETOUAN PARK signed on June 10, 2022: 9 industrial lots.\"\n\nTotal surface Valid industrial Investment Long-term\narea projects amount employment\n8 ha 8 350 MMAD 1000\n\nThe start of the commissioning of the Tanja Balia economic activities zone: 117\npremises allocated.\n\nwww.investangier.com\n\nLoukkos Agropole: 150 ha; global cost 457 MDH; 47 companies in process of set up; 8,000 long-term jobs.\nTetouan Park land leasing offer: 8 ha; 8 valid industrial projects; investment amount 350 MMAD; 1,000 long-term jobs.\nTanja Balia economic activities zone: 117 premises allocated."
        },
        {
          "retrieval_chunk_id": "eng_presentation_cri_tta_vf_semantic_027__r001a",
          "document_id": "eng_presentation_cri_tta_vf",
          "document_family_id": "cri_presentation",
          "filename": "ENG_Presentation_CRI_TTA.json",
          "language": "en",
          "topic_id": "industrial_ecosystem",
          "content_type": "statistics",
          "page_start": 37,
          "page_end": 37,
          "source_pages": [
            37
          ],
          "dense_score": 0.8261782,
          "ranking_score": 0.8311782,
          "text": "Sere aeirt seca Once you are here, you are everywhere! 4 fee,\nSala ‘mares = SE\n° e e °\nCompetitive Varied land offer aimed at productive investment\n& multisectoral ——=— Legend\nhosting platforms —\nic) 2\nf Fahs-Anjra = (2) Fishing port\n23 Operational economic | ZIGTENAYA a a > A FNIDEG | eer\nA and industrial zones 2 Commercial zones 2 Tanger a gaan Fridoq platform TS tonger mea port\ncovering an area Zilighogha, a ae, e oo 8 iw\nof 150 ha asjer LEON ar\nNat a oe | a i [) zMartit\nS »} Tetouan Shor\n+3900 1 Agro-pole covering sesaeex : ange DUAN a\nha an area of 150 ha mere i pap omegenrns\noun |\nZAE Assilah~_ AM\n4 industrial acceleration 1 Offshoring zone 2 ie) f\nzones covering an area (P21) covering 20 ha [ LARACHE F@ Bd vecua | &\nof 2,500 ha ZHostal As\n8 Muttisectoral industrial 5 Zones in the Leracne Aare >, moe\nzones covering an FF process of being di\narea of 700 ha developed 2\n6 Economic activity\nzones covering an area of 53 ha 1\napproximately 160 ha\n1 Free logistics zone\ncovering ee ~400 millon MaD\nof 250ha"
        },
        {
          "retrieval_chunk_id": "investors_guide_territorial_opportunities_en_chunk_0005__r002c",
          "document_id": "investors_guide_territorial_opportunities_en",
          "document_family_id": "investors_guide_territorial_opportunities",
          "filename": "Investors_Guide_territorial_opportunities_EN.json",
          "language": "en",
          "topic_id": "investment_opportunity",
          "content_type": "investment_opportunity",
          "page_start": 27,
          "page_end": 27,
          "source_pages": [
            27
          ],
          "dense_score": 0.81237185,
          "ranking_score": 0.81737185,
          "text": "guidance, insurance and social coverage)."
        },
        {
          "retrieval_chunk_id": "investors_guide_territorial_opportunities_en_chunk_0002__r003",
          "document_id": "investors_guide_territorial_opportunities_en",
          "document_family_id": "investors_guide_territorial_opportunities",
          "filename": "Investors_Guide_territorial_opportunities_EN.json",
          "language": "en",
          "topic_id": "investment_opportunity",
          "content_type": "investment_opportunity",
          "page_start": 18,
          "page_end": 18,
          "source_pages": [
            18
          ],
          "dense_score": 0.8104334,
          "ranking_score": 0.8154334,
          "text": "HEXXEDE SIEISE 1 SOJoXo\nCo MB OzE?\n\nINVESTAMGIER CENTRE RÉGIONAL D'INVESTISSEMENT\n\ndamena da rca ls ANGER TÉTOUAN AL HOCEIMA"
        },
        {
          "retrieval_chunk_id": "eng_presentation_cri_tta_vf_semantic_022__r001",
          "document_id": "eng_presentation_cri_tta_vf",
          "document_family_id": "cri_presentation",
          "filename": "ENG_Presentation_CRI_TTA.json",
          "language": "en",
          "topic_id": "infrastructure",
          "content_type": "statistics",
          "page_start": 30,
          "page_end": 30,
          "source_pages": [
            30
          ],
          "dense_score": 0.81035864,
          "ranking_score": 0.81535864,
          "text": "Engine of the regional economy, in continuous development\n© SAU: 730,000 ha © 18 fishing ports & landing @ 2 identified areas:\n© 80% of the national @ Total area: 795 ha, of which\nagricultural added value“ (2% of the national tonnage)\nWith a value of 722 million MAD\n© 34 million workdays (75% of the national value) ®"
        }
      ],
      "experimental_v2": [
        {
          "evidence_id": "E1",
          "retrieval_chunk_id": "manar_al_moustatmir_eng_png_phase3f_0006__r001",
          "parent_semantic_chunk_id": "manar_al_moustatmir_eng_png_phase3f_0006",
          "document_id": "manar_al_moustatmir_eng_png",
          "document_family_id": "manar_al_moustatmir_news_2023",
          "filename": "Manar_Al_Moustatmir_ENG_PNG.json",
          "document_title": "Investment and entrepreneurship news review",
          "language": "en",
          "topic_id": "investment_news",
          "content_type": "investment_opportunity",
          "semantic_tags": [
            "investment_news",
            "investment_opportunity",
            "project_announcement"
          ],
          "heading_path": [
            "Land offer at Tetouan Park"
          ],
          "page_start": 9,
          "page_end": 9,
          "source_pages": [
            9
          ],
          "text": "= Allocation of plots at the first phase (SO hectares) of the Loukkos Agropole\nin Larache.\n\n—\n\na Poh = @Fnideq\n2 | \\~ Tanger @\n(@ Maiq\nSurface area Global Tetouan\nat term cost .\nAssileh (@)\n150 ha 457 MDH aiecsing\nCompanies in Long-term abgrepote\nprocess of set up employment Ouszza0e\n47 8000\n\nm Launch of a land leasing offer at Tetouan Park under the partnership\nagreement related to land mobilization within the industrial and logistics park\nTETOUAN PARK signed on June 10, 2022: 9 industrial lots.\"\n\nTotal surface Valid industrial Investment Long-term\narea projects amount employment\n8 ha 8 350 MMAD 1000\n\nThe start of the commissioning of the Tanja Balia economic activities zone: 117\npremises allocated.\n\nwww.investangier.com\n\nLoukkos Agropole: 150 ha; global cost 457 MDH; 47 companies in process of set up; 8,000 long-term jobs.\nTetouan Park land leasing offer: 8 ha; 8 valid industrial projects; investment amount 350 MMAD; 1,000 long-term jobs.\nTanja Balia economic activities zone: 117 premises allocated.",
          "source_spans": [
            {
              "page": 9,
              "text": "= Allocation of plots at the first phase (SO hectares) of the Loukkos Agropole\nin Larache.\n\n—\n\na Poh = @Fnideq\n2 | \\~ Tanger @\n(@ Maiq\nSurface area Global Tetouan\nat term cost .\nAssileh (@)\n150 ha 457 MDH aiecsing\nCompanies in Long-term abgrepote\nprocess of set up employment Ouszza0e\n47 8000\n\nm Launch of a land leasing offer at Tetouan Park under the partnership\nagreement related to land mobilization within the industrial and logistics park\nTETOUAN PARK signed on June 10, 2022: 9 industrial lots.\"\n\nTotal surface Valid industrial Investment Long-term\narea projects amount employment\n8 ha 8 350 MMAD 1000\n\nThe start of the commissioning of the Tanja Balia economic activities zone: 117\npremises allocated.\n\nwww.investangier.com\n\nLoukkos Agropole: 150 ha; global cost 457 MDH; 47 companies in process of set up; 8,000 long-term jobs.\nTetouan Park land leasing offer: 8 ha; 8 valid industrial projects; investment amount 350 MMAD; 1,000 long-term jobs.\nTanja Balia economic activities zone: 117 premises allocated."
            }
          ],
          "dense_score": 0.83712626,
          "ranking_score": 0.84212626,
          "expanded_from_sibling": false,
          "retrieval_chunk_index": 0,
          "retrieval_chunk_count": 1,
          "temporal_scope": {
            "primary_year": null,
            "years_mentioned": [
              2022
            ],
            "reference_period": {
              "type": null,
              "year": null,
              "semester": null,
              "quarter": null,
              "start_date": null,
              "end_date": null
            }
          }
        },
        {
          "evidence_id": "E2",
          "retrieval_chunk_id": "eng_presentation_cri_tta_vf_semantic_027__r001a",
          "parent_semantic_chunk_id": "eng_presentation_cri_tta_vf_semantic_027",
          "document_id": "eng_presentation_cri_tta_vf",
          "document_family_id": "cri_presentation",
          "filename": "ENG_Presentation_CRI_TTA.json",
          "document_title": "Presentation of the Regional Investment Center",
          "language": "en",
          "topic_id": "industrial_ecosystem",
          "content_type": "statistics",
          "semantic_tags": [
            "industrial_ecosystem",
            "automotive_industry",
            "logistics",
            "renewable_energy",
            "agri_food",
            "offshoring",
            "infrastructure",
            "regional_indicators"
          ],
          "heading_path": [
            "Industrial ecosystem"
          ],
          "page_start": 37,
          "page_end": 37,
          "source_pages": [
            37
          ],
          "text": "Sere aeirt seca Once you are here, you are everywhere! 4 fee,\nSala ‘mares = SE\n° e e °\nCompetitive Varied land offer aimed at productive investment\n& multisectoral ——=— Legend\nhosting platforms —\nic) 2\nf Fahs-Anjra = (2) Fishing port\n23 Operational economic | ZIGTENAYA a a > A FNIDEG | eer\nA and industrial zones 2 Commercial zones 2 Tanger a gaan Fridoq platform TS tonger mea port\ncovering an area Zilighogha, a ae, e oo 8 iw\nof 150 ha asjer LEON ar\nNat a oe | a i [) zMartit\nS »} Tetouan Shor\n+3900 1 Agro-pole covering sesaeex : ange DUAN a\nha an area of 150 ha mere i pap omegenrns\noun |\nZAE Assilah~_ AM\n4 industrial acceleration 1 Offshoring zone 2 ie) f\nzones covering an area (P21) covering 20 ha [ LARACHE F@ Bd vecua | &\nof 2,500 ha ZHostal As\n8 Muttisectoral industrial 5 Zones in the Leracne Aare >, moe\nzones covering an FF process of being di\narea of 700 ha developed 2\n6 Economic activity\nzones covering an area of 53 ha 1\napproximately 160 ha\n1 Free logistics zone\ncovering ee ~400 millon MaD\nof 250ha",
          "source_spans": [
            {
              "page": 37,
              "text": "Sere aeirt seca Once you are here, you are everywhere! 4 fee,\nSala ‘mares = SE\n° e e °\nCompetitive Varied land offer aimed at productive investment\n& multisectoral ——=— Legend\nhosting platforms —\nic) 2\nf Fahs-Anjra = (2) Fishing port\n23 Operational economic | ZIGTENAYA a a > A FNIDEG | eer\nA and industrial zones 2 Commercial zones 2 Tanger a gaan Fridoq platform TS tonger mea port\ncovering an area Zilighogha, a ae, e oo 8 iw\nof 150 ha asjer LEON ar\nNat a oe | a i [) zMartit\nS »} Tetouan Shor\n+3900 1 Agro-pole covering sesaeex : ange DUAN a\nha an area of 150 ha mere i pap omegenrns\noun |\nZAE Assilah~_ AM\n4 industrial acceleration 1 Offshoring zone 2 ie) f\nzones covering an area (P21) covering 20 ha [ LARACHE F@ Bd vecua | &\nof 2,500 ha ZHostal As\n8 Muttisectoral industrial 5 Zones in the Leracne Aare >, moe\nzones covering an FF process of being di\narea of 700 ha developed 2\n6 Economic activity\nzones covering an area of 53 ha 1\napproximately 160 ha\n1 Free logistics zone\ncovering ee ~400 millon MaD\nof 250ha"
            }
          ],
          "dense_score": 0.8261782,
          "ranking_score": 0.8311782,
          "expanded_from_sibling": false,
          "retrieval_chunk_index": 0,
          "retrieval_chunk_count": 2,
          "temporal_scope": {
            "primary_year": null,
            "years_mentioned": [
              2017
            ],
            "reference_period": {
              "type": null,
              "year": null,
              "semester": null,
              "quarter": null,
              "start_date": null,
              "end_date": null
            }
          }
        },
        {
          "evidence_id": "E3",
          "retrieval_chunk_id": "investors_guide_territorial_opportunities_en_chunk_0005__r002c",
          "parent_semantic_chunk_id": "investors_guide_territorial_opportunities_en_chunk_0005",
          "document_id": "investors_guide_territorial_opportunities_en",
          "document_family_id": "investors_guide_territorial_opportunities",
          "filename": "Investors_Guide_territorial_opportunities_EN.json",
          "document_title": "Investors Guide to Territorial Opportunities",
          "language": "en",
          "topic_id": "investment_opportunity",
          "content_type": "investment_opportunity",
          "semantic_tags": [
            "agri_food",
            "agri_food_red_fruit_processing",
            "investment_opportunity",
            "larache"
          ],
          "heading_path": [
            "Investors Guide to Territorial Opportunities",
            "Industrial unit for red fruit processing"
          ],
          "page_start": 27,
          "page_end": 27,
          "source_pages": [
            27
          ],
          "text": "guidance, insurance and social coverage).",
          "source_spans": [
            {
              "page": 27,
              "text": "guidance, insurance and social coverage)."
            }
          ],
          "dense_score": 0.81237185,
          "ranking_score": 0.81737185,
          "expanded_from_sibling": false,
          "retrieval_chunk_index": 4,
          "retrieval_chunk_count": 7,
          "temporal_scope": {
            "primary_year": null,
            "years_mentioned": [
              2013,
              2014,
              2015,
              2019,
              2020
            ],
            "reference_period": {
              "type": null,
              "year": null,
              "semester": null,
              "quarter": null,
              "start_date": null,
              "end_date": null
            }
          }
        },
        {
          "evidence_id": "E4",
          "retrieval_chunk_id": "investors_guide_territorial_opportunities_en_chunk_0002__r003",
          "parent_semantic_chunk_id": "investors_guide_territorial_opportunities_en_chunk_0002",
          "document_id": "investors_guide_territorial_opportunities_en",
          "document_family_id": "investors_guide_territorial_opportunities",
          "filename": "Investors_Guide_territorial_opportunities_EN.json",
          "document_title": "Investors Guide to Territorial Opportunities",
          "language": "en",
          "topic_id": "investment_opportunity",
          "content_type": "investment_opportunity",
          "semantic_tags": [
            "agri_food",
            "agri_food_flour_mill",
            "investment_opportunity",
            "ouezzane"
          ],
          "heading_path": [
            "Investors Guide to Territorial Opportunities",
            "Industrial flour mill"
          ],
          "page_start": 18,
          "page_end": 18,
          "source_pages": [
            18
          ],
          "text": "HEXXEDE SIEISE 1 SOJoXo\nCo MB OzE?\n\nINVESTAMGIER CENTRE RÉGIONAL D'INVESTISSEMENT\n\ndamena da rca ls ANGER TÉTOUAN AL HOCEIMA",
          "source_spans": [
            {
              "page": 18,
              "text": "HEXXEDE SIEISE 1 SOJoXo\nCo MB OzE?\n\nINVESTAMGIER CENTRE RÉGIONAL D'INVESTISSEMENT\n\ndamena da rca ls ANGER TÉTOUAN AL HOCEIMA"
            }
          ],
          "dense_score": 0.8104334,
          "ranking_score": 0.8154334,
          "expanded_from_sibling": false,
          "retrieval_chunk_index": 6,
          "retrieval_chunk_count": 7,
          "temporal_scope": {
            "primary_year": null,
            "years_mentioned": [
              1987,
              2013,
              2018,
              2020,
              2021,
              2022,
              2058
            ],
            "reference_period": {
              "type": null,
              "year": null,
              "semester": null,
              "quarter": null,
              "start_date": null,
              "end_date": null
            }
          }
        },
        {
          "evidence_id": "E5",
          "retrieval_chunk_id": "eng_presentation_cri_tta_vf_semantic_022__r001",
          "parent_semantic_chunk_id": "eng_presentation_cri_tta_vf_semantic_022",
          "document_id": "eng_presentation_cri_tta_vf",
          "document_family_id": "cri_presentation",
          "filename": "ENG_Presentation_CRI_TTA.json",
          "document_title": "Presentation of the Regional Investment Center",
          "language": "en",
          "topic_id": "infrastructure",
          "content_type": "statistics",
          "semantic_tags": [
            "infrastructure",
            "regional_indicators"
          ],
          "heading_path": [
            "Infrastructure and logistics"
          ],
          "page_start": 30,
          "page_end": 30,
          "source_pages": [
            30
          ],
          "text": "Engine of the regional economy, in continuous development\n© SAU: 730,000 ha © 18 fishing ports & landing @ 2 identified areas:\n© 80% of the national @ Total area: 795 ha, of which\nagricultural added value“ (2% of the national tonnage)\nWith a value of 722 million MAD\n© 34 million workdays (75% of the national value) ®",
          "source_spans": [
            {
              "page": 30,
              "text": "Engine of the regional economy, in continuous development\n© SAU: 730,000 ha © 18 fishing ports & landing @ 2 identified areas:\n© 80% of the national @ Total area: 795 ha, of which\nagricultural added value“ (2% of the national tonnage)\nWith a value of 722 million MAD\n© 34 million workdays (75% of the national value) ®"
            }
          ],
          "dense_score": 0.81035864,
          "ranking_score": 0.81535864,
          "expanded_from_sibling": false,
          "retrieval_chunk_index": 0,
          "retrieval_chunk_count": 1,
          "temporal_scope": {
            "primary_year": null,
            "years_mentioned": [],
            "reference_period": {
              "type": null,
              "year": null,
              "semester": null,
              "quarter": null,
              "start_date": null,
              "end_date": null
            }
          }
        }
      ],
      "status": "review_required"
    },
    "Q032": {
      "query": {
        "query_id": "Q032",
        "language": "ar",
        "question": "ما هي مؤشرات مناخ الاستثمار ورضا المستثمرين؟",
        "category": "statistics",
        "explicit_year": null,
        "expected_topics": [
          "business_climate",
          "investor_satisfaction"
        ],
        "expected_document_families": [
          "investment_climate_indicators"
        ],
        "acceptable_languages": [
          "ar",
          "fr",
          "en",
          "es"
        ]
      },
      "baseline_v1": [
        {
          "chunk_id": "ar_pr_sentation_cri_tta_vf_p41_c1",
          "document_id": "ar_pr_sentation_cri_tta_vf",
          "document_family_id": "cri_presentation",
          "filename": "AR_Présentation CRI TTA VF.pdf",
          "language": "ar",
          "page": 41,
          "page_start": 41,
          "page_end": 41,
          "source_pages": [
            41
          ],
          "dense_score": 0.839326,
          "ranking_score": 0.839326,
          "retrieval_score": 0.839326,
          "final_score": 0.839326,
          "text": "0\n\nا ع\nالا ع 1 ا\nدقاف <>7 -070000 7\nإن هناء فا كل مكان 58 روه سلما وانشهية ولشر ع الساسات التموطيخ\nدلاء 0\n-\n\n100 ا ا\n\n89 من الشركات راضية عن استقرارها\n2200 يدهة مللجة_'تطواق الكسيفة\n\nأهم حوافز الاستثمار بالجهة اتجاهات وآفاق نمو الأعمال فى المنطقة\n\nجودة الحياة و/229 من المشاركين يعتبرون الوضع الحالي لشركاتهم مرضيًا\n\nم95 مع وجود آفاق متفائلة للنمو على جميع المستويات\n\nالموقع الجغرافي\nا\nومرافق استقبال متطورة0 بنية تحتية؟ض ل\n\nتوفر المهارات؟آ؟آ 0\n21111606061012\n\n00111 |110101010101000 1111 1أ001ظغظك\n\n© توجه صاعد © مستقر © في اتجاه الإنخفاض\n\nالمصدر: استطلاع أي أجرته مؤسسة التمويل الدولية ومجموعة البنك الدولي في عام 2025"
        },
        {
          "chunk_id": "akhbar_al_moustatmir_news_p1_c1",
          "document_id": "akhbar_al_moustatmir_news",
          "document_family_id": "manar_al_moustatmir_news_2023",
          "filename": "Akhbar Al Moustatmir News VA compress.pdf",
          "language": "ar",
          "page": 1,
          "page_start": 1,
          "page_end": 1,
          "source_pages": [
            1
          ],
          "dense_score": 0.8269385,
          "ranking_score": 0.8269385,
          "retrieval_score": 0.8269385,
          "final_score": 0.8269385,
          "text": "حقائق\nعلامات\nبارومتر\nالإستثمار \nقضية\nالسياحة الخاصة\nLES CHIFFRES CLÉS DE\nL'INVESTISSEMENT\nET DE L'ENTREPRENEURIAT\nde l’année 2023\n1\nأخبـار\nمنارالمستثمر\nرقم\n2024 لسنة\nمؤشرات الاستثمار\nوريادة الأعمال\nبارزة\nالاستثمار\nمقياس\nخاص بالسياحة\nملف\nأحداث"
        },
        {
          "chunk_id": "ar_pr_sentation_cri_tta_vf_p52_c1",
          "document_id": "ar_pr_sentation_cri_tta_vf",
          "document_family_id": "cri_presentation",
          "filename": "AR_Présentation CRI TTA VF.pdf",
          "language": "ar",
          "page": 52,
          "page_start": 52,
          "page_end": 52,
          "source_pages": [
            52
          ],
          "dense_score": 0.8177085,
          "ranking_score": 0.8177085,
          "retrieval_score": 0.8177085,
          "final_score": 0.8177085,
          "text": "حي ال ا د\nوفيس الهسو للاستتبار 5 50 ثزاء كوه 8\nم ا 5 إن كنتم هناء فالتم مي كل مكان 58 لجس 1 اساي\n\nلقع تنا ا لم ع ا ل\n\nميثاق الاستثمار المحور الأول: نظام دعم أساسى\n\nالجديد (0/11)\n\nمنحة قطاعية لتحفيز الاستثمار فى القطاعات ذات الأولوية\n\n9 النقل و التجهيز السياحة والخدمات 2\nع ا\nمكلك\nْ تربية الأحياء المائية 5 ما\n0-0 الطاقات المتجددة لذ\n3 6 - 2"
        },
        {
          "chunk_id": "eng_indicateurs_climat_dinvestissement_p2_c1",
          "document_id": "eng_indicateurs_climat_dinvestissement",
          "document_family_id": "investment_climate_indicators",
          "filename": "ENG_Indicateurs-climat-dinvestissement.pdf",
          "language": "en",
          "page": 2,
          "page_start": 2,
          "page_end": 2,
          "source_pages": [
            2
          ],
          "dense_score": 0.8152964,
          "ranking_score": 0.8152964,
          "retrieval_score": 0.8152964,
          "final_score": 0.8152964,
          "text": "SUMMARY\n\nContext — 1\nSurveyed Profiles — 2\nMain results — 3\n\nAxis 1: Investors' Perception of the Business Climate in the Region — 6\n• Reasons for Establishment in the TTA Region — 8\n• Trends and Growth Perspectives of Businesses in the Region — 10\n\nAxis 2: Level of satisfaction and interaction regarding the services provided by CRI TTA — 12\n\nAxis 3: Stakeholders' Perspective on the Business Climate in the Region — 18\n• Perception of the Business Climate — 19\n• Performance in Environmental & Energy Efficiency Matters — 22\n• Expectations Regarding the CRI TTA — 25\n\nwww.investangier.com"
        },
        {
          "chunk_id": "akhbar_al_moustatmir_news_p6_c1",
          "document_id": "akhbar_al_moustatmir_news",
          "document_family_id": "manar_al_moustatmir_news_2023",
          "filename": "Akhbar Al Moustatmir News VA compress.pdf",
          "language": "ar",
          "page": 6,
          "page_start": 6,
          "page_end": 6,
          "source_pages": [
            6
          ],
          "dense_score": 0.81082493,
          "ranking_score": 0.81082493,
          "retrieval_score": 0.81082493,
          "final_score": 0.81082493,
          "text": "فهرس\nwww.investangier.com\nأحداث بارزة\nملف خاص بالسياحة\nمقياس الاستثمار والمقاولات بجهة طنجة تطوان أصيلة\nعرض الجهوي تقرير عن أنشطة الترويج\nملف تربية الأحياء المائية\nشهادات: فاعلو النظام البيئي لتربية الأحياء البحرية\nالدلائل والكتيبات\nلقد وضعوا فينا ثقتهم\n01\n05\n17\n24\n25\n27\n34\n35"
        }
      ],
      "baseline_v2": [
        {
          "retrieval_chunk_id": "akhbar_al_moustatmir_news_phase3f_0001__r001",
          "document_id": "akhbar_al_moustatmir_news",
          "document_family_id": "manar_al_moustatmir_news_2023",
          "filename": "Akhbar_Al_Moustatmir_News.json",
          "language": "ar",
          "topic_id": "investment_news",
          "content_type": "statistics",
          "page_start": 1,
          "page_end": 1,
          "source_pages": [
            1
          ],
          "dense_score": 0.83981377,
          "ranking_score": 0.84481377,
          "text": "حقائق\nعلامات\nبارومتر\nالإستثمار \nقضية\nالسياحة الخاصة\nLES CHIFFRES CLÉS DE\nL'INVESTISSEMENT\nET DE L'ENTREPRENEURIAT\nde l’année 2023\n1\nأخبـار\nمنارالمستثمر\nرقم\n2024 لسنة\nمؤشرات الاستثمار\nوريادة الأعمال\nبارزة\nالاستثمار\nمقياس\nخاص بالسياحة\nملف\nأحداث"
        },
        {
          "retrieval_chunk_id": "ar_pr_sentation_cri_tta_vf_semantic_024__r001",
          "document_id": "ar_pr_sentation_cri_tta_vf",
          "document_family_id": "cri_presentation",
          "filename": "AR_Presentation_CRI_TTA.json",
          "language": "ar",
          "topic_id": "regional_positioning",
          "content_type": "narrative",
          "page_start": 41,
          "page_end": 41,
          "source_pages": [
            41
          ],
          "dense_score": 0.83762527,
          "ranking_score": 0.84262527,
          "text": "0\n\nا ع\nالا ع 1 ا\nدقاف <>7 -070000 7\nإن هناء فا كل مكان 58 روه سلما وانشهية ولشر ع الساسات التموطيخ\nدلاء 0\n-\n\n100 ا ا\n\n89 من الشركات راضية عن استقرارها\n2200 يدهة مللجة_'تطواق الكسيفة\n\nأهم حوافز الاستثمار بالجهة اتجاهات وآفاق نمو الأعمال فى المنطقة\n\nجودة الحياة و/229 من المشاركين يعتبرون الوضع الحالي لشركاتهم مرضيًا\n\nم95 مع وجود آفاق متفائلة للنمو على جميع المستويات\n\nالموقع الجغرافي\nا\nومرافق استقبال متطورة0 بنية تحتية؟ض ل\n\nتوفر المهارات؟آ؟آ 0\n21111606061012\n\n00111 |110101010101000 1111 1أ001ظغظك\n\n© توجه صاعد © مستقر © في اتجاه الإنخفاض\n\nالمصدر: استطلاع أي أجرته مؤسسة التمويل الدولية ومجموعة البنك الدولي في عام 2025"
        },
        {
          "retrieval_chunk_id": "chiffres_cles_crui_1er_semestre_2024_arabe_chunk_003__r001",
          "document_id": "chiffres_cles_crui_1er_semestre_2024_arabe",
          "document_family_id": "crui_key_figures_2024_h1",
          "filename": "Chiffres_cles_CRUI_1er_semestre_2024_Arabe.json",
          "language": "ar",
          "topic_id": "sector_distribution",
          "content_type": "statistics",
          "page_start": 3,
          "page_end": 3,
          "source_pages": [
            3
          ],
          "dense_score": 0.81229025,
          "ranking_score": 0.81729025,
          "text": "إن كنتم هنا، فأنتم في كل مكان\n\nتوزيع حجم الاستثمارات حسب القطاع\n\nيواصل القطاع الصناعي نموه الاستثنائي بأكثر من نصف الاستثمارات التي تمت المصادقة عليها\n\nإجمالي الاستثمارات: 40,76 مليار درهم\n\nالصناعة: 54%\nالسياحة: 22%\nالطاقة والمناجم: 15%\nقطاعات أخرى: 6%\nالتجارة: 2%\nالبناء والأشغال العامة: 1%\n\nwww.investangier.com"
        },
        {
          "retrieval_chunk_id": "akhbar_al_moustatmir_news_phase3f_0003__r001",
          "document_id": "akhbar_al_moustatmir_news",
          "document_family_id": "manar_al_moustatmir_news_2023",
          "filename": "Akhbar_Al_Moustatmir_News.json",
          "language": "ar",
          "topic_id": "investment_guide",
          "content_type": "narrative",
          "page_start": 6,
          "page_end": 6,
          "source_pages": [
            6
          ],
          "dense_score": 0.8118213,
          "ranking_score": 0.8168213,
          "text": "فهرس\nwww.investangier.com\nأحداث بارزة\nملف خاص بالسياحة\nمقياس الاستثمار والمقاولات بجهة طنجة تطوان أصيلة\nعرض الجهوي تقرير عن أنشطة الترويج\nملف تربية الأحياء المائية\nشهادات: فاعلو النظام البيئي لتربية الأحياء البحرية\nالدلائل والكتيبات\nلقد وضعوا فينا ثقتهم\n01\n05\n17\n24\n25\n27\n34\n35"
        },
        {
          "retrieval_chunk_id": "ar_pr_sentation_cri_tta_vf_semantic_033__r001",
          "document_id": "ar_pr_sentation_cri_tta_vf",
          "document_family_id": "cri_presentation",
          "filename": "AR_Presentation_CRI_TTA.json",
          "language": "ar",
          "topic_id": "regional_positioning",
          "content_type": "narrative",
          "page_start": 53,
          "page_end": 54,
          "source_pages": [
            53,
            54
          ],
          "dense_score": 0.80822104,
          "ranking_score": 0.81322104,
          "text": "و ا عد ف سد\n\nا 01 م فس 0 202010 8\nلو ا ا\n\nميثاق الاستئمار المحور الثاني: نظام خاص يطبق على مشاريع الاستثمار ذات الطابع الاستراتيجي\n\nالجديد (1/11)\n\nمشاريع يبلغ حجم استثمارها 2 مليار درهم أو أكثر وتستوفي على الأقل أحد الشروط التالية\n\n» أن يكون لها تأثير كبير على عدد مناصب الشغل المباشرة أو غير المباشرة التى سيتم إحداثها؛\n\n* أن يكون لها أثر ملحوظ على الإشعاع الاقتصادي والتموقع الاستراتيجي للمغرب على المستوى الجهوي أو القاري أو الدولي؛\n* أن تساهم فى تطوير المنظومة القطاعية أو النشاط القطاعى؛\n\n* أن تُساهم بشكل كبير في تطوير واعتماد التكنولوجيات الجديدة\n\nالمملكة المفربية اليس العومة»\n0 لخعن “د وويد\nل ان له\nٍ\n\n0 6 1 “6\nلي ل\n\nإن كنتم هناء فأنتم في كل مكان؟؟ بيك\n\n٠ إعفاء من الضريبة على الشركات خلال السنوات الخمس الأولى\n٠ تخفيض نسبة الضريبة على الشركات إلى 9620 خلال العشرين سنة التالية\n٠» إعفاء من الضريبة على القيمة المضافة مع الحق في الخصم\n* إعفاء من الضريبة على الأرباج والتوزيعات المشابهة للحصص\n\n٠» إعفاء من الرسوم الجمركية"
        }
      ],
      "experimental_v2": [
        {
          "evidence_id": "E1",
          "retrieval_chunk_id": "akhbar_al_moustatmir_news_phase3f_0001__r001",
          "parent_semantic_chunk_id": "akhbar_al_moustatmir_news_phase3f_0001",
          "document_id": "akhbar_al_moustatmir_news",
          "document_family_id": "manar_al_moustatmir_news_2023",
          "filename": "Akhbar_Al_Moustatmir_News.json",
          "document_title": "أخبار الاستثمار وريادة الأعمال",
          "language": "ar",
          "topic_id": "investment_news",
          "content_type": "statistics",
          "semantic_tags": [
            "investment_news",
            "news_edition_2023",
            "regional_statistics"
          ],
          "heading_path": [
            "مؤشرات الاستثمار وريادة الأعمال لسنة 2023"
          ],
          "page_start": 1,
          "page_end": 1,
          "source_pages": [
            1
          ],
          "text": "حقائق\nعلامات\nبارومتر\nالإستثمار \nقضية\nالسياحة الخاصة\nLES CHIFFRES CLÉS DE\nL'INVESTISSEMENT\nET DE L'ENTREPRENEURIAT\nde l’année 2023\n1\nأخبـار\nمنارالمستثمر\nرقم\n2024 لسنة\nمؤشرات الاستثمار\nوريادة الأعمال\nبارزة\nالاستثمار\nمقياس\nخاص بالسياحة\nملف\nأحداث",
          "source_spans": [
            {
              "page": 1,
              "text": "حقائق\nعلامات\nبارومتر\nالإستثمار \nقضية\nالسياحة الخاصة\nLES CHIFFRES CLÉS DE\nL'INVESTISSEMENT\nET DE L'ENTREPRENEURIAT\nde l’année 2023\n1\nأخبـار\nمنارالمستثمر\nرقم\n2024 لسنة\nمؤشرات الاستثمار\nوريادة الأعمال\nبارزة\nالاستثمار\nمقياس\nخاص بالسياحة\nملف\nأحداث"
            }
          ],
          "dense_score": 0.83981377,
          "ranking_score": 0.84481377,
          "expanded_from_sibling": false,
          "retrieval_chunk_index": 0,
          "retrieval_chunk_count": 1,
          "temporal_scope": {
            "primary_year": null,
            "years_mentioned": [
              2023,
              2024
            ],
            "reference_period": {
              "type": null,
              "year": null,
              "semester": null,
              "quarter": null,
              "start_date": null,
              "end_date": null
            }
          }
        },
        {
          "evidence_id": "E2",
          "retrieval_chunk_id": "ar_pr_sentation_cri_tta_vf_semantic_024__r001",
          "parent_semantic_chunk_id": "ar_pr_sentation_cri_tta_vf_semantic_024",
          "document_id": "ar_pr_sentation_cri_tta_vf",
          "document_family_id": "cri_presentation",
          "filename": "AR_Presentation_CRI_TTA.json",
          "document_title": "تقديم المركز الجهوي للاستثمار",
          "language": "ar",
          "topic_id": "regional_positioning",
          "content_type": "narrative",
          "semantic_tags": [
            "regional_positioning"
          ],
          "heading_path": [
            "التموقع الجهوي"
          ],
          "page_start": 41,
          "page_end": 41,
          "source_pages": [
            41
          ],
          "text": "0\n\nا ع\nالا ع 1 ا\nدقاف <>7 -070000 7\nإن هناء فا كل مكان 58 روه سلما وانشهية ولشر ع الساسات التموطيخ\nدلاء 0\n-\n\n100 ا ا\n\n89 من الشركات راضية عن استقرارها\n2200 يدهة مللجة_'تطواق الكسيفة\n\nأهم حوافز الاستثمار بالجهة اتجاهات وآفاق نمو الأعمال فى المنطقة\n\nجودة الحياة و/229 من المشاركين يعتبرون الوضع الحالي لشركاتهم مرضيًا\n\nم95 مع وجود آفاق متفائلة للنمو على جميع المستويات\n\nالموقع الجغرافي\nا\nومرافق استقبال متطورة0 بنية تحتية؟ض ل\n\nتوفر المهارات؟آ؟آ 0\n21111606061012\n\n00111 |110101010101000 1111 1أ001ظغظك\n\n© توجه صاعد © مستقر © في اتجاه الإنخفاض\n\nالمصدر: استطلاع أي أجرته مؤسسة التمويل الدولية ومجموعة البنك الدولي في عام 2025",
          "source_spans": [
            {
              "page": 41,
              "text": "0\n\nا ع\nالا ع 1 ا\nدقاف <>7 -070000 7\nإن هناء فا كل مكان 58 روه سلما وانشهية ولشر ع الساسات التموطيخ\nدلاء 0\n-\n\n100 ا ا\n\n89 من الشركات راضية عن استقرارها\n2200 يدهة مللجة_'تطواق الكسيفة\n\nأهم حوافز الاستثمار بالجهة اتجاهات وآفاق نمو الأعمال فى المنطقة\n\nجودة الحياة و/229 من المشاركين يعتبرون الوضع الحالي لشركاتهم مرضيًا\n\nم95 مع وجود آفاق متفائلة للنمو على جميع المستويات\n\nالموقع الجغرافي\nا\nومرافق استقبال متطورة0 بنية تحتية؟ض ل\n\nتوفر المهارات؟آ؟آ 0\n21111606061012\n\n00111 |110101010101000 1111 1أ001ظغظك\n\n© توجه صاعد © مستقر © في اتجاه الإنخفاض\n\nالمصدر: استطلاع أي أجرته مؤسسة التمويل الدولية ومجموعة البنك الدولي في عام 2025"
            }
          ],
          "dense_score": 0.83762527,
          "ranking_score": 0.84262527,
          "expanded_from_sibling": false,
          "retrieval_chunk_index": 0,
          "retrieval_chunk_count": 1,
          "temporal_scope": {
            "primary_year": null,
            "years_mentioned": [
              2025
            ],
            "reference_period": {
              "type": null,
              "year": null,
              "semester": null,
              "quarter": null,
              "start_date": null,
              "end_date": null
            }
          }
        },
        {
          "evidence_id": "E3",
          "retrieval_chunk_id": "chiffres_cles_crui_1er_semestre_2024_arabe_chunk_003__r001",
          "parent_semantic_chunk_id": "chiffres_cles_crui_1er_semestre_2024_arabe_chunk_003",
          "document_id": "chiffres_cles_crui_1er_semestre_2024_arabe",
          "document_family_id": "crui_key_figures_2024_h1",
          "filename": "Chiffres_cles_CRUI_1er_semestre_2024_Arabe.json",
          "document_title": "المؤشرات الرئيسية والإحصائيات",
          "language": "ar",
          "topic_id": "sector_distribution",
          "content_type": "statistics",
          "semantic_tags": [
            "sector_distribution",
            "investment_amount"
          ],
          "heading_path": [
            "إن كنتم هنا، فأنتم في كل مكان"
          ],
          "page_start": 3,
          "page_end": 3,
          "source_pages": [
            3
          ],
          "text": "إن كنتم هنا، فأنتم في كل مكان\n\nتوزيع حجم الاستثمارات حسب القطاع\n\nيواصل القطاع الصناعي نموه الاستثنائي بأكثر من نصف الاستثمارات التي تمت المصادقة عليها\n\nإجمالي الاستثمارات: 40,76 مليار درهم\n\nالصناعة: 54%\nالسياحة: 22%\nالطاقة والمناجم: 15%\nقطاعات أخرى: 6%\nالتجارة: 2%\nالبناء والأشغال العامة: 1%\n\nwww.investangier.com",
          "source_spans": [
            {
              "page": 3,
              "text": "إن كنتم هنا، فأنتم في كل مكان\n\nتوزيع حجم الاستثمارات حسب القطاع\n\nيواصل القطاع الصناعي نموه الاستثنائي بأكثر من نصف الاستثمارات التي تمت المصادقة عليها\n\nإجمالي الاستثمارات: 40,76 مليار درهم\n\nالصناعة: 54%\nالسياحة: 22%\nالطاقة والمناجم: 15%\nقطاعات أخرى: 6%\nالتجارة: 2%\nالبناء والأشغال العامة: 1%\n\nwww.investangier.com"
            }
          ],
          "dense_score": 0.81229025,
          "ranking_score": 0.81729025,
          "expanded_from_sibling": false,
          "retrieval_chunk_index": 0,
          "retrieval_chunk_count": 1,
          "temporal_scope": {
            "primary_year": 2024,
            "years_mentioned": [],
            "reference_period": {
              "type": "semester",
              "year": 2024,
              "semester": 1,
              "quarter": null,
              "start_date": null,
              "end_date": null
            }
          }
        },
        {
          "evidence_id": "E4",
          "retrieval_chunk_id": "akhbar_al_moustatmir_news_phase3f_0003__r001",
          "parent_semantic_chunk_id": "akhbar_al_moustatmir_news_phase3f_0003",
          "document_id": "akhbar_al_moustatmir_news",
          "document_family_id": "manar_al_moustatmir_news_2023",
          "filename": "Akhbar_Al_Moustatmir_News.json",
          "document_title": "أخبار الاستثمار وريادة الأعمال",
          "language": "ar",
          "topic_id": "investment_guide",
          "content_type": "narrative",
          "semantic_tags": [
            "investment_guide",
            "investment_news"
          ],
          "heading_path": [
            "الفهرس"
          ],
          "page_start": 6,
          "page_end": 6,
          "source_pages": [
            6
          ],
          "text": "فهرس\nwww.investangier.com\nأحداث بارزة\nملف خاص بالسياحة\nمقياس الاستثمار والمقاولات بجهة طنجة تطوان أصيلة\nعرض الجهوي تقرير عن أنشطة الترويج\nملف تربية الأحياء المائية\nشهادات: فاعلو النظام البيئي لتربية الأحياء البحرية\nالدلائل والكتيبات\nلقد وضعوا فينا ثقتهم\n01\n05\n17\n24\n25\n27\n34\n35",
          "source_spans": [
            {
              "page": 6,
              "text": "فهرس\nwww.investangier.com\nأحداث بارزة\nملف خاص بالسياحة\nمقياس الاستثمار والمقاولات بجهة طنجة تطوان أصيلة\nعرض الجهوي تقرير عن أنشطة الترويج\nملف تربية الأحياء المائية\nشهادات: فاعلو النظام البيئي لتربية الأحياء البحرية\nالدلائل والكتيبات\nلقد وضعوا فينا ثقتهم\n01\n05\n17\n24\n25\n27\n34\n35"
            }
          ],
          "dense_score": 0.8118213,
          "ranking_score": 0.8168213,
          "expanded_from_sibling": false,
          "retrieval_chunk_index": 0,
          "retrieval_chunk_count": 1,
          "temporal_scope": {
            "primary_year": null,
            "years_mentioned": [],
            "reference_period": {
              "type": null,
              "year": null,
              "semester": null,
              "quarter": null,
              "start_date": null,
              "end_date": null
            }
          }
        },
        {
          "evidence_id": "E5",
          "retrieval_chunk_id": "ar_pr_sentation_cri_tta_vf_semantic_033__r001",
          "parent_semantic_chunk_id": "ar_pr_sentation_cri_tta_vf_semantic_033",
          "document_id": "ar_pr_sentation_cri_tta_vf",
          "document_family_id": "cri_presentation",
          "filename": "AR_Presentation_CRI_TTA.json",
          "document_title": "تقديم المركز الجهوي للاستثمار",
          "language": "ar",
          "topic_id": "regional_positioning",
          "content_type": "narrative",
          "semantic_tags": [
            "regional_positioning"
          ],
          "heading_path": [
            "التموقع الجهوي"
          ],
          "page_start": 53,
          "page_end": 54,
          "source_pages": [
            53,
            54
          ],
          "text": "و ا عد ف سد\n\nا 01 م فس 0 202010 8\nلو ا ا\n\nميثاق الاستئمار المحور الثاني: نظام خاص يطبق على مشاريع الاستثمار ذات الطابع الاستراتيجي\n\nالجديد (1/11)\n\nمشاريع يبلغ حجم استثمارها 2 مليار درهم أو أكثر وتستوفي على الأقل أحد الشروط التالية\n\n» أن يكون لها تأثير كبير على عدد مناصب الشغل المباشرة أو غير المباشرة التى سيتم إحداثها؛\n\n* أن يكون لها أثر ملحوظ على الإشعاع الاقتصادي والتموقع الاستراتيجي للمغرب على المستوى الجهوي أو القاري أو الدولي؛\n* أن تساهم فى تطوير المنظومة القطاعية أو النشاط القطاعى؛\n\n* أن تُساهم بشكل كبير في تطوير واعتماد التكنولوجيات الجديدة\n\nالمملكة المفربية اليس العومة»\n0 لخعن “د وويد\nل ان له\nٍ\n\n0 6 1 “6\nلي ل\n\nإن كنتم هناء فأنتم في كل مكان؟؟ بيك\n\n٠ إعفاء من الضريبة على الشركات خلال السنوات الخمس الأولى\n٠ تخفيض نسبة الضريبة على الشركات إلى 9620 خلال العشرين سنة التالية\n٠» إعفاء من الضريبة على القيمة المضافة مع الحق في الخصم\n* إعفاء من الضريبة على الأرباج والتوزيعات المشابهة للحصص\n\n٠» إعفاء من الرسوم الجمركية",
          "source_spans": [
            {
              "page": 53,
              "text": "و ا عد ف سد\n\nا 01 م فس 0 202010 8\nلو ا ا\n\nميثاق الاستئمار المحور الثاني: نظام خاص يطبق على مشاريع الاستثمار ذات الطابع الاستراتيجي\n\nالجديد (1/11)\n\nمشاريع يبلغ حجم استثمارها 2 مليار درهم أو أكثر وتستوفي على الأقل أحد الشروط التالية\n\n» أن يكون لها تأثير كبير على عدد مناصب الشغل المباشرة أو غير المباشرة التى سيتم إحداثها؛\n\n* أن يكون لها أثر ملحوظ على الإشعاع الاقتصادي والتموقع الاستراتيجي للمغرب على المستوى الجهوي أو القاري أو الدولي؛\n* أن تساهم فى تطوير المنظومة القطاعية أو النشاط القطاعى؛\n\n* أن تُساهم بشكل كبير في تطوير واعتماد التكنولوجيات الجديدة"
            },
            {
              "page": 54,
              "text": "المملكة المفربية اليس العومة»\n0 لخعن “د وويد\nل ان له\nٍ\n\n0 6 1 “6\nلي ل\n\nإن كنتم هناء فأنتم في كل مكان؟؟ بيك\n\n٠ إعفاء من الضريبة على الشركات خلال السنوات الخمس الأولى\n٠ تخفيض نسبة الضريبة على الشركات إلى 9620 خلال العشرين سنة التالية\n٠» إعفاء من الضريبة على القيمة المضافة مع الحق في الخصم\n* إعفاء من الضريبة على الأرباج والتوزيعات المشابهة للحصص\n\n٠» إعفاء من الرسوم الجمركية"
            }
          ],
          "dense_score": 0.80822104,
          "ranking_score": 0.81322104,
          "expanded_from_sibling": false,
          "retrieval_chunk_index": 0,
          "retrieval_chunk_count": 1,
          "temporal_scope": {
            "primary_year": null,
            "years_mentioned": [],
            "reference_period": {
              "type": null,
              "year": null,
              "semester": null,
              "quarter": null,
              "start_date": null,
              "end_date": null
            }
          }
        }
      ],
      "status": "review_required"
    },
    "Q027": {
      "query": {
        "query_id": "Q027",
        "language": "ar",
        "question": "ما هي فرص الاستثمار في قطاع السياحة؟",
        "category": "investment_opportunity",
        "explicit_year": null,
        "expected_topics": [
          "investment_opportunity",
          "tourism"
        ],
        "expected_document_families": [
          "investors_guide_territorial_opportunities"
        ],
        "acceptable_languages": [
          "ar",
          "fr",
          "en"
        ]
      },
      "baseline_v1": [
        {
          "chunk_id": "chiffres_cles_crui_1er_semestre_2024_arabe_p4_c1",
          "document_id": "chiffres_cles_crui_1er_semestre_2024_arabe",
          "document_family_id": "crui_key_figures_2024_h1",
          "filename": "Chiffres clés CRUI 1er semestre 2024_Arabe.pdf",
          "language": "ar",
          "page": 4,
          "page_start": 4,
          "page_end": 4,
          "source_pages": [
            4
          ],
          "dense_score": 0.8362026,
          "ranking_score": 0.8362026,
          "retrieval_score": 0.8362026,
          "final_score": 0.8362026,
          "text": "إن كنتم هنا، فأنتم في كل مكان\n\nتشكل الصناعة القطاع الرائد في توفير فرص شغل على المدى المتوسط والبعيد، بحصة تقدر بـ 83%\n\nالصناعة: 83%\nالسياحة: 7%\nقطاعات أخرى: 10%\n\nwww.investangier.com"
        },
        {
          "chunk_id": "arabe_chiffres_cles_2025_p8_c1",
          "document_id": "arabe_chiffres_cles_2025",
          "document_family_id": "chiffres_cles_2025",
          "filename": "Arabe_ Chiffres clés 2025.pdf",
          "language": "ar",
          "page": 8,
          "page_start": 8,
          "page_end": 8,
          "source_pages": [
            8
          ],
          "dense_score": 0.8358096,
          "ranking_score": 0.8358096,
          "retrieval_score": 0.8358096,
          "final_score": 0.8358096,
          "text": "حصيلة اللجنة الجهوية الموحدة للاستثمار (5/6)\nدينامية قوية للاستثمار السياحي مدعومة برؤية واعدة\nلقد اختاروا الجهة سنة 2025\n\n7 مؤسسات مفتوحة سنة 2025\n+300 غرفة\n194 مليون درهم من الاستثمارات\n\n31 مؤسسة في طور الإنجاز\n2 036 غرفة إضافية\nمنها 1 220 غرفة من فئة 3 نجوم فأكثر\n4,8 مليار درهم من الاستثمارات المرتقبة\n\nالمؤسسات المفتوحة سنة 2025 / المؤسسات في طور الإنجاز في 2025:\nطنجة - أصيلة: 9 / 15 — 1 244 / 2 307 غرفة\nالعرائش: 1 — 60 غرفة\nوزان: 1 — 106 غرف\nالفحص أنجرة: 4 — 154 غرفة\nالمضيق - الفنيدق: 5 / 1 — 812 / 152 غرفة\nتطوان: 2 / 1 — 70 / 70 غرفة\nشفشاون: 1 / 1 — 64 / 20 غرفة\nالحسيمة: 1 — 42 غرفة\n\nwww.investangier.com\n08"
        },
        {
          "chunk_id": "akhbar_al_moustatmir_news_p26_c1",
          "document_id": "akhbar_al_moustatmir_news",
          "document_family_id": "manar_al_moustatmir_news_2023",
          "filename": "Akhbar Al Moustatmir News VA compress.pdf",
          "language": "ar",
          "page": 26,
          "page_start": 26,
          "page_end": 26,
          "source_pages": [
            26
          ],
          "dense_score": 0.8331109,
          "ranking_score": 0.8331109,
          "retrieval_score": 0.8331109,
          "final_score": 0.8331109,
          "text": "www.investangier.com\n20\n52\n36,6\n~73,4\n2021\n2022\n2023\n+41%\nالسنة\n~37 500\n~58 000\n~70 000\n2021\n2022\n2023\n+20,6%\n44\nمشروع\n9%\n20,5%\n13,7%\n56,8%\nالصناعة\nالسياحة\nالصناعات الغذائية\nالخدمات\nالتوزيع القطاعي\nحسب عدد المشاريع\nالتوزيع القطاعي\nحسب مبلغ الاستثمار\n18\nمليار\nدرهم54,8%\n37,7%\n3,3% 4,2%\n+10 200\nوظائف مستقرة متوقعة على المدى الطويل\nتطور مبالغ الاستثمار المعتمدة من\n2023-2021 CRUI\n()بمليارات الدراهم\nالسنة\nتطور عدد الوظائف المتوقعة من خلال المشاريع الاستثمارية المعتمدة\n2023-2021 CRUIمن قبل\nمشروع اتفاقية استثمار معCRUI\n44"
        },
        {
          "chunk_id": "chiffres_cles_crui_1er_semestre_2024_arabe_p3_c1",
          "document_id": "chiffres_cles_crui_1er_semestre_2024_arabe",
          "document_family_id": "crui_key_figures_2024_h1",
          "filename": "Chiffres clés CRUI 1er semestre 2024_Arabe.pdf",
          "language": "ar",
          "page": 3,
          "page_start": 3,
          "page_end": 3,
          "source_pages": [
            3
          ],
          "dense_score": 0.8323315,
          "ranking_score": 0.8323315,
          "retrieval_score": 0.8323315,
          "final_score": 0.8323315,
          "text": "إن كنتم هنا، فأنتم في كل مكان\n\nتوزيع حجم الاستثمارات حسب القطاع\n\nيواصل القطاع الصناعي نموه الاستثنائي بأكثر من نصف الاستثمارات التي تمت المصادقة عليها\n\nإجمالي الاستثمارات: 40,76 مليار درهم\n\nالصناعة: 54%\nالسياحة: 22%\nالطاقة والمناجم: 15%\nقطاعات أخرى: 6%\nالتجارة: 2%\nالبناء والأشغال العامة: 1%\n\nwww.investangier.com"
        },
        {
          "chunk_id": "ar_pr_sentation_cri_tta_vf_p23_c1",
          "document_id": "ar_pr_sentation_cri_tta_vf",
          "document_family_id": "cri_presentation",
          "filename": "AR_Présentation CRI TTA VF.pdf",
          "language": "ar",
          "page": 23,
          "page_start": 23,
          "page_end": 23,
          "source_pages": [
            23
          ],
          "dense_score": 0.82971925,
          "ranking_score": 0.82971925,
          "retrieval_score": 0.82971925,
          "final_score": 0.82971925,
          "text": "السياحة"
        }
      ],
      "baseline_v2": [
        {
          "retrieval_chunk_id": "chiffres_cles_crui_1er_semestre_2024_arabe_chunk_003__r001",
          "document_id": "chiffres_cles_crui_1er_semestre_2024_arabe",
          "document_family_id": "crui_key_figures_2024_h1",
          "filename": "Chiffres_cles_CRUI_1er_semestre_2024_Arabe.json",
          "language": "ar",
          "topic_id": "sector_distribution",
          "content_type": "statistics",
          "page_start": 3,
          "page_end": 3,
          "source_pages": [
            3
          ],
          "dense_score": 0.83912504,
          "ranking_score": 0.84412504,
          "text": "إن كنتم هنا، فأنتم في كل مكان\n\nتوزيع حجم الاستثمارات حسب القطاع\n\nيواصل القطاع الصناعي نموه الاستثنائي بأكثر من نصف الاستثمارات التي تمت المصادقة عليها\n\nإجمالي الاستثمارات: 40,76 مليار درهم\n\nالصناعة: 54%\nالسياحة: 22%\nالطاقة والمناجم: 15%\nقطاعات أخرى: 6%\nالتجارة: 2%\nالبناء والأشغال العامة: 1%\n\nwww.investangier.com"
        },
        {
          "retrieval_chunk_id": "chiffres_cles_crui_1er_semestre_2024_arabe_chunk_004__r001",
          "document_id": "chiffres_cles_crui_1er_semestre_2024_arabe",
          "document_family_id": "crui_key_figures_2024_h1",
          "filename": "Chiffres_cles_CRUI_1er_semestre_2024_Arabe.json",
          "language": "ar",
          "topic_id": "industrial_investment",
          "content_type": "statistics",
          "page_start": 4,
          "page_end": 4,
          "source_pages": [
            4
          ],
          "dense_score": 0.83853364,
          "ranking_score": 0.84353364,
          "text": "إن كنتم هنا، فأنتم في كل مكان\n\nتشكل الصناعة القطاع الرائد في توفير فرص شغل على المدى المتوسط والبعيد، بحصة تقدر بـ 83%\n\nالصناعة: 83%\nالسياحة: 7%\nقطاعات أخرى: 10%\n\nwww.investangier.com"
        },
        {
          "retrieval_chunk_id": "akhbar_al_moustatmir_news_phase3f_0007__r001",
          "document_id": "akhbar_al_moustatmir_news",
          "document_family_id": "manar_al_moustatmir_news_2023",
          "filename": "Akhbar_Al_Moustatmir_News.json",
          "language": "ar",
          "topic_id": "investment_news",
          "content_type": "investment_opportunity",
          "page_start": 10,
          "page_end": 10,
          "source_pages": [
            10
          ],
          "dense_score": 0.82248604,
          "ranking_score": 0.83948604,
          "text": "04\nwww.investangier.com\n تعزیز العرض العقاري المخصص لقطاع\nالسیاحة من خلال إتاحة فرص عقاریة \n متر مربع لبناء 2949 للمستثمرین بمساحة\n نجوم أو أكثر في أصیلة.4 فندق\nبعد انتھاء ھذا الإعلان عن الاستثمار، تم \n ملفات، تم اختیار مشروع واحد لبناء 3 تقدیم\n غرفة بتكلفة 104 * یتألف من4 فندق\n ملیون درھم مغربي، 106 استثماریة تبلغ\n فرصة عمل.56 مما یتیح خلق\n ھكتار70 مساحة\nالقدرة المركبة\nجرین باور1 المغرب\nتشغیل أول مركب خاص للطاقة الشمسیة\nعلى الصعید الوطني\n میجاوات30\n()في الدفعة الأولى"
        },
        {
          "retrieval_chunk_id": "akhbar_al_moustatmir_news_phase3f_0029__r001b",
          "document_id": "akhbar_al_moustatmir_news",
          "document_family_id": "manar_al_moustatmir_news_2023",
          "filename": "Akhbar_Al_Moustatmir_News.json",
          "language": "ar",
          "topic_id": "investment_news",
          "content_type": "investment_opportunity",
          "page_start": 42,
          "page_end": 42,
          "source_pages": [
            42
          ],
          "dense_score": 0.82646346,
          "ranking_score": 0.83946346,
          "text": "36\nwww.investangier.com\nTIERRA BENDITA\nHOUARA GESTION\nROMANTICO CO LTD\nاليابان الدولية للتبغ\nالنشاط\nالاستثمار\nالعدد المتوقع للوظائف\nالمكان\nإنتاج التبغ\nمليون درهم\n170 \nتطوان بارك\n930\nشركة طاقة المغربیة للرياح\nالنشاط\nالاستثمار\nالعدد المتوقع للوظائف\nالمكان\nالطاقات\nمليون درهم\n15 \nالفنیدق، تطوان-فحص أنجرة، المضیق\n1400\nھوارة للتدبیر\nالنشاط\nالاستثمار\nالعدد المتوقع للوظائف\nالمكان\n غرفة131 نجوم مع5 فندق\nمليون درهم\n200 \nطنجة\n240\nرومانتیك كو المحدودة\nالنشاط\nالاستثمار\nالعدد المتوقع للوظائف\nالمكان\nصنع حقائب الید والمحافظ والحقائب\nمليون درهم\n1000 800 \nزاي طنجة تیك\n55\nباوماك الكترونيك المغرب\nالاستثمار\nالعدد المتوقع للوظائف\nالمكان\nمليون درهم\n280 \n مدينة طنجة للسيارات\n179\n إلى\nدريسكولز\nالنشاط\nالاستثمار\nالعدد المتوقع للوظائف\nالمكان\nتعبئة المنتجات الزراعیة\nمليون درهم\n600\n العرائش- أغروبول لوكوس\n150\nسانت ريجیس\nالنشاط\nالاستثمار\nالعدد المتوقع للوظائف\nالمكان\n مفتاح100 نجوم مع5 فندق\nمليون درهم\n300 \nالفنیدق-المضیق\n980\nبلیسد لاند\nالنشاط\nالاستثمار\nالعدد المتوقع للوظائف\nالمكان\n غرفة67 نجوم مع4 فندق\nمليون درهم\n107 \nوزان\n67"
        },
        {
          "retrieval_chunk_id": "arabe_chiffres_cles_2025_chunk_008__r001",
          "document_id": "arabe_chiffres_cles_2025",
          "document_family_id": "chiffres_cles_2025",
          "filename": "Arabe_Chiffres_cles_2025.json",
          "language": "ar",
          "topic_id": "sector_investment",
          "content_type": "statistics",
          "page_start": 8,
          "page_end": 8,
          "source_pages": [
            8
          ],
          "dense_score": 0.83445287,
          "ranking_score": 0.83945287,
          "text": "حصيلة اللجنة الجهوية الموحدة للاستثمار (5/6)\nدينامية قوية للاستثمار السياحي مدعومة برؤية واعدة\nلقد اختاروا الجهة سنة 2025\n\n7 مؤسسات مفتوحة سنة 2025\n+300 غرفة\n194 مليون درهم من الاستثمارات\n\n31 مؤسسة في طور الإنجاز\n2 036 غرفة إضافية\nمنها 1 220 غرفة من فئة 3 نجوم فأكثر\n4,8 مليار درهم من الاستثمارات المرتقبة\n\nالمؤسسات المفتوحة سنة 2025 / المؤسسات في طور الإنجاز في 2025:\nطنجة - أصيلة: 9 / 15 — 1 244 / 2 307 غرفة\nالعرائش: 1 — 60 غرفة\nوزان: 1 — 106 غرف\nالفحص أنجرة: 4 — 154 غرفة\nالمضيق - الفنيدق: 5 / 1 — 812 / 152 غرفة\nتطوان: 2 / 1 — 70 / 70 غرفة\nشفشاون: 1 / 1 — 64 / 20 غرفة\nالحسيمة: 1 — 42 غرفة\n\nwww.investangier.com\n08"
        }
      ],
      "experimental_v2": [
        {
          "evidence_id": "E1",
          "retrieval_chunk_id": "chiffres_cles_crui_1er_semestre_2024_arabe_chunk_003__r001",
          "parent_semantic_chunk_id": "chiffres_cles_crui_1er_semestre_2024_arabe_chunk_003",
          "document_id": "chiffres_cles_crui_1er_semestre_2024_arabe",
          "document_family_id": "crui_key_figures_2024_h1",
          "filename": "Chiffres_cles_CRUI_1er_semestre_2024_Arabe.json",
          "document_title": "المؤشرات الرئيسية والإحصائيات",
          "language": "ar",
          "topic_id": "sector_distribution",
          "content_type": "statistics",
          "semantic_tags": [
            "sector_distribution",
            "investment_amount"
          ],
          "heading_path": [
            "إن كنتم هنا، فأنتم في كل مكان"
          ],
          "page_start": 3,
          "page_end": 3,
          "source_pages": [
            3
          ],
          "text": "إن كنتم هنا، فأنتم في كل مكان\n\nتوزيع حجم الاستثمارات حسب القطاع\n\nيواصل القطاع الصناعي نموه الاستثنائي بأكثر من نصف الاستثمارات التي تمت المصادقة عليها\n\nإجمالي الاستثمارات: 40,76 مليار درهم\n\nالصناعة: 54%\nالسياحة: 22%\nالطاقة والمناجم: 15%\nقطاعات أخرى: 6%\nالتجارة: 2%\nالبناء والأشغال العامة: 1%\n\nwww.investangier.com",
          "source_spans": [
            {
              "page": 3,
              "text": "إن كنتم هنا، فأنتم في كل مكان\n\nتوزيع حجم الاستثمارات حسب القطاع\n\nيواصل القطاع الصناعي نموه الاستثنائي بأكثر من نصف الاستثمارات التي تمت المصادقة عليها\n\nإجمالي الاستثمارات: 40,76 مليار درهم\n\nالصناعة: 54%\nالسياحة: 22%\nالطاقة والمناجم: 15%\nقطاعات أخرى: 6%\nالتجارة: 2%\nالبناء والأشغال العامة: 1%\n\nwww.investangier.com"
            }
          ],
          "dense_score": 0.83912504,
          "ranking_score": 0.84412504,
          "expanded_from_sibling": false,
          "retrieval_chunk_index": 0,
          "retrieval_chunk_count": 1,
          "temporal_scope": {
            "primary_year": 2024,
            "years_mentioned": [],
            "reference_period": {
              "type": "semester",
              "year": 2024,
              "semester": 1,
              "quarter": null,
              "start_date": null,
              "end_date": null
            }
          }
        },
        {
          "evidence_id": "E2",
          "retrieval_chunk_id": "chiffres_cles_crui_1er_semestre_2024_arabe_chunk_004__r001",
          "parent_semantic_chunk_id": "chiffres_cles_crui_1er_semestre_2024_arabe_chunk_004",
          "document_id": "chiffres_cles_crui_1er_semestre_2024_arabe",
          "document_family_id": "crui_key_figures_2024_h1",
          "filename": "Chiffres_cles_CRUI_1er_semestre_2024_Arabe.json",
          "document_title": "المؤشرات الرئيسية والإحصائيات",
          "language": "ar",
          "topic_id": "industrial_investment",
          "content_type": "statistics",
          "semantic_tags": [
            "sector_distribution",
            "industrial_investment",
            "investment_amount",
            "projected_jobs"
          ],
          "heading_path": [
            "إن كنتم هنا، فأنتم في كل مكان"
          ],
          "page_start": 4,
          "page_end": 4,
          "source_pages": [
            4
          ],
          "text": "إن كنتم هنا، فأنتم في كل مكان\n\nتشكل الصناعة القطاع الرائد في توفير فرص شغل على المدى المتوسط والبعيد، بحصة تقدر بـ 83%\n\nالصناعة: 83%\nالسياحة: 7%\nقطاعات أخرى: 10%\n\nwww.investangier.com",
          "source_spans": [
            {
              "page": 4,
              "text": "إن كنتم هنا، فأنتم في كل مكان\n\nتشكل الصناعة القطاع الرائد في توفير فرص شغل على المدى المتوسط والبعيد، بحصة تقدر بـ 83%\n\nالصناعة: 83%\nالسياحة: 7%\nقطاعات أخرى: 10%\n\nwww.investangier.com"
            }
          ],
          "dense_score": 0.83853364,
          "ranking_score": 0.84353364,
          "expanded_from_sibling": false,
          "retrieval_chunk_index": 0,
          "retrieval_chunk_count": 1,
          "temporal_scope": {
            "primary_year": 2024,
            "years_mentioned": [],
            "reference_period": {
              "type": "semester",
              "year": 2024,
              "semester": 1,
              "quarter": null,
              "start_date": null,
              "end_date": null
            }
          }
        },
        {
          "evidence_id": "E3",
          "retrieval_chunk_id": "akhbar_al_moustatmir_news_phase3f_0007__r001",
          "parent_semantic_chunk_id": "akhbar_al_moustatmir_news_phase3f_0007",
          "document_id": "akhbar_al_moustatmir_news",
          "document_family_id": "manar_al_moustatmir_news_2023",
          "filename": "Akhbar_Al_Moustatmir_News.json",
          "document_title": "أخبار الاستثمار وريادة الأعمال",
          "language": "ar",
          "topic_id": "investment_news",
          "content_type": "investment_opportunity",
          "semantic_tags": [
            "investment_news",
            "investment_opportunity",
            "tourism"
          ],
          "heading_path": [
            "العرض العقاري السياحي بأصيلة"
          ],
          "page_start": 10,
          "page_end": 10,
          "source_pages": [
            10
          ],
          "text": "04\nwww.investangier.com\n تعزیز العرض العقاري المخصص لقطاع\nالسیاحة من خلال إتاحة فرص عقاریة \n متر مربع لبناء 2949 للمستثمرین بمساحة\n نجوم أو أكثر في أصیلة.4 فندق\nبعد انتھاء ھذا الإعلان عن الاستثمار، تم \n ملفات، تم اختیار مشروع واحد لبناء 3 تقدیم\n غرفة بتكلفة 104 * یتألف من4 فندق\n ملیون درھم مغربي، 106 استثماریة تبلغ\n فرصة عمل.56 مما یتیح خلق\n ھكتار70 مساحة\nالقدرة المركبة\nجرین باور1 المغرب\nتشغیل أول مركب خاص للطاقة الشمسیة\nعلى الصعید الوطني\n میجاوات30\n()في الدفعة الأولى",
          "source_spans": [
            {
              "page": 10,
              "text": "04\nwww.investangier.com\n تعزیز العرض العقاري المخصص لقطاع\nالسیاحة من خلال إتاحة فرص عقاریة \n متر مربع لبناء 2949 للمستثمرین بمساحة\n نجوم أو أكثر في أصیلة.4 فندق\nبعد انتھاء ھذا الإعلان عن الاستثمار، تم \n ملفات، تم اختیار مشروع واحد لبناء 3 تقدیم\n غرفة بتكلفة 104 * یتألف من4 فندق\n ملیون درھم مغربي، 106 استثماریة تبلغ\n فرصة عمل.56 مما یتیح خلق\n ھكتار70 مساحة\nالقدرة المركبة\nجرین باور1 المغرب\nتشغیل أول مركب خاص للطاقة الشمسیة\nعلى الصعید الوطني\n میجاوات30\n()في الدفعة الأولى"
            }
          ],
          "dense_score": 0.82248604,
          "ranking_score": 0.83948604,
          "expanded_from_sibling": false,
          "retrieval_chunk_index": 0,
          "retrieval_chunk_count": 1,
          "temporal_scope": {
            "primary_year": null,
            "years_mentioned": [],
            "reference_period": {
              "type": null,
              "year": null,
              "semester": null,
              "quarter": null,
              "start_date": null,
              "end_date": null
            }
          }
        },
        {
          "evidence_id": "E4",
          "retrieval_chunk_id": "akhbar_al_moustatmir_news_phase3f_0029__r001b",
          "parent_semantic_chunk_id": "akhbar_al_moustatmir_news_phase3f_0029",
          "document_id": "akhbar_al_moustatmir_news",
          "document_family_id": "manar_al_moustatmir_news_2023",
          "filename": "Akhbar_Al_Moustatmir_News.json",
          "document_title": "أخبار الاستثمار وريادة الأعمال",
          "language": "ar",
          "topic_id": "investment_news",
          "content_type": "investment_opportunity",
          "semantic_tags": [
            "investment_news",
            "investment_opportunity",
            "project_announcement"
          ],
          "heading_path": [
            "مشاريع وشركات مختارة"
          ],
          "page_start": 42,
          "page_end": 42,
          "source_pages": [
            42
          ],
          "text": "36\nwww.investangier.com\nTIERRA BENDITA\nHOUARA GESTION\nROMANTICO CO LTD\nاليابان الدولية للتبغ\nالنشاط\nالاستثمار\nالعدد المتوقع للوظائف\nالمكان\nإنتاج التبغ\nمليون درهم\n170 \nتطوان بارك\n930\nشركة طاقة المغربیة للرياح\nالنشاط\nالاستثمار\nالعدد المتوقع للوظائف\nالمكان\nالطاقات\nمليون درهم\n15 \nالفنیدق، تطوان-فحص أنجرة، المضیق\n1400\nھوارة للتدبیر\nالنشاط\nالاستثمار\nالعدد المتوقع للوظائف\nالمكان\n غرفة131 نجوم مع5 فندق\nمليون درهم\n200 \nطنجة\n240\nرومانتیك كو المحدودة\nالنشاط\nالاستثمار\nالعدد المتوقع للوظائف\nالمكان\nصنع حقائب الید والمحافظ والحقائب\nمليون درهم\n1000 800 \nزاي طنجة تیك\n55\nباوماك الكترونيك المغرب\nالاستثمار\nالعدد المتوقع للوظائف\nالمكان\nمليون درهم\n280 \n مدينة طنجة للسيارات\n179\n إلى\nدريسكولز\nالنشاط\nالاستثمار\nالعدد المتوقع للوظائف\nالمكان\nتعبئة المنتجات الزراعیة\nمليون درهم\n600\n العرائش- أغروبول لوكوس\n150\nسانت ريجیس\nالنشاط\nالاستثمار\nالعدد المتوقع للوظائف\nالمكان\n مفتاح100 نجوم مع5 فندق\nمليون درهم\n300 \nالفنیدق-المضیق\n980\nبلیسد لاند\nالنشاط\nالاستثمار\nالعدد المتوقع للوظائف\nالمكان\n غرفة67 نجوم مع4 فندق\nمليون درهم\n107 \nوزان\n67",
          "source_spans": [
            {
              "page": 42,
              "text": "36\nwww.investangier.com\nTIERRA BENDITA\nHOUARA GESTION\nROMANTICO CO LTD\nاليابان الدولية للتبغ\nالنشاط\nالاستثمار\nالعدد المتوقع للوظائف\nالمكان\nإنتاج التبغ\nمليون درهم\n170 \nتطوان بارك\n930\nشركة طاقة المغربیة للرياح\nالنشاط\nالاستثمار\nالعدد المتوقع للوظائف\nالمكان\nالطاقات\nمليون درهم\n15 \nالفنیدق، تطوان-فحص أنجرة، المضیق\n1400\nھوارة للتدبیر\nالنشاط\nالاستثمار\nالعدد المتوقع للوظائف\nالمكان\n غرفة131 نجوم مع5 فندق\nمليون درهم\n200 \nطنجة\n240\nرومانتیك كو المحدودة\nالنشاط\nالاستثمار\nالعدد المتوقع للوظائف\nالمكان\nصنع حقائب الید والمحافظ والحقائب\nمليون درهم\n1000 800 \nزاي طنجة تیك\n55\nباوماك الكترونيك المغرب\nالاستثمار\nالعدد المتوقع للوظائف\nالمكان\nمليون درهم\n280 \n مدينة طنجة للسيارات\n179\n إلى\nدريسكولز\nالنشاط\nالاستثمار\nالعدد المتوقع للوظائف\nالمكان\nتعبئة المنتجات الزراعیة\nمليون درهم\n600\n العرائش- أغروبول لوكوس\n150\nسانت ريجیس\nالنشاط\nالاستثمار\nالعدد المتوقع للوظائف\nالمكان\n مفتاح100 نجوم مع5 فندق\nمليون درهم\n300 \nالفنیدق-المضیق\n980\nبلیسد لاند\nالنشاط\nالاستثمار\nالعدد المتوقع للوظائف\nالمكان\n غرفة67 نجوم مع4 فندق\nمليون درهم\n107 \nوزان\n67"
            }
          ],
          "dense_score": 0.82646346,
          "ranking_score": 0.83946346,
          "expanded_from_sibling": false,
          "retrieval_chunk_index": 1,
          "retrieval_chunk_count": 3,
          "temporal_scope": {
            "primary_year": null,
            "years_mentioned": [],
            "reference_period": {
              "type": null,
              "year": null,
              "semester": null,
              "quarter": null,
              "start_date": null,
              "end_date": null
            }
          }
        },
        {
          "evidence_id": "E5",
          "retrieval_chunk_id": "arabe_chiffres_cles_2025_chunk_008__r001",
          "parent_semantic_chunk_id": "arabe_chiffres_cles_2025_chunk_008",
          "document_id": "arabe_chiffres_cles_2025",
          "document_family_id": "chiffres_cles_2025",
          "filename": "Arabe_Chiffres_cles_2025.json",
          "document_title": "المؤشرات الرئيسية والإحصائيات",
          "language": "ar",
          "topic_id": "sector_investment",
          "content_type": "statistics",
          "semantic_tags": [
            "sector_investment",
            "tourism_investment"
          ],
          "heading_path": [
            "حصيلة اللجنة الجهوية الموحدة للاستثمار (5/6)"
          ],
          "page_start": 8,
          "page_end": 8,
          "source_pages": [
            8
          ],
          "text": "حصيلة اللجنة الجهوية الموحدة للاستثمار (5/6)\nدينامية قوية للاستثمار السياحي مدعومة برؤية واعدة\nلقد اختاروا الجهة سنة 2025\n\n7 مؤسسات مفتوحة سنة 2025\n+300 غرفة\n194 مليون درهم من الاستثمارات\n\n31 مؤسسة في طور الإنجاز\n2 036 غرفة إضافية\nمنها 1 220 غرفة من فئة 3 نجوم فأكثر\n4,8 مليار درهم من الاستثمارات المرتقبة\n\nالمؤسسات المفتوحة سنة 2025 / المؤسسات في طور الإنجاز في 2025:\nطنجة - أصيلة: 9 / 15 — 1 244 / 2 307 غرفة\nالعرائش: 1 — 60 غرفة\nوزان: 1 — 106 غرف\nالفحص أنجرة: 4 — 154 غرفة\nالمضيق - الفنيدق: 5 / 1 — 812 / 152 غرفة\nتطوان: 2 / 1 — 70 / 70 غرفة\nشفشاون: 1 / 1 — 64 / 20 غرفة\nالحسيمة: 1 — 42 غرفة\n\nwww.investangier.com\n08",
          "source_spans": [
            {
              "page": 8,
              "text": "حصيلة اللجنة الجهوية الموحدة للاستثمار (5/6)\nدينامية قوية للاستثمار السياحي مدعومة برؤية واعدة\nلقد اختاروا الجهة سنة 2025\n\n7 مؤسسات مفتوحة سنة 2025\n+300 غرفة\n194 مليون درهم من الاستثمارات\n\n31 مؤسسة في طور الإنجاز\n2 036 غرفة إضافية\nمنها 1 220 غرفة من فئة 3 نجوم فأكثر\n4,8 مليار درهم من الاستثمارات المرتقبة\n\nالمؤسسات المفتوحة سنة 2025 / المؤسسات في طور الإنجاز في 2025:\nطنجة - أصيلة: 9 / 15 — 1 244 / 2 307 غرفة\nالعرائش: 1 — 60 غرفة\nوزان: 1 — 106 غرف\nالفحص أنجرة: 4 — 154 غرفة\nالمضيق - الفنيدق: 5 / 1 — 812 / 152 غرفة\nتطوان: 2 / 1 — 70 / 70 غرفة\nشفشاون: 1 / 1 — 64 / 20 غرفة\nالحسيمة: 1 — 42 غرفة\n\nwww.investangier.com\n08"
            }
          ],
          "dense_score": 0.83445287,
          "ranking_score": 0.83945287,
          "expanded_from_sibling": false,
          "retrieval_chunk_index": 0,
          "retrieval_chunk_count": 1,
          "temporal_scope": {
            "primary_year": 2025,
            "years_mentioned": [
              2025
            ],
            "reference_period": {
              "type": "year",
              "year": 2025,
              "semester": null,
              "quarter": null,
              "start_date": null,
              "end_date": null
            }
          }
        }
      ],
      "status": "review_required"
    },
    "Q029": {
      "query": {
        "query_id": "Q029",
        "language": "ar",
        "question": "ما هي المناطق الصناعية والاقتصادية في الجهة؟",
        "category": "industrial_zones",
        "explicit_year": null,
        "expected_topics": [
          "industrial_zones_overview",
          "industrial_zone_profile"
        ],
        "expected_document_families": [
          "industrial_zones_panorama"
        ],
        "acceptable_languages": [
          "ar",
          "fr",
          "en",
          "es"
        ]
      },
      "baseline_v1": [
        {
          "chunk_id": "ar_pr_sentation_cri_tta_vf_p35_c1",
          "document_id": "ar_pr_sentation_cri_tta_vf",
          "document_family_id": "cri_presentation",
          "filename": "AR_Présentation CRI TTA VF.pdf",
          "language": "ar",
          "page": 35,
          "page_start": 35,
          "page_end": 35,
          "source_pages": [
            35
          ],
          "dense_score": 0.82650965,
          "ranking_score": 0.82650965,
          "retrieval_score": 0.82650965,
          "final_score": 0.82650965,
          "text": "يا ألم\n\nل م\nفنل زم شا ل نم عع دمرىء بس\n\nالعرض الترابي\nللاستثمار\n\n.إن كنتم هناء فأنتم في كل مكان؟؟\n\nوزو سلما والشسية وتشيع الساسيي\n4 لوتيد م لاصو ا\nال ع عرو تي ات مها م\n\nة الصناعية والرقمية في المغرب\n\nمنصة استقبال تم تقديمها أمام جلالة الملك محمد السادس نصره الله سنة 2017\n\n0 أنشطة\nالطيران\n\nالسيارات\n\nالتجارة الإلكترونية\n. الاتصالات\nالطاقات المتجددة\nالنقل\n\nالأجهزة المنزلية\n\n. الصناعات الدوائية\n2 إنتاج المواد\n\n5 الصناعات الزراعية والغذائية\n\nا\n0\n\nم \" دعق ٍّ\n\n27\nقرارًا بالترخيص للتركيب\nتم منحها\n\nمدينة ذكية تتسع ل 300,000 نسمة\n\nالاستثمار: مليار دولار\nعدد مناصب الشغل يصل إلى 100,000\nالإيرادات: 15 مليار دولار سنوبا\n\nالمساحة: 2,167 هكتارا. منها 947 هكتارا مخصصة\nلمنطقة التسريع د هكتار قيد التطوبر\n4\n\nهكتا الا ١\nالأو 00 التجاري الأولى, من رق\n\n0 11+ 27+\nمنصب شغل متوقع مليار درهم من الاستثمارات\n\nالمنطقة اللوجستيكية طبه كءالا ا مصنع رونو\nكٍ 4 يدق 0 - 0 ع منطقة الأنشطة الإقتصادية مفوغة\n١ 5 منطقة الأنشطة الإقتصادية المجد\nالإقتصادية حيضرة 3 500 م منطقة الأنشطة الإقتصادية العوامة\nك_ المنطقة الحرة لطنجة\nالمنطقة الصناعية مرنيل: المنطقة الصناعية\nكزناية: لهاع هوأرماأهي عل أوعع\n264 1 5\nهكتارًا من الأراضي التي سيتم مشروع أصبح عمليا مشاريع قيد الإنشاء\n\nتعبئتها من خلال المشاريع ع الي\nوافقت عليها اللجنة الجهوية\nالموحدة للاستثمار\n\nون 58 غه عا مومرمج لاكمم روجع\n\n5ع ااانا امعل/ا,عوصة 1"
        },
        {
          "chunk_id": "ar_pr_sentation_cri_tta_vf_p34_c1",
          "document_id": "ar_pr_sentation_cri_tta_vf",
          "document_family_id": "cri_presentation",
          "filename": "AR_Présentation CRI TTA VF.pdf",
          "language": "ar",
          "page": 34,
          "page_start": 34,
          "page_end": 34,
          "source_pages": [
            34
          ],
          "dense_score": 0.82415867,
          "ranking_score": 0.82415867,
          "retrieval_score": 0.82415867,
          "final_score": 0.82415867,
          "text": "ا سين\n465 ر. إن كنتم هناء فأنتم في كل مكان؟؟\n\nالعرض الترابي عرض عقاري متنوع مخصص للاستتمار المنتج\n\nللاستتصار ”\n\n-- مصنع رونو\n\n3 2 5 2 الطروق الوظنية 00: 9 اله ١ منطقة الأنشطة الإقتصادية المجد\n2 مناطق تجارية 0 كك ادك الحديحية 5 ميناء المسافرين 0 --89 0 190.900 ._منضفة سشدة بيتتصية تعومة\nبمساحة 160 هسكتار سس الطريق السيار ديكا الصيد ا\nسس قطار البراق ص مطار 1 ٍ المنطقة الحرة لطنجة\nسس الطريق السريع 1 ميناء طنجة المتوسط المنطقة الصناعبة مرتيل 6 6 / _- المنطقة لصناعية\nمنصة استقبال المنطقة الصناعية تطوان 1:\n\n1 قطب فلاحي\n\nبمساحة 150 هسكتار انيه\n\n0 3+ هكتار\n\n4 مناطق تسريع صناعي بمساحة\nإجمالية قدرها 2.500 هكتار\n\n1 منطقة ترحيل الخدمات\nبمساحة 20 هكتار\n\n© مناطق صناعية متعددة\n\nالقطاعات بمساحة إجمالية\nتبلغ 700 هكتار ل القطب الفلاحي الصناعي اللوكوس\n\n6 مناطق أنشطة اقتصادية\n\nهكتا\nبمساحةتقدربحوالي 160صكتار 3 ككتار\n\nمنطقة الأنشطة الإقتصادية وزان\n\n1 منطقة لوجستية حرة"
        },
        {
          "chunk_id": "arabe_chiffres_cles_2025_p7_c1",
          "document_id": "arabe_chiffres_cles_2025",
          "document_family_id": "chiffres_cles_2025",
          "filename": "Arabe_ Chiffres clés 2025.pdf",
          "language": "ar",
          "page": 7,
          "page_start": 7,
          "page_end": 7,
          "source_pages": [
            7
          ],
          "dense_score": 0.8186874,
          "ranking_score": 0.8186874,
          "retrieval_score": 0.8186874,
          "final_score": 0.8186874,
          "text": "حصيلة اللجنة الجهوية الموحدة للاستثمار (4/6)\nالجهة تعزز تموقعها الصناعي كرافعة لنموها الاقتصادي\nلقد اختاروا الجهة سنة 2025\n\nعدد المشاريع\nقيمة الاستثمار (مليار درهم)\nعدد الوظائف\n\n278 ملف\n+30 مليار درهم من الاستثمارات\n+43 800 منصب شغل متوقع\n+430 هكتاراً تمت تعبئتها\n\nطنجة\nالعرائش\nوزان\nشفشاون\nتطوان\nالحسيمة\n\nالمنطقة الحرة بطنجة: 67 | 1,30 | 5 464\nمنطقة التسريع الصناعي طنجة - أوطموتيف سيتي: 88 | 10,08 | 21 389\nطنجة تيك: 13 | 1,28 | 1 018\nالقطب الفلاحي اللوكوس: 22 | 7,39 | 5 392\nالمنطقة الاقتصادية أصيلة: 13 | 0,22 | 1 216\nالمنطقة الصناعية كزناية: 18 | 0,67 | 1 852\nمنطقة الأنشطة الاقتصادية قصر بجير: 5 | 0,04 | 826\nمنطقة الأنشطة الاقتصادية وزان: 3 | 0,19 | 564\nمنطقة الأنشطة الاقتصادية آيت قمرة: 7 | 0,11 | 295\nمنطقة الأنشطة الاقتصادية إمزورن: 4 | 0,01 | 170\nتطوان بارك\nمنطقة الأنشطة الاقتصادية حيدارة\nM’DIQ\nFNIDEQ\n\nwww.investangier.com\n07"
        },
        {
          "chunk_id": "akhbar_al_moustatmir_news_p9_c1",
          "document_id": "akhbar_al_moustatmir_news",
          "document_family_id": "manar_al_moustatmir_news_2023",
          "filename": "Akhbar Al Moustatmir News VA compress.pdf",
          "language": "ar",
          "page": 9,
          "page_start": 9,
          "page_end": 9,
          "source_pages": [
            9
          ],
          "dense_score": 0.8042944,
          "ranking_score": 0.8042944,
          "retrieval_score": 0.8042944,
          "final_score": 0.8042944,
          "text": "03\nwww.investangier.com\n03\nwww.investangier.com\nإطلاق عــرض أرض للإيجــار فــي تطــوان بــارك بموجــب اتفاقيــة الشراكــة\nالمتعلقــة بتعبئــة أراضي المنطقــة الصناعيــة واللوجســتية بتطــوان بــارك\nقطع صناعية9 :2022 يونيو10 الموقعة في\n8\nالمساحة\nالإجمالي\n8\nالمشاريع الصناعية\nالمصادق عليها\n350 MMAD\nمبلغ الاستثمار\n1 000\nالوظائف\nھكتـار( مـن قطـب50) تخصیـص القطـع الأرضیـة على مسـتوى الدفعـة الأولى\nلوكوس الزراعي في العرائش\n47\nالتكلفة\nلإجمالية\nالشركات\n8 000\nالوظائف\nالمساحة\nمبنى117 بدء تشغيل منطقة النشاط الاقتصادي في طنجة البالیة :تخصیص\n150\n457\nفي طور التأسيس"
        },
        {
          "chunk_id": "chiffres_cles_crui_1er_semestre_2024_arabe_p4_c1",
          "document_id": "chiffres_cles_crui_1er_semestre_2024_arabe",
          "document_family_id": "crui_key_figures_2024_h1",
          "filename": "Chiffres clés CRUI 1er semestre 2024_Arabe.pdf",
          "language": "ar",
          "page": 4,
          "page_start": 4,
          "page_end": 4,
          "source_pages": [
            4
          ],
          "dense_score": 0.79904187,
          "ranking_score": 0.79904187,
          "retrieval_score": 0.79904187,
          "final_score": 0.79904187,
          "text": "إن كنتم هنا، فأنتم في كل مكان\n\nتشكل الصناعة القطاع الرائد في توفير فرص شغل على المدى المتوسط والبعيد، بحصة تقدر بـ 83%\n\nالصناعة: 83%\nالسياحة: 7%\nقطاعات أخرى: 10%\n\nwww.investangier.com"
        }
      ],
      "baseline_v2": [
        {
          "retrieval_chunk_id": "ar_pr_sentation_cri_tta_vf_semantic_019__r001a",
          "document_id": "ar_pr_sentation_cri_tta_vf",
          "document_family_id": "cri_presentation",
          "filename": "AR_Presentation_CRI_TTA.json",
          "language": "ar",
          "topic_id": "territorial_offer",
          "content_type": "narrative",
          "page_start": 34,
          "page_end": 35,
          "source_pages": [
            34,
            35
          ],
          "dense_score": 0.82328194,
          "ranking_score": 0.82828194,
          "text": "ا سين\n465 ر. إن كنتم هناء فأنتم في كل مكان؟؟\n\nالعرض الترابي عرض عقاري متنوع مخصص للاستتمار المنتج\n\nللاستتصار ”\n\n-- مصنع رونو\n\n3 2 5 2 الطروق الوظنية 00: 9 اله ١ منطقة الأنشطة الإقتصادية المجد\n2 مناطق تجارية 0 كك ادك الحديحية 5 ميناء المسافرين 0 --89 0 190.900 ._منضفة سشدة بيتتصية تعومة\nبمساحة 160 هسكتار سس الطريق السيار ديكا الصيد ا\nسس قطار البراق ص مطار 1 ٍ المنطقة الحرة لطنجة\nسس الطريق السريع 1 ميناء طنجة المتوسط المنطقة الصناعبة مرتيل 6 6 / _- المنطقة لصناعية\nمنصة استقبال المنطقة الصناعية تطوان 1:\n\n1 قطب فلاحي\n\nبمساحة 150 هسكتار انيه\n\n0 3+ هكتار\n\n4 مناطق تسريع صناعي بمساحة\nإجمالية قدرها 2.500 هكتار\n\n1 منطقة ترحيل الخدمات\nبمساحة 20 هكتار\n\n© مناطق صناعية متعددة\n\nالقطاعات بمساحة إجمالية\nتبلغ 700 هكتار ل القطب الفلاحي الصناعي اللوكوس\n\n6 مناطق أنشطة اقتصادية\n\nهكتا\nبمساحةتقدربحوالي 160صكتار 3 ككتار\n\nمنطقة الأنشطة الإقتصادية وزان\n\n1 منطقة لوجستية حرة\n\nيا ألم\n\nل م\nفنل زم شا ل نم عع دمرىء بس\n\nالعرض الترابي\nللاستثمار\n\n.إن كنتم هناء فأنتم في كل مكان؟؟\n\nوزو سلما والشسية وتشيع الساسيي\n4 لوتيد م لاصو ا\nال ع عرو تي ات مها م\n\nة الصناعية والرقمية في المغرب"
        },
        {
          "retrieval_chunk_id": "ar_pr_sentation_cri_tta_vf_semantic_005__r001",
          "document_id": "ar_pr_sentation_cri_tta_vf",
          "document_family_id": "cri_presentation",
          "filename": "AR_Presentation_CRI_TTA.json",
          "language": "ar",
          "topic_id": "industrial_ecosystem",
          "content_type": "narrative",
          "page_start": 11,
          "page_end": 11,
          "source_pages": [
            11
          ],
          "dense_score": 0.81974673,
          "ranking_score": 0.82474673,
          "text": "عو\n\nاكيم\n\nيل\n\nإن كنتم هناء فأنتم في كل مكان؟\n\nمزايا الجهة 2/2 طنجة-تطوان-الحسيمة. قطب اقتصادى تنافسي على الصعيد الوطني\n\nبإشعاع دولي\n\nجودة حياة مميزة\nلله مناخ معتدل\n\n3 توفر البنيات التحتية المرافقة والتجهيزات\nالضربيت\n\n© أمن ونظافة الفضاءات العمومية\n\n8 تنشيط ثقافي وسياحي متنوع\n\n7\n\n016\nتك\n\nإطار تحفيزي جذاب\nميثاق الاستثمار\n\nالصندوق الجهوى لدعم الاستثمار\n(بميزانية قدرها مليار درهم) \"/اعم عملم\"\n\nنظام ضريبى تفضيلى لفائدة مناطق\nالتسريع الصناعى والمناطق الحرة\n\nإعفاء من الضريبة على الشركات لمدة 5 سنوات\nالأواى. معدل مخفض بنسبة 6/20 خلال\nالعشرين سنة التالية. إعفاء من الرسوم\nالجمركية. إعفاء من الضريبة على القيمة\nالمضافة\n\nاقتصاد متنوع وأنظمة بيئية ناضجة\n\nيعتمد هيكل الناتج الداخلى الإجمالي\n\nالجهوي أساسا على القطاع الثالثي (46,2»/).\nيليه القطاع الثانوي (34,3»'). ثم الأنشطة\n\nالأولية (9,3/,)\nتتوفر الجهة على قطاعات اقتصادية رائدة,\n\nمثل صناعة السيارات. النسيج والملابس,\nالصناعات الغذائية. اللوجستيك. الطاقات\n\nالمتجددة. السياحة, وغيرها\nنضجح المنظومات الاقتصادية وتطور\n\nالفاعلين الاقتصاديين عبر كامل سلسلة\nالقيم (الصناعة. خدمات الدعم. المنعشون\nالعقاريون. هياكل المواكبة..)"
        },
        {
          "retrieval_chunk_id": "arabe_chiffres_cles_2025_chunk_007__r001",
          "document_id": "arabe_chiffres_cles_2025",
          "document_family_id": "chiffres_cles_2025",
          "filename": "Arabe_Chiffres_cles_2025.json",
          "language": "ar",
          "topic_id": "sector_investment",
          "content_type": "statistics",
          "page_start": 7,
          "page_end": 7,
          "source_pages": [
            7
          ],
          "dense_score": 0.8153165,
          "ranking_score": 0.8203165,
          "text": "حصيلة اللجنة الجهوية الموحدة للاستثمار (4/6)\nالجهة تعزز تموقعها الصناعي كرافعة لنموها الاقتصادي\nلقد اختاروا الجهة سنة 2025\n\nعدد المشاريع\nقيمة الاستثمار (مليار درهم)\nعدد الوظائف\n\n278 ملف\n+30 مليار درهم من الاستثمارات\n+43 800 منصب شغل متوقع\n+430 هكتاراً تمت تعبئتها\n\nطنجة\nالعرائش\nوزان\nشفشاون\nتطوان\nالحسيمة\n\nالمنطقة الحرة بطنجة: 67 | 1,30 | 5 464\nمنطقة التسريع الصناعي طنجة - أوطموتيف سيتي: 88 | 10,08 | 21 389\nطنجة تيك: 13 | 1,28 | 1 018\nالقطب الفلاحي اللوكوس: 22 | 7,39 | 5 392\nالمنطقة الاقتصادية أصيلة: 13 | 0,22 | 1 216\nالمنطقة الصناعية كزناية: 18 | 0,67 | 1 852\nمنطقة الأنشطة الاقتصادية قصر بجير: 5 | 0,04 | 826\nمنطقة الأنشطة الاقتصادية وزان: 3 | 0,19 | 564\nمنطقة الأنشطة الاقتصادية آيت قمرة: 7 | 0,11 | 295\nمنطقة الأنشطة الاقتصادية إمزورن: 4 | 0,01 | 170\nتطوان بارك\nمنطقة الأنشطة الاقتصادية حيدارة\nM’DIQ\nFNIDEQ\n\nwww.investangier.com\n07"
        },
        {
          "retrieval_chunk_id": "ar_pr_sentation_cri_tta_vf_semantic_008__r001",
          "document_id": "ar_pr_sentation_cri_tta_vf",
          "document_family_id": "cri_presentation",
          "filename": "AR_Presentation_CRI_TTA.json",
          "language": "ar",
          "topic_id": "industrial_ecosystem",
          "content_type": "narrative",
          "page_start": 14,
          "page_end": 15,
          "source_pages": [
            14,
            15
          ],
          "dense_score": 0.8168807,
          "ranking_score": 0.8198807,
          "text": "الصناعة\n\nإن كنتم هناء فأنتم في كل مكان؟؟\n\nال ار\n\nثاني قطب صناعي في المغرب التوزيع القطاعي للرقم الاستدلالي للأعمال الصناعية الجهوية\n\nصناعات أخرى\n12\n\nالصناعة الغذائية\nصناعة السيارات 2\n\nثاني أكبر مساهم في الصادرات 549\n\n| ثاني مساهم في حجم الأعمال\n\nالكهرباء\nأول جهة من خلال تركيز رأس المال وال لكترونيات [الأجنى 6\n\n0 مخزون العمالة للقطاع\nالصناعي على المستوى الوطني\n\nالألبسة والنسيج\n\n12\n\n() مقياس الصناعة المغربية لسنة 2022\n(2) الحسابات الجهوية لسنة 2022. المندوبية السامية للتخطيط\n\n06 فتن الناتج المحلي الإجمالي\nالصناعي الوطني (2)\n\n06 من الناتج المحلي الإجمالي\nالجهوي\n\n145,4 مليار درهم في حجم الأعمال\n\n7 مليار درهم في الصادرات\n\n70 مساهمة المنطقة في\nخلق القيمة المضافة ()\n\nحوالي 250 ألف وظيفة"
        },
        {
          "retrieval_chunk_id": "ar_pr_sentation_cri_tta_vf_semantic_014__r001",
          "document_id": "ar_pr_sentation_cri_tta_vf",
          "document_family_id": "cri_presentation",
          "filename": "AR_Presentation_CRI_TTA.json",
          "language": "ar",
          "topic_id": "industrial_ecosystem",
          "content_type": "narrative",
          "page_start": 27,
          "page_end": 27,
          "source_pages": [
            27
          ],
          "dense_score": 0.8101099,
          "ranking_score": 0.8111099,
          "text": "1 س0 000 000\n\nالقع 00 لالم عن لاجس م ل 2\n\nقطاع الصناعة ات قوية للتنمية الزراعية الصناعية مدعومة بالقطب الفلاحى الصناعى\n\nظ 2 7 من رقم المعاملات\n\nظ أ> 150 هكتار من المساحة\nا الصناعية الجهوية\n\nامك منها 50 هكتار كمرحلة أولى\n\n80 مليون درهم كلفة\n\nعلى المستوى الجهوي\n\nإحم 36 مشروعاً تم تثبيته\n\nالسلاسل الرائدة\n\nاسسمسسير\n\n© التغليف واللوجستيك\n\nظ 0 5 مليار درهم كاستثمارات مرتقبة\n\nعلى المدى البعيد\n\nظ 2 0ه منصب شغل متوقع\n\nلقد اختاروا الجهة\n\nا\n\n7/5 معرمنراوى #ممناعهكدن)» 7 [| /©#١\nكوم ظ 8 ١ سزنة ديات 0 تهت"
        }
      ],
      "experimental_v2": [
        {
          "evidence_id": "E1",
          "retrieval_chunk_id": "ar_pr_sentation_cri_tta_vf_semantic_019__r001a",
          "parent_semantic_chunk_id": "ar_pr_sentation_cri_tta_vf_semantic_019",
          "document_id": "ar_pr_sentation_cri_tta_vf",
          "document_family_id": "cri_presentation",
          "filename": "AR_Presentation_CRI_TTA.json",
          "document_title": "تقديم المركز الجهوي للاستثمار",
          "language": "ar",
          "topic_id": "territorial_offer",
          "content_type": "narrative",
          "semantic_tags": [
            "territorial_offer"
          ],
          "heading_path": [
            "العرض الترابي للاستثمار"
          ],
          "page_start": 34,
          "page_end": 35,
          "source_pages": [
            34,
            35
          ],
          "text": "ا سين\n465 ر. إن كنتم هناء فأنتم في كل مكان؟؟\n\nالعرض الترابي عرض عقاري متنوع مخصص للاستتمار المنتج\n\nللاستتصار ”\n\n-- مصنع رونو\n\n3 2 5 2 الطروق الوظنية 00: 9 اله ١ منطقة الأنشطة الإقتصادية المجد\n2 مناطق تجارية 0 كك ادك الحديحية 5 ميناء المسافرين 0 --89 0 190.900 ._منضفة سشدة بيتتصية تعومة\nبمساحة 160 هسكتار سس الطريق السيار ديكا الصيد ا\nسس قطار البراق ص مطار 1 ٍ المنطقة الحرة لطنجة\nسس الطريق السريع 1 ميناء طنجة المتوسط المنطقة الصناعبة مرتيل 6 6 / _- المنطقة لصناعية\nمنصة استقبال المنطقة الصناعية تطوان 1:\n\n1 قطب فلاحي\n\nبمساحة 150 هسكتار انيه\n\n0 3+ هكتار\n\n4 مناطق تسريع صناعي بمساحة\nإجمالية قدرها 2.500 هكتار\n\n1 منطقة ترحيل الخدمات\nبمساحة 20 هكتار\n\n© مناطق صناعية متعددة\n\nالقطاعات بمساحة إجمالية\nتبلغ 700 هكتار ل القطب الفلاحي الصناعي اللوكوس\n\n6 مناطق أنشطة اقتصادية\n\nهكتا\nبمساحةتقدربحوالي 160صكتار 3 ككتار\n\nمنطقة الأنشطة الإقتصادية وزان\n\n1 منطقة لوجستية حرة\n\nيا ألم\n\nل م\nفنل زم شا ل نم عع دمرىء بس\n\nالعرض الترابي\nللاستثمار\n\n.إن كنتم هناء فأنتم في كل مكان؟؟\n\nوزو سلما والشسية وتشيع الساسيي\n4 لوتيد م لاصو ا\nال ع عرو تي ات مها م\n\nة الصناعية والرقمية في المغرب",
          "source_spans": [
            {
              "page": 34,
              "text": "ا سين\n465 ر. إن كنتم هناء فأنتم في كل مكان؟؟\n\nالعرض الترابي عرض عقاري متنوع مخصص للاستتمار المنتج\n\nللاستتصار ”\n\n-- مصنع رونو\n\n3 2 5 2 الطروق الوظنية 00: 9 اله ١ منطقة الأنشطة الإقتصادية المجد\n2 مناطق تجارية 0 كك ادك الحديحية 5 ميناء المسافرين 0 --89 0 190.900 ._منضفة سشدة بيتتصية تعومة\nبمساحة 160 هسكتار سس الطريق السيار ديكا الصيد ا\nسس قطار البراق ص مطار 1 ٍ المنطقة الحرة لطنجة\nسس الطريق السريع 1 ميناء طنجة المتوسط المنطقة الصناعبة مرتيل 6 6 / _- المنطقة لصناعية\nمنصة استقبال المنطقة الصناعية تطوان 1:\n\n1 قطب فلاحي\n\nبمساحة 150 هسكتار انيه\n\n0 3+ هكتار\n\n4 مناطق تسريع صناعي بمساحة\nإجمالية قدرها 2.500 هكتار\n\n1 منطقة ترحيل الخدمات\nبمساحة 20 هكتار\n\n© مناطق صناعية متعددة\n\nالقطاعات بمساحة إجمالية\nتبلغ 700 هكتار ل القطب الفلاحي الصناعي اللوكوس\n\n6 مناطق أنشطة اقتصادية\n\nهكتا\nبمساحةتقدربحوالي 160صكتار 3 ككتار\n\nمنطقة الأنشطة الإقتصادية وزان\n\n1 منطقة لوجستية حرة"
            },
            {
              "page": 35,
              "text": "يا ألم\n\nل م\nفنل زم شا ل نم عع دمرىء بس\n\nالعرض الترابي\nللاستثمار\n\n.إن كنتم هناء فأنتم في كل مكان؟؟\n\nوزو سلما والشسية وتشيع الساسيي\n4 لوتيد م لاصو ا\nال ع عرو تي ات مها م\n\nة الصناعية والرقمية في المغرب"
            }
          ],
          "dense_score": 0.82328194,
          "ranking_score": 0.82828194,
          "expanded_from_sibling": false,
          "retrieval_chunk_index": 0,
          "retrieval_chunk_count": 2,
          "temporal_scope": {
            "primary_year": null,
            "years_mentioned": [
              2017
            ],
            "reference_period": {
              "type": null,
              "year": null,
              "semester": null,
              "quarter": null,
              "start_date": null,
              "end_date": null
            }
          }
        },
        {
          "evidence_id": "E2",
          "retrieval_chunk_id": "ar_pr_sentation_cri_tta_vf_semantic_005__r001",
          "parent_semantic_chunk_id": "ar_pr_sentation_cri_tta_vf_semantic_005",
          "document_id": "ar_pr_sentation_cri_tta_vf",
          "document_family_id": "cri_presentation",
          "filename": "AR_Presentation_CRI_TTA.json",
          "document_title": "تقديم المركز الجهوي للاستثمار",
          "language": "ar",
          "topic_id": "industrial_ecosystem",
          "content_type": "narrative",
          "semantic_tags": [
            "industrial_ecosystem"
          ],
          "heading_path": [
            "المنظومة الصناعية"
          ],
          "page_start": 11,
          "page_end": 11,
          "source_pages": [
            11
          ],
          "text": "عو\n\nاكيم\n\nيل\n\nإن كنتم هناء فأنتم في كل مكان؟\n\nمزايا الجهة 2/2 طنجة-تطوان-الحسيمة. قطب اقتصادى تنافسي على الصعيد الوطني\n\nبإشعاع دولي\n\nجودة حياة مميزة\nلله مناخ معتدل\n\n3 توفر البنيات التحتية المرافقة والتجهيزات\nالضربيت\n\n© أمن ونظافة الفضاءات العمومية\n\n8 تنشيط ثقافي وسياحي متنوع\n\n7\n\n016\nتك\n\nإطار تحفيزي جذاب\nميثاق الاستثمار\n\nالصندوق الجهوى لدعم الاستثمار\n(بميزانية قدرها مليار درهم) \"/اعم عملم\"\n\nنظام ضريبى تفضيلى لفائدة مناطق\nالتسريع الصناعى والمناطق الحرة\n\nإعفاء من الضريبة على الشركات لمدة 5 سنوات\nالأواى. معدل مخفض بنسبة 6/20 خلال\nالعشرين سنة التالية. إعفاء من الرسوم\nالجمركية. إعفاء من الضريبة على القيمة\nالمضافة\n\nاقتصاد متنوع وأنظمة بيئية ناضجة\n\nيعتمد هيكل الناتج الداخلى الإجمالي\n\nالجهوي أساسا على القطاع الثالثي (46,2»/).\nيليه القطاع الثانوي (34,3»'). ثم الأنشطة\n\nالأولية (9,3/,)\nتتوفر الجهة على قطاعات اقتصادية رائدة,\n\nمثل صناعة السيارات. النسيج والملابس,\nالصناعات الغذائية. اللوجستيك. الطاقات\n\nالمتجددة. السياحة, وغيرها\nنضجح المنظومات الاقتصادية وتطور\n\nالفاعلين الاقتصاديين عبر كامل سلسلة\nالقيم (الصناعة. خدمات الدعم. المنعشون\nالعقاريون. هياكل المواكبة..)",
          "source_spans": [
            {
              "page": 11,
              "text": "عو\n\nاكيم\n\nيل\n\nإن كنتم هناء فأنتم في كل مكان؟\n\nمزايا الجهة 2/2 طنجة-تطوان-الحسيمة. قطب اقتصادى تنافسي على الصعيد الوطني\n\nبإشعاع دولي\n\nجودة حياة مميزة\nلله مناخ معتدل\n\n3 توفر البنيات التحتية المرافقة والتجهيزات\nالضربيت\n\n© أمن ونظافة الفضاءات العمومية\n\n8 تنشيط ثقافي وسياحي متنوع\n\n7\n\n016\nتك\n\nإطار تحفيزي جذاب\nميثاق الاستثمار\n\nالصندوق الجهوى لدعم الاستثمار\n(بميزانية قدرها مليار درهم) \"/اعم عملم\"\n\nنظام ضريبى تفضيلى لفائدة مناطق\nالتسريع الصناعى والمناطق الحرة\n\nإعفاء من الضريبة على الشركات لمدة 5 سنوات\nالأواى. معدل مخفض بنسبة 6/20 خلال\nالعشرين سنة التالية. إعفاء من الرسوم\nالجمركية. إعفاء من الضريبة على القيمة\nالمضافة\n\nاقتصاد متنوع وأنظمة بيئية ناضجة\n\nيعتمد هيكل الناتج الداخلى الإجمالي\n\nالجهوي أساسا على القطاع الثالثي (46,2»/).\nيليه القطاع الثانوي (34,3»'). ثم الأنشطة\n\nالأولية (9,3/,)\nتتوفر الجهة على قطاعات اقتصادية رائدة,\n\nمثل صناعة السيارات. النسيج والملابس,\nالصناعات الغذائية. اللوجستيك. الطاقات\n\nالمتجددة. السياحة, وغيرها\nنضجح المنظومات الاقتصادية وتطور\n\nالفاعلين الاقتصاديين عبر كامل سلسلة\nالقيم (الصناعة. خدمات الدعم. المنعشون\nالعقاريون. هياكل المواكبة..)"
            }
          ],
          "dense_score": 0.81974673,
          "ranking_score": 0.82474673,
          "expanded_from_sibling": false,
          "retrieval_chunk_index": 0,
          "retrieval_chunk_count": 1,
          "temporal_scope": {
            "primary_year": null,
            "years_mentioned": [],
            "reference_period": {
              "type": null,
              "year": null,
              "semester": null,
              "quarter": null,
              "start_date": null,
              "end_date": null
            }
          }
        },
        {
          "evidence_id": "E3",
          "retrieval_chunk_id": "arabe_chiffres_cles_2025_chunk_007__r001",
          "parent_semantic_chunk_id": "arabe_chiffres_cles_2025_chunk_007",
          "document_id": "arabe_chiffres_cles_2025",
          "document_family_id": "chiffres_cles_2025",
          "filename": "Arabe_Chiffres_cles_2025.json",
          "document_title": "المؤشرات الرئيسية والإحصائيات",
          "language": "ar",
          "topic_id": "sector_investment",
          "content_type": "statistics",
          "semantic_tags": [
            "sector_investment",
            "industrial_investment"
          ],
          "heading_path": [
            "حصيلة اللجنة الجهوية الموحدة للاستثمار (4/6)"
          ],
          "page_start": 7,
          "page_end": 7,
          "source_pages": [
            7
          ],
          "text": "حصيلة اللجنة الجهوية الموحدة للاستثمار (4/6)\nالجهة تعزز تموقعها الصناعي كرافعة لنموها الاقتصادي\nلقد اختاروا الجهة سنة 2025\n\nعدد المشاريع\nقيمة الاستثمار (مليار درهم)\nعدد الوظائف\n\n278 ملف\n+30 مليار درهم من الاستثمارات\n+43 800 منصب شغل متوقع\n+430 هكتاراً تمت تعبئتها\n\nطنجة\nالعرائش\nوزان\nشفشاون\nتطوان\nالحسيمة\n\nالمنطقة الحرة بطنجة: 67 | 1,30 | 5 464\nمنطقة التسريع الصناعي طنجة - أوطموتيف سيتي: 88 | 10,08 | 21 389\nطنجة تيك: 13 | 1,28 | 1 018\nالقطب الفلاحي اللوكوس: 22 | 7,39 | 5 392\nالمنطقة الاقتصادية أصيلة: 13 | 0,22 | 1 216\nالمنطقة الصناعية كزناية: 18 | 0,67 | 1 852\nمنطقة الأنشطة الاقتصادية قصر بجير: 5 | 0,04 | 826\nمنطقة الأنشطة الاقتصادية وزان: 3 | 0,19 | 564\nمنطقة الأنشطة الاقتصادية آيت قمرة: 7 | 0,11 | 295\nمنطقة الأنشطة الاقتصادية إمزورن: 4 | 0,01 | 170\nتطوان بارك\nمنطقة الأنشطة الاقتصادية حيدارة\nM’DIQ\nFNIDEQ\n\nwww.investangier.com\n07",
          "source_spans": [
            {
              "page": 7,
              "text": "حصيلة اللجنة الجهوية الموحدة للاستثمار (4/6)\nالجهة تعزز تموقعها الصناعي كرافعة لنموها الاقتصادي\nلقد اختاروا الجهة سنة 2025\n\nعدد المشاريع\nقيمة الاستثمار (مليار درهم)\nعدد الوظائف\n\n278 ملف\n+30 مليار درهم من الاستثمارات\n+43 800 منصب شغل متوقع\n+430 هكتاراً تمت تعبئتها\n\nطنجة\nالعرائش\nوزان\nشفشاون\nتطوان\nالحسيمة\n\nالمنطقة الحرة بطنجة: 67 | 1,30 | 5 464\nمنطقة التسريع الصناعي طنجة - أوطموتيف سيتي: 88 | 10,08 | 21 389\nطنجة تيك: 13 | 1,28 | 1 018\nالقطب الفلاحي اللوكوس: 22 | 7,39 | 5 392\nالمنطقة الاقتصادية أصيلة: 13 | 0,22 | 1 216\nالمنطقة الصناعية كزناية: 18 | 0,67 | 1 852\nمنطقة الأنشطة الاقتصادية قصر بجير: 5 | 0,04 | 826\nمنطقة الأنشطة الاقتصادية وزان: 3 | 0,19 | 564\nمنطقة الأنشطة الاقتصادية آيت قمرة: 7 | 0,11 | 295\nمنطقة الأنشطة الاقتصادية إمزورن: 4 | 0,01 | 170\nتطوان بارك\nمنطقة الأنشطة الاقتصادية حيدارة\nM’DIQ\nFNIDEQ\n\nwww.investangier.com\n07"
            }
          ],
          "dense_score": 0.8153165,
          "ranking_score": 0.8203165,
          "expanded_from_sibling": false,
          "retrieval_chunk_index": 0,
          "retrieval_chunk_count": 1,
          "temporal_scope": {
            "primary_year": 2025,
            "years_mentioned": [
              2025
            ],
            "reference_period": {
              "type": "year",
              "year": 2025,
              "semester": null,
              "quarter": null,
              "start_date": null,
              "end_date": null
            }
          }
        },
        {
          "evidence_id": "E4",
          "retrieval_chunk_id": "ar_pr_sentation_cri_tta_vf_semantic_008__r001",
          "parent_semantic_chunk_id": "ar_pr_sentation_cri_tta_vf_semantic_008",
          "document_id": "ar_pr_sentation_cri_tta_vf",
          "document_family_id": "cri_presentation",
          "filename": "AR_Presentation_CRI_TTA.json",
          "document_title": "تقديم المركز الجهوي للاستثمار",
          "language": "ar",
          "topic_id": "industrial_ecosystem",
          "content_type": "narrative",
          "semantic_tags": [
            "industrial_ecosystem"
          ],
          "heading_path": [
            "المنظومة الصناعية"
          ],
          "page_start": 14,
          "page_end": 15,
          "source_pages": [
            14,
            15
          ],
          "text": "الصناعة\n\nإن كنتم هناء فأنتم في كل مكان؟؟\n\nال ار\n\nثاني قطب صناعي في المغرب التوزيع القطاعي للرقم الاستدلالي للأعمال الصناعية الجهوية\n\nصناعات أخرى\n12\n\nالصناعة الغذائية\nصناعة السيارات 2\n\nثاني أكبر مساهم في الصادرات 549\n\n| ثاني مساهم في حجم الأعمال\n\nالكهرباء\nأول جهة من خلال تركيز رأس المال وال لكترونيات [الأجنى 6\n\n0 مخزون العمالة للقطاع\nالصناعي على المستوى الوطني\n\nالألبسة والنسيج\n\n12\n\n() مقياس الصناعة المغربية لسنة 2022\n(2) الحسابات الجهوية لسنة 2022. المندوبية السامية للتخطيط\n\n06 فتن الناتج المحلي الإجمالي\nالصناعي الوطني (2)\n\n06 من الناتج المحلي الإجمالي\nالجهوي\n\n145,4 مليار درهم في حجم الأعمال\n\n7 مليار درهم في الصادرات\n\n70 مساهمة المنطقة في\nخلق القيمة المضافة ()\n\nحوالي 250 ألف وظيفة",
          "source_spans": [
            {
              "page": 14,
              "text": "الصناعة"
            },
            {
              "page": 15,
              "text": "إن كنتم هناء فأنتم في كل مكان؟؟\n\nال ار\n\nثاني قطب صناعي في المغرب التوزيع القطاعي للرقم الاستدلالي للأعمال الصناعية الجهوية\n\nصناعات أخرى\n12\n\nالصناعة الغذائية\nصناعة السيارات 2\n\nثاني أكبر مساهم في الصادرات 549\n\n| ثاني مساهم في حجم الأعمال\n\nالكهرباء\nأول جهة من خلال تركيز رأس المال وال لكترونيات [الأجنى 6\n\n0 مخزون العمالة للقطاع\nالصناعي على المستوى الوطني\n\nالألبسة والنسيج\n\n12\n\n() مقياس الصناعة المغربية لسنة 2022\n(2) الحسابات الجهوية لسنة 2022. المندوبية السامية للتخطيط\n\n06 فتن الناتج المحلي الإجمالي\nالصناعي الوطني (2)\n\n06 من الناتج المحلي الإجمالي\nالجهوي\n\n145,4 مليار درهم في حجم الأعمال\n\n7 مليار درهم في الصادرات\n\n70 مساهمة المنطقة في\nخلق القيمة المضافة ()\n\nحوالي 250 ألف وظيفة"
            }
          ],
          "dense_score": 0.8168807,
          "ranking_score": 0.8198807,
          "expanded_from_sibling": false,
          "retrieval_chunk_index": 0,
          "retrieval_chunk_count": 1,
          "temporal_scope": {
            "primary_year": null,
            "years_mentioned": [
              2022
            ],
            "reference_period": {
              "type": null,
              "year": null,
              "semester": null,
              "quarter": null,
              "start_date": null,
              "end_date": null
            }
          }
        },
        {
          "evidence_id": "E5",
          "retrieval_chunk_id": "ar_pr_sentation_cri_tta_vf_semantic_014__r001",
          "parent_semantic_chunk_id": "ar_pr_sentation_cri_tta_vf_semantic_014",
          "document_id": "ar_pr_sentation_cri_tta_vf",
          "document_family_id": "cri_presentation",
          "filename": "AR_Presentation_CRI_TTA.json",
          "document_title": "تقديم المركز الجهوي للاستثمار",
          "language": "ar",
          "topic_id": "industrial_ecosystem",
          "content_type": "narrative",
          "semantic_tags": [
            "industrial_ecosystem"
          ],
          "heading_path": [
            "المنظومة الصناعية"
          ],
          "page_start": 27,
          "page_end": 27,
          "source_pages": [
            27
          ],
          "text": "1 س0 000 000\n\nالقع 00 لالم عن لاجس م ل 2\n\nقطاع الصناعة ات قوية للتنمية الزراعية الصناعية مدعومة بالقطب الفلاحى الصناعى\n\nظ 2 7 من رقم المعاملات\n\nظ أ> 150 هكتار من المساحة\nا الصناعية الجهوية\n\nامك منها 50 هكتار كمرحلة أولى\n\n80 مليون درهم كلفة\n\nعلى المستوى الجهوي\n\nإحم 36 مشروعاً تم تثبيته\n\nالسلاسل الرائدة\n\nاسسمسسير\n\n© التغليف واللوجستيك\n\nظ 0 5 مليار درهم كاستثمارات مرتقبة\n\nعلى المدى البعيد\n\nظ 2 0ه منصب شغل متوقع\n\nلقد اختاروا الجهة\n\nا\n\n7/5 معرمنراوى #ممناعهكدن)» 7 [| /©#١\nكوم ظ 8 ١ سزنة ديات 0 تهت",
          "source_spans": [
            {
              "page": 27,
              "text": "1 س0 000 000\n\nالقع 00 لالم عن لاجس م ل 2\n\nقطاع الصناعة ات قوية للتنمية الزراعية الصناعية مدعومة بالقطب الفلاحى الصناعى\n\nظ 2 7 من رقم المعاملات\n\nظ أ> 150 هكتار من المساحة\nا الصناعية الجهوية\n\nامك منها 50 هكتار كمرحلة أولى\n\n80 مليون درهم كلفة\n\nعلى المستوى الجهوي\n\nإحم 36 مشروعاً تم تثبيته\n\nالسلاسل الرائدة\n\nاسسمسسير\n\n© التغليف واللوجستيك\n\nظ 0 5 مليار درهم كاستثمارات مرتقبة\n\nعلى المدى البعيد\n\nظ 2 0ه منصب شغل متوقع\n\nلقد اختاروا الجهة\n\nا\n\n7/5 معرمنراوى #ممناعهكدن)» 7 [| /©#١\nكوم ظ 8 ١ سزنة ديات 0 تهت"
            }
          ],
          "dense_score": 0.8101099,
          "ranking_score": 0.8111099,
          "expanded_from_sibling": false,
          "retrieval_chunk_index": 0,
          "retrieval_chunk_count": 1,
          "temporal_scope": {
            "primary_year": null,
            "years_mentioned": [],
            "reference_period": {
              "type": null,
              "year": null,
              "semester": null,
              "quarter": null,
              "start_date": null,
              "end_date": null
            }
          }
        }
      ],
      "status": "review_required"
    },
    "Q036": {
      "query": {
        "query_id": "Q036",
        "language": "es",
        "question": "¿Qué oportunidades de inversión existen en el sector turístico?",
        "category": "investment_opportunity",
        "explicit_year": null,
        "expected_topics": [
          "investment_opportunity",
          "tourism"
        ],
        "expected_document_families": [
          "investors_guide_territorial_opportunities"
        ],
        "acceptable_languages": [
          "es",
          "fr",
          "en"
        ]
      },
      "baseline_v1": [
        {
          "chunk_id": "chiffres_cles_crui_1er_semestre_2024_espagnol_p4_c1",
          "document_id": "chiffres_cles_crui_1er_semestre_2024_espagnol",
          "document_family_id": "crui_key_figures_2024_h1",
          "filename": "Chiffres clés CRUI 1er semestre 2024_Espagnol.pdf",
          "language": "es",
          "page": 4,
          "page_start": 4,
          "page_end": 4,
          "source_pages": [
            4
          ],
          "dense_score": 0.84429896,
          "ranking_score": 0.84429896,
          "retrieval_score": 0.84429896,
          "final_score": 0.84429896,
          "text": "¡Una vez aquí, está en todas partes!\n\nEl sector industrial continúa su excepcional crecimiento con más de la mitad de las inversiones aprobadas.\n\nIndustria: 83%\nTurismo: 7%\nOtros sectores: 10%\n\nwww.investangier.com"
        },
        {
          "chunk_id": "investment_business_support_single_window_es_p12_c1",
          "document_id": "investment_business_support_single_window_es",
          "document_family_id": "investment_business_support_single_window",
          "filename": "Investment and Business Support Single Window_ES.pdf",
          "language": "es",
          "page": 12,
          "page_start": 12,
          "page_end": 12,
          "source_pages": [
            12
          ],
          "dense_score": 0.8391863,
          "ranking_score": 0.8391863,
          "retrieval_score": 0.8391863,
          "final_score": 0.8391863,
          "text": "GUÍA DE LA OFERTA TERRITORIAL DE LAS OPORTUNIDADES DE INVERSIÓN Y ASESORAMIENTO\n\nEl Centro Regional de Inversiones de la región Tánger-Tetuán-Alhucemas lanzó una nueva guía sobre “La oferta territorial de las oportunidades de inversión y asesoramiento”. Un entregable, fruto de varios meses de trabajo, convergencia, ideación e inteligencia colectiva entre los diferentes actores económicos de la región.\n\nLa guía incluye también un banco de proyectos listo para utilizar, en diversos sectores y territorios, contiene 50 oportunidades de inversión en toda la región, y traza un mapa de los actores de acompañamiento que intervienen en toda la cadena de valor empresarial, con el objetivo de orientar a los inversores hacia nuevas áreas de inversión y facilitarles el acceso, a través de un enfoque optimizado y personalizado en nuestro portal de acompañamiento digital Manar Al Moustatmir, y toda la información relacionada con las ofertas de asesoramiento propuestas por los organismos especializados en la materia, cada uno según su ámbito de intervención.\n\nCon esta nueva guía, sencilla y práctica, los inversores y los emprendedores de proyectos encontrarán su camino hacia el mundo del emprendimiento y la inversión, y descubrirán todas las herramientas necesarias para el éxito de sus proyectos.\n\nEscanear para descargar\n\n12"
        },
        {
          "chunk_id": "chiffres_cles_crui_1er_semestre_2024_espagnol_p3_c1",
          "document_id": "chiffres_cles_crui_1er_semestre_2024_espagnol",
          "document_family_id": "crui_key_figures_2024_h1",
          "filename": "Chiffres clés CRUI 1er semestre 2024_Espagnol.pdf",
          "language": "es",
          "page": 3,
          "page_start": 3,
          "page_end": 3,
          "source_pages": [
            3
          ],
          "dense_score": 0.8362442,
          "ranking_score": 0.8362442,
          "retrieval_score": 0.8362442,
          "final_score": 0.8362442,
          "text": "¡Una vez aquí, está en todas partes!\n\nDesglose del volumen de inversión por sector\n\nEl sector industrial continúa su excepcional crecimiento con más de la mitad de las inversiones aprobadas.\n\nTotal de inversiones: 40,76 mil millones MAD\n\nIndustria: 54%\nTurismo: 22%\nEnergía y minas: 15%\nOtros sectores: 6%\nComercio: 2%\nConstrucción y Obras Públicas: 1%\n\nwww.investangier.com"
        },
        {
          "chunk_id": "manar_al_moustatmir_eng_png_p11_c1",
          "document_id": "manar_al_moustatmir_eng_png",
          "document_family_id": "manar_al_moustatmir_news_2023",
          "filename": "Manar Al Moustatmir ENG PNG Latest version.pdf",
          "language": "en",
          "page": 11,
          "page_start": 11,
          "page_end": 11,
          "source_pages": [
            11
          ],
          "dense_score": 0.83402056,
          "ranking_score": 0.83402056,
          "retrieval_score": 0.83402056,
          "final_score": 0.83402056,
          "text": "Focus on TOURISM\nwww.investangier.com"
        },
        {
          "chunk_id": "esp_chiffres_cles_annee_2025_p8_c1",
          "document_id": "esp_chiffres_cles_annee_2025",
          "document_family_id": "chiffres_cles_2025",
          "filename": "ESP_Chiffres clés de l_année 2025.pdf",
          "language": "es",
          "page": 8,
          "page_start": 8,
          "page_end": 8,
          "source_pages": [
            8
          ],
          "dense_score": 0.83338654,
          "ranking_score": 0.83338654,
          "retrieval_score": 0.83338654,
          "final_score": 0.83338654,
          "text": "Balance de la CRUI (5/6)\n\nUna fuerte dinámica de inversión turística respaldada por una visión ambiciosa\n\nProyectos operacionales:\n7 establecimientos abiertos en 2025\n+300 habitaciones\n194 millones MAD de inversión\n\nProyectos en curso:\n31 establecimientos en fase de construcción\n2 036 habitaciones adicionales\nincluidas 1 220 habitaciones de 4 estrellas y más\n4,8 mil millones MAD de inversión proyectada\n\nLeyenda del mapa:\nEstablecimiento turístico abierto en 2025\nHabitaciones adicionales abiertas en 2025\nEstablecimiento turístico autorizado en 2025\nHabitaciones adicionales autorizadas en 2025\n\nValores territoriales visibles:\nTanger-Assilah: 3 establecimientos abiertos; 157 habitaciones adicionales abiertas; 19 establecimientos autorizados; 1 643 habitaciones adicionales autorizadas\nFahs Anjra: 2 establecimientos autorizados; 26 habitaciones adicionales autorizadas\nM’Diq-Fnideq: 2 establecimientos autorizados; 119 habitaciones adicionales autorizadas\nTetuán: 1 establecimiento abierto; 63 habitaciones adicionales abiertas; 1 establecimiento autorizado; 9 habitaciones adicionales autorizadas\nChefchaouen: 2 establecimientos abiertos; 24 habitaciones adicionales abiertas; 5 establecimientos autorizados; 215 habitaciones adicionales autorizadas\nAl Hoceima: 2 establecimientos autorizados; 24 habitaciones adicionales autorizadas\nLarache: 1 establecimiento abierto; 50 habitaciones adicionales abiertas\n\nEligieron la Región en 2025\n\nwww.investangier.com\n08"
        }
      ],
      "baseline_v2": [
        {
          "retrieval_chunk_id": "chiffres_cles_crui_1er_semestre_2024_espagnol_chunk_004__r001",
          "document_id": "chiffres_cles_crui_1er_semestre_2024_espagnol",
          "document_family_id": "crui_key_figures_2024_h1",
          "filename": "Chiffres_cles_CRUI_1er_semestre_2024_Espagnol.json",
          "language": "es",
          "topic_id": "industrial_investment",
          "content_type": "statistics",
          "page_start": 4,
          "page_end": 4,
          "source_pages": [
            4
          ],
          "dense_score": 0.8443805,
          "ranking_score": 0.8493805,
          "text": "¡Una vez aquí, está en todas partes!\n\nEl sector industrial continúa su excepcional crecimiento con más de la mitad de las inversiones aprobadas.\n\nIndustria: 83%\nTurismo: 7%\nOtros sectores: 10%\n\nwww.investangier.com"
        },
        {
          "retrieval_chunk_id": "chiffres_cles_crui_1er_semestre_2024_espagnol_chunk_003__r001",
          "document_id": "chiffres_cles_crui_1er_semestre_2024_espagnol",
          "document_family_id": "crui_key_figures_2024_h1",
          "filename": "Chiffres_cles_CRUI_1er_semestre_2024_Espagnol.json",
          "language": "es",
          "topic_id": "sector_distribution",
          "content_type": "statistics",
          "page_start": 3,
          "page_end": 3,
          "source_pages": [
            3
          ],
          "dense_score": 0.8357866,
          "ranking_score": 0.8407866,
          "text": "¡Una vez aquí, está en todas partes!\n\nDesglose del volumen de inversión por sector\n\nEl sector industrial continúa su excepcional crecimiento con más de la mitad de las inversiones aprobadas.\n\nTotal de inversiones: 40,76 mil millones MAD\n\nIndustria: 54%\nTurismo: 22%\nEnergía y minas: 15%\nOtros sectores: 6%\nComercio: 2%\nConstrucción y Obras Públicas: 1%\n\nwww.investangier.com"
        },
        {
          "retrieval_chunk_id": "investment_business_support_single_window_es_phase3f_0011__r001",
          "document_id": "investment_business_support_single_window_es",
          "document_family_id": "investment_business_support_single_window",
          "filename": "Investment_Business_Support_Single_Window_ES.json",
          "language": "es",
          "topic_id": "business_support",
          "content_type": "service",
          "page_start": 12,
          "page_end": 12,
          "source_pages": [
            12
          ],
          "dense_score": 0.8345958,
          "ranking_score": 0.8395958,
          "text": "GUÍA DE LA OFERTA TERRITORIAL DE LAS OPORTUNIDADES DE INVERSIÓN Y ASESORAMIENTO\n\nEl Centro Regional de Inversiones de la región Tánger-Tetuán-Alhucemas lanzó una nueva guía sobre “La oferta territorial de las oportunidades de inversión y asesoramiento”. Un entregable, fruto de varios meses de trabajo, convergencia, ideación e inteligencia colectiva entre los diferentes actores económicos de la región.\n\nLa guía incluye también un banco de proyectos listo para utilizar, en diversos sectores y territorios, contiene 50 oportunidades de inversión en toda la región, y traza un mapa de los actores de acompañamiento que intervienen en toda la cadena de valor empresarial, con el objetivo de orientar a los inversores hacia nuevas áreas de inversión y facilitarles el acceso, a través de un enfoque optimizado y personalizado en nuestro portal de acompañamiento digital Manar Al Moustatmir, y toda la información relacionada con las ofertas de asesoramiento propuestas por los organismos especializados en la materia, cada uno según su ámbito de intervención.\n\nCon esta nueva guía, sencilla y práctica, los inversores y los emprendedores de proyectos encontrarán su camino hacia el mundo del emprendimiento y la inversión, y descubrirán todas las herramientas necesarias para el éxito de sus proyectos.\n\nEscanear para descargar\n\n12"
        },
        {
          "retrieval_chunk_id": "esp_chiffres_cles_annee_2025_chunk_008__r001",
          "document_id": "esp_chiffres_cles_annee_2025",
          "document_family_id": "chiffres_cles_2025",
          "filename": "ESP_Chiffres_cles_annee_2025.json",
          "language": "es",
          "topic_id": "sector_investment",
          "content_type": "statistics",
          "page_start": 8,
          "page_end": 8,
          "source_pages": [
            8
          ],
          "dense_score": 0.83458835,
          "ranking_score": 0.83958835,
          "text": "Balance de la CRUI (5/6)\n\nUna fuerte dinámica de inversión turística respaldada por una visión ambiciosa\n\nProyectos operacionales:\n7 establecimientos abiertos en 2025\n+300 habitaciones\n194 millones MAD de inversión\n\nProyectos en curso:\n31 establecimientos en fase de construcción\n2 036 habitaciones adicionales\nincluidas 1 220 habitaciones de 4 estrellas y más\n4,8 mil millones MAD de inversión proyectada\n\nLeyenda del mapa:\nEstablecimiento turístico abierto en 2025\nHabitaciones adicionales abiertas en 2025\nEstablecimiento turístico autorizado en 2025\nHabitaciones adicionales autorizadas en 2025\n\nValores territoriales visibles:\nTanger-Assilah: 3 establecimientos abiertos; 157 habitaciones adicionales abiertas; 19 establecimientos autorizados; 1 643 habitaciones adicionales autorizadas\nFahs Anjra: 2 establecimientos autorizados; 26 habitaciones adicionales autorizadas\nM’Diq-Fnideq: 2 establecimientos autorizados; 119 habitaciones adicionales autorizadas\nTetuán: 1 establecimiento abierto; 63 habitaciones adicionales abiertas; 1 establecimiento autorizado; 9 habitaciones adicionales autorizadas\nChefchaouen: 2 establecimientos abiertos; 24 habitaciones adicionales abiertas; 5 establecimientos autorizados; 215 habitaciones adicionales autorizadas\nAl Hoceima: 2 establecimientos autorizados; 24 habitaciones adicionales autorizadas\nLarache: 1 establecimiento abierto; 50 habitaciones adicionales abiertas\n\nEligieron la Región en 2025\n\nwww.investangier.com\n08"
        },
        {
          "retrieval_chunk_id": "esp_presentation_cri_tta_vf_semantic_007__r001",
          "document_id": "esp_presentation_cri_tta_vf",
          "document_family_id": "cri_presentation",
          "filename": "ESP_Presentation_CRI_TTA.json",
          "language": "es",
          "topic_id": "territorial_offer",
          "content_type": "narrative",
          "page_start": 7,
          "page_end": 7,
          "source_pages": [
            7
          ],
          "dense_score": 0.8345827,
          "ranking_score": 0.8395827,
          "text": "sl ¿al\n¡Una vez aquí, está en todas partes! E A\n\nINVESTANGIER CeNmEneOCHAL reason\n\nMonografía\n\nAtractivos de la Región\nTánger-Tetuán-Alhucemas\n\nSectores clave de la Región\n\nOferta territorial para la inversión"
        }
      ],
      "experimental_v2": [
        {
          "evidence_id": "E1",
          "retrieval_chunk_id": "chiffres_cles_crui_1er_semestre_2024_espagnol_chunk_004__r001",
          "parent_semantic_chunk_id": "chiffres_cles_crui_1er_semestre_2024_espagnol_chunk_004",
          "document_id": "chiffres_cles_crui_1er_semestre_2024_espagnol",
          "document_family_id": "crui_key_figures_2024_h1",
          "filename": "Chiffres_cles_CRUI_1er_semestre_2024_Espagnol.json",
          "document_title": "Cifras clave y estadísticas",
          "language": "es",
          "topic_id": "industrial_investment",
          "content_type": "statistics",
          "semantic_tags": [
            "sector_distribution",
            "industrial_investment",
            "investment_amount",
            "projected_jobs"
          ],
          "heading_path": [
            "¡Una vez aquí, está en todas partes!"
          ],
          "page_start": 4,
          "page_end": 4,
          "source_pages": [
            4
          ],
          "text": "¡Una vez aquí, está en todas partes!\n\nEl sector industrial continúa su excepcional crecimiento con más de la mitad de las inversiones aprobadas.\n\nIndustria: 83%\nTurismo: 7%\nOtros sectores: 10%\n\nwww.investangier.com",
          "source_spans": [
            {
              "page": 4,
              "text": "¡Una vez aquí, está en todas partes!\n\nEl sector industrial continúa su excepcional crecimiento con más de la mitad de las inversiones aprobadas.\n\nIndustria: 83%\nTurismo: 7%\nOtros sectores: 10%\n\nwww.investangier.com"
            }
          ],
          "dense_score": 0.8443805,
          "ranking_score": 0.8493805,
          "expanded_from_sibling": false,
          "retrieval_chunk_index": 0,
          "retrieval_chunk_count": 1,
          "temporal_scope": {
            "primary_year": 2024,
            "years_mentioned": [],
            "reference_period": {
              "type": "semester",
              "year": 2024,
              "semester": 1,
              "quarter": null,
              "start_date": null,
              "end_date": null
            }
          }
        },
        {
          "evidence_id": "E2",
          "retrieval_chunk_id": "chiffres_cles_crui_1er_semestre_2024_espagnol_chunk_003__r001",
          "parent_semantic_chunk_id": "chiffres_cles_crui_1er_semestre_2024_espagnol_chunk_003",
          "document_id": "chiffres_cles_crui_1er_semestre_2024_espagnol",
          "document_family_id": "crui_key_figures_2024_h1",
          "filename": "Chiffres_cles_CRUI_1er_semestre_2024_Espagnol.json",
          "document_title": "Cifras clave y estadísticas",
          "language": "es",
          "topic_id": "sector_distribution",
          "content_type": "statistics",
          "semantic_tags": [
            "sector_distribution",
            "investment_amount"
          ],
          "heading_path": [
            "¡Una vez aquí, está en todas partes!"
          ],
          "page_start": 3,
          "page_end": 3,
          "source_pages": [
            3
          ],
          "text": "¡Una vez aquí, está en todas partes!\n\nDesglose del volumen de inversión por sector\n\nEl sector industrial continúa su excepcional crecimiento con más de la mitad de las inversiones aprobadas.\n\nTotal de inversiones: 40,76 mil millones MAD\n\nIndustria: 54%\nTurismo: 22%\nEnergía y minas: 15%\nOtros sectores: 6%\nComercio: 2%\nConstrucción y Obras Públicas: 1%\n\nwww.investangier.com",
          "source_spans": [
            {
              "page": 3,
              "text": "¡Una vez aquí, está en todas partes!\n\nDesglose del volumen de inversión por sector\n\nEl sector industrial continúa su excepcional crecimiento con más de la mitad de las inversiones aprobadas.\n\nTotal de inversiones: 40,76 mil millones MAD\n\nIndustria: 54%\nTurismo: 22%\nEnergía y minas: 15%\nOtros sectores: 6%\nComercio: 2%\nConstrucción y Obras Públicas: 1%\n\nwww.investangier.com"
            }
          ],
          "dense_score": 0.8357866,
          "ranking_score": 0.8407866,
          "expanded_from_sibling": false,
          "retrieval_chunk_index": 0,
          "retrieval_chunk_count": 1,
          "temporal_scope": {
            "primary_year": 2024,
            "years_mentioned": [],
            "reference_period": {
              "type": "semester",
              "year": 2024,
              "semester": 1,
              "quarter": null,
              "start_date": null,
              "end_date": null
            }
          }
        },
        {
          "evidence_id": "E3",
          "retrieval_chunk_id": "investment_business_support_single_window_es_phase3f_0011__r001",
          "parent_semantic_chunk_id": "investment_business_support_single_window_es_phase3f_0011",
          "document_id": "investment_business_support_single_window_es",
          "document_family_id": "investment_business_support_single_window",
          "filename": "Investment_Business_Support_Single_Window_ES.json",
          "document_title": "Apoyo a los inversores y las empresas",
          "language": "es",
          "topic_id": "business_support",
          "content_type": "service",
          "semantic_tags": [
            "business_support",
            "investment_guide"
          ],
          "heading_path": [
            "Guía de la oferta territorial"
          ],
          "page_start": 12,
          "page_end": 12,
          "source_pages": [
            12
          ],
          "text": "GUÍA DE LA OFERTA TERRITORIAL DE LAS OPORTUNIDADES DE INVERSIÓN Y ASESORAMIENTO\n\nEl Centro Regional de Inversiones de la región Tánger-Tetuán-Alhucemas lanzó una nueva guía sobre “La oferta territorial de las oportunidades de inversión y asesoramiento”. Un entregable, fruto de varios meses de trabajo, convergencia, ideación e inteligencia colectiva entre los diferentes actores económicos de la región.\n\nLa guía incluye también un banco de proyectos listo para utilizar, en diversos sectores y territorios, contiene 50 oportunidades de inversión en toda la región, y traza un mapa de los actores de acompañamiento que intervienen en toda la cadena de valor empresarial, con el objetivo de orientar a los inversores hacia nuevas áreas de inversión y facilitarles el acceso, a través de un enfoque optimizado y personalizado en nuestro portal de acompañamiento digital Manar Al Moustatmir, y toda la información relacionada con las ofertas de asesoramiento propuestas por los organismos especializados en la materia, cada uno según su ámbito de intervención.\n\nCon esta nueva guía, sencilla y práctica, los inversores y los emprendedores de proyectos encontrarán su camino hacia el mundo del emprendimiento y la inversión, y descubrirán todas las herramientas necesarias para el éxito de sus proyectos.\n\nEscanear para descargar\n\n12",
          "source_spans": [
            {
              "page": 12,
              "text": "GUÍA DE LA OFERTA TERRITORIAL DE LAS OPORTUNIDADES DE INVERSIÓN Y ASESORAMIENTO\n\nEl Centro Regional de Inversiones de la región Tánger-Tetuán-Alhucemas lanzó una nueva guía sobre “La oferta territorial de las oportunidades de inversión y asesoramiento”. Un entregable, fruto de varios meses de trabajo, convergencia, ideación e inteligencia colectiva entre los diferentes actores económicos de la región.\n\nLa guía incluye también un banco de proyectos listo para utilizar, en diversos sectores y territorios, contiene 50 oportunidades de inversión en toda la región, y traza un mapa de los actores de acompañamiento que intervienen en toda la cadena de valor empresarial, con el objetivo de orientar a los inversores hacia nuevas áreas de inversión y facilitarles el acceso, a través de un enfoque optimizado y personalizado en nuestro portal de acompañamiento digital Manar Al Moustatmir, y toda la información relacionada con las ofertas de asesoramiento propuestas por los organismos especializados en la materia, cada uno según su ámbito de intervención.\n\nCon esta nueva guía, sencilla y práctica, los inversores y los emprendedores de proyectos encontrarán su camino hacia el mundo del emprendimiento y la inversión, y descubrirán todas las herramientas necesarias para el éxito de sus proyectos.\n\nEscanear para descargar\n\n12"
            }
          ],
          "dense_score": 0.8345958,
          "ranking_score": 0.8395958,
          "expanded_from_sibling": false,
          "retrieval_chunk_index": 0,
          "retrieval_chunk_count": 1,
          "temporal_scope": {
            "primary_year": null,
            "years_mentioned": [],
            "reference_period": {
              "type": null,
              "year": null,
              "semester": null,
              "quarter": null,
              "start_date": null,
              "end_date": null
            }
          }
        },
        {
          "evidence_id": "E4",
          "retrieval_chunk_id": "esp_chiffres_cles_annee_2025_chunk_008__r001",
          "parent_semantic_chunk_id": "esp_chiffres_cles_annee_2025_chunk_008",
          "document_id": "esp_chiffres_cles_annee_2025",
          "document_family_id": "chiffres_cles_2025",
          "filename": "ESP_Chiffres_cles_annee_2025.json",
          "document_title": "Cifras clave y estadísticas",
          "language": "es",
          "topic_id": "sector_investment",
          "content_type": "statistics",
          "semantic_tags": [
            "sector_investment",
            "tourism_investment"
          ],
          "heading_path": [
            "Balance de la CRUI (5/6)"
          ],
          "page_start": 8,
          "page_end": 8,
          "source_pages": [
            8
          ],
          "text": "Balance de la CRUI (5/6)\n\nUna fuerte dinámica de inversión turística respaldada por una visión ambiciosa\n\nProyectos operacionales:\n7 establecimientos abiertos en 2025\n+300 habitaciones\n194 millones MAD de inversión\n\nProyectos en curso:\n31 establecimientos en fase de construcción\n2 036 habitaciones adicionales\nincluidas 1 220 habitaciones de 4 estrellas y más\n4,8 mil millones MAD de inversión proyectada\n\nLeyenda del mapa:\nEstablecimiento turístico abierto en 2025\nHabitaciones adicionales abiertas en 2025\nEstablecimiento turístico autorizado en 2025\nHabitaciones adicionales autorizadas en 2025\n\nValores territoriales visibles:\nTanger-Assilah: 3 establecimientos abiertos; 157 habitaciones adicionales abiertas; 19 establecimientos autorizados; 1 643 habitaciones adicionales autorizadas\nFahs Anjra: 2 establecimientos autorizados; 26 habitaciones adicionales autorizadas\nM’Diq-Fnideq: 2 establecimientos autorizados; 119 habitaciones adicionales autorizadas\nTetuán: 1 establecimiento abierto; 63 habitaciones adicionales abiertas; 1 establecimiento autorizado; 9 habitaciones adicionales autorizadas\nChefchaouen: 2 establecimientos abiertos; 24 habitaciones adicionales abiertas; 5 establecimientos autorizados; 215 habitaciones adicionales autorizadas\nAl Hoceima: 2 establecimientos autorizados; 24 habitaciones adicionales autorizadas\nLarache: 1 establecimiento abierto; 50 habitaciones adicionales abiertas\n\nEligieron la Región en 2025\n\nwww.investangier.com\n08",
          "source_spans": [
            {
              "page": 8,
              "text": "Balance de la CRUI (5/6)\n\nUna fuerte dinámica de inversión turística respaldada por una visión ambiciosa\n\nProyectos operacionales:\n7 establecimientos abiertos en 2025\n+300 habitaciones\n194 millones MAD de inversión\n\nProyectos en curso:\n31 establecimientos en fase de construcción\n2 036 habitaciones adicionales\nincluidas 1 220 habitaciones de 4 estrellas y más\n4,8 mil millones MAD de inversión proyectada\n\nLeyenda del mapa:\nEstablecimiento turístico abierto en 2025\nHabitaciones adicionales abiertas en 2025\nEstablecimiento turístico autorizado en 2025\nHabitaciones adicionales autorizadas en 2025\n\nValores territoriales visibles:\nTanger-Assilah: 3 establecimientos abiertos; 157 habitaciones adicionales abiertas; 19 establecimientos autorizados; 1 643 habitaciones adicionales autorizadas\nFahs Anjra: 2 establecimientos autorizados; 26 habitaciones adicionales autorizadas\nM’Diq-Fnideq: 2 establecimientos autorizados; 119 habitaciones adicionales autorizadas\nTetuán: 1 establecimiento abierto; 63 habitaciones adicionales abiertas; 1 establecimiento autorizado; 9 habitaciones adicionales autorizadas\nChefchaouen: 2 establecimientos abiertos; 24 habitaciones adicionales abiertas; 5 establecimientos autorizados; 215 habitaciones adicionales autorizadas\nAl Hoceima: 2 establecimientos autorizados; 24 habitaciones adicionales autorizadas\nLarache: 1 establecimiento abierto; 50 habitaciones adicionales abiertas\n\nEligieron la Región en 2025\n\nwww.investangier.com\n08"
            }
          ],
          "dense_score": 0.83458835,
          "ranking_score": 0.83958835,
          "expanded_from_sibling": false,
          "retrieval_chunk_index": 0,
          "retrieval_chunk_count": 1,
          "temporal_scope": {
            "primary_year": 2025,
            "years_mentioned": [
              2025
            ],
            "reference_period": {
              "type": "year",
              "year": 2025,
              "semester": null,
              "quarter": null,
              "start_date": null,
              "end_date": null
            }
          }
        },
        {
          "evidence_id": "E5",
          "retrieval_chunk_id": "esp_presentation_cri_tta_vf_semantic_007__r001",
          "parent_semantic_chunk_id": "esp_presentation_cri_tta_vf_semantic_007",
          "document_id": "esp_presentation_cri_tta_vf",
          "document_family_id": "cri_presentation",
          "filename": "ESP_Presentation_CRI_TTA.json",
          "document_title": "Presentación del Centro Regional de Inversiones",
          "language": "es",
          "topic_id": "territorial_offer",
          "content_type": "narrative",
          "semantic_tags": [
            "territorial_offer"
          ],
          "heading_path": [
            "Oferta territorial para la inversión"
          ],
          "page_start": 7,
          "page_end": 7,
          "source_pages": [
            7
          ],
          "text": "sl ¿al\n¡Una vez aquí, está en todas partes! E A\n\nINVESTANGIER CeNmEneOCHAL reason\n\nMonografía\n\nAtractivos de la Región\nTánger-Tetuán-Alhucemas\n\nSectores clave de la Región\n\nOferta territorial para la inversión",
          "source_spans": [
            {
              "page": 7,
              "text": "sl ¿al\n¡Una vez aquí, está en todas partes! E A\n\nINVESTANGIER CeNmEneOCHAL reason\n\nMonografía\n\nAtractivos de la Región\nTánger-Tetuán-Alhucemas\n\nSectores clave de la Región\n\nOferta territorial para la inversión"
            }
          ],
          "dense_score": 0.8345827,
          "ranking_score": 0.8395827,
          "expanded_from_sibling": false,
          "retrieval_chunk_index": 0,
          "retrieval_chunk_count": 1,
          "temporal_scope": {
            "primary_year": null,
            "years_mentioned": [],
            "reference_period": {
              "type": null,
              "year": null,
              "semester": null,
              "quarter": null,
              "start_date": null,
              "end_date": null
            }
          }
        }
      ],
      "status": "review_required"
    },
    "Q048": {
      "query": {
        "query_id": "Q048",
        "language": "ar",
        "question": "ما هي فرص الاستثمار الصناعي في المنطقة؟",
        "category": "investment_opportunity",
        "explicit_year": null,
        "expected_topics": [
          "industrial_investment",
          "investment_opportunity"
        ],
        "expected_document_families": [
          "investors_guide_territorial_opportunities",
          "industrial_zones_panorama"
        ],
        "acceptable_languages": [
          "ar",
          "fr",
          "en",
          "es"
        ]
      },
      "baseline_v1": [
        {
          "chunk_id": "chiffres_cles_crui_1er_semestre_2024_arabe_p3_c1",
          "document_id": "chiffres_cles_crui_1er_semestre_2024_arabe",
          "document_family_id": "crui_key_figures_2024_h1",
          "filename": "Chiffres clés CRUI 1er semestre 2024_Arabe.pdf",
          "language": "ar",
          "page": 3,
          "page_start": 3,
          "page_end": 3,
          "source_pages": [
            3
          ],
          "dense_score": 0.8402388,
          "ranking_score": 0.8402388,
          "retrieval_score": 0.8402388,
          "final_score": 0.8402388,
          "text": "إن كنتم هنا، فأنتم في كل مكان\n\nتوزيع حجم الاستثمارات حسب القطاع\n\nيواصل القطاع الصناعي نموه الاستثنائي بأكثر من نصف الاستثمارات التي تمت المصادقة عليها\n\nإجمالي الاستثمارات: 40,76 مليار درهم\n\nالصناعة: 54%\nالسياحة: 22%\nالطاقة والمناجم: 15%\nقطاعات أخرى: 6%\nالتجارة: 2%\nالبناء والأشغال العامة: 1%\n\nwww.investangier.com"
        },
        {
          "chunk_id": "ar_pr_sentation_cri_tta_vf_p41_c1",
          "document_id": "ar_pr_sentation_cri_tta_vf",
          "document_family_id": "cri_presentation",
          "filename": "AR_Présentation CRI TTA VF.pdf",
          "language": "ar",
          "page": 41,
          "page_start": 41,
          "page_end": 41,
          "source_pages": [
            41
          ],
          "dense_score": 0.83517325,
          "ranking_score": 0.83517325,
          "retrieval_score": 0.83517325,
          "final_score": 0.83517325,
          "text": "0\n\nا ع\nالا ع 1 ا\nدقاف <>7 -070000 7\nإن هناء فا كل مكان 58 روه سلما وانشهية ولشر ع الساسات التموطيخ\nدلاء 0\n-\n\n100 ا ا\n\n89 من الشركات راضية عن استقرارها\n2200 يدهة مللجة_'تطواق الكسيفة\n\nأهم حوافز الاستثمار بالجهة اتجاهات وآفاق نمو الأعمال فى المنطقة\n\nجودة الحياة و/229 من المشاركين يعتبرون الوضع الحالي لشركاتهم مرضيًا\n\nم95 مع وجود آفاق متفائلة للنمو على جميع المستويات\n\nالموقع الجغرافي\nا\nومرافق استقبال متطورة0 بنية تحتية؟ض ل\n\nتوفر المهارات؟آ؟آ 0\n21111606061012\n\n00111 |110101010101000 1111 1أ001ظغظك\n\n© توجه صاعد © مستقر © في اتجاه الإنخفاض\n\nالمصدر: استطلاع أي أجرته مؤسسة التمويل الدولية ومجموعة البنك الدولي في عام 2025"
        },
        {
          "chunk_id": "akhbar_al_moustatmir_news_p9_c1",
          "document_id": "akhbar_al_moustatmir_news",
          "document_family_id": "manar_al_moustatmir_news_2023",
          "filename": "Akhbar Al Moustatmir News VA compress.pdf",
          "language": "ar",
          "page": 9,
          "page_start": 9,
          "page_end": 9,
          "source_pages": [
            9
          ],
          "dense_score": 0.83395183,
          "ranking_score": 0.83395183,
          "retrieval_score": 0.83395183,
          "final_score": 0.83395183,
          "text": "03\nwww.investangier.com\n03\nwww.investangier.com\nإطلاق عــرض أرض للإيجــار فــي تطــوان بــارك بموجــب اتفاقيــة الشراكــة\nالمتعلقــة بتعبئــة أراضي المنطقــة الصناعيــة واللوجســتية بتطــوان بــارك\nقطع صناعية9 :2022 يونيو10 الموقعة في\n8\nالمساحة\nالإجمالي\n8\nالمشاريع الصناعية\nالمصادق عليها\n350 MMAD\nمبلغ الاستثمار\n1 000\nالوظائف\nھكتـار( مـن قطـب50) تخصیـص القطـع الأرضیـة على مسـتوى الدفعـة الأولى\nلوكوس الزراعي في العرائش\n47\nالتكلفة\nلإجمالية\nالشركات\n8 000\nالوظائف\nالمساحة\nمبنى117 بدء تشغيل منطقة النشاط الاقتصادي في طنجة البالیة :تخصیص\n150\n457\nفي طور التأسيس"
        },
        {
          "chunk_id": "ar_pr_sentation_cri_tta_vf_p35_c1",
          "document_id": "ar_pr_sentation_cri_tta_vf",
          "document_family_id": "cri_presentation",
          "filename": "AR_Présentation CRI TTA VF.pdf",
          "language": "ar",
          "page": 35,
          "page_start": 35,
          "page_end": 35,
          "source_pages": [
            35
          ],
          "dense_score": 0.833197,
          "ranking_score": 0.833197,
          "retrieval_score": 0.833197,
          "final_score": 0.833197,
          "text": "يا ألم\n\nل م\nفنل زم شا ل نم عع دمرىء بس\n\nالعرض الترابي\nللاستثمار\n\n.إن كنتم هناء فأنتم في كل مكان؟؟\n\nوزو سلما والشسية وتشيع الساسيي\n4 لوتيد م لاصو ا\nال ع عرو تي ات مها م\n\nة الصناعية والرقمية في المغرب\n\nمنصة استقبال تم تقديمها أمام جلالة الملك محمد السادس نصره الله سنة 2017\n\n0 أنشطة\nالطيران\n\nالسيارات\n\nالتجارة الإلكترونية\n. الاتصالات\nالطاقات المتجددة\nالنقل\n\nالأجهزة المنزلية\n\n. الصناعات الدوائية\n2 إنتاج المواد\n\n5 الصناعات الزراعية والغذائية\n\nا\n0\n\nم \" دعق ٍّ\n\n27\nقرارًا بالترخيص للتركيب\nتم منحها\n\nمدينة ذكية تتسع ل 300,000 نسمة\n\nالاستثمار: مليار دولار\nعدد مناصب الشغل يصل إلى 100,000\nالإيرادات: 15 مليار دولار سنوبا\n\nالمساحة: 2,167 هكتارا. منها 947 هكتارا مخصصة\nلمنطقة التسريع د هكتار قيد التطوبر\n4\n\nهكتا الا ١\nالأو 00 التجاري الأولى, من رق\n\n0 11+ 27+\nمنصب شغل متوقع مليار درهم من الاستثمارات\n\nالمنطقة اللوجستيكية طبه كءالا ا مصنع رونو\nكٍ 4 يدق 0 - 0 ع منطقة الأنشطة الإقتصادية مفوغة\n١ 5 منطقة الأنشطة الإقتصادية المجد\nالإقتصادية حيضرة 3 500 م منطقة الأنشطة الإقتصادية العوامة\nك_ المنطقة الحرة لطنجة\nالمنطقة الصناعية مرنيل: المنطقة الصناعية\nكزناية: لهاع هوأرماأهي عل أوعع\n264 1 5\nهكتارًا من الأراضي التي سيتم مشروع أصبح عمليا مشاريع قيد الإنشاء\n\nتعبئتها من خلال المشاريع ع الي\nوافقت عليها اللجنة الجهوية\nالموحدة للاستثمار\n\nون 58 غه عا مومرمج لاكمم روجع\n\n5ع ااانا امعل/ا,عوصة 1"
        },
        {
          "chunk_id": "akhbar_al_moustatmir_news_p4_c1",
          "document_id": "akhbar_al_moustatmir_news",
          "document_family_id": "manar_al_moustatmir_news_2023",
          "filename": "Akhbar Al Moustatmir News VA compress.pdf",
          "language": "ar",
          "page": 4,
          "page_start": 4,
          "page_end": 4,
          "source_pages": [
            4
          ],
          "dense_score": 0.83093226,
          "ranking_score": 0.83093226,
          "retrieval_score": 0.83093226,
          "final_score": 0.83093226,
          "text": "مقدمة\nwww.investangier.com\n،أعزائي القراء\nجهة \nحققتها \nالتي \nالرائعة \nالإنجازات \nببعض \nنشارككم \nأن \nيسرنا \nالحسيمة في مجال الاستثمار الإنتاجي. وتعكس هذه الإنجازات -تطوان-طنجة\nالذكاء الجماعي لمجتمع الاستثمار بأكمله في الجهة، التي أصبحت بسرعة \nقاطرة للتنمية على المستوى الوطني. وبفضل الأصول الطبيعية والاقتصادية \nالعديدة، بالإضافة إلى البنية التحتية ذات المستوى العالمي مثل مجمع ميناء \nطنجة المتوسط والقطار فائق السرعة، وضعت المنطقة نفسها كبوابة طبيعية \nلمفترق طرق أوروبا وإفريقيا وأمريكا وآسيا.\nهذا التحول المبهر يعود إلى رؤية مستنيرة، وضعها صاحب الجلالة الملك محمد \nالسادس، نصره هللا. كما تمثل هذه الرؤية استراتيجية شاملة تركز على جاذبية \nالاستثمارات الإنتاجية، وقد ساهمت في جذب الشركات ذات الشهرة العالمية.\nتم تبني هذه الاستراتيجية بنجاح، حيث أظهرت فوائدها بوضوح من خلال تحقيق \nنتائج ملموسة وإيجابية. فقد تم تقديم عدد كبير من طلبات الاستثمار الواسعة \nالنطاق إلى المركز الجهوي للاستثمار في الجهة، وبفضل الجهود المبذولة، \n709 على2023 ( في سنةCRUI) وافقت اللجنة الجهوية الموحدة للاستثمار\nمشاريع استثمارية. تبلغ الاستثمارات الإجمالية لهذه المشاريع أكثر من \nمليار درهم، والتي من المتوقع أن تسهم في خلق أكثر من 73\n. فرصة عمل مباشر70000"
        }
      ],
      "baseline_v2": [
        {
          "retrieval_chunk_id": "chiffres_cles_crui_1er_semestre_2024_arabe_chunk_003__r001",
          "document_id": "chiffres_cles_crui_1er_semestre_2024_arabe",
          "document_family_id": "crui_key_figures_2024_h1",
          "filename": "Chiffres_cles_CRUI_1er_semestre_2024_Arabe.json",
          "language": "ar",
          "topic_id": "sector_distribution",
          "content_type": "statistics",
          "page_start": 3,
          "page_end": 3,
          "source_pages": [
            3
          ],
          "dense_score": 0.8477998,
          "ranking_score": 0.8527998,
          "text": "إن كنتم هنا، فأنتم في كل مكان\n\nتوزيع حجم الاستثمارات حسب القطاع\n\nيواصل القطاع الصناعي نموه الاستثنائي بأكثر من نصف الاستثمارات التي تمت المصادقة عليها\n\nإجمالي الاستثمارات: 40,76 مليار درهم\n\nالصناعة: 54%\nالسياحة: 22%\nالطاقة والمناجم: 15%\nقطاعات أخرى: 6%\nالتجارة: 2%\nالبناء والأشغال العامة: 1%\n\nwww.investangier.com"
        },
        {
          "retrieval_chunk_id": "akhbar_al_moustatmir_news_phase3f_0006__r001",
          "document_id": "akhbar_al_moustatmir_news",
          "document_family_id": "manar_al_moustatmir_news_2023",
          "filename": "Akhbar_Al_Moustatmir_News.json",
          "language": "ar",
          "topic_id": "investment_news",
          "content_type": "investment_opportunity",
          "page_start": 9,
          "page_end": 9,
          "source_pages": [
            9
          ],
          "dense_score": 0.82433903,
          "ranking_score": 0.83733903,
          "text": "03\nwww.investangier.com\n03\nwww.investangier.com\n إطلاق عــرض أرض للإيجــار فــي تطــوان بــارك بموجــب اتفاقيــة الشراكــة\n المتعلقــة بتعبئــة أراضي المنطقــة الصناعيــة واللوجســتية بتطــوان بــارك\n قطع صناعية9 :2022 يونيو10 الموقعة في\n8\nالمساحة\nالإجمالي\n8\nالمشاريع الصناعية\nالمصادق عليها\n350 MMAD\nمبلغ الاستثمار\n1 000\nالوظائف\n ھكتـار( مـن قطـب50) تخصیـص القطـع الأرضیـة على مسـتوى الدفعـة الأولى\nلوكوس الزراعي في العرائش\n47\n التكلفة\nلإجمالية\nالشركات\n8 000\nالوظائف\nالمساحة\n مبنى117 بدء تشغيل منطقة النشاط الاقتصادي في طنجة البالیة :تخصیص\n150\n457\nفي طور التأسيس"
        },
        {
          "retrieval_chunk_id": "ar_pr_sentation_cri_tta_vf_semantic_019__r001b",
          "document_id": "ar_pr_sentation_cri_tta_vf",
          "document_family_id": "cri_presentation",
          "filename": "AR_Presentation_CRI_TTA.json",
          "language": "ar",
          "topic_id": "territorial_offer",
          "content_type": "narrative",
          "page_start": 35,
          "page_end": 35,
          "source_pages": [
            35
          ],
          "dense_score": 0.83079207,
          "ranking_score": 0.83579207,
          "text": "منصة استقبال تم تقديمها أمام جلالة الملك محمد السادس نصره الله سنة 2017\n\n0 أنشطة\nالطيران\n\nالسيارات\n\nالتجارة الإلكترونية\n. الاتصالات\nالطاقات المتجددة\nالنقل\n\nالأجهزة المنزلية\n\n. الصناعات الدوائية\n2 إنتاج المواد\n\n5 الصناعات الزراعية والغذائية\n\nا\n0\n\nم \" دعق ٍّ\n\n27\nقرارًا بالترخيص للتركيب\nتم منحها\n\nمدينة ذكية تتسع ل 300,000 نسمة\n\nالاستثمار: مليار دولار\nعدد مناصب الشغل يصل إلى 100,000\nالإيرادات: 15 مليار دولار سنوبا\n\nالمساحة: 2,167 هكتارا. منها 947 هكتارا مخصصة\nلمنطقة التسريع د هكتار قيد التطوبر\n4\n\nهكتا الا ١\nالأو 00 التجاري الأولى, من رق\n\n0 11+ 27+\nمنصب شغل متوقع مليار درهم من الاستثمارات\n\nالمنطقة اللوجستيكية طبه كءالا ا مصنع رونو\nكٍ 4 يدق 0 - 0 ع منطقة الأنشطة الإقتصادية مفوغة\n١ 5 منطقة الأنشطة الإقتصادية المجد\nالإقتصادية حيضرة 3 500 م منطقة الأنشطة الإقتصادية العوامة\nك_ المنطقة الحرة لطنجة\nالمنطقة الصناعية مرنيل: المنطقة الصناعية\nكزناية: لهاع هوأرماأهي عل أوعع\n264 1 5\nهكتارًا من الأراضي التي سيتم مشروع أصبح عمليا مشاريع قيد الإنشاء\n\nتعبئتها من خلال المشاريع ع الي\nوافقت عليها اللجنة الجهوية\nالموحدة للاستثمار\n\nون 58 غه عا مومرمج لاكمم روجع\n\n5ع ااانا امعل/ا,عوصة 1"
        },
        {
          "retrieval_chunk_id": "ar_pr_sentation_cri_tta_vf_semantic_024__r001",
          "document_id": "ar_pr_sentation_cri_tta_vf",
          "document_family_id": "cri_presentation",
          "filename": "AR_Presentation_CRI_TTA.json",
          "language": "ar",
          "topic_id": "regional_positioning",
          "content_type": "narrative",
          "page_start": 41,
          "page_end": 41,
          "source_pages": [
            41
          ],
          "dense_score": 0.83067304,
          "ranking_score": 0.83567304,
          "text": "0\n\nا ع\nالا ع 1 ا\nدقاف <>7 -070000 7\nإن هناء فا كل مكان 58 روه سلما وانشهية ولشر ع الساسات التموطيخ\nدلاء 0\n-\n\n100 ا ا\n\n89 من الشركات راضية عن استقرارها\n2200 يدهة مللجة_'تطواق الكسيفة\n\nأهم حوافز الاستثمار بالجهة اتجاهات وآفاق نمو الأعمال فى المنطقة\n\nجودة الحياة و/229 من المشاركين يعتبرون الوضع الحالي لشركاتهم مرضيًا\n\nم95 مع وجود آفاق متفائلة للنمو على جميع المستويات\n\nالموقع الجغرافي\nا\nومرافق استقبال متطورة0 بنية تحتية؟ض ل\n\nتوفر المهارات؟آ؟آ 0\n21111606061012\n\n00111 |110101010101000 1111 1أ001ظغظك\n\n© توجه صاعد © مستقر © في اتجاه الإنخفاض\n\nالمصدر: استطلاع أي أجرته مؤسسة التمويل الدولية ومجموعة البنك الدولي في عام 2025"
        },
        {
          "retrieval_chunk_id": "akhbar_al_moustatmir_news_phase3f_0002__r001b",
          "document_id": "akhbar_al_moustatmir_news",
          "document_family_id": "manar_al_moustatmir_news_2023",
          "filename": "Akhbar_Al_Moustatmir_News.json",
          "language": "ar",
          "topic_id": "investment_news",
          "content_type": "narrative",
          "page_start": 4,
          "page_end": 4,
          "source_pages": [
            4
          ],
          "dense_score": 0.8293917,
          "ranking_score": 0.8343917,
          "text": "مقدمة\nwww.investangier.com\n،أعزائي القراء\nجهة \nحققتها \nالتي \nالرائعة \nالإنجازات \nببعض \nنشارككم \nأن \nيسرنا \nالحسيمة في مجال الاستثمار الإنتاجي. وتعكس هذه الإنجازات -تطوان-طنجة\nالذكاء الجماعي لمجتمع الاستثمار بأكمله في الجهة، التي أصبحت بسرعة \nقاطرة للتنمية على المستوى الوطني. وبفضل الأصول الطبيعية والاقتصادية \nالعديدة، بالإضافة إلى البنية التحتية ذات المستوى العالمي مثل مجمع ميناء \nطنجة المتوسط والقطار فائق السرعة، وضعت المنطقة نفسها كبوابة طبيعية \nلمفترق طرق أوروبا وإفريقيا وأمريكا وآسيا.\nهذا التحول المبهر يعود إلى رؤية مستنيرة، وضعها صاحب الجلالة الملك محمد \nالسادس، نصره هللا. كما تمثل هذه الرؤية استراتيجية شاملة تركز على جاذبية \nالاستثمارات الإنتاجية، وقد ساهمت في جذب الشركات ذات الشهرة العالمية.\nتم تبني هذه الاستراتيجية بنجاح، حيث أظهرت فوائدها بوضوح من خلال تحقيق \nنتائج ملموسة وإيجابية. فقد تم تقديم عدد كبير من طلبات الاستثمار الواسعة \nالنطاق إلى المركز الجهوي للاستثمار في الجهة، وبفضل الجهود المبذولة، \n 709 على2023 ( في سنةCRUI) وافقت اللجنة الجهوية الموحدة للاستثمار\n مشاريع استثمارية. تبلغ الاستثمارات الإجمالية لهذه المشاريع أكثر من \n مليار درهم، والتي من المتوقع أن تسهم في خلق أكثر من 73\n. فرصة عمل مباشر70000"
        }
      ],
      "experimental_v2": [
        {
          "evidence_id": "E1",
          "retrieval_chunk_id": "chiffres_cles_crui_1er_semestre_2024_arabe_chunk_003__r001",
          "parent_semantic_chunk_id": "chiffres_cles_crui_1er_semestre_2024_arabe_chunk_003",
          "document_id": "chiffres_cles_crui_1er_semestre_2024_arabe",
          "document_family_id": "crui_key_figures_2024_h1",
          "filename": "Chiffres_cles_CRUI_1er_semestre_2024_Arabe.json",
          "document_title": "المؤشرات الرئيسية والإحصائيات",
          "language": "ar",
          "topic_id": "sector_distribution",
          "content_type": "statistics",
          "semantic_tags": [
            "sector_distribution",
            "investment_amount"
          ],
          "heading_path": [
            "إن كنتم هنا، فأنتم في كل مكان"
          ],
          "page_start": 3,
          "page_end": 3,
          "source_pages": [
            3
          ],
          "text": "إن كنتم هنا، فأنتم في كل مكان\n\nتوزيع حجم الاستثمارات حسب القطاع\n\nيواصل القطاع الصناعي نموه الاستثنائي بأكثر من نصف الاستثمارات التي تمت المصادقة عليها\n\nإجمالي الاستثمارات: 40,76 مليار درهم\n\nالصناعة: 54%\nالسياحة: 22%\nالطاقة والمناجم: 15%\nقطاعات أخرى: 6%\nالتجارة: 2%\nالبناء والأشغال العامة: 1%\n\nwww.investangier.com",
          "source_spans": [
            {
              "page": 3,
              "text": "إن كنتم هنا، فأنتم في كل مكان\n\nتوزيع حجم الاستثمارات حسب القطاع\n\nيواصل القطاع الصناعي نموه الاستثنائي بأكثر من نصف الاستثمارات التي تمت المصادقة عليها\n\nإجمالي الاستثمارات: 40,76 مليار درهم\n\nالصناعة: 54%\nالسياحة: 22%\nالطاقة والمناجم: 15%\nقطاعات أخرى: 6%\nالتجارة: 2%\nالبناء والأشغال العامة: 1%\n\nwww.investangier.com"
            }
          ],
          "dense_score": 0.8477998,
          "ranking_score": 0.8527998,
          "expanded_from_sibling": false,
          "retrieval_chunk_index": 0,
          "retrieval_chunk_count": 1,
          "temporal_scope": {
            "primary_year": 2024,
            "years_mentioned": [],
            "reference_period": {
              "type": "semester",
              "year": 2024,
              "semester": 1,
              "quarter": null,
              "start_date": null,
              "end_date": null
            }
          }
        },
        {
          "evidence_id": "E2",
          "retrieval_chunk_id": "akhbar_al_moustatmir_news_phase3f_0006__r001",
          "parent_semantic_chunk_id": "akhbar_al_moustatmir_news_phase3f_0006",
          "document_id": "akhbar_al_moustatmir_news",
          "document_family_id": "manar_al_moustatmir_news_2023",
          "filename": "Akhbar_Al_Moustatmir_News.json",
          "document_title": "أخبار الاستثمار وريادة الأعمال",
          "language": "ar",
          "topic_id": "investment_news",
          "content_type": "investment_opportunity",
          "semantic_tags": [
            "investment_news",
            "investment_opportunity",
            "project_announcement"
          ],
          "heading_path": [
            "العرض العقاري بتطوان بارك"
          ],
          "page_start": 9,
          "page_end": 9,
          "source_pages": [
            9
          ],
          "text": "03\nwww.investangier.com\n03\nwww.investangier.com\n إطلاق عــرض أرض للإيجــار فــي تطــوان بــارك بموجــب اتفاقيــة الشراكــة\n المتعلقــة بتعبئــة أراضي المنطقــة الصناعيــة واللوجســتية بتطــوان بــارك\n قطع صناعية9 :2022 يونيو10 الموقعة في\n8\nالمساحة\nالإجمالي\n8\nالمشاريع الصناعية\nالمصادق عليها\n350 MMAD\nمبلغ الاستثمار\n1 000\nالوظائف\n ھكتـار( مـن قطـب50) تخصیـص القطـع الأرضیـة على مسـتوى الدفعـة الأولى\nلوكوس الزراعي في العرائش\n47\n التكلفة\nلإجمالية\nالشركات\n8 000\nالوظائف\nالمساحة\n مبنى117 بدء تشغيل منطقة النشاط الاقتصادي في طنجة البالیة :تخصیص\n150\n457\nفي طور التأسيس",
          "source_spans": [
            {
              "page": 9,
              "text": "03\nwww.investangier.com\n03\nwww.investangier.com\n إطلاق عــرض أرض للإيجــار فــي تطــوان بــارك بموجــب اتفاقيــة الشراكــة\n المتعلقــة بتعبئــة أراضي المنطقــة الصناعيــة واللوجســتية بتطــوان بــارك\n قطع صناعية9 :2022 يونيو10 الموقعة في\n8\nالمساحة\nالإجمالي\n8\nالمشاريع الصناعية\nالمصادق عليها\n350 MMAD\nمبلغ الاستثمار\n1 000\nالوظائف\n ھكتـار( مـن قطـب50) تخصیـص القطـع الأرضیـة على مسـتوى الدفعـة الأولى\nلوكوس الزراعي في العرائش\n47\n التكلفة\nلإجمالية\nالشركات\n8 000\nالوظائف\nالمساحة\n مبنى117 بدء تشغيل منطقة النشاط الاقتصادي في طنجة البالیة :تخصیص\n150\n457\nفي طور التأسيس"
            }
          ],
          "dense_score": 0.82433903,
          "ranking_score": 0.83733903,
          "expanded_from_sibling": false,
          "retrieval_chunk_index": 0,
          "retrieval_chunk_count": 1,
          "temporal_scope": {
            "primary_year": null,
            "years_mentioned": [
              2022
            ],
            "reference_period": {
              "type": null,
              "year": null,
              "semester": null,
              "quarter": null,
              "start_date": null,
              "end_date": null
            }
          }
        },
        {
          "evidence_id": "E3",
          "retrieval_chunk_id": "ar_pr_sentation_cri_tta_vf_semantic_019__r001b",
          "parent_semantic_chunk_id": "ar_pr_sentation_cri_tta_vf_semantic_019",
          "document_id": "ar_pr_sentation_cri_tta_vf",
          "document_family_id": "cri_presentation",
          "filename": "AR_Presentation_CRI_TTA.json",
          "document_title": "تقديم المركز الجهوي للاستثمار",
          "language": "ar",
          "topic_id": "territorial_offer",
          "content_type": "narrative",
          "semantic_tags": [
            "territorial_offer"
          ],
          "heading_path": [
            "العرض الترابي للاستثمار"
          ],
          "page_start": 35,
          "page_end": 35,
          "source_pages": [
            35
          ],
          "text": "منصة استقبال تم تقديمها أمام جلالة الملك محمد السادس نصره الله سنة 2017\n\n0 أنشطة\nالطيران\n\nالسيارات\n\nالتجارة الإلكترونية\n. الاتصالات\nالطاقات المتجددة\nالنقل\n\nالأجهزة المنزلية\n\n. الصناعات الدوائية\n2 إنتاج المواد\n\n5 الصناعات الزراعية والغذائية\n\nا\n0\n\nم \" دعق ٍّ\n\n27\nقرارًا بالترخيص للتركيب\nتم منحها\n\nمدينة ذكية تتسع ل 300,000 نسمة\n\nالاستثمار: مليار دولار\nعدد مناصب الشغل يصل إلى 100,000\nالإيرادات: 15 مليار دولار سنوبا\n\nالمساحة: 2,167 هكتارا. منها 947 هكتارا مخصصة\nلمنطقة التسريع د هكتار قيد التطوبر\n4\n\nهكتا الا ١\nالأو 00 التجاري الأولى, من رق\n\n0 11+ 27+\nمنصب شغل متوقع مليار درهم من الاستثمارات\n\nالمنطقة اللوجستيكية طبه كءالا ا مصنع رونو\nكٍ 4 يدق 0 - 0 ع منطقة الأنشطة الإقتصادية مفوغة\n١ 5 منطقة الأنشطة الإقتصادية المجد\nالإقتصادية حيضرة 3 500 م منطقة الأنشطة الإقتصادية العوامة\nك_ المنطقة الحرة لطنجة\nالمنطقة الصناعية مرنيل: المنطقة الصناعية\nكزناية: لهاع هوأرماأهي عل أوعع\n264 1 5\nهكتارًا من الأراضي التي سيتم مشروع أصبح عمليا مشاريع قيد الإنشاء\n\nتعبئتها من خلال المشاريع ع الي\nوافقت عليها اللجنة الجهوية\nالموحدة للاستثمار\n\nون 58 غه عا مومرمج لاكمم روجع\n\n5ع ااانا امعل/ا,عوصة 1",
          "source_spans": [
            {
              "page": 35,
              "text": "منصة استقبال تم تقديمها أمام جلالة الملك محمد السادس نصره الله سنة 2017\n\n0 أنشطة\nالطيران\n\nالسيارات\n\nالتجارة الإلكترونية\n. الاتصالات\nالطاقات المتجددة\nالنقل\n\nالأجهزة المنزلية\n\n. الصناعات الدوائية\n2 إنتاج المواد\n\n5 الصناعات الزراعية والغذائية\n\nا\n0\n\nم \" دعق ٍّ\n\n27\nقرارًا بالترخيص للتركيب\nتم منحها\n\nمدينة ذكية تتسع ل 300,000 نسمة\n\nالاستثمار: مليار دولار\nعدد مناصب الشغل يصل إلى 100,000\nالإيرادات: 15 مليار دولار سنوبا\n\nالمساحة: 2,167 هكتارا. منها 947 هكتارا مخصصة\nلمنطقة التسريع د هكتار قيد التطوبر\n4\n\nهكتا الا ١\nالأو 00 التجاري الأولى, من رق\n\n0 11+ 27+\nمنصب شغل متوقع مليار درهم من الاستثمارات\n\nالمنطقة اللوجستيكية طبه كءالا ا مصنع رونو\nكٍ 4 يدق 0 - 0 ع منطقة الأنشطة الإقتصادية مفوغة\n١ 5 منطقة الأنشطة الإقتصادية المجد\nالإقتصادية حيضرة 3 500 م منطقة الأنشطة الإقتصادية العوامة\nك_ المنطقة الحرة لطنجة\nالمنطقة الصناعية مرنيل: المنطقة الصناعية\nكزناية: لهاع هوأرماأهي عل أوعع\n264 1 5\nهكتارًا من الأراضي التي سيتم مشروع أصبح عمليا مشاريع قيد الإنشاء\n\nتعبئتها من خلال المشاريع ع الي\nوافقت عليها اللجنة الجهوية\nالموحدة للاستثمار\n\nون 58 غه عا مومرمج لاكمم روجع\n\n5ع ااانا امعل/ا,عوصة 1"
            }
          ],
          "dense_score": 0.83079207,
          "ranking_score": 0.83579207,
          "expanded_from_sibling": false,
          "retrieval_chunk_index": 1,
          "retrieval_chunk_count": 2,
          "temporal_scope": {
            "primary_year": null,
            "years_mentioned": [
              2017
            ],
            "reference_period": {
              "type": null,
              "year": null,
              "semester": null,
              "quarter": null,
              "start_date": null,
              "end_date": null
            }
          }
        },
        {
          "evidence_id": "E4",
          "retrieval_chunk_id": "ar_pr_sentation_cri_tta_vf_semantic_024__r001",
          "parent_semantic_chunk_id": "ar_pr_sentation_cri_tta_vf_semantic_024",
          "document_id": "ar_pr_sentation_cri_tta_vf",
          "document_family_id": "cri_presentation",
          "filename": "AR_Presentation_CRI_TTA.json",
          "document_title": "تقديم المركز الجهوي للاستثمار",
          "language": "ar",
          "topic_id": "regional_positioning",
          "content_type": "narrative",
          "semantic_tags": [
            "regional_positioning"
          ],
          "heading_path": [
            "التموقع الجهوي"
          ],
          "page_start": 41,
          "page_end": 41,
          "source_pages": [
            41
          ],
          "text": "0\n\nا ع\nالا ع 1 ا\nدقاف <>7 -070000 7\nإن هناء فا كل مكان 58 روه سلما وانشهية ولشر ع الساسات التموطيخ\nدلاء 0\n-\n\n100 ا ا\n\n89 من الشركات راضية عن استقرارها\n2200 يدهة مللجة_'تطواق الكسيفة\n\nأهم حوافز الاستثمار بالجهة اتجاهات وآفاق نمو الأعمال فى المنطقة\n\nجودة الحياة و/229 من المشاركين يعتبرون الوضع الحالي لشركاتهم مرضيًا\n\nم95 مع وجود آفاق متفائلة للنمو على جميع المستويات\n\nالموقع الجغرافي\nا\nومرافق استقبال متطورة0 بنية تحتية؟ض ل\n\nتوفر المهارات؟آ؟آ 0\n21111606061012\n\n00111 |110101010101000 1111 1أ001ظغظك\n\n© توجه صاعد © مستقر © في اتجاه الإنخفاض\n\nالمصدر: استطلاع أي أجرته مؤسسة التمويل الدولية ومجموعة البنك الدولي في عام 2025",
          "source_spans": [
            {
              "page": 41,
              "text": "0\n\nا ع\nالا ع 1 ا\nدقاف <>7 -070000 7\nإن هناء فا كل مكان 58 روه سلما وانشهية ولشر ع الساسات التموطيخ\nدلاء 0\n-\n\n100 ا ا\n\n89 من الشركات راضية عن استقرارها\n2200 يدهة مللجة_'تطواق الكسيفة\n\nأهم حوافز الاستثمار بالجهة اتجاهات وآفاق نمو الأعمال فى المنطقة\n\nجودة الحياة و/229 من المشاركين يعتبرون الوضع الحالي لشركاتهم مرضيًا\n\nم95 مع وجود آفاق متفائلة للنمو على جميع المستويات\n\nالموقع الجغرافي\nا\nومرافق استقبال متطورة0 بنية تحتية؟ض ل\n\nتوفر المهارات؟آ؟آ 0\n21111606061012\n\n00111 |110101010101000 1111 1أ001ظغظك\n\n© توجه صاعد © مستقر © في اتجاه الإنخفاض\n\nالمصدر: استطلاع أي أجرته مؤسسة التمويل الدولية ومجموعة البنك الدولي في عام 2025"
            }
          ],
          "dense_score": 0.83067304,
          "ranking_score": 0.83567304,
          "expanded_from_sibling": false,
          "retrieval_chunk_index": 0,
          "retrieval_chunk_count": 1,
          "temporal_scope": {
            "primary_year": null,
            "years_mentioned": [
              2025
            ],
            "reference_period": {
              "type": null,
              "year": null,
              "semester": null,
              "quarter": null,
              "start_date": null,
              "end_date": null
            }
          }
        },
        {
          "evidence_id": "E5",
          "retrieval_chunk_id": "akhbar_al_moustatmir_news_phase3f_0002__r001b",
          "parent_semantic_chunk_id": "akhbar_al_moustatmir_news_phase3f_0002",
          "document_id": "akhbar_al_moustatmir_news",
          "document_family_id": "manar_al_moustatmir_news_2023",
          "filename": "Akhbar_Al_Moustatmir_News.json",
          "document_title": "أخبار الاستثمار وريادة الأعمال",
          "language": "ar",
          "topic_id": "investment_news",
          "content_type": "narrative",
          "semantic_tags": [
            "editorial",
            "investment_news",
            "news_edition_2023"
          ],
          "heading_path": [
            "كلمة تحريرية"
          ],
          "page_start": 4,
          "page_end": 4,
          "source_pages": [
            4
          ],
          "text": "مقدمة\nwww.investangier.com\n،أعزائي القراء\nجهة \nحققتها \nالتي \nالرائعة \nالإنجازات \nببعض \nنشارككم \nأن \nيسرنا \nالحسيمة في مجال الاستثمار الإنتاجي. وتعكس هذه الإنجازات -تطوان-طنجة\nالذكاء الجماعي لمجتمع الاستثمار بأكمله في الجهة، التي أصبحت بسرعة \nقاطرة للتنمية على المستوى الوطني. وبفضل الأصول الطبيعية والاقتصادية \nالعديدة، بالإضافة إلى البنية التحتية ذات المستوى العالمي مثل مجمع ميناء \nطنجة المتوسط والقطار فائق السرعة، وضعت المنطقة نفسها كبوابة طبيعية \nلمفترق طرق أوروبا وإفريقيا وأمريكا وآسيا.\nهذا التحول المبهر يعود إلى رؤية مستنيرة، وضعها صاحب الجلالة الملك محمد \nالسادس، نصره هللا. كما تمثل هذه الرؤية استراتيجية شاملة تركز على جاذبية \nالاستثمارات الإنتاجية، وقد ساهمت في جذب الشركات ذات الشهرة العالمية.\nتم تبني هذه الاستراتيجية بنجاح، حيث أظهرت فوائدها بوضوح من خلال تحقيق \nنتائج ملموسة وإيجابية. فقد تم تقديم عدد كبير من طلبات الاستثمار الواسعة \nالنطاق إلى المركز الجهوي للاستثمار في الجهة، وبفضل الجهود المبذولة، \n 709 على2023 ( في سنةCRUI) وافقت اللجنة الجهوية الموحدة للاستثمار\n مشاريع استثمارية. تبلغ الاستثمارات الإجمالية لهذه المشاريع أكثر من \n مليار درهم، والتي من المتوقع أن تسهم في خلق أكثر من 73\n. فرصة عمل مباشر70000",
          "source_spans": [
            {
              "page": 4,
              "text": "مقدمة\nwww.investangier.com\n،أعزائي القراء\nجهة \nحققتها \nالتي \nالرائعة \nالإنجازات \nببعض \nنشارككم \nأن \nيسرنا \nالحسيمة في مجال الاستثمار الإنتاجي. وتعكس هذه الإنجازات -تطوان-طنجة\nالذكاء الجماعي لمجتمع الاستثمار بأكمله في الجهة، التي أصبحت بسرعة \nقاطرة للتنمية على المستوى الوطني. وبفضل الأصول الطبيعية والاقتصادية \nالعديدة، بالإضافة إلى البنية التحتية ذات المستوى العالمي مثل مجمع ميناء \nطنجة المتوسط والقطار فائق السرعة، وضعت المنطقة نفسها كبوابة طبيعية \nلمفترق طرق أوروبا وإفريقيا وأمريكا وآسيا.\nهذا التحول المبهر يعود إلى رؤية مستنيرة، وضعها صاحب الجلالة الملك محمد \nالسادس، نصره هللا. كما تمثل هذه الرؤية استراتيجية شاملة تركز على جاذبية \nالاستثمارات الإنتاجية، وقد ساهمت في جذب الشركات ذات الشهرة العالمية.\nتم تبني هذه الاستراتيجية بنجاح، حيث أظهرت فوائدها بوضوح من خلال تحقيق \nنتائج ملموسة وإيجابية. فقد تم تقديم عدد كبير من طلبات الاستثمار الواسعة \nالنطاق إلى المركز الجهوي للاستثمار في الجهة، وبفضل الجهود المبذولة، \n 709 على2023 ( في سنةCRUI) وافقت اللجنة الجهوية الموحدة للاستثمار\n مشاريع استثمارية. تبلغ الاستثمارات الإجمالية لهذه المشاريع أكثر من \n مليار درهم، والتي من المتوقع أن تسهم في خلق أكثر من 73\n. فرصة عمل مباشر70000"
            }
          ],
          "dense_score": 0.8293917,
          "ranking_score": 0.8343917,
          "expanded_from_sibling": false,
          "retrieval_chunk_index": 1,
          "retrieval_chunk_count": 3,
          "temporal_scope": {
            "primary_year": null,
            "years_mentioned": [
              2002,
              2023
            ],
            "reference_period": {
              "type": null,
              "year": null,
              "semester": null,
              "quarter": null,
              "start_date": null,
              "end_date": null
            }
          }
        }
      ],
      "status": "review_required"
    }
  }
}

## LLM preflight

{
  "status": "FAIL",
  "model": "qwen/qwen3.8-27b",
  "checks": [
    {
      "name": "trivial_request",
      "status": "FAIL",
      "category": "connection",
      "error": "LLM generation failed: Connection error."
    }
  ],
  "category": "connection"
}

## Generated-answer comparison

{
  "subset_count": 0,
  "status": "not_run_due_to_preflight"
}

## Final 4E.1 gate

{
  "retrieval_remains_at_least_frozen_v2": true,
  "multilingual_remains_at_least_frozen_v2": true,
  "abstention_calibrated": true,
  "strict_year_conflict_behavior_improves": true,
  "generated_answer_evaluation_completed": false,
  "groundedness_at_least_v1": false,
  "exact_citations": true,
  "status": "V2_NOT_READY"
}

No production cutover was performed. Proposed policies remain evaluation-only.
