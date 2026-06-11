# AI Contract

## Purpose
Document how AI assistance should behave while building this repository (requirements, boundaries, and success criteria).

## Required kickoff prompt (must be followed)
Before generating or editing any code, the AI must:

1. Read `docs/AI_CONTRACT.md`, `docs/ARCHITECTURE.md`, and `docs/ZACHMAN_ONTOLOGY_FOR_AI_ARCHITECTURE.md`.
2. Acknowledge these rules explicitly in its first response.

Prompt snippet to use at the start of a new AI session:

```
You are a Trudy Architectural Lead. Before writing any code, read the following files:
AI_CONTRACT.md, ARCHITECTURE.md, and ZACHMAN_ONTOLOGY_FOR_AI_ARCHITECTURE.md.

Your goal is to scaffold a 6x6 visual web page that represents the Zachman Framework for a Zero Trust enterprise.
Every component you build must align with the "Never Trust, Always Verify" principle and the structural rules of the
Zachman Framework.

You are forbidden from creating one-off hacks; all logic must be rule-based and modular.
```

## Scope
AI may help with:
- Translating `ARCHITECTURE.md` into implementation tasks.
- Producing code scaffolding under `src/`.
- Creating ingestion/data mapping logic for Zachman-matrix CSVs under `data/` and `src/db/`.
- Writing tests and documentation updates.

## Mandatory engineering constraints
- **Zachman alignment**: UI and data models must preserve the 6x6 structure (rows × columns) and keep labels/axes explicit.
- **Zero Trust alignment**: Treat all inputs (CSV, user input, URL params) as untrusted; validate and constrain.
- **No one-off hacks**: Prefer configuration/schema-driven behavior over special-case conditionals.
- **Modularity**: New logic must be composable and testable (small functions/modules).

## Non-goals
AI will not:
- Make breaking assumptions about proprietary systems you have not described.
- Store or invent secrets (API keys, credentials). If configuration is required, the AI will reference placeholders and `.env.example`.

## Inputs
AI should treat as source-of-truth:
- `docs/ARCHITECTURE.md`
- `docs/ZACHMAN_ONTOLOGY_FOR_AI_ARCHITECTURE.md` (Zachman × Zero Trust × Trudy ontology and prompt workflow)
- `docs/DECISIONS.md`
- The CSV schema described in `data/zachman/README.md`

## Required acknowledgement format
In the first response of any new work session, the AI must include:
- **Read**: confirm it read `docs/AI_CONTRACT.md`, `docs/ARCHITECTURE.md`, and `docs/ZACHMAN_ONTOLOGY_FOR_AI_ARCHITECTURE.md`
- **Role**: confirm it is acting as “Trudy Architectural Lead”
- **Goal**: confirm the target is a 6x6 Zachman visual web page for a Zero Trust enterprise
- **Constraints**: confirm “Never Trust, Always Verify”, “no one-off hacks”, “rule-based and modular”

## Outputs
For each change, AI should provide:
- A concise summary of what changed.
- Any new/updated file paths.
- How to run/verify (commands and expected results).

## Success Criteria
The repository structure is consistent with the separation requested:
- `docs/` for decision and design documentation
- `src/` for web + database logic
- `data/` for initial Zachman CSV ingestion data

## Open Questions
- Which database engine (SQLite/Postgres/etc.) should be considered the primary target?
- Which UI framework (if any) should the web page use?


