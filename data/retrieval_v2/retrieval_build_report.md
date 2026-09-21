# Phase 4A — Retrieval chunk build report

## Scope

Built deterministic retrieval records from all schema-2.2 semantic JSON documents. Semantic JSON, raw JSON, Qdrant, embeddings, loaders, retrievers, prompts, and production collections were not modified.

- Semantic documents: 33
- Semantic parents: 913
- Retrieval records: 1901
- Previous retrieval-record count: 1901
- Parents covered: 913 / 913
- Parents with at least one indexable record: 906 / 913
- Parents with only non-indexable records: 7
- Unsplit parents: 628
- Split parents: 285

## Offset-based page mapping

Split segments retain original character offsets in the semantic parent text. Page mapping uses those offsets against ordered source spans and never searches reconstructed segment text.

- Exact mappings: 1901
- Parent mappings: 0

### Remaining parent mappings

- None.

## Indexability gate

Indexability is conservative and does not use character count alone. Short factual, statistical, cost, contact, project, FAQ, and eligibility records remain indexable.

- Indexable records: 1894
- Non-indexable records: 7
- Short indexable records (<200 chars): 135

### Indexability reason distribution

- `boilerplate_only`: 2
- `navigation_only`: 5
- `semantic_content`: 1811
- `short_but_informative`: 83

### Non-indexable records

- `eng_presentation_cri_tta_vf_semantic_008__r001` — `boilerplate_only`, 60 chars, family `cri_presentation`; text: `Monograph Tangier-Tetouan-Al Hoceima, The Region at a Glance`
- `eng_presentation_cri_tta_vf_semantic_013__r001` — `boilerplate_only`, 170 chars, family `cri_presentation`; text: `INDUSTRY sw contributing for the Sectoral breakdown of business volume Tangier-Tetouan-Al Hoceima, an emerging centre for cutting-edge industry the region to va`
- `eng_presentation_cri_tta_vf_semantic_018__r001` — `navigation_only`, 9 chars, family `cri_presentation`; text: `LOGISTICS`
- `esp_presentation_cri_tta_vf_semantic_012__r001` — `navigation_only`, 9 chars, family `cri_presentation`; text: `INDUSTRIA`
- `fr_chiffres_cles_annee_2025_p18_c01__r001` — `navigation_only`, 37 chars, family `chiffres_cles_2025`; text: `ONCE YOU ARE HERE, YOU ARE EVERYWHERE`
- `nv_guide_cout_facteurs_cri_2024_phase3f_0019__r001` — `navigation_only`, 10 chars, family `production_factor_cost_guide_2024`; text: `TRANSPORTS`
- `nv_guide_cout_facteurs_cri_2024_phase3f_0028__r001` — `navigation_only`, 9 chars, family `production_factor_cost_guide_2024`; text: `FORMATION`

## Retrieval design

Parents at or below 4,500 characters remain intact. Larger parents are split using original-offset paragraph/sentence/line boundaries toward approximately 3,000 characters. No generic overlap is applied at clean boundaries. Each record retains full parent source spans for Phase 4A provenance.

## E5 token-budget validation

- Tokenizer/model: `intfloat/multilingual-e5-base`
- Model maximum sequence length: 512 tokens
- Safe maximum: 500 tokens, counted with `add_special_tokens=True` and including the literal `passage: ` prefix and heading context
- Oversized indexable records before refinement (>500): 477
- Oversized indexable records after refinement (>500): 0
- Records over 512 before: 460
- Records over 512 after: 0
- Records additionally split: 477
- Final maximum embedding token count: 499
- Final median embedding token count: 315.0
- Final mean embedding token count: 279.4

### Records split for token budget

