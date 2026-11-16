#!/usr/bin/env sh
# Install this stack into each detected agent: the skills of this repo, then the third-party skills
# listed in external.txt.
# Usage:
#   ./install.sh [--link] [skill ...]   every skill and external.txt, or only the named skills of this repo
# --link symlinks each skill to this checkout, so a pull or an edit here is live everywhere.
set -eu

HERE=$(cd "$(dirname "$0")" && pwd -P)
SRC="$HERE/skills"
LIST="$HERE/external.txt"
STAMP="$HOME/.agents/.external-skills.sum"
MANAGED="$HOME/.agents/.external-skills"
LOCK="$HOME/.agents/.skill-lock.json"

[ -d "$SRC" ] || { echo "error: $SRC not found (run from a checkout of the repo)"; exit 1; }

LINK=0
if [ "${1:-}" = "--link" ]; then LINK=1; shift; fi

if [ "$#" -gt 0 ]; then
  SKILLS="$*"
  EXTERNAL=0
else
  SKILLS=$(cd "$SRC" && for d in */; do printf '%s ' "${d%/}"; done)
  EXTERNAL=1
fi

# external.txt is applied only when it changed: npx skills add fetches every source. Only skills this script
# installed (MANAGED) or npx copies of this repo's own skills are removed, never another tool's.
external() {
  command -v npx >/dev/null 2>&1 || { echo "skip external.txt: npx is missing"; return 0; }
  sum=$(cksum < "$LIST")
  [ "$(cat "$STAMP" 2>/dev/null)" = "$sum" ] && return 0
  wanted=$(grep -v '^#' "$LIST" | awk '{ for (i = 2; i <= NF; i++) print $i }')
  stale=$(cat "$MANAGED" 2>/dev/null || true)
  if [ -f "$LOCK" ] && command -v jq >/dev/null 2>&1; then
    stale="$stale
$(jq -r '.skills | to_entries[] | select(.value.source == "falistos/skills") | .key' "$LOCK")"
  fi
  failed=0
  for name in $stale; do
    printf '%s\n' "$wanted" | grep -qx "$name" && continue
    if (cd /tmp && npx -y skills remove "$name" -g -y </dev/null >/dev/null); then
      echo "removed: $name"
    else
      echo "failed: removing $name"; failed=1
    fi
  done
  grep -v '^#' "$LIST" | {
    status=0
    while read -r source names; do
      [ -n "$source" ] || continue
      # shellcheck disable=SC2086
      if (cd /tmp && npx -y skills add "$source" -g -y -s $names </dev/null >/dev/null); then
        echo "external: $source"
      else
        echo "failed: $source"; status=1
      fi
    done
    exit $status
  } || failed=1
  [ "$failed" = 0 ] || return 1
  mkdir -p "$(dirname "$STAMP")"
  printf '%s\n' "$wanted" > "$MANAGED"
  printf '%s\n' "$sum" > "$STAMP"
}

# Claude and Grok read their own folder; Codex, opencode and the others read ~/.agents/skills.
DESTS=""
[ -d "$HOME/.claude" ] && DESTS="$DESTS $HOME/.claude/skills"
[ -d "$HOME/.grok" ] && DESTS="$DESTS $HOME/.grok/skills"
{ [ -d "$HOME/.agents" ] || [ -d "$HOME/.codex" ]; } && DESTS="$DESTS $HOME/.agents/skills"
[ -z "$DESTS" ] && DESTS="$HOME/.claude/skills"

# Remove the npx copies of skills this repo now links before linking over them.
failed=0
[ "$EXTERNAL" = 1 ] && { external || failed=1; }

for skill in $SKILLS; do
  [ -d "$SRC/$skill" ] || { echo "skip: unknown skill '$skill'"; continue; }
  for base in $DESTS; do
    dest="$base/$skill"
    mkdir -p "$base"
    if [ -L "$dest" ]; then
      current=$(readlink "$dest")
      case $current in
        "$SRC/$skill") [ "$LINK" = 1 ] && continue ;;
        "$SRC"/*|*/.agents/skills/"$skill") ;;
        *) echo "skip: $dest links to $current, not this repo"; continue ;;
      esac
    fi
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

[ "$failed" = 0 ] || { echo "error: external.txt was not fully applied; the next run retries it"; exit 1; }
