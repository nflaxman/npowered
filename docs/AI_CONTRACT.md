# AI Contract

## Purpose
Document how AI assistance should behave while building this repository (requirements, boundaries, and success criteria).

## Scope
AI may help with:
- Translating `ARCHITECTURE.md` into implementation tasks.
- Producing code scaffolding under `src/`.
- Creating ingestion/data mapping logic for Zachman-matrix CSVs under `data/` and `src/db/`.
- Writing tests and documentation updates.

## Non-goals
AI will not:
- Make breaking assumptions about proprietary systems you have not described.
- Store or invent secrets (API keys, credentials). If configuration is required, the AI will reference placeholders and `.env.example`.

## Inputs
AI should treat as source-of-truth:
- `docs/ARCHITECTURE.md`
- `docs/DECISIONS.md`
- The CSV schema described in `data/zachman/README.md`

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