- `akhbar_al_moustatmir_news_phase3f_0002__r001` — 867 tokens before; produced 3 deterministic descendants.
- `akhbar_al_moustatmir_news_phase3f_0015__r001` — 648 tokens before; produced 2 deterministic descendants.
- `akhbar_al_moustatmir_news_phase3f_0026__r001` — 1294 tokens before; produced 3 deterministic descendants.
- `akhbar_al_moustatmir_news_phase3f_0027__r001` — 597 tokens before; produced 2 deterministic descendants.
- `akhbar_al_moustatmir_news_phase3f_0027__r003` — 766 tokens before; produced 3 deterministic descendants.
- `akhbar_al_moustatmir_news_phase3f_0029__r001` — 911 tokens before; produced 3 deterministic descendants.
- `ar_pr_sentation_cri_tta_vf_semantic_002__r001` — 567 tokens before; produced 2 deterministic descendants.
- `ar_pr_sentation_cri_tta_vf_semantic_004__r001` — 694 tokens before; produced 3 deterministic descendants.
- `ar_pr_sentation_cri_tta_vf_semantic_011__r001` — 503 tokens before; produced 2 deterministic descendants.
- `ar_pr_sentation_cri_tta_vf_semantic_013__r001` — 511 tokens before; produced 2 deterministic descendants.
- `ar_pr_sentation_cri_tta_vf_semantic_019__r001` — 699 tokens before; produced 2 deterministic descendants.
- `ar_pr_sentation_cri_tta_vf_semantic_035__r001` — 755 tokens before; produced 3 deterministic descendants.
- `arabe_chiffres_cles_2025_chunk_015__r001` — 506 tokens before; produced 2 deterministic descendants.
- `brochure_secteur_logistique_chunk_002__r001` — 965 tokens before; produced 3 deterministic descendants.
- `brochure_secteur_logistique_chunk_003__r001` — 925 tokens before; produced 3 deterministic descendants.
- `brochure_secteur_logistique_chunk_004__r001` — 872 tokens before; produced 4 deterministic descendants.
- `brochure_secteur_logistique_chunk_005__r001` — 858 tokens before; produced 3 deterministic descendants.
- `eng_panorama_des_zi_semantic_003_005__r001` — 713 tokens before; produced 3 deterministic descendants.
- `eng_panorama_des_zi_semantic_007_009__r001` — 734 tokens before; produced 3 deterministic descendants.
- `eng_panorama_des_zi_semantic_010_012__r001` — 517 tokens before; produced 2 deterministic descendants.
- `eng_panorama_des_zi_semantic_013_015__r001` — 516 tokens before; produced 2 deterministic descendants.
- `eng_panorama_des_zi_semantic_028_030__r001` — 541 tokens before; produced 2 deterministic descendants.
- `eng_panorama_des_zi_semantic_045_046__r001` — 543 tokens before; produced 2 deterministic descendants.
- `eng_panorama_des_zi_semantic_061_062__r001` — 664 tokens before; produced 2 deterministic descendants.
- `eng_panorama_des_zi_semantic_069_071__r001` — 563 tokens before; produced 2 deterministic descendants.
- `eng_panorama_des_zi_semantic_075_077__r001` — 528 tokens before; produced 2 deterministic descendants.
- `eng_panorama_des_zi_semantic_089_091__r001` — 733 tokens before; produced 3 deterministic descendants.
- `eng_presentation_cri_tta_vf_semantic_027__r001` — 618 tokens before; produced 2 deterministic descendants.
- `es_panorama_des_zi_semantic_002_002__r001` — 528 tokens before; produced 2 deterministic descendants.
- `es_panorama_des_zi_semantic_003_005__r001` — 762 tokens before; produced 3 deterministic descendants.
- `es_panorama_des_zi_semantic_031_032__r001` — 587 tokens before; produced 2 deterministic descendants.
- `es_panorama_des_zi_semantic_045_046__r001` — 525 tokens before; produced 2 deterministic descendants.
- `es_panorama_des_zi_semantic_061_062__r001` — 693 tokens before; produced 2 deterministic descendants.
- `es_panorama_des_zi_semantic_069_071__r001` — 518 tokens before; produced 2 deterministic descendants.
- `es_panorama_des_zi_semantic_083_084__r001` — 563 tokens before; produced 2 deterministic descendants.
- `esp_chiffres_cles_annee_2025_chunk_015__r001` — 527 tokens before; produced 2 deterministic descendants.
- `esp_indicateurs_climat_dinvestissement_chunk_006__r001` — 538 tokens before; produced 2 deterministic descendants.
- `esp_presentation_cri_tta_vf_semantic_016__r001` — 532 tokens before; produced 2 deterministic descendants.
- `esp_presentation_cri_tta_vf_semantic_024__r001` — 547 tokens before; produced 2 deterministic descendants.
- `fr_chiffres_cles_annee_2025_p15_c01__r001` — 587 tokens before; produced 2 deterministic descendants.
- `fr_indicateurs_climat_dinvestissement_chunk_006__r001` — 574 tokens before; produced 2 deterministic descendants.
- `panorama_zones_economiques_industrielles_fr_semantic_002_002__r001` — 799 tokens before; produced 3 deterministic descendants.
- `panorama_zones_economiques_industrielles_fr_semantic_003_005__r001` — 875 tokens before; produced 3 deterministic descendants.
- `panorama_zones_economiques_industrielles_fr_semantic_007_009__r001` — 658 tokens before; produced 2 deterministic descendants.
- `panorama_zones_economiques_industrielles_fr_semantic_013_015__r001` — 542 tokens before; produced 2 deterministic descendants.
- `panorama_zones_economiques_industrielles_fr_semantic_022_024__r001` — 558 tokens before; produced 2 deterministic descendants.
- `panorama_zones_economiques_industrielles_fr_semantic_025_027__r001` — 531 tokens before; produced 2 deterministic descendants.
- `panorama_zones_economiques_industrielles_fr_semantic_028_030__r001` — 600 tokens before; produced 2 deterministic descendants.
- `panorama_zones_economiques_industrielles_fr_semantic_031_032__r001` — 709 tokens before; produced 2 deterministic descendants.
- `panorama_zones_economiques_industrielles_fr_semantic_033_035__r001` — 615 tokens before; produced 2 deterministic descendants.
- `panorama_zones_economiques_industrielles_fr_semantic_039_041__r001` — 504 tokens before; produced 2 deterministic descendants.
- `panorama_zones_economiques_industrielles_fr_semantic_045_046__r001` — 700 tokens before; produced 2 deterministic descendants.
- `panorama_zones_economiques_industrielles_fr_semantic_047_049__r001` — 511 tokens before; produced 2 deterministic descendants.
- `panorama_zones_economiques_industrielles_fr_semantic_055_057__r001` — 502 tokens before; produced 2 deterministic descendants.
- `panorama_zones_economiques_industrielles_fr_semantic_058_060__r001` — 540 tokens before; produced 2 deterministic descendants.
- `panorama_zones_economiques_industrielles_fr_semantic_061_062__r001` — 782 tokens before; produced 3 deterministic descendants.
- `panorama_zones_economiques_industrielles_fr_semantic_069_071__r001` — 666 tokens before; produced 2 deterministic descendants.
- `panorama_zones_economiques_industrielles_fr_semantic_078_079__r001` — 572 tokens before; produced 2 deterministic descendants.
- `panorama_zones_economiques_industrielles_fr_semantic_083_084__r001` — 711 tokens before; produced 2 deterministic descendants.
- `fr_presentation_cri_tta_vf_semantic_004__r001` — 549 tokens before; produced 2 deterministic descendants.
- `fr_presentation_cri_tta_vf_semantic_020__r001` — 677 tokens before; produced 2 deterministic descendants.
- `fr_presentation_cri_tta_vf_semantic_029__r001` — 849 tokens before; produced 3 deterministic descendants.
- `guide_branchement_electricite_eau_assainissement_grands_comptes_phase3f_0007__r001` — 732 tokens before; produced 3 deterministic descendants.
- `guide_branchement_electricite_eau_assainissement_grands_comptes_phase3f_0008__r001` — 628 tokens before; produced 2 deterministic descendants.
- `guide_branchement_electricite_eau_assainissement_grands_comptes_phase3f_0010__r001` — 667 tokens before; produced 2 deterministic descendants.
- `guide_branchement_electricite_eau_assainissement_grands_comptes_phase3f_0012__r001` — 751 tokens before; produced 3 deterministic descendants.
- `guide_du_financement_des_entreprises_vision_preamble__r001` — 640 tokens before; produced 3 deterministic descendants.
- `guide_du_financement_des_entreprises_partner_messages__r001` — 864 tokens before; produced 3 deterministic descendants.
- `guide_du_financement_des_entreprises_partner_messages__r002` — 653 tokens before; produced 2 deterministic descendants.
- `guide_du_financement_des_entreprises_financing_matrix__r001` — 749 tokens before; produced 3 deterministic descendants.
- `guide_du_financement_des_entreprises_equity_love_money__r001` — 722 tokens before; produced 2 deterministic descendants.
- `guide_du_financement_des_entreprises_tpe_agr_support__r001` — 942 tokens before; produced 3 deterministic descendants.
- `guide_du_financement_des_entreprises_youth_inclusion__r001` — 545 tokens before; produced 2 deterministic descendants.
- `guide_du_financement_des_entreprises_entrepreneurial_support_products__r001` — 669 tokens before; produced 2 deterministic descendants.
- `guide_du_financement_des_entreprises_entrepreneurial_support_products__r002` — 747 tokens before; produced 3 deterministic descendants.
- `guide_du_financement_des_entreprises_pret_tpe__r001` — 650 tokens before; produced 2 deterministic descendants.
- `guide_du_financement_des_entreprises_pret_tpe__r002` — 630 tokens before; produced 2 deterministic descendants.
- `guide_du_financement_des_entreprises_pret_voiture__r001` — 712 tokens before; produced 2 deterministic descendants.
- `guide_du_financement_des_entreprises_pret_entreprise__r001` — 686 tokens before; produced 2 deterministic descendants.
- `guide_du_financement_des_entreprises_intelak__r001` — 690 tokens before; produced 2 deterministic descendants.
- `guide_du_financement_des_entreprises_intelak_al_moustatmir_qarawi__r001` — 687 tokens before; produced 2 deterministic descendants.
- `guide_du_financement_des_entreprises_credit_bail_mobilier__r001` — 704 tokens before; produced 3 deterministic descendants.
- `guide_du_financement_des_entreprises_credit_bail_mobilier__r002` — 681 tokens before; produced 2 deterministic descendants.
- `guide_du_financement_des_entreprises_credit_bail_immobilier__r001` — 765 tokens before; produced 3 deterministic descendants.
- `guide_du_financement_des_entreprises_lease_back__r001` — 504 tokens before; produced 2 deterministic descendants.
- `guide_du_financement_des_entreprises_investment_credit_medium_long_term__r001` — 810 tokens before; produced 3 deterministic descendants.
- `guide_du_financement_des_entreprises_amortizable_working_credit__r001` — 532 tokens before; produced 2 deterministic descendants.
- `guide_du_financement_des_entreprises_real_estate_development_credit__r001` — 533 tokens before; produced 2 deterministic descendants.
- `guide_du_financement_des_entreprises_consolidation_credit__r001` — 551 tokens before; produced 2 deterministic descendants.
- `guide_du_financement_des_entreprises_cash_facility__r001` — 605 tokens before; produced 2 deterministic descendants.
- `guide_du_financement_des_entreprises_non_recourse_discount__r001` — 557 tokens before; produced 2 deterministic descendants.
- `guide_du_financement_des_entreprises_commercial_discount__r001` — 554 tokens before; produced 2 deterministic descendants.
- `guide_du_financement_des_entreprises_invoice_advances__r001` — 539 tokens before; produced 2 deterministic descendants.
- `guide_du_financement_des_entreprises_campaign_credit__r001` — 505 tokens before; produced 2 deterministic descendants.
- `guide_du_financement_des_entreprises_local_public_market_guarantee__r001` — 734 tokens before; produced 3 deterministic descendants.
- `guide_du_financement_des_entreprises_export_public_market_guarantee__r001` — 549 tokens before; produced 2 deterministic descendants.
- `guide_du_financement_des_entreprises_public_market_advances__r001` — 586 tokens before; produced 2 deterministic descendants.
- `guide_du_financement_des_entreprises_import_guarantee_letter__r001` — 537 tokens before; produced 2 deterministic descendants.
- `guide_du_financement_des_entreprises_documentary_credit__r001` — 672 tokens before; produced 2 deterministic descendants.
- `guide_du_financement_des_entreprises_foreign_currency_endorsement__r001` — 535 tokens before; produced 2 deterministic descendants.
- `guide_du_financement_des_entreprises_foreign_currency_guarantee__r001` — 546 tokens before; produced 2 deterministic descendants.
- `guide_du_financement_des_entreprises_foreign_currency_import_refinancing__r001` — 545 tokens before; produced 2 deterministic descendants.
- `guide_du_financement_des_entreprises_customs_guarantee__r001` — 1056 tokens before; produced 3 deterministic descendants.
- `guide_du_financement_des_entreprises_export_pre_financing_dirhams__r001` — 559 tokens before; produced 2 deterministic descendants.
- `guide_du_financement_des_entreprises_export_pre_financing_currency__r001` — 568 tokens before; produced 2 deterministic descendants.
- `guide_du_financement_des_entreprises_foreign_export_receivables_advance__r001` — 559 tokens before; produced 2 deterministic descendants.
- `guide_du_financement_des_entreprises_foreign_currency_receivables_mobilization__r001` — 554 tokens before; produced 2 deterministic descendants.
- `guide_du_financement_des_entreprises_mourabaha__r001` — 539 tokens before; produced 2 deterministic descendants.
- `guide_du_financement_des_entreprises_tamwil_chamal__r001` — 662 tokens before; produced 2 deterministic descendants.
- `guide_du_financement_des_entreprises_green_invest__r001` — 567 tokens before; produced 2 deterministic descendants.
- `guide_du_financement_des_entreprises_green_invest__r002` — 736 tokens before; produced 3 deterministic descendants.
- `guide_du_financement_des_entreprises_renovotel__r001` — 983 tokens before; produced 3 deterministic descendants.
- `guide_du_financement_des_entreprises_mdm_invest__r001` — 834 tokens before; produced 4 deterministic descendants.
- `guide_du_financement_des_entreprises_french_line__r001` — 829 tokens before; produced 3 deterministic descendants.
- `guide_du_financement_des_entreprises_tatwir_croissance_verte__r001` — 725 tokens before; produced 3 deterministic descendants.
- `guide_du_financement_des_entreprises_mouwakaba__r001` — 850 tokens before; produced 3 deterministic descendants.
- `guide_du_financement_des_entreprises_finea_guarantees__r001` — 667 tokens before; produced 2 deterministic descendants.
- `guide_du_financement_des_entreprises_finea_guarantees__r002` — 665 tokens before; produced 2 deterministic descendants.
- `guide_du_financement_des_entreprises_finea_private_market_advances__r001` — 1025 tokens before; produced 4 deterministic descendants.
- `guide_du_financement_des_entreprises_finea_private_market_advances_followup__r001` — 994 tokens before; produced 3 deterministic descendants.
- `guide_du_financement_des_entreprises_industrial_ecosystem_aid__r001` — 761 tokens before; produced 3 deterministic descendants.
- `guide_du_financement_des_entreprises_industrial_ecosystem_aid__r002` — 659 tokens before; produced 2 deterministic descendants.
- `guide_du_financement_des_entreprises_investment_charter_aid__r001` — 527 tokens before; produced 2 deterministic descendants.
- `guide_du_financement_des_entreprises_hassan_ii_fund__r001` — 736 tokens before; produced 3 deterministic descendants.
- `guide_du_financement_des_entreprises_hassan_ii_fund__r002` — 726 tokens before; produced 3 deterministic descendants.
- `guide_du_financement_des_entreprises_agricultural_development_fund__r001` — 776 tokens before; produced 3 deterministic descendants.
- `guide_du_financement_des_entreprises_agricultural_development_fund__r002` — 604 tokens before; produced 3 deterministic descendants.
- `guide_du_financement_des_entreprises_export_growth_contracts__r001` — 751 tokens before; produced 3 deterministic descendants.
- `guide_du_financement_des_entreprises_export_growth_contracts__r002` — 502 tokens before; produced 2 deterministic descendants.
- `guide_du_financement_des_entreprises_contractual_regime__r001` — 704 tokens before; produced 2 deterministic descendants.
- `guide_du_financement_des_entreprises_contractual_regime__r002` — 546 tokens before; produced 2 deterministic descendants.
- `guide_du_financement_des_entreprises_ebrd_advice__r001` — 740 tokens before; produced 3 deterministic descendants.
- `guide_du_financement_des_entreprises_ebrd_advice__r002` — 717 tokens before; produced 3 deterministic descendants.
- `guide_du_financement_des_entreprises_ifc_financing__r001` — 845 tokens before; produced 3 deterministic descendants.
- `guide_du_financement_des_entreprises_venture_capital__r001` — 511 tokens before; produced 2 deterministic descendants.
- `guide_du_financement_des_entreprises_public_share_offering__r001` — 702 tokens before; produced 2 deterministic descendants.
- `guide_du_financement_des_entreprises_public_share_offering__r002` — 557 tokens before; produced 2 deterministic descendants.
- `guide_du_financement_des_entreprises_bond_issuance__r001` — 555 tokens before; produced 2 deterministic descendants.
- `guide_du_financement_des_entreprises_business_plan_definition__r002` — 611 tokens before; produced 2 deterministic descendants.
- `guide_du_financement_des_entreprises_business_plan_definition__r003` — 632 tokens before; produced 3 deterministic descendants.
- `guide_du_financement_des_entreprises_business_plan_cover_and_company__r001` — 765 tokens before; produced 3 deterministic descendants.
- `guide_du_financement_des_entreprises_business_plan_cover_and_company__r002` — 753 tokens before; produced 3 deterministic descendants.
- `guide_du_financement_des_entreprises_business_plan_legal_annexes__r001` — 559 tokens before; produced 2 deterministic descendants.
- `guide_du_financement_des_entreprises_real_guarantees__r001` — 1118 tokens before; produced 4 deterministic descendants.
- `guide_du_financement_des_entreprises_contact_directory_local__r001` — 1287 tokens before; produced 5 deterministic descendants.
- `guide_du_financement_des_entreprises_contact_directory_microfinance__r001` — 1196 tokens before; produced 4 deterministic descendants.
- `guide_du_financement_des_entreprises_contact_directory_banks_leasing__r001` — 1164 tokens before; produced 4 deterministic descendants.
- `guide_du_financement_des_entreprises_contact_directory_banks_leasing__r002` — 1084 tokens before; produced 5 deterministic descendants.
- `guide_du_financement_des_entreprises_contact_directory_banks_leasing__r004` — 862 tokens before; produced 3 deterministic descendants.
- `guide_du_financement_des_entreprises_contact_directory_public_capital__r002` — 1009 tokens before; produced 3 deterministic descendants.
- `guide_du_financement_des_entreprises_contact_directory_public_capital__r003` — 802 tokens before; produced 3 deterministic descendants.
- `guide_du_financement_des_entreprises_glossary_a_to_c__r001` — 1023 tokens before; produced 3 deterministic descendants.
- `guide_du_financement_des_entreprises_glossary_c_to_e__r001` — 1058 tokens before; produced 3 deterministic descendants.
- `guide_du_financement_des_entreprises_glossary_c_to_e__r002` — 915 tokens before; produced 3 deterministic descendants.
- `guide_du_financement_des_entreprises_glossary_f_to_r__r001` — 533 tokens before; produced 2 deterministic descendants.
- `guide_programme_integre_appui_financement_entreprises_ar_chunk_002__r001` — 720 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_en_phase3d1_chunk_0002__r001` — 613 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_phase3d1_chunk_0003__r001` — 703 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_en_phase3d1_chunk_0004__r001` — 539 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_en_phase3d1_chunk_0005__r001` — 511 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0002__r001` — 758 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0002__r002` — 782 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0003__r001` — 737 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0003__r002` — 795 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0004__r001` — 743 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0004__r002` — 774 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0005__r001` — 666 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0005__r002` — 699 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0005__r003` — 614 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0006__r001` — 714 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0006__r002` — 693 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0007__r001` — 713 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0007__r002` — 736 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0008__r001` — 593 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0008__r002` — 657 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0008__r003` — 590 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0009__r001` — 642 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0009__r002` — 605 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0009__r003` — 651 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0009__r004` — 526 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0009__r005` — 705 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0009__r006` — 511 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0010__r001` — 620 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0010__r002` — 523 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0011__r001` — 586 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0011__r003` — 684 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0012__r001` — 641 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0012__r002` — 758 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0013__r001` — 650 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0013__r003` — 558 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0014__r001` — 756 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0014__r002` — 711 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0014__r003` — 679 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0015__r001` — 928 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0015__r002` — 774 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0016__r001` — 653 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0016__r002` — 722 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0016__r003` — 663 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0017__r001` — 671 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0017__r002` — 683 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0017__r003` — 1005 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0017__r004` — 582 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0018__r001` — 694 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0018__r002` — 645 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0019__r001` — 638 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0019__r002` — 549 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0020__r001` — 679 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0020__r002` — 741 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0021__r001` — 622 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0021__r002` — 574 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0021__r003` — 671 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0022__r001` — 874 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0022__r002` — 634 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0023__r001` — 768 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0023__r002` — 696 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0024__r001` — 693 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0025__r001` — 686 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0025__r002` — 608 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0025__r003` — 609 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0026__r002` — 510 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0026__r003` — 752 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0027__r001` — 696 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0027__r002` — 660 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0028__r001` — 639 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0028__r002` — 617 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0029__r001` — 663 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0029__r002` — 532 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0029__r003` — 631 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0030__r001` — 678 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0030__r002` — 665 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0030__r003` — 717 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0031__r001` — 671 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0031__r004` — 633 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0032__r001` — 585 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0032__r002` — 528 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0032__r005` — 523 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0033__r001` — 780 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0033__r002` — 774 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0033__r003` — 563 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0033__r004` — 587 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0034__r001` — 839 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0034__r002` — 660 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0034__r004` — 581 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0035__r001` — 709 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0035__r002` — 671 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0036__r001` — 763 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0036__r002` — 637 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0036__r003` — 665 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0036__r005` — 521 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0037__r001` — 663 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0038__r001` — 705 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0038__r002` — 530 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0038__r003` — 586 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0038__r004` — 615 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0039__r001` — 635 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0039__r002` — 611 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0039__r003` — 675 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0040__r001` — 584 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0040__r002` — 730 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0041__r001` — 689 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0041__r004` — 589 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0042__r001` — 556 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0042__r002` — 502 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0043__r001` — 525 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0043__r002` — 568 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0044__r001` — 554 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0044__r002` — 601 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0045__r002` — 513 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0045__r003` — 606 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0046__r001` — 558 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0046__r002` — 673 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0046__r003` — 548 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0046__r004` — 525 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0047__r001` — 608 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0047__r003` — 590 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0047__r004` — 515 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0048__r001` — 588 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0048__r003` — 527 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0048__r004` — 520 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0048__r005` — 550 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0049__r001` — 725 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0049__r002` — 580 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0049__r004` — 569 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0050__r001` — 659 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0050__r003` — 528 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0050__r004` — 766 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0051__r001` — 604 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_en_chunk_0051__r003` — 529 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_phase3d1_chunk_0002__r001` — 798 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_phase3d1_chunk_0002__r002` — 767 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_phase3d1_chunk_0003__r001` — 584 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_phase3d1_chunk_0003__r003` — 884 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_phase3d1_chunk_0004__r001` — 705 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_phase3d1_chunk_0005__r001` — 755 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_phase3d1_chunk_0005__r002` — 644 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0002__r001` — 726 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0002__r002` — 525 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0003__r001` — 657 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0003__r002` — 636 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0004__r001` — 756 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0004__r002` — 740 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0004__r003` — 689 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0004__r004` — 889 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0005__r001` — 711 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0005__r002` — 760 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0005__r003` — 692 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0006__r001` — 624 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0006__r004` — 834 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0008__r001` — 609 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0008__r002` — 756 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0008__r003` — 679 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0009__r001` — 784 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0009__r002` — 781 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0009__r003` — 726 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0009__r004` — 733 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0009__r005` — 755 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0011__r001` — 661 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0011__r003` — 611 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0012__r001` — 707 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0012__r002` — 600 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0013__r001` — 807 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0013__r002` — 667 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0070__r001` — 519 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0014__r001` — 836 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0014__r002` — 896 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0014__r003` — 537 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0015__r001` — 856 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0015__r002` — 926 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0015__r003` — 639 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0016__r001` — 830 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0016__r002` — 736 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0016__r003` — 753 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0016__r004` — 598 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0017__r001` — 906 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0017__r002` — 510 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0017__r004` — 667 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0018__r001` — 766 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0018__r002` — 719 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0019__r001` — 814 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0019__r002` — 628 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0020__r001` — 807 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0021__r001` — 724 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0021__r002` — 612 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0021__r003` — 766 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0022__r001` — 702 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0022__r002` — 973 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0022__r003` — 771 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0023__r001` — 940 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0023__r002` — 873 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0023__r003` — 887 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0024__r001` — 982 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0025__r001` — 919 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0025__r002` — 757 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0025__r003` — 784 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0026__r001` — 1159 tokens before; produced 4 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0027__r001` — 904 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0027__r002` — 616 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0028__r001` — 871 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0028__r002` — 774 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0028__r003` — 585 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0028__r005` — 534 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0029__r001` — 896 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0029__r002` — 711 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0029__r003` — 776 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0085__r001` — 764 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0030__r001` — 816 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0030__r002` — 916 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0031__r002` — 851 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0032__r001` — 741 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0032__r002` — 740 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0032__r003` — 697 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0032__r004` — 527 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0033__r001` — 799 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0033__r002` — 917 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0033__r003` — 702 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0034__r001` — 1109 tokens before; produced 4 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0034__r002` — 779 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0034__r003` — 738 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0035__r002` — 788 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0035__r003` — 868 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0035__r004` — 569 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0036__r001` — 856 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0036__r002` — 809 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0036__r003` — 872 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0036__r004` — 654 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0036__r005` — 649 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0037__r001` — 764 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0037__r002` — 595 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0038__r001` — 781 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0038__r002` — 814 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0038__r003` — 746 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0039__r001` — 747 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0039__r002` — 748 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0039__r003` — 516 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0040__r001` — 772 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0040__r002` — 875 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0041__r001` — 832 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0041__r002` — 655 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0041__r003` — 699 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0042__r001` — 745 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0043__r001` — 632 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0043__r002` — 664 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0043__r003` — 601 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0044__r001` — 714 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0044__r002` — 507 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0045__r001` — 637 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0045__r002` — 711 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0045__r003` — 716 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0046__r001` — 818 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0046__r002` — 819 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0046__r003` — 586 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0046__r004` — 629 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0047__r001` — 810 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0047__r002` — 579 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0047__r003` — 635 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0047__r004` — 625 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0048__r001` — 720 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0048__r002` — 634 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0048__r003` — 582 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0048__r004` — 670 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0049__r001` — 888 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0049__r002` — 695 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0049__r004` — 684 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0050__r001` — 767 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0050__r002` — 815 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0050__r004` — 539 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0051__r001` — 801 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_chunk_0051__r003` — 570 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_phase3d1_chunk_1003__r001` — 510 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_phase3d1_chunk_1003__r002` — 525 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_phase3d1_chunk_1003__r003` — 726 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_phase3d1_chunk_1005__r001` — 889 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_phase3d1_chunk_1008__r001` — 741 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_phase3d1_chunk_1009__r001` — 876 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_phase3d1_chunk_1010__r001` — 994 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_phase3d1_chunk_1014__r001` — 749 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_phase3d1_chunk_1017__r001` — 773 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_phase3d1_chunk_1018__r001` — 663 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_phase3d1_chunk_1022__r001` — 1212 tokens before; produced 4 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_phase3d1_chunk_1028__r001` — 678 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_phase3d1_chunk_1030__r001` — 1036 tokens before; produced 4 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_phase3d1_chunk_1039__r001` — 783 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_phase3d1_chunk_1041__r001` — 1060 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_phase3d1_chunk_1042__r001` — 821 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_phase3d1_chunk_1044__r001` — 597 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_phase3d1_chunk_1045__r001` — 1095 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_phase3d1_chunk_1047__r001` — 930 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_phase3d1_chunk_1048__r001` — 656 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_phase3d1_chunk_1051__r001` — 572 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_phase3d1_chunk_1052__r001` — 582 tokens before; produced 2 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_phase3d1_chunk_1054__r001` — 752 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_phase3d1_chunk_1054__r002` — 682 tokens before; produced 3 deterministic descendants.
- `investors_guide_territorial_opportunities_fr_phase3d1_chunk_1054__r004` — 514 tokens before; produced 2 deterministic descendants.
- `manar_al_moustatmir_eng_png_phase3f_0002__r001` — 986 tokens before; produced 3 deterministic descendants.
- `manar_al_moustatmir_eng_png_phase3f_0015__r001` — 686 tokens before; produced 2 deterministic descendants.
- `manar_al_moustatmir_eng_png_phase3f_0020__r001` — 728 tokens before; produced 3 deterministic descendants.
- `manar_al_moustatmir_eng_png_phase3f_0026__r001` — 674 tokens before; produced 2 deterministic descendants.
- `manar_al_moustatmir_eng_png_phase3f_0026__r002` — 638 tokens before; produced 2 deterministic descendants.
- `manar_al_moustatmir_eng_png_phase3f_0027__r001` — 647 tokens before; produced 2 deterministic descendants.
- `manar_al_moustatmir_eng_png_phase3f_0027__r002` — 616 tokens before; produced 2 deterministic descendants.
- `manar_al_moustatmir_eng_png_phase3f_0030__r001` — 991 tokens before; produced 3 deterministic descendants.
- `manar_al_moustatmir_news_phase3f_0002__r001` — 999 tokens before; produced 4 deterministic descendants.
- `manar_al_moustatmir_news_phase3f_0015__r001` — 624 tokens before; produced 2 deterministic descendants.
- `manar_al_moustatmir_news_phase3f_0026__r003` — 679 tokens before; produced 2 deterministic descendants.
- `manar_al_moustatmir_news_phase3f_0027__r002` — 567 tokens before; produced 2 deterministic descendants.
- `manar_al_moustatmir_news_phase3f_0027__r003` — 813 tokens before; produced 3 deterministic descendants.
- `manar_al_moustatmir_news_phase3f_0030__r001` — 1171 tokens before; produced 3 deterministic descendants.
- `nv_guide_cout_facteurs_cri_2024_phase3f_0006__r001` — 514 tokens before; produced 2 deterministic descendants.
- `nv_guide_cout_facteurs_cri_2024_phase3f_0008__r001` — 553 tokens before; produced 2 deterministic descendants.
- `nv_guide_cout_facteurs_cri_2024_phase3f_0017__r001` — 908 tokens before; produced 4 deterministic descendants.
- `nv_guide_cout_facteurs_cri_2024_phase3f_0018__r001` — 569 tokens before; produced 2 deterministic descendants.
- `nv_guide_cout_facteurs_cri_2024_phase3f_0022__r001` — 1128 tokens before; produced 3 deterministic descendants.
- `nv_guide_cout_facteurs_cri_2024_phase3f_0024__r001` — 523 tokens before; produced 2 deterministic descendants.
- `nv_guide_cout_facteurs_cri_2024_phase3f_0024__r002` — 599 tokens before; produced 2 deterministic descendants.
- `nv_guide_cout_facteurs_cri_2024_phase3f_0024__r003` — 552 tokens before; produced 2 deterministic descendants.
- `nv_guide_cout_facteurs_cri_2024_phase3f_0030__r001` — 574 tokens before; produced 2 deterministic descendants.
- `nv_guide_cout_facteurs_cri_2024_phase3f_0031__r001` — 619 tokens before; produced 2 deterministic descendants.

