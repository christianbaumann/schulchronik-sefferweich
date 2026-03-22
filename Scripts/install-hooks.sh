#!/usr/bin/env bash
# Install git hooks for the Schulchronik project.
set -e
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
HOOKS_DIR="$REPO_ROOT/.git/hooks"
HOOKS_SRC="$REPO_ROOT/Scripts/hooks"

for hook in "$HOOKS_SRC"/*; do
    name=$(basename "$hook")
    ln -sf "$hook" "$HOOKS_DIR/$name"
    echo "Installed hook: $name"
done
