# Performance numbers

Before producing or acting on baseline/comparison/regression/library/config numbers, answer with run evidence.
A user-requested ballpark may use one disclosed run but still checks correctness and actual timed work (4/7);
choosing options is not a ballpark.

## Prepare

Write the exact claim to test; read the script's timed/counted/excluded work. Inspect machine load (`uptime`)
and cores (`nproc` or macOS `sysctl -n hw.ncpu`). Identify competing load; if it cannot stop, interleave both
sides and disclose it.

## Seven questions

1. **Limiter:** identify core/lock/disk/network/GC/load-generator limit from a separate profiling run, not
   reported timings. Use JVM JFR/async-profiler, Python py-spy, Node CPU profile, per-process top, IO wait or
   strace; a live server uses its own profiler. Map hotspot to source; understand an unchanged number before
   calling a change useless.
2. **Tuning:** production build/flags/JVM, realistic warm/cold caches, matched versions/data, shipped
   pooling/batching. Defaults or a fixable setting (per-row commit, missing index, debug build) leave a side
   untuned; tune and rerun before choosing.
3. **Limits:** compare arithmetic to bandwidth/cores. Removing 10% of work yields at most ~11% speedup;
   impossible results suggest cache/no-op/bug.
4. **Errors:** count failures/non-success results and validate outputs; add counters if missing. Fast
   rejections and slow timeouts/retries distort timing.
5. **Reproduction:** ≥5 runs per side alternating A/B; JVM microbenchmarks use JMH forks/warmup. Report
   median/range; differences within spread are unmeasurable.
6. **Relevance:** measure realistic end-to-end command/tick/request sizes/concurrency and express micro
   results as a share.
7. **Actual work:** prove consumption/completion inside the timed region (rows/bytes/result use); unconsumed
   streams, unjoined futures, discarded JIT results and timeouts can time absent work.

## Report

Verdict: faster/slower/no measurable difference/inconclusive. Give number/unit, runs, range and limiter.
Unnamed limiter, untuned side or unchecked 4/7 means inconclusive; name the gap. PR body gets one primary
number; full runs/spread/limiter evidence go in linked notes/artifacts.