## Chunk-size diagnostics

- Minimum: 9
- Median: 1124.0
- Mean: 1034.3
- Maximum: 2334
- <50: 27
- <100: 52
- <200: 142
- >3,000: 0
- >4,500: 0
- >5,000: 0
- >8,000: 0
- >12,000: 0

## Boilerplate diagnostics

Repeated source lines were counted but not removed. No aggressive boilerplate suppression was applied to embedding_text.

- `www.investangier.com` — 278 parent occurrences
- `k Contact sur la région` — 80 parent occurrences
- `Description de l’offre de service` — 80 parent occurrences
- `Couverture territoriale` — 80 parent occurrences
- `Champs d’intervention` — 79 parent occurrences
- `b Critères d’éligibilité` — 76 parent occurrences
- `e Plafond de financement` — 76 parent occurrences
- `i Documents nécessaires` — 73 parent occurrences
- `h Modalités de remboursement` — 72 parent occurrences
- `c Conditions de garanties` — 70 parent occurrences
- `d Coût du financement de l’opération` — 64 parent occurrences
- `MATRICE SWOT DE L’OPPORTUNITÉ D’INVESTISSEMENT` — 55 parent occurrences
- `DESCRIPTION DU PROJET` — 52 parent occurrences
- `Coût potentiel de l’investissement` — 47 parent occurrences
- `www.manaralmoustatmir.com` — 45 parent occurrences
- `CENTRE RÉGIONAL D'INVESTISSEMENT` — 45 parent occurrences
- `Dispositifs d'appui prevus dans le cadre de la` — 45 parent occurrences
- `charte d'investissement` — 44 parent occurrences
- `+212 (0) 539 342 303` — 41 parent occurrences
- `Programme « IDMAJ » / Programme « TAEHIL »` — 38 parent occurrences

