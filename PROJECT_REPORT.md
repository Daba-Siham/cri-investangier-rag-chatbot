# Rapport technique — Chatbot RAG multilingue CRI / Investangier

## 1. Résumé exécutif

Ce projet implémente un chatbot documentaire multilingue pour le Centre Régional d'Investissement Tanger-Tétouan-Al Hoceima. Les langues principales sont le français, l'arabe, l'anglais et l'espagnol ; le support amazigh/tamazight reste expérimental.

Le dépôt conserve une **V1 fonctionnelle** et documente une **V2 sémantique** construite séparément. V2 organise les documents par unités de connaissance, familles multilingues, temporalité et provenance exacte. Son retrieval a été évalué avec de meilleurs résultats que V1. La comparaison finale des réponses générées n'a pas été terminée à cause des quotas du fournisseur LLM, et aucun cutover V2 production n'a été réalisé.

## 2. Architecture et responsabilités

```text
PDF / sources CRI
    → JSON brut V1
    → JSON sémantique 2.2
    → retrieval chunks V2
    → multilingual-E5-base
    → Qdrant V2
    → Retriever V2
    → Context Builder / citations exactes
    → client OpenAI-compatible
    → FastAPI
    → React / TypeScript
```

La V1 reste associée à `cri_chunks_multilingual_e5_base`. La V2 utilise `cri_chunks_multilingual_e5_v2`. Cette séparation permet de comparer les systèmes et de conserver une voie de retour historique.

Les responsabilités principales sont réparties entre `src/ingestion`, `src/chunking`, `src/embeddings`, `src/vectorstore`, `src/retrieval`, `src/generation`, `src/rag`, `src/conversation`, `src/api` et `frontend`.

## 3. Données et représentation documentaire

### 3.1 V1 — JSON d'extraction

```json
{
  "document_id": "...",
  "filename": "...",
  "language": "fr",
  "pages": [{"page": 1, "text": "..."}]
}
```

Ce format est page-oriented : il conserve le texte extrait et la page PDF. La préparation historique applique un découpage par caractères, environ 2 800 caractères avec overlap 400, et alimente la baseline.

### 3.2 V2 — JSON sémantique 2.2

La V2 utilise `data/semantic_json/*.json` et le schéma 2.2. Le document contient `document_family_id`, un bloc `metadata`, des sections, sous-sections et chunks sémantiques. Chaque chunk conserve notamment :

- `topic_id` et `semantic_tags` canoniques ;
- `content_type` ;
- `heading_path` dans la langue source ;
- `temporal_scope` ;
- `page_start`, `page_end` et `source_spans` exacts ;
- le texte source original.

Le JSON brut est la couche d'extraction immuable. Le JSON sémantique est la couche de connaissance canonique de V2. Les traductions partagent une famille documentaire seulement lorsqu'elles correspondent réellement au même document ou à la même édition.

## 4. Embeddings et Qdrant

Le modèle V1/V2 documenté est `intfloat/multilingual-e5-base`, dimension 768, avec convention `passage:` pour les documents et `query:` pour les requêtes.

| Élément | V1 | V2 |
|---|---|---|
| Collection | `cri_chunks_multilingual_e5_base` | `cri_chunks_multilingual_e5_v2` |
| Taille | 1 893 points | 1 901 retrieval records / 1 894 points indexés |
| Parents | Chunks page/caractères | 913 parents sémantiques |
| Découpage | caractères, 2 800 / overlap 400 | sous-chunks sémantiques token-safe |
| Maximum V2 validé | non applicable | 499 tokens d'embedding |
| Similarité | cosine | cosine |

La V2 ne modifie pas la collection V1. L'ingestion V2 est réalisée par `scripts/ingest_qdrant_v2.py` avec une collection distincte et des payloads compacts, tandis que le JSONL conserve la provenance détaillée.

## 5. Retrieval V1 et V2

V1 utilise environ K=10 candidats, K=5 résultats finaux, une déduplication historique par document et le seuil historique `0.823114`. V2 utilise K=30 candidats et K=5 résultats finaux, regroupe les enfants d'un même parent sémantique, applique une diversité souple par famille documentaire, conserve la recherche interlingue et utilise les métadonnées sémantiques/temporelles comme faibles signaux.

Le seuil V2 candidat `0.825` est exclusivement issu de l'évaluation d'abstention. Il ne doit pas être présenté comme un seuil production.

`src/retrieval/context_builder_v2.py` sépare la pertinence de l'assemblage du contexte. Il résout les `source_spans` depuis `data/retrieval_v2/retrieval_chunks.jsonl`, clippe la provenance aux sous-chunks réellement utilisés et génère des citations déterministes.

## 6. Résultats V2

