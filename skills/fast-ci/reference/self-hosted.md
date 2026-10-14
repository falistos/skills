# Self-hosted runners

Self-hosted runners remove per-minute cost and can keep warm disks, but queue time, caches and isolation
become yours.

## Scheduling

- **Labels describe capabilities, not hosts**: target `[self-hosted, Linux, X64]`, and pin a job to a
  named host only when it needs something only that host has (a device, a licensed tool, a big disk).
  A pinned light job waits behind the heavy ones: a 1.5-minute job queued 3.7 hours over two days on
  one pinned host, and 2 seconds once it could run anywhere in the pool.
- **Let a variable choose the pool**, so a repo can move between hosted and self-hosted runners without
  editing every job: `runs-on: ${{ vars.CI_RUNNER || 'ubuntu-latest' }}`, with the variable set at
  organization level. A repo-level value naming a single host pins every job of that repo.
- **A scarce resource is locked around that resource only** (a device, a port range, a game server), and
  the lock spans repos, since GitHub concurrency groups are per repository. Build before taking the lock;
  release it on failure and cancel.

## A mixed pool

- **Architectures differ**: download binaries by `$RUNNER_ARCH` (`X64`, `ARM64`), check them by checksum,
  and build ARM64 natively on an ARM host rather than under QEMU.
- **Hosts differ**: provision tools the same way on every host of a pool, never by hand. Linux jobs can
  bring their toolchain in a `container:`; macOS and Windows runners cannot run container jobs.
- **Users differ**: a container job runs as root and leaves root-owned files in the runner's directories,
  which break the next job on that host. Either `chown` the workspace back to the runner's user
  (`$(stat -c %u:%g "$RUNNER_TEMP")`) before and after the job, or keep caches in a named Docker volume.

## Caches

- **Persistent runners keep caches on disk** (`~/.gradle`, `~/.cache`, the pnpm store, `~/.cargo`):
  measure the Actions cache round-trips there, which may only upload and download what the disk already
  holds; `gradle/actions/setup-gradle` took up to 27 minutes per job for nothing on one pool, and
  `cache-disabled: true` removed it. Ephemeral runners start cold: keep the remote cache on them.
- **Container jobs mount the host cache** instead of starting cold.
- **Disks fill up**: prune Docker images and build caches on a schedule, and alert on free space.

## Security

- **Trusted code only**: never run workflows from fork PRs on persistent self-hosted runners (disable it
  in the organization's Actions settings); public repos use ephemeral runners or hosted ones.
- No `pull_request_target` with a checkout of the PR's code, no secrets on command lines, and no
  long-lived credentials on the host that a job could read.
