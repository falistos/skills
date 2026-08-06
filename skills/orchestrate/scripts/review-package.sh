#!/usr/bin/env bash
# Package a commit range for review: commits + stat + full diff in one file,
# so neither the orchestrator nor the reviewer pays the git plumbing in context.
# Usage: review-package.sh <base> <head> <out-file> [repo-dir]
set -euo pipefail
base=$1 head=$2 out=$3 repo=${4:-.}
{
  echo "# Review package: $base..$head"
  echo
  echo "## Commits"
  git -C "$repo" log --oneline "$base..$head"
  echo
  echo "## Stat"
  git -C "$repo" diff --stat "$base" "$head"
  echo
  echo "## Diff"
  git -C "$repo" diff -U10 "$base" "$head"
} > "$out"
echo "$out"
