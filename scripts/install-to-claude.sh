#!/usr/bin/env sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
SOURCE_DIR=$(CDPATH= cd -- "$SCRIPT_DIR/../anti-distill" && pwd)
TARGET_ROOT="${1:-$HOME/.claude/skills}"
TARGET_DIR="$TARGET_ROOT/anti-distill"

mkdir -p "$TARGET_ROOT"
rm -rf "$TARGET_DIR"
cp -R "$SOURCE_DIR" "$TARGET_DIR"

printf 'Installed anti-distill to %s\n' "$TARGET_DIR"