## Phase-4B Qdrant payload planning

Phase 4A JSONL retains full source_spans. A compact future Qdrant payload should include: retrieval_chunk_id, parent_semantic_chunk_id, document_id, document_family_id, filename, language, document_title, topic_id, content_type, semantic_tags, heading_path, page_start, page_end, source_pages, page_mapping_precision, primary_year, years_mentioned, reference_period_type, reference_period_year, reference_period_end_date, retrieval_chunk_index, retrieval_chunk_count, is_subchunk, indexable, and text. Full source_spans should remain in the semantic/provenance layer and be resolved separately rather than duplicated into every production payload.

## Validation

Semantic input validation: PASS for 33 schema-2.2 documents.
Retrieval coverage: PASS — 913 parents covered / 913.
Retrieval IDs: PASS.
Metadata inheritance and bounds: PASS.
Indexability fields: PASS.
Indexable embedding text: PASS.
Offset-based exact mapping consistency: PASS.
Exact page mappings: PASS — 1901 exact, 0 parent.
E5 safe token budget: PASS — all indexable embedding inputs are <= 500 tokens.
Determinism SHA-256: PASS — current `5062E2135C8856EB5BE03D68F0D065C8460825B6899F52E839487FD0519011F2`.

## Output artifacts

- `data\retrieval_v2\retrieval_chunks.jsonl`
- `data\retrieval_v2\retrieval_manifest.json`
- `data\retrieval_v2\retrieval_build_report.md`

Qdrant ingestion: **not performed**. Production embeddings: **not calculated**.
