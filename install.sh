#!/usr/bin/env sh
# Install skills from this collection into each detected agent (Claude Code, Codex).
# Usage:
#   ./install.sh                 install every skill
#   ./install.sh orchestrate ... install only the named skills
set -eu

HERE=$(cd "$(dirname "$0")" && pwd)
SRC="$HERE/skills"

[ -d "$SRC" ] || { echo "error: $SRC not found (run from a checkout of the repo)"; exit 1; }

# Which skills to install: args, or all directories under skills/.
if [ "$#" -gt 0 ]; then
  SKILLS="$*"
else
  SKILLS=$(cd "$SRC" && for d in */; do printf '%s ' "${d%/}"; done)
fi

# Destination agent skill dirs.
DESTS=""
[ -d "$HOME/.claude" ] && DESTS="$DESTS $HOME/.claude/skills"
[ -d "$HOME/.codex" ]  && DESTS="$DESTS $HOME/.codex/skills"
[ -z "$DESTS" ] && DESTS="$HOME/.claude/skills"

for skill in $SKILLS; do
  [ -d "$SRC/$skill" ] || { echo "skip: unknown skill '$skill'"; continue; }
  for base in $DESTS; do
    dest="$base/$skill"
    mkdir -p "$base"
    rm -rf "$dest"
    cp -R "$SRC/$skill" "$dest"
    echo "installed: $dest"
  done
done