| Métrique | V1 | V2 |
|---|---:|---:|
| Family Recall@1 | 0,36 | 0,60 |
| Family Recall@3 | 0,56 | 0,76 |
| Family Recall@5 | 0,64 | 0,86 |
| Family MRR | 0,469 | 0,693 |
| Succès interlingue | 0,22 | 0,38 |

Family Recall@5 V2 par langue : FR `1,00`, EN `0,8667`, AR `0,60`, ES `0,90`. L'arabe reste la faiblesse principale de l'évaluation.

Ces valeurs évaluent le retrieval. Elles ne démontrent pas une supériorité des réponses générées, puisque le benchmark final V1/V2 de génération est resté incomplet à cause des quotas API.

## 7. Génération et configuration LLM

`src/generation/llm_client.py` est un client générique OpenAI-compatible. Groq a été utilisé pour le développement avec `qwen/qwen3.8-27b`, mais Groq n'est pas une dépendance architecturale de la V2.

`src/utils/config.py` charge `.env` et lit les variables suivantes :

```text
LLM_API_KEY
LLM_BASE_URL
LLM_MODEL
LLM_TEMPERATURE
LLM_MAX_TOKENS
LLM_TIMEOUT_SECONDS
LLM_MAX_RETRIES
```

Pour OpenAI, l'équipe CRI doit choisir le modèle et fournir ses propres valeurs. Exemple documentaire, sans secret :

```env
LLM_API_KEY=<clé OpenAI de CRI>
LLM_BASE_URL=<base URL compatible>
LLM_MODEL=<modèle choisi>
LLM_TEMPERATURE=0.0
LLM_MAX_TOKENS=1024
LLM_TIMEOUT_SECONDS=30
LLM_MAX_RETRIES=1
```

Cette migration de fournisseur ne nécessite normalement pas de reconstruire le JSON sémantique, les embeddings E5, Qdrant ou le retrieval. Les tests de génération, langue, sortie structurée et citations doivent être rejoués.

## 8. Intégration FAQ historique

La base FAQ historique de l'entreprise **n'est pas présente dans ce dépôt**. Elle doit être intégrée par un adaptateur vers les unités sémantiques V2, avec `content_type: "faq"` lorsque cela est approprié.

Mapping recommandé : catégorie vers topic, question vers titre/tags, réponse approuvée vers texte source, langue vers `metadata.language`, date vers `temporal_scope`, identifiant FAQ vers provenance stable. Une FAQ sans page PDF ne doit pas recevoir une page inventée ; son type de source doit être conservé explicitement.

Deux stratégies sont possibles :

- **RAG unifié**, où les FAQ deviennent des preuves normales de V2 ;
- **priorité FAQ canonique**, où une correspondance FAQ approuvée est traitée avant le fallback documentaire.

La priorité FAQ canonique n'est **pas implémentée**.

## 9. État actuel

| Composant | État |
|---|---|
| JSON brut V1 | Disponible |
| JSON sémantique V2 | Implémenté |
| Retrieval chunks V2 | Implémenté |
| Qdrant V2 | Implémenté |
| Retriever V2 | Évalué |
| Provenance exacte | Validée |
| Abstention V2 | Expérimentale/calibrée |
| Temporalité V2 | Expérimentale/évaluée |
| Génération | Fonctionnelle |
| Benchmark génération V1/V2 | Incomplet — quota fournisseur |
| FAQ historique | Non implémentée |
| OpenAI production | Non configuré |
| Cutover production V2 | Non effectué |

Le dernier gate est `V2_NOT_READY`. Cela signifie que la comparaison des réponses n'a pas été finalisée, non que le retrieval V2 a échoué.

## 10. Tests et exécution

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
docker compose up -d
python scripts/run_api.py
```

Tests :

```powershell
python -m pytest tests -p no:cacheprovider
cd frontend
npm test
npm run build
```

Les évaluations V2 sont documentées par `scripts/evaluate_retriever_v2.py`, `scripts/evaluate_context_v2.py`, `scripts/evaluate_rag_v1_vs_v2.py` et les scripts `evaluate_rag_4e1.py` à `evaluate_rag_4e3.py`.

## 11. Difficultés et limites

- Le retrieval arabe reste plus faible que FR/EN/ES.
- Le benchmark de génération doit être rejoué avec un fournisseur et un quota maîtrisés.
- La FAQ historique doit encore être convertie et validée.
- La configuration OpenAI de l'entreprise n'est pas fournie.
- Aucun cutover V2 ni déploiement production n'est inclus.
- Le support Amazigh/Tamazight reste expérimental.

## 12. Sécurité et transfert

Ne pas committer `.env`, clés API, PDF internes, JSON confidentiels, stockage Qdrant local, `.venv`, `node_modules` ou caches. Avant transfert : fournir un `.env.example`, utiliser une clé OpenAI appartenant à CRI, ne pas transférer de credentials Groq personnels, vérifier la politique Git des données internes et inspecter l'historique pour les secrets.
