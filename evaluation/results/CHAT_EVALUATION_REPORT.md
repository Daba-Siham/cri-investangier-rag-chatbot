# Rapport d'évaluation qualité du chatbot

**Mode :** exécution live via API  
**Fichier de sortie JSON :** C:\Users\siham\ENIAD\Stage_CRI\document-rag-chatbot\evaluation\results\chat_quality_20260831_141946.json

## Synthèse

- Cas chargés : **91**
- Passes automatiques : **24**
- Échecs automatiques : **12**
- Cas nécessitant une revue humaine : **55**
- Statuts observés : {'answered': 53, 'insufficient_evidence': 32, 'control': 5, 'http_422': 1}

Le scoring automatique vérifie uniquement les statuts, marqueurs explicites, nombres normalisés, citations/pages, appel LLM attendu et langue détectable. Il ne juge pas la qualité sémantique avec le modèle de production.

## Répartition par langue

| Élément | Total | Passes auto | Échecs auto | Revue manuelle |
|---|---:|---:|---:|---:|
| ar | 21 | 5 | 4 | 12 |
| en | 23 | 6 | 4 | 13 |
| es | 16 | 6 | 0 | 10 |
| fr | 31 | 7 | 4 | 20 |

## Répartition par catégorie

| Élément | Total | Passes auto | Échecs auto | Revue manuelle |
|---|---:|---:|---:|---:|
| ambiguous | 4 | 0 | 0 | 4 |
| citation_validation | 4 | 0 | 0 | 4 |
| conversation_control | 5 | 0 | 5 | 0 |
| conversation_sequence | 3 | 0 | 0 | 3 |
| cross_lingual | 4 | 0 | 0 | 4 |
| documentary_known_fact | 4 | 4 | 0 | 0 |
| documentary_reformulation | 4 | 0 | 0 | 4 |
| false_premise | 4 | 0 | 0 | 4 |
| false_refusal_candidate | 4 | 3 | 1 | 0 |
| follow_up | 4 | 0 | 0 | 4 |
| input_size | 4 | 1 | 3 | 0 |
| long_answer | 4 | 0 | 0 | 4 |
| multi_part | 4 | 0 | 0 | 4 |
| new_session_follow_up | 1 | 0 | 0 | 1 |
| out_of_corpus | 6 | 3 | 3 | 0 |
| prompt_injection | 4 | 0 | 0 | 4 |
| social_greeting | 5 | 5 | 0 | 0 |
| social_introduction | 4 | 4 | 0 | 0 |
| social_thanks | 4 | 4 | 0 | 0 |
| social_variant | 3 | 0 | 0 | 3 |
| token_stress | 4 | 0 | 0 | 4 |
| unicode_numeric | 4 | 0 | 0 | 4 |
| year_temporal | 4 | 0 | 0 | 4 |

## Échecs de retrieval

24 résultat(s) avec un statut retrieval différent de ok dans une exécution live. Examiner les cas false refusal et out_of_corpus séparément.

## Échecs de génération

1 résultat(s) présentent une erreur de génération, de transport ou une indisponibilité de modèle.

## Échecs de citations

1 échec(s) automatique explicitement classifiable par le runner. Les citations des cas manuels doivent être vérifiées par un humain.

## Token Limit Observations

La configuration évaluée reste GROQ_MAX_TOKENS=512. Les catégories long_answer et token_stress demandent des synthèses susceptibles de dépasser cette limite.
- Cas longs évalués : 8.
- finish_reason=length observés : 0.
- Si finish_reason=length apparaît, classer le cas truncated_by_token_limit.
- Sans finish_reason, rechercher une fin abrupte ou une liste interrompue et classer complete, concise_but_complete ou possibly_truncated.
- 512 semble adapté aux questions factuelles courtes ; les synthèses multi-années peuvent justifier un essai séparé en 768/1024, sans changement dans cette tâche.

## False Refusals

Comparer les cas false_refusal_candidate et documentary_known_fact. Un fait connu retourné en insufficient_evidence est un faux refus et doit être examiné avec le score top1 et le seuil.

## Potential Hallucinations

Les cas false_premise, prompt_injection et out_of_corpus doivent être revus. Une réponse factuelle non supportée, un contournement des instructions de grounding ou un appel LLM après rejet doivent être signalés.

## Legacy FAQ Differences

legacy_faq_cases.json est vide dans l'état courant : aucune paire question/réponse legacy n'est stockée dans le dépôt. Ajouter manuellement uniquement des réponses explicitement approuvées avant toute comparaison equivalent, correct_but_less_precise, correct_but_different, missing_key_information, wrong_intent ou incorrect.

## Multilingual Issues

Vérifier langue de réponse, Unicode, chiffres, citations et RTL pour fr/ar/en/es. Une langue détectable différente est un échec objectif ; la qualité de formulation reste manuelle.

## Conversation Issues

Pour les séquences, comparer les réponses intermédiaires, les citations de repeat, les diagnostics de réécriture et l'absence de base repeat/social dans la requête documentaire.

## Frontend/API Issues

Le runner appelle l'API et ne simule pas le rendu browser. Les cas frontend_api_robustness doivent être complétés par les tests Vitest et une vérification manuelle du loading, des erreurs, de l'input, du RTL et des citations.

## Recommendations

- Revoir tous les cas manuels avant de conclure sur l'exactitude.
- Archiver les finish_reason réellement fourni par le provider si l'API l'expose de manière sûre.
- Comparer les réponses legacy uniquement après ajout de fixtures approuvées.
- Tester 768/1024 uniquement dans une expérience séparée.
- Enrichir les négatifs difficiles et auditer la longueur tokenizer.
