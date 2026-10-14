---
name: fast-ci
description: >-
  Make GitHub Actions CI/CD fast and dependable: measure how long a PR waits for its verdict, find what
  sets it, then cut queue, setup, redundant work and wasted runs, and avoid the required-check, cache,
  concurrency and release traps. Use when creating or editing a workflow, when CI is slow, queued, flaky
  or red for no code reason, when waiting on a PR's checks, or when asked to optimize CI/CD.
license: MIT
compatibility: GitHub Actions. scripts/ci needs Python 3.9+ and an authenticated gh CLI.
---

# Fast CI

Optimize **time to verdict**: how long the author of a PR, human or agent, waits between a push and a
trustworthy result on the checks that block the merge. It is the wait before CI starts (approvals,
labels), plus queue time, plus the longest chain of required jobs, plus every rerun a flake forces.

## 1. Measure

```sh
scripts/ci stats -R owner/repo --days 14        # --workflow ci.yml to focus, --runs N (max 1000)
```

It reads the required checks of the default branch (rulesets; classic branch protection needs admin
rights), then prints the PR time to verdict per commit, the last substantial job before it (a candidate
bottleneck: confirm the required checks wait for it), per-workflow elapsed time with failure, approval
and rerun rates, per-job queue and run time, and the slowest steps. Jobs that no required check waits
for cost money, not time to verdict.

| Symptom in the numbers | Likely cause | Section |
|---|---|---|
| runs waiting for approval, most verdicts red within seconds, PRs that get CI days after opening | a human gate before CI | 2 |
| queue p90 over a minute | capacity, concurrency limits, runner labels | 5 |
| the test step itself is the slowest step | the suite, not CI | 4 |
| setup, install or cache steps among the slowest | cold or broken caches | 3 |
| one job or `needs:` chain finishes last before most verdicts | the critical path | 4 |
| failures or reruns above a few percent | flakes or infrastructure | 6 |

**Stop when it is good enough.** Below about 5 minutes at p90 with few failures, apply section 2 and the
security line, and leave the rest: every extra job (change detection, fan-in, shards) costs a runner, a
checkout and a setup. Otherwise keep the numbers; the same command after the change is the proof.

## 2. Triggers and required checks

- **One required check: a fan-in job** (`ci-ok`) with `if: ${{ !cancelled() }}` that `needs` every gating
  job and checks each `needs.<job>.result` itself, since branch rules count a skipped job as passing. It
  fails unless each succeeded, or was skipped because change detection said so. Jobs can then change
  without touching branch rules. See [`assets/skeleton.yml`](assets/skeleton.yml).
- **Path filtering for a required workflow lives in a job `if:`**, never in `on.paths`: a required
  workflow skipped by `paths`, branch filters or a `[skip ci]` message leaves its check Pending forever.
  `on.paths` is fine for workflows nobody requires. Run everything on the default branch, on toolchain,
  lockfile or CI changes, and whenever detection is unsure.
- **With a merge queue, also trigger on `merge_group`**, or the required check never reports.
- **On a public repo the gate needs no secret**: a `pull_request` from a fork gets none and a read-only
  token. Steps that need one (coverage upload, preview deploy) go in a job guarded by
  `github.event.pull_request.head.repo.full_name == github.repository`, or run after merge.
- **Keep project gates off the fast lane**: when PRs wait for a maintainer's label before any CI, run the
  cheap secretless checks (lint, types, unit tests) on `pull_request` right away and keep only the costly
  or secret-bearing jobs behind the label. GitHub's approval of first-time fork contributors still
  applies to every workflow; changing it is a repository setting, not a YAML change.
- **Run once per change**: `push` limited to the default branch plus `pull_request`. Keep the default
  `pull_request` types; `labeled` or `edited` events that re-run heavy jobs waste runs.
- **Concurrency**: PR runs share `${{ github.workflow }}-${{ github.ref }}` with `cancel-in-progress`.
  Default-branch runs get their own group (`github.run_id`), never cancelled: a shared group drops pending
  runs and hides which merge broke. Deploys to one target share a group with `queue: max` (up to 100
  pending, in arrival order, not commit order: refuse to deploy a revision older than the live one).
- **`timeout-minutes` on every job** (the default is 6 hours) and a per-test timeout in the test runner.

## 3. Caches and setup

- **Dependencies**: the `setup-*` actions' built-in cache, or `actions/cache` keyed on the lockfile hash
  with `restore-keys` so a lockfile change starts warm. The default branch's cache serves every PR; a PR's
  own cache serves only that PR. Restrict PR writes (`actions/cache/restore`) only when caches evict each
  other (10 GB per repo by default, unused entries dropped after 7 days).
- **Build outputs beat dependencies**: Gradle build and configuration cache, Turborepo or Nx remote cache,
  sccache or ccache, Docker `buildx` with `cache-from`/`cache-to`. Keep keys stable: no timestamps, run
  ids or unused env vars in cache inputs.
- **Check that the cache works**: "Cache not found" on every run, or failed saves, means each job starts
  cold. Drop a cache whose restore and save outlast the work it skips.
