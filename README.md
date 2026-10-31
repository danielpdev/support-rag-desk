# Support RAG Desk

Tenant-scoped support answers with citations and escalation.

[![verification](https://github.com/danielpdev/support-rag-desk/actions/workflows/ci.yml/badge.svg)](https://github.com/danielpdev/support-rag-desk/actions/workflows/ci.yml)

**Role focus:** Applied AI Engineer / RAG Engineer. **Status:** working local portfolio implementation, with synthetic data.

![Application screenshot](docs/screenshot.png)

## The engineering decision

Workspace filtering happens before ranking and before any prompt is built. Fixture mode returns a source extract; local mode combines MiniLM retrieval and a Qwen answer. Unsupported queries create a review ticket.

```mermaid
flowchart LR
  Question --> Workspace_filter; Workspace_filter --> Retrieval; Retrieval --> Local_LLM; Local_LLM --> Citation_validation; Citation_validation --> Answer_or_escalation
```

## Run locally

Requirements: Python 3.12, [uv](https://docs.astral.sh/uv/getting-started/installation/) and Make.

```bash
git clone https://github.com/danielpdev/support-rag-desk.git
cd support-rag-desk
make setup
make demo
make test
make eval
```

`make demo` uses an isolated temporary database where relevant, so it is safe to repeat. `make eval` writes a timestamped report to `reports/evaluation-fixture.json`. Fixture mode is deterministic and does not represent model inference. There is no recurring hosting or API subscription cost.

For the React interface (Node 22+ and pnpm 11.25.0):

```bash
make web-setup web-build
make serve
```

Open `http://127.0.0.1:8102`. The same server exposes `/docs`.

### Real local model mode

Install Ollama, then in a separate terminal run:

```bash
OLLAMA_HOST=127.0.0.1:11435 OLLAMA_NO_CLOUD=1 ollama serve
```

```bash
OLLAMA_HOST=127.0.0.1:11435 ollama pull qwen3:4b
make eval-local
```

The router also uses `qwen3:1.7b` as fallback; download it explicitly when running that project. No paid API key is required. First-time model/package downloads require internet and disk space. Inference runs locally. A missing model or dependency is an explicit error, never a silent fixture fallback.

### PostgreSQL

The zero-service quickstart uses SQLite. The same SQLAlchemy domain layer also runs on PostgreSQL:

```bash
docker compose up -d postgres
DATABASE_URL=postgresql+psycopg://portfolio:local-demo-only@127.0.0.1:55441/demo make serve
```

`tests/test_postgres.py` uses `POSTGRES_TEST_URL` and drops its test tables during cleanup. Point it only at a dedicated disposable test database. CI provisions one independently. Local demonstration credentials are deliberately non-secret and must never be reused for production.

[Watch the recorded demo](docs/demo.webm) · [Reproduce the walkthrough](docs/DEMO.md)

## Verification and evidence

Different refund policies for Acme and Beacon, unsupported questions, scoped escalation queues and a model response citing an unknown source.

- [Evaluation report](reports/evaluation-fixture.json) — measured during an actual run; inspect the mode and dataset size.
- [Development and authorship](docs/DEVELOPMENT.md).
- [Romanian interview preparation](docs/INTERVIEW_RO.md).
- [Design notes](docs/DESIGN.md).
- [Demo walkthrough](docs/DEMO.md).

CI uses standard GitHub-hosted runners and deterministic tests without downloading LLM weights. The lockfiles record exact package versions. Local-model results, when present, live in `reports/evaluation-local.json`; hardware/model identities are in `reports/environment.json`.

## Limits and next iteration

Workspace selection is a local demo control, not authentication. Citation-ID validation does not prove semantic entailment. Six English documents are not a production knowledge base. Shared retrieval conventions with rag-retrieval-lab are disclosed; this project adds the product workflow and persistence.

Next: Bind workspace identity to a verified session and add a larger adversarial groundedness dataset.

The local demonstration does not include production authentication, secret management or operational service guarantees. Bind it to localhost and use synthetic data. These projects demonstrate engineering decisions; they do not claim real customers, paid production deployments or guaranteed interviews.

[Explore the complete 20-project portfolio](docs/PORTFOLIO.md)

## Project ownership

Implemented with Codex assistance for Daniel Popa. The owner should review the code, run it, make an independent change and rehearse the tradeoffs before presenting it at interview. That human understanding check is pending and cannot be verified automatically. See [development notes](docs/DEVELOPMENT.md).

MIT for original source; dependencies/models retain their own licenses. See [third-party notices](THIRD_PARTY.md).

## Reproduce browser acceptance

```bash
make web-setup web-build
uv run --frozen --group browser playwright install chromium
uv run --frozen --group browser python scripts/ui_smoke.py
```

The script starts and stops its own local API using a temporary database. It checks a meaningful UI action and mobile overflow.

Use `make serve-local` to start the API/UI with its optional local-model dependencies explicitly enabled.
