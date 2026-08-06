# Spawning and tracking a Codex fleet

To run several Codex workers at once, launch each as a background process writing to its own files, then track them. Keep the outputs in a gitignored dir (e.g. `.codex/`):

```
# one worker, launched in the background:
codex exec --json -s read-only -o .codex/w1.msg "PROMPT" </dev/null >.codex/w1.jsonl 2>&1
```

- `--json` streams structured events to `w1.jsonl`; `-o` still writes the clean final message to `w1.msg`. You get both.
- The **session id** is the first event: `{"type":"thread.started","thread_id":"019f…"}` — `head -1 .codex/w1.jsonl` gives it. Capture it per worker.

Tracking, without a wrapper — and **judge the artifacts, never the exit code**: a worker can exit non-zero with a complete, correct deliverable, and a "clean" launch may have produced nothing (the silent-cwd failure — check early that the `.jsonl`/`.msg` files exist and grow).

- **Completion** — you're notified as each background process exits; react rather than busy-poll. Done = `turn.completed` in the JSONL (with token usage) + the final answer in `.msg`.
- **Liveness** — `stat` the `.jsonl`: recent mtime and growing size = alive; a stale file = dead or never started. **Hang recovery**: mtime stale ≥5 min → kill the process, then `codex exec resume <thread_id> "You were interrupted mid-task — continue."` — the thread keeps its context.
- **Progress / status** — count `item.completed` events; parse the last `agent_message` for a relayable "what's it doing".
- **Follow up** — resume by captured id: `codex exec resume <thread_id> "next instruction"`. (`--last` is cwd-filtered and races with any other Codex run on the machine — always resume by id.)

**Parallelism caution.** Read-only workers fan out freely. But several `workspace-write` workers on the same working tree will collide on files — give each its own directory or git worktree, or run the writers serially. This is the same coherence trap as any multi-agent build: freeze who-owns-what before fanning out.

Scale to the task: a handful of workers with clear, non-overlapping scopes — not a swarm. Each `codex exec` is a full GPT-5.x agent; they're expensive and heavy.
