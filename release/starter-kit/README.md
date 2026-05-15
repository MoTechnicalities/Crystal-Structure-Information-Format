# Crystal Bank Starter Kit

This is a compact, CPU-only prototype that demonstrates portable SSD-friendly crystal banks with auditable contradiction behavior.

## Why this exists

It gives interested parties something larger than a toy script, but still small enough to inspect quickly in a GitHub release.

## Included files

1. `crystal_bank_runtime.py`
   - Core bank model, phase math, trace generation, checksum export/import.
2. `crystal_bank_cli.py`
   - CLI for create, ingest, query, trace, benchmark, system-benchmark, and demo flows.
3. `run_demo.py`
   - One-command demo launcher.
4. `interactive_menu.py`
   - Interactive menu wrapper for non-technical exploration.
5. `sample_bank.json`
   - Generated demo bank artifact.

## Quick start

From repository root:

```bash
python3 release/starter-kit/run_demo.py
```

Expected last line:

```text
RESULT: PASS
```

## What the demo proves

1. Query scoring prefers coherent crystal over contradictory crystal.
2. Contradiction trace residual is near pi for the contradictory triangle.
3. A tiny English-to-Spanish bank example works for a translated query.
4. Local benchmark prints CPU-only query throughput.

## Interactive menu

From repository root:

```bash
python3 release/starter-kit/interactive_menu.py
```

## Benchmark against this machine specs

This mode reports CPU, RAM, disk, bank size, load/save/trace timings, query QPS, and a fit assessment.

```bash
python3 release/starter-kit/crystal_bank_cli.py system-benchmark --bank release/starter-kit/sample_bank.json --queries 20000
```

## Large-scale demonstration without large committed data

This mode generates synthetic tiers on demand, benchmarks each tier, and writes a small JSON report without storing large datasets in the repo.

```bash
python3 release/starter-kit/crystal_bank_cli.py scale-benchmark \
   --tier small:1000 \
   --tier medium:5000 \
   --tier large:15000 \
   --query-count 2000
```

Expected output:
1. Multiple tier summaries.
2. A rollup section.
3. Optional report at `release/starter-kit/reports/scale_benchmark_report.json`.

## CLI examples

Create a new bank:

```bash
python3 release/starter-kit/crystal_bank_cli.py create --bank release/starter-kit/my_bank.json --name my-bank
```

Ingest a claim:

```bash
python3 release/starter-kit/crystal_bank_cli.py ingest \
  --bank release/starter-kit/my_bank.json \
  --crystal biology_en \
  --subject Whale \
  --relation is_a \
  --object Mammal \
  --polarity true \
  --source manual
```

Run a query:

```bash
python3 release/starter-kit/crystal_bank_cli.py query \
  --bank release/starter-kit/my_bank.json \
  --subject Whale \
  --relation is_a \
  --object Mammal \
  --polarity true
```

Run benchmark:

```bash
python3 release/starter-kit/crystal_bank_cli.py benchmark \
  --bank release/starter-kit/my_bank.json \
  --subject Whale \
  --relation is_a \
  --object Mammal \
  --polarity true \
  --queries 10000
```

## Portability notes

1. Bank file is plain JSON with SHA-256 checksum verification.
2. No GPU dependencies.
3. Works with standard Python 3.
