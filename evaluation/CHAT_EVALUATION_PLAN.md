# Plan d'évaluation qualité du chatbot

## Objectif

Ce plan décrit l'évaluation de l'implémentation actuelle. Il ne modifie ni retrieval, ni embeddings, ni Qdrant, ni prompts Groq, ni frontend, ni routeur de production.

Le jeu principal est evaluation/chat_test_cases.json. Les faits attendus ne sont renseignés automatiquement que lorsqu'ils sont supportés par les fixtures ou résultats existants du dépôt. Les autres cas ont manual_review=true.

## Préparation

1. Démarrer Qdrant et le backend lorsque l'évaluation live est souhaitée.
2. Vérifier que la configuration locale correspond à .env.example sans copier de secret dans les résultats.
3. Lancer une première exécution limitée.
4. Inspecter les résultats JSON et le rapport Markdown.
5. Faire ensuite la revue qualitative des cas marqués manual_review_required.

## Échelle de revue humaine

| Note | Interprétation |
|---:|---|
| 5 | Correct, complet, clair et entièrement grounded |
| 4 | Correct, avec une omission mineure |
| 3 | Globalement correct mais incomplet ou imprécis |
| 2 | Problème important de pertinence ou de précision |
| 1 | Réponse incorrecte |
| 0 | Hallucination, contournement du grounding ou réponse dangereusement trompeuse |

### Dimensions séparées

Pour chaque cas qualitatif, noter séparément :

- exactitude factuelle ;
- complétude par rapport à la question ;
- grounding dans les passages retournés ;
- qualité des citations ;
- langue de la réponse ;
- qualité Unicode/RTL ;
- clarté et concision ;
- équivalence avec une réponse legacy lorsqu'une comparaison existe.

## Critères de revue

### Réponse

Vérifier que chaque affirmation est supportée par les passages récupérés. Une réponse concise peut obtenir 4 ou 5 si elle répond réellement à la demande. Une réponse très longue ne mérite pas une meilleure note si elle ajoute des informations non demandées.

### Refus

Un refus est approprié si la question est hors corpus ou si l'évidence est insuffisante. Un faux refus correspond à une question dont le fait est documenté mais que le système classe insufficient_evidence.

### Citations

Contrôler :

- existence d'une citation pour une réponse documentaire ;
- correspondance document/page avec l'évidence ;
- absence de citation inventée ;
- cohérence entre les affirmations et la page citée.

### Langue et arabe

La réponse doit suivre la langue de la question lorsque cela est possible. Pour l'arabe, vérifier ordre de lecture, nombres, ponctuation et absence d'inversion de caractères. Les citations peuvent garder une mise en page distincte pour les filenames.

### Conversations

Les séquences doivent être revues dans l'ordre :

- document -> repeat ;
- document -> follow-up ;
- document -> thanks -> follow-up ;
- document -> greeting -> follow-up ;
- nouvelle session -> follow-up sans historique.

Pour repeat, comparer réponse et citations et vérifier, avec diagnostics, l'absence d'un nouvel appel retrieval/LLM. Pour un follow-up, vérifier que la requête réécrite provient du dernier tour documentaire et non d'un message de contrôle.

## Longueur et tokens

GROQ_MAX_TOKENS reste 512 pendant cette évaluation. Les cas long_answer et token_stress demandent :

- finish_reason lorsque l'interface le rend disponible ;
- détection d'une fin abrupte ;
- comparaison entre question et parties effectivement couvertes ;
- classification complete, concise_but_complete, possibly_truncated ou truncated_by_token_limit.

finish_reason=length doit être signalé comme recommandation, sans changer la configuration.

## Entrées

MAX_USER_MESSAGE_CHARACTERS vaut 5000. Les cas input_size vérifient :

- entrée nominale ;
- environ 1000 caractères ;
- environ 4900 caractères ;
- plus de 5000 caractères.

Le cas dépassant la limite doit être rejeté par validation API sans appel LLM.

## Sécurité de l'évaluation

Les résultats peuvent contenir question, réponse, citations, statuts et métadonnées de génération bornées. Ils ne doivent jamais contenir :

- clé API ;
- header Authorization ;
- prompt complet ;
- contexte complet ;
- secrets d'environnement.

Les tests d'injection portent uniquement sur le grounding documentaire ; aucun payload offensif n'est nécessaire.

## Résultat final

Le script produit evaluation/results/chat_quality_YYYYMMDD_HHMMSS.json et met à jour evaluation/results/CHAT_EVALUATION_REPORT.md. Le rapport distingue le scoring objectif du besoin de revue humaine. Les conclusions sur l'exactitude sémantique ne doivent pas être produites par un LLM identique au modèle évalué.

## Commandes

Évaluation complète via le backend local :

    python scripts/evaluate_chat_quality.py --live-api

Une langue :

    python scripts/evaluate_chat_quality.py --live-api --language ar

Une catégorie et une limite :

    python scripts/evaluate_chat_quality.py --live-api --category follow_up --limit 4

Sortie personnalisée :

    python scripts/evaluate_chat_quality.py --live-api --output evaluation/results/my_run.json

