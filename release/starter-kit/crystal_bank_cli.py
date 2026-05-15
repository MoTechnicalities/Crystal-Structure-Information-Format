#!/usr/bin/env python3
"""
CLI for the Crystal Bank Starter Kit.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import platform
import shutil
import time
from pathlib import Path
from typing import Iterable

from crystal_bank_runtime import CrystalBank


def _load_or_new(path: str, name: str = "portable-crystal-bank") -> CrystalBank:
    p = Path(path)
    if p.exists():
        return CrystalBank.load(path)
    return CrystalBank(name=name)


def cmd_create(args: argparse.Namespace) -> int:
    bank = CrystalBank(name=args.name)
    checksum = bank.save(args.bank)
    print(json.dumps({"action": "create", "bank": args.bank, "checksum": checksum, "summary": bank.summary()}, indent=2))
    return 0


def cmd_ingest(args: argparse.Namespace) -> int:
    bank = _load_or_new(args.bank)
    edge = bank.add_claim(
        crystal_label=args.crystal,
        subject=args.subject,
        relation=args.relation,
        object_=args.object,
        polarity=args.polarity,
        source=args.source,
        phase_override=args.phase,
    )
    checksum = bank.save(args.bank)
    print(
        json.dumps(
            {
                "action": "ingest",
                "bank": args.bank,
                "crystal": args.crystal,
                "checksum": checksum,
                "edge": {
                    "subject": edge.subject,
                    "relation": edge.relation,
                    "object": edge.object,
                    "polarity": edge.polarity,
                    "phase": edge.phase,
                },
            },
            indent=2,
        )
    )
    return 0


def cmd_summary(args: argparse.Namespace) -> int:
    bank = CrystalBank.load(args.bank)
    print(json.dumps(bank.summary(), indent=2))
    return 0


def cmd_query(args: argparse.Namespace) -> int:
    bank = CrystalBank.load(args.bank)
    ranking = bank.query(
        subject=args.subject,
        relation=args.relation,
        object_=args.object,
        expected_polarity=args.polarity,
    )
    best_label, best_score = ranking[0]
    output = {
        "query": {
            "subject": args.subject,
            "relation": args.relation,
            "object": args.object,
            "expected_polarity": args.polarity,
        },
        "best_match": {"crystal": best_label, "score": best_score},
        "ranking": [{"crystal": label, "score": score} for label, score in ranking],
    }
    print(json.dumps(output, indent=2))
    return 0


def cmd_trace(args: argparse.Namespace) -> int:
    bank = CrystalBank.load(args.bank)
    trace = bank.triangle_trace(
        crystal_label=args.crystal,
        a=args.a,
        b=args.b,
        c=args.c,
        relation_ab=args.rel_ab,
        relation_bc=args.rel_bc,
        relation_ac=args.rel_ac,
    )
    print(json.dumps(trace.__dict__, indent=2))
    return 0


def cmd_benchmark(args: argparse.Namespace) -> int:
    bank = CrystalBank.load(args.bank)
    t0 = time.perf_counter()
    for _ in range(args.queries):
        bank.query(
            subject=args.subject,
            relation=args.relation,
            object_=args.object,
            expected_polarity=args.polarity,
        )
    elapsed = time.perf_counter() - t0
    qps = args.queries / elapsed if elapsed > 0 else float("inf")
    print(
        json.dumps(
            {
                "queries": args.queries,
                "elapsed_seconds": elapsed,
                "qps": qps,
                "cpu_only": True,
            },
            indent=2,
        )
    )
    return 0


def _read_cpu_model() -> str:
    cpuinfo = Path("/proc/cpuinfo")
    if cpuinfo.exists():
        for line in cpuinfo.read_text(encoding="utf-8", errors="ignore").splitlines():
            if line.lower().startswith("model name"):
                parts = line.split(":", 1)
                if len(parts) == 2:
                    return parts[1].strip()
    return platform.processor() or "unknown"


def _read_total_ram_bytes() -> int:
    meminfo = Path("/proc/meminfo")
    if meminfo.exists():
        for line in meminfo.read_text(encoding="utf-8", errors="ignore").splitlines():
            if line.startswith("MemTotal:"):
                kb = int(line.split()[1])
                return kb * 1024
    return 0


def _bytes_to_gb(nbytes: int) -> float:
    return nbytes / (1024.0 ** 3)


def cmd_system_benchmark(args: argparse.Namespace) -> int:
    bank_path = Path(args.bank)
    if not bank_path.exists():
        print(json.dumps({"error": f"Bank file not found: {args.bank}"}, indent=2))
        return 2

    load_t0 = time.perf_counter()
    bank = CrystalBank.load(args.bank)
    load_elapsed = time.perf_counter() - load_t0

    query_t0 = time.perf_counter()
    for _ in range(args.queries):
        bank.query(
            subject=args.subject,
            relation=args.relation,
            object_=args.object,
            expected_polarity=args.polarity,
        )
    query_elapsed = time.perf_counter() - query_t0
    qps = args.queries / query_elapsed if query_elapsed > 0 else float("inf")

    trace_t0 = time.perf_counter()
    trace = bank.triangle_trace(
        crystal_label=args.trace_crystal,
        a=args.trace_a,
        b=args.trace_b,
        c=args.trace_c,
        relation_ab=args.trace_rel_ab,
        relation_bc=args.trace_rel_bc,
        relation_ac=args.trace_rel_ac,
    )
    trace_elapsed = time.perf_counter() - trace_t0

    save_t0 = time.perf_counter()
    checksum = bank.save(args.tmp_save)
    save_elapsed = time.perf_counter() - save_t0

    tmp_path = Path(args.tmp_save)
    tmp_size = tmp_path.stat().st_size if tmp_path.exists() else 0
    if tmp_path.exists():
        tmp_path.unlink()

    logical_cores = os.cpu_count() or 1
    cpu_model = _read_cpu_model()
    ram_total = _read_total_ram_bytes()
    disk = shutil.disk_usage(str(bank_path.parent))
    bank_size = bank_path.stat().st_size

    qps_per_core = qps / logical_cores if logical_cores else qps
    ram_fraction = (bank_size / ram_total) if ram_total else 0.0
    disk_fraction = (bank_size / disk.total) if disk.total else 0.0

    fit = {
        "cpu_query_fit": "excellent" if qps_per_core >= 5000 else "good" if qps_per_core >= 1000 else "entry",
        "memory_fit": "excellent" if ram_fraction < 0.01 else "good" if ram_fraction < 0.05 else "heavy",
        "storage_fit": "excellent" if disk_fraction < 0.001 else "good",
    }

    output = {
        "cpu_only": True,
        "system": {
            "platform": platform.platform(),
            "python": platform.python_version(),
            "cpu_model": cpu_model,
            "logical_cores": logical_cores,
            "ram_total_gb": _bytes_to_gb(ram_total),
            "disk_total_gb": _bytes_to_gb(disk.total),
            "disk_free_gb": _bytes_to_gb(disk.free),
        },
        "bank": {
            "path": str(bank_path),
            "size_bytes": bank_size,
            "size_mb": bank_size / (1024.0 ** 2),
            "crystal_count": len(bank.crystals),
            "edge_count": sum(len(c.edges) for c in bank.crystals.values()),
        },
        "benchmarks": {
            "load_ms": load_elapsed * 1000.0,
            "save_ms": save_elapsed * 1000.0,
            "trace_ms": trace_elapsed * 1000.0,
            "query": {
                "count": args.queries,
                "elapsed_seconds": query_elapsed,
                "qps": qps,
                "qps_per_core": qps_per_core,
            },
            "trace_residual": trace.residual,
            "save_checksum": checksum,
            "tmp_save_size_bytes": tmp_size,
        },
        "fit_assessment": fit,
    }
    print(json.dumps(output, indent=2))
    return 0


def _synthetic_bank(tier_name: str, crystal_count: int, edge_span: int) -> CrystalBank:
    bank = CrystalBank(name=f"synthetic-{tier_name}")
    base = bank.phase_for("is_a", "true")
    contradictory = bank.phase_for("is_a", "false")

    for crystal_index in range(crystal_count):
        label = f"{tier_name}_crystal_{crystal_index:06d}"
        subject = f"Entity{crystal_index:06d}"
        middle = f"Type{crystal_index % edge_span:04d}"
        target = f"Property{(crystal_index * 7) % edge_span:04d}"
        bank.add_claim(label, subject, "is_a", middle, "true", "synthetic", phase_override=base)
        bank.add_claim(label, middle, "supports", target, "true", "synthetic")
        bank.add_claim(label, subject, "is_a", target, "true", "synthetic", phase_override=base)

        if crystal_index % 10 == 0:
            bank.add_claim(label, subject, "is_a", target, "false", "synthetic", phase_override=contradictory)

    return bank


def _bank_query_probe(bank: CrystalBank, query_count: int, subject_seed: str, target_seed: str) -> Dict[str, float]:
    t0 = time.perf_counter()
    for idx in range(query_count):
        subject = f"{subject_seed}{idx:06d}"
        target = f"{target_seed}{(idx * 7) % 128:04d}"
        bank.query(subject, "is_a", target, "true")
    elapsed = time.perf_counter() - t0
    return {
        "queries": query_count,
        "elapsed_seconds": elapsed,
        "qps": (query_count / elapsed) if elapsed > 0 else float("inf"),
    }


def cmd_scale_benchmark(args: argparse.Namespace) -> int:
    tiers = []
    for tier in args.tier:
        parts = tier.split(":", 1)
        if len(parts) != 2:
            print(json.dumps({"error": f"Invalid tier '{tier}'. Use NAME:CRYSTALS"}, indent=2))
            return 2
        tier_name, crystal_str = parts
        crystal_count = int(crystal_str)
        bank = _synthetic_bank(tier_name=tier_name, crystal_count=crystal_count, edge_span=args.edge_span)

        query_probe = _bank_query_probe(
            bank=bank,
            query_count=args.query_count,
            subject_seed="Entity",
            target_seed="Property",
        )

        trace_start = time.perf_counter()
        trace = bank.triangle_trace(
            crystal_label=f"{tier_name}_crystal_000000",
            a="Entity000000",
            b=f"Type{0:04d}",
            c=f"Property{0:04d}",
            relation_ab="is_a",
            relation_bc="supports",
            relation_ac="is_a",
        )
        trace_ms = (time.perf_counter() - trace_start) * 1000.0

        save_path = Path(args.workdir) / f"{tier_name}_{crystal_count}_bank.json"
        save_start = time.perf_counter()
        checksum = bank.save(str(save_path))
        save_ms = (time.perf_counter() - save_start) * 1000.0
        load_start = time.perf_counter()
        loaded = CrystalBank.load(str(save_path))
        load_ms = (time.perf_counter() - load_start) * 1000.0
        file_size = save_path.stat().st_size

        tiers.append(
            {
                "tier": tier_name,
                "crystal_count": crystal_count,
                "edge_count": sum(len(c.edges) for c in bank.crystals.values()),
                "file_size_bytes": file_size,
                "build_summary": bank.summary(),
                "query_probe": query_probe,
                "trace_ms": trace_ms,
                "trace_residual": trace.residual,
                "save_ms": save_ms,
                "load_ms": load_ms,
                "checksum": checksum,
                "roundtrip_crystal_count": len(loaded.crystals),
            }
        )

        if save_path.exists():
            save_path.unlink()

    total_crystals = sum(item["crystal_count"] for item in tiers)
    total_edges = sum(item["edge_count"] for item in tiers)
    output = {
        "mode": "synthetic-scale-benchmark",
        "cpu_only": True,
        "bank_tiers": tiers,
        "rollup": {
            "tier_count": len(tiers),
            "total_crystals": total_crystals,
            "total_edges": total_edges,
            "largest_tier": max((item["crystal_count"] for item in tiers), default=0),
            "best_qps": max((item["query_probe"]["qps"] for item in tiers), default=0.0),
            "smallest_load_ms": min((item["load_ms"] for item in tiers), default=0.0),
        },
        "spec_targets": {
            "large_scale_indicator": "multiple synthetic tiers generated on-demand without committed bulky data",
            "portable": True,
            "persisted_assets": "small temporary tier files only",
            "benchmark_queries_per_tier": args.query_count,
        },
    }

    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        output["report_path"] = str(out_path)
        out_path.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(json.dumps(output, indent=2, sort_keys=True))
    return 0


def _populate_demo_bank(bank: CrystalBank) -> None:
    coherent = "whale_coherent_en"
    contradictory = "whale_contradictory_en"
    spanish = "whale_coherent_es"

    bank.add_claim(coherent, "Whale", "is_a", "Mammal", "true", "demo")
    bank.add_claim(coherent, "Mammal", "is_a", "Warm-blooded", "true", "demo")
    bank.add_claim(coherent, "Whale", "is_a", "Warm-blooded", "true", "demo")

    bank.add_claim(contradictory, "Whale", "is_a", "Mammal", "true", "demo")
    bank.add_claim(contradictory, "Mammal", "is_a", "Warm-blooded", "true", "demo")
    base = bank.phase_for("is_a", "true")
    composed = (base + base)
    anti_phase_direct = composed + math.pi
    bank.add_claim(
        contradictory,
        "Whale",
        "is_a",
        "Warm-blooded",
        "false",
        "demo",
        phase_override=anti_phase_direct,
    )

    bank.add_claim(spanish, "Ballena", "is_a", "Mamifero", "true", "demo")
    bank.add_claim(spanish, "Mamifero", "is_a", "Sangre-caliente", "true", "demo")
    bank.add_claim(spanish, "Ballena", "is_a", "Sangre-caliente", "true", "demo")


def cmd_demo(args: argparse.Namespace) -> int:
    bank = CrystalBank(name="starter-kit-demo")
    _populate_demo_bank(bank)
    checksum = bank.save(args.bank)

    # Query should prefer coherent over contradictory.
    ranking = bank.query("Whale", "is_a", "Warm-blooded", "true")
    coherent_score = next(score for label, score in ranking if label == "whale_coherent_en")
    contradictory_score = next(score for label, score in ranking if label == "whale_contradictory_en")

    trace = bank.triangle_trace(
        crystal_label="whale_contradictory_en",
        a="Whale",
        b="Mammal",
        c="Warm-blooded",
        relation_ab="is_a",
        relation_bc="is_a",
        relation_ac="is_a",
    )

    # Tiny bridge demo by direct edge translation and resonance check.
    bridge = {
        "Whale": "Ballena",
        "Mammal": "Mamifero",
        "Warm-blooded": "Sangre-caliente",
    }
    en_phase = bank.phase_for("is_a", "true")
    direct_match = bank.query("Ballena", "is_a", "Sangre-caliente", "true")[0]

    checks = {
        "query_prefers_coherent": coherent_score < contradictory_score,
        "trace_residual_near_pi": abs(trace.residual - math.pi) < 1e-9,
        "bridge_terms_present": len(bridge) == 3,
        "spanish_query_hits_spanish_crystal": direct_match[0] == "whale_coherent_es",
        "base_phase_nonzero": abs(en_phase) > 0,
    }

    benchmark_queries = 5000
    t0 = time.perf_counter()
    for _ in range(benchmark_queries):
        bank.query("Whale", "is_a", "Warm-blooded", "true")
    elapsed = time.perf_counter() - t0
    qps = benchmark_queries / elapsed if elapsed > 0 else float("inf")

    output = {
        "bank_file": args.bank,
        "checksum": checksum,
        "summary": bank.summary(),
        "query_ranking": [{"crystal": label, "score": score} for label, score in ranking],
        "contradiction_trace": trace.__dict__,
        "bridge_map_en_to_es": bridge,
        "benchmark": {
            "queries": benchmark_queries,
            "elapsed_seconds": elapsed,
            "qps": qps,
            "cpu_only": True,
        },
        "checks": checks,
    }
    print(json.dumps(output, indent=2))
    print("RESULT:", "PASS" if all(checks.values()) else "FAIL")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Crystal Bank Starter Kit CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    p_create = sub.add_parser("create", help="Create an empty portable crystal bank")
    p_create.add_argument("--bank", required=True, help="Path to bank JSON file")
    p_create.add_argument("--name", default="portable-crystal-bank", help="Bank name")
    p_create.set_defaults(func=cmd_create)

    p_ingest = sub.add_parser("ingest", help="Add or update one claim edge")
    p_ingest.add_argument("--bank", required=True)
    p_ingest.add_argument("--crystal", required=True)
    p_ingest.add_argument("--subject", required=True)
    p_ingest.add_argument("--relation", required=True)
    p_ingest.add_argument("--object", required=True)
    p_ingest.add_argument("--polarity", choices=["true", "false"], required=True)
    p_ingest.add_argument("--source", default="manual")
    p_ingest.add_argument("--phase", type=float, default=None, help="Optional explicit phase override in radians")
    p_ingest.set_defaults(func=cmd_ingest)

    p_summary = sub.add_parser("summary", help="Show bank summary")
    p_summary.add_argument("--bank", required=True)
    p_summary.set_defaults(func=cmd_summary)

    p_query = sub.add_parser("query", help="Query crystal ranking by expected claim polarity")
    p_query.add_argument("--bank", required=True)
    p_query.add_argument("--subject", required=True)
    p_query.add_argument("--relation", required=True)
    p_query.add_argument("--object", required=True)
    p_query.add_argument("--polarity", choices=["true", "false"], required=True)
    p_query.set_defaults(func=cmd_query)

    p_trace = sub.add_parser("trace", help="Emit auditable triangle conflict trace")
    p_trace.add_argument("--bank", required=True)
    p_trace.add_argument("--crystal", required=True)
    p_trace.add_argument("--a", required=True)
    p_trace.add_argument("--b", required=True)
    p_trace.add_argument("--c", required=True)
    p_trace.add_argument("--rel-ab", required=True)
    p_trace.add_argument("--rel-bc", required=True)
    p_trace.add_argument("--rel-ac", required=True)
    p_trace.set_defaults(func=cmd_trace)

    p_bench = sub.add_parser("benchmark", help="Run CPU-only local query throughput benchmark")
    p_bench.add_argument("--bank", required=True)
    p_bench.add_argument("--subject", required=True)
    p_bench.add_argument("--relation", required=True)
    p_bench.add_argument("--object", required=True)
    p_bench.add_argument("--polarity", choices=["true", "false"], required=True)
    p_bench.add_argument("--queries", type=int, default=10000)
    p_bench.set_defaults(func=cmd_benchmark)

    p_sys = sub.add_parser("system-benchmark", help="Benchmark runtime against current machine specs")
    p_sys.add_argument("--bank", default="release/starter-kit/sample_bank.json")
    p_sys.add_argument("--subject", default="Whale")
    p_sys.add_argument("--relation", default="is_a")
    p_sys.add_argument("--object", default="Warm-blooded")
    p_sys.add_argument("--polarity", choices=["true", "false"], default="true")
    p_sys.add_argument("--queries", type=int, default=20000)
    p_sys.add_argument("--trace-crystal", default="whale_contradictory_en")
    p_sys.add_argument("--trace-a", default="Whale")
    p_sys.add_argument("--trace-b", default="Mammal")
    p_sys.add_argument("--trace-c", default="Warm-blooded")
    p_sys.add_argument("--trace-rel-ab", default="is_a")
    p_sys.add_argument("--trace-rel-bc", default="is_a")
    p_sys.add_argument("--trace-rel-ac", default="is_a")
    p_sys.add_argument("--tmp-save", default="release/starter-kit/.tmp_bench_save.json")
    p_sys.set_defaults(func=cmd_system_benchmark)

    p_scale = sub.add_parser("scale-benchmark", help="Generate synthetic tiers to demonstrate large-scale portability")
    p_scale.add_argument(
        "--tier",
        action="append",
        required=True,
        help="Tier definition in NAME:CRYSTALS format; repeat for multiple tiers",
    )
    p_scale.add_argument("--edge-span", type=int, default=128, help="Synthetic relation span for generated crystals")
    p_scale.add_argument("--query-count", type=int, default=2000, help="Queries to run per tier")
    p_scale.add_argument("--workdir", default="release/starter-kit/.scale_tmp", help="Temp work directory for tier files")
    p_scale.add_argument("--out", default="release/starter-kit/reports/scale_benchmark_report.json", help="Optional report output path")
    p_scale.set_defaults(func=cmd_scale_benchmark)

    p_demo = sub.add_parser("demo", help="Create demo bank, run checks, print PASS/FAIL")
    p_demo.add_argument(
        "--bank",
        default="release/starter-kit/sample_bank.json",
        help="Output path for generated demo bank",
    )
    p_demo.set_defaults(func=cmd_demo)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
