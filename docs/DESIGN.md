# Design record

## Decision

Workspace filtering happens before ranking and before any prompt is built. Fixture mode returns a source extract; local mode combines MiniLM retrieval and a Qwen answer. Unsupported queries create a review ticket.

## Failure model

Different refund policies for Acme and Beacon, unsupported questions, scoped escalation queues and a model response citing an unknown source.

## Tradeoffs

Workspace selection is a local demo control, not authentication. Citation-ID validation does not prove semantic entailment. Six English documents are not a production knowledge base. Shared retrieval conventions with rag-retrieval-lab are disclosed; this project adds the product workflow and persistence.

## Next change to defend in review

Bind workspace identity to a verified session and add a larger adversarial groundedness dataset.

## Reproducibility

`uv.lock` pins Python dependencies; the web lockfile pins the React build where present. Model-backed evaluations use a separately installed local service. Dataset examples are synthetic and intentionally small. Reported timing is a local observation, not a throughput SLA. Run `make test` after changing state transitions and `make eval` after changing decisions. Keep inference quality separate from deterministic invariant checks.
