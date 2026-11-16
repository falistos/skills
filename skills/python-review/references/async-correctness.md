# Async correctness

For async-heavy code; repo standards override this reference. Focus on lifetime/cancellation behavior rather
than mechanically replacing API names.

## Ownership

- Prefer TaskGroup (3.11+) for sibling work: failure cancels siblings and raises ExceptionGroup. Ordinary
  gather leaves siblings running after a failure; gather with `return_exceptions=True` fits intentional
  independent outcomes or shutdown, and older targets may require it.
- Keep a strong owner reference to background tasks; the loop holds weak references. Use TaskGroup for scoped
  lifetime, otherwise an owner task set with done callbacks removing completed entries. FastAPI
  BackgroundTasks fits framework-owned work.
- Bound per-item concurrency with Semaphore inside scheduled TaskGroup tasks; shutdown cancels owned tasks
  then awaits all outcomes under a timeout.
- Queue(maxsize=N) gives backpressure; task_done belongs in finally so join completes.

## Cancellation and blocking

- Propagate CancelledError; on 3.8+ it bypasses `except Exception`, but bare/BaseException catches do not.
  Check third-party cancellation types too.
- Release resources in finally/async-with. Critical awaited cleanup may need shielding against repeated
  cancellation, sparingly and with an owned lifetime.
- asyncio.timeout covers multiple awaits and composes with TaskGroup; inner awaits see CancelledError, the
  boundary raises TimeoutError. timeout_at uses an absolute deadline.
- Layer request and outbound-call budgets (for example timeout(30) around an AsyncClient timeout of 10).
- Inspect sync sleep/HTTP/DB/filesystem calls and CPU work in async bodies. Reuse a long-lived async HTTP
  client; move blocking IO off the loop and CPU work to an appropriate executor.
- threading.Lock across await can block/deadlock; use asyncio.Lock for async state. Real thread-shared
  resources may require threading.Lock, but holding it across await indicates a design problem.

## Review leads

Trace gather/wait_for, discarded or briefly held create_task results, sequential await comprehensions, async
functions with no await, __del__ cleanup and result polling. Already-awaited task.result is fine.

Libraries expose coroutines rather than asyncio.run/run_until_complete; the app owns loop startup. Inside
coroutines use get_running_loop only if needed. Async generators require async iteration.
