# Retrieval question review sheet

Evidence excerpts below are short excerpts copied from the referenced chunks in `data/processed/chunks.json`. Equivalent translated pages are listed together where the same fact is present.

| ID | Language | Topic | Cross-lingual? | Expected source page(s) | Evidence excerpt |
|---|---|---|---|---|---|
| q001 | fr | CRUI / investment 2024 | yes | `chiffres_cles_crui_1er_semestre_2024_francais` p2; translated equivalents p2 | “379 Projets approuvés soit 87,5%” |
| q002 | fr | CRUI / sectors | no | `chiffres_cles_crui_1er_semestre_2024_francais` p3 | “Industrie : 54%” |
| q003 | fr | logistics | no | `brochure_secteur_logistique` p6 | “connectivité maritime hebdomadaire vers 180 ports mondiaux” |
| q004 | fr | logistics / training | no | `brochure_secteur_logistique` p4 | “accueil de 7429 stagiaires… dont 3769 dans la Région” |
| q005 | fr | business creation | yes | `fr_chiffres_cles_annee_2025` p2; translated equivalents p2 | “15 286 NOUVELLES ENTREPRISES CRÉÉES EN 2025” |
| q006 | ar | CRUI / investment 2023 | yes | `akhbar_al_moustatmir_news` p25; `manar_al_moustatmir_news` p25 | “وافقت… على 709 طلبا” |
| q007 | ar | CRUI / conventions 2023 | yes | `akhbar_al_moustatmir_news` p5; French/English equivalents p5 | “18 مليار درهم… 10.200 فرصة عمل” |
| q008 | ar | energy | yes | `arabe_chiffres_cles_2025` p9; translated equivalents p9 | “11 مشروع… 22,4 مليار درهم” |
| q009 | ar | support / financing | no | `guide_programme_integre_appui_financement_entreprises_ar` p2 | “نضج الفكرة… إحداث المقاولة… البحث عن التمويلات” |
| q010 | ar | CRUI / investment 2025 | yes | `arabe_chiffres_cles_2025` p5; translated equivalents p5 | “487 ملف استثماري تمت المصادقة عليه” |
| q011 | es | CRUI / investment 2024 | yes | `chiffres_cles_crui_1er_semestre_2024_espagnol` p2; translated equivalents p2 | “379 proyectos aprobados” |
| q012 | es | CRUI / sectors | no | `chiffres_cles_crui_1er_semestre_2024_espagnol` p3 | “Industria: 54%” |
| q013 | es | energy | no | `esp_chiffres_cles_annee_2025` p9 | “11 proyectos aprobados… 2,4 GW de potencia instalada” |
| q014 | es | business creation | no | `esp_chiffres_cles_annee_2025` p2 | “15 286 NUEVAS EMPRESAS CREADAS EN 2025” |
| q015 | es | Tanger Tech / industry | no | `esp_presentation_cri_tta_vf` p32 | “Superficie 2 167 Ha… 100 000 Empleos” |
| q016 | en | business creation | no | `eng_chiffres_cles_annee_2025` p2 | “15 286 NEW COMPANIES CREATED IN 2025” |
| q017 | en | company support | no | `eng_chiffres_cles_annee_2025` p10 | “Facilitating finance access… Promoting innovation and entrepreneurship” |
| q018 | en | PIAFE / financing | no | `eng_chiffres_cles_annee_2025` p11 | “4 672 Financed files” |
| q019 | en | economic zones | no | `eng_panorama_des_zi` p46 | “Fnideq Economic Activity Zone… creation of 400 jobs” |
| q020 | en | CRUI / investment 2025 | yes | `eng_chiffres_cles_annee_2025` p5; translated equivalents p5 | “487 Acts approved by the CRUI” |
| q021 | fr | out of corpus | no | none | Expected source: none |
| q022 | ar | خارج corpus | no | none | Expected source: none |
| q023 | es | fuera del corpus | no | none | Expected source: none |
| q024 | en | out of corpus | no | none | Expected source: none |
| q025 | fr | out of corpus | no | none | Expected source: none |
| q026 | ar | خارج corpus | no | none | Expected source: none |
| q027 | es | fuera del corpus | no | none | Expected source: none |
| q028 | en | out of corpus | no | none | Expected source: none |
| q029 | fr | out of corpus | no | none | Expected source: none |

## Special human-review notes

- q001, q005, q008, q010, q011, and q020 intentionally include translated equivalent pages. Confirm that the equivalence policy is desired before scoring.
- q006 and q007 distinguish 2023 material from the 2024 and 2025 CRUI fact sheets; do not substitute a later-year page.
- q004 now explicitly asks for both the national capacity (7 429) and the regional capacity (3 769); both values come from `brochure_secteur_logistique` p4.
- q017 is a multi-item semantic retrieval question. Its ground truth is the source page being retrieved, not completeness of any generated answer; review this interpretation before scoring.
