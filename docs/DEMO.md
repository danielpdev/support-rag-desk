# Demo walkthrough

## Start

```bash
make setup
make demo
make test
make eval
```

## What to show

Workspace filtering happens before ranking and before any prompt is built. Fixture mode returns a source extract; local mode combines MiniLM retrieval and a Qwen answer. Unsupported queries create a review ticket.

## Failure case to discuss

Different refund policies for Acme and Beacon, unsupported questions, scoped escalation queues and a model response citing an unknown source.

## Evidence

Open the JSON evaluation report alongside the implementation. Distinguish synthetic fixture outputs, synthetic trace timing, actual elapsed evaluation time, and local model inference. Do not present a tiny test set as a production benchmark.

## Closing tradeoff

Workspace selection is a local demo control, not authentication. Citation-ID validation does not prove semantic entailment. Six English documents are not a production knowledge base. Shared retrieval conventions with rag-retrieval-lab are disclosed; this project adds the product workflow and persistence.

The repository's `docs/demo.webm` or `docs/demo.mp4`, when present, records the demonstration. A terminal replay is also available for focused projects as `docs/demo.cast`.