- **Lockfiles enforced**: `npm ci`, `pnpm install --frozen-lockfile`, `uv sync --locked`, `cargo --locked`.
- **Shallow checkout** (the default `fetch-depth: 1`); full history, LFS and submodules only where read.

## 4. The critical path

- **Profile the suite before touching YAML** (`pytest --durations=20`, nextest's timings, a Gradle build
  scan): a per-test database reset, a real network call or a fixed sleep costs more than any CI change,
  and sharding only spreads it across runners. Replace sleeps with readiness checks.
- **Cut `needs:` that are not data dependencies**: lint, typecheck, build and tests start together.
- **More cores before more jobs**: `ubuntu-latest` has 2 cores on a private repo and 4 on a public one. A
  build or suite that uses every core (cargo, Gradle `--parallel`, `pytest -n auto`, Jest and Vitest
  workers) often finishes sooner on a larger runner than split into shards that each pay setup.
- **Shard the long test job by measured durations** (nextest partitions, pytest-split, Playwright or Jest
  `--shard`); bound it with `max-parallel` when shards saturate the runners.
- **Build once, test many** when the build outlasts the artifact round-trip: one job builds, test jobs
  download it (`upload-artifact`, nextest's archive; `compression-level: 0` for already-compressed files).
- **Test what changed in monorepos** with the build tool's own graph (Nx affected, Turborepo `--filter`,
  Bazel, Gradle), and check its selection against the full suite on the default branch before trusting it.
- **Two tiers, chosen by risk**: keep representative E2E and every supported platform on PRs, since shared
  code breaks one platform alone. Move exhaustive matrix combinations, benchmarks and long soak tests
  after merge or nightly. Without a merge queue, the run after each merge is what catches two PRs that
  pass alone and break together.

## 5. Runners and queue

- **Find what the queue waits for before adding runners**: the plan's concurrent-job limit (20 on Free, 40
  on Pro, 60 on Team, 500 on Enterprise, shared by the whole account, 5 macOS jobs below Enterprise), a
  concurrency group, a runner label only one machine has, or an environment approval.
- **Then buy capacity**, cheapest first: larger hosted runners, a third-party runner provider, self-hosted
  runners. Read [`reference/self-hosted.md`](reference/self-hosted.md) before adding or changing one.
- **ARM64**: native ARM runners (`ubuntu-24.04-arm`, free on public repos), not QEMU emulation.
- **Cost**: a hosted macOS minute costs about ten Linux minutes, a Windows one almost two. Trim redundant
  matrix combinations before removing platform coverage from PRs.

## 6. Failures

- **Retry a flaky test once in the test runner and report it as flaky** (nextest retries,
  pytest-rerunfailures, Playwright `retries`); keep the list. Never `continue-on-error` on a gating step.
- **Set `fail-fast` on purpose**: the default `true` cancels a matrix's other legs on the first failure,
  so a rerun is needed to see the rest.
- **Tell infrastructure from code**: a lost runner, a full disk or a wrong-architecture binary needs a
  platform fix, not a test change. `scripts/ci wait` labels each failure `infra`, `unclear` (timeouts,
  network) or `code` (no platform signature); confirm the cause before acting on it.

## 7. The gate and agents

- **One gate command, identical locally and in CI** (`make check`, `just check`, a script), named in the
  contributor docs or `AGENTS.md`. Agents run it before pushing; CI confirms, it does not discover.
- **A failure fits on one screen**: the failing test, its assertion and a short log tail; full logs go to
  an artifact. Humans and agents fix faster, and agents spend less context.
- **Wait with `scripts/ci wait --required [PR]`**, not a polling loop: it prints one line, then nothing
  until GitHub's required checks for that PR decide, then one line per check and, for each failure, the
  failed step and the log tail. Without `--required` (or with a SHA) it waits for every check. Exit
  codes: 0 green, 1 failed, 2 timeout, 3 no checks, 4 tool error.

## 8. Releases and deploys

- **Build once, promote**: a release publishes the artifact the default branch built for that exact SHA
  (`docker buildx imagetools create` to re-tag an image, the same binary or package); it does not rebuild.
- **Events caused by `GITHUB_TOKEN` trigger no workflow**, except dispatch events and `pull_request`
  opened, synchronize and reopened, whose runs wait for approval: automation that must trigger CI
  unattended uses a GitHub App token.

## 9. Security that costs nothing

`permissions: contents: read` by default, write scopes per job; every action pinned by commit SHA with a
version comment; `persist-credentials: false` on checkout unless a later step pushes; OIDC
(`id-token: write`) instead of long-lived cloud secrets; never `pull_request_target` with a checkout of
the PR's code; `actionlint` and `zizmor` on workflow changes.

## Verify a workflow change

`actionlint` and `zizmor` the file, push it on a PR, `scripts/ci wait`. Triggers on the default branch,
tags or schedules cannot run on a PR: name the run to check after merge. Then `scripts/ci stats` against
the numbers from step 1.
