#!/usr/bin/env sh
# Install skills from this collection into each detected agent.
# Usage:
#   ./install.sh [--link] [skill ...]   every skill, or only the named ones
# --link symlinks each skill to this checkout, so a pull or an edit here is live everywhere.
set -eu

HERE=$(cd "$(dirname "$0")" && pwd)
SRC="$HERE/skills"

[ -d "$SRC" ] || { echo "error: $SRC not found (run from a checkout of the repo)"; exit 1; }

LINK=0
if [ "${1:-}" = "--link" ]; then LINK=1; shift; fi

if [ "$#" -gt 0 ]; then
  SKILLS="$*"
else
  SKILLS=$(cd "$SRC" && for d in */; do printf '%s ' "${d%/}"; done)
fi

# ~/.agents/skills is the shared directory Codex and other skill-aware agents read.
DESTS=""
[ -d "$HOME/.claude" ] && DESTS="$DESTS $HOME/.claude/skills"
[ -d "$HOME/.agents" ] || [ -d "$HOME/.codex" ] && DESTS="$DESTS $HOME/.agents/skills"
[ -z "$DESTS" ] && DESTS="$HOME/.claude/skills"

for skill in $SKILLS; do
  [ -d "$SRC/$skill" ] || { echo "skip: unknown skill '$skill'"; continue; }
  for base in $DESTS; do
    dest="$base/$skill"
    mkdir -p "$base"
    rm -rf "$dest"
    if [ "$LINK" = 1 ]; then
      ln -s "$SRC/$skill" "$dest"
      echo "linked: $dest"
    else
      cp -R "$SRC/$skill" "$dest"
      find "$dest" -name .DS_Store -type f -exec rm -f {} +
      echo "installed: $dest"
    fi
  done
done
