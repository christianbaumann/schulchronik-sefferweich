#!/usr/bin/env bash
# Wrapper for git push that handles the CI race condition.
# Retries pull --rebase + push up to 3 times to handle the window
# where CI auto-commits arrive between rebase and push.
#
# Usage: bash Scripts/git-push.sh [push args...]
#   e.g.: bash Scripts/git-push.sh
#         bash Scripts/git-push.sh origin main

set -e
MAX_RETRIES=3

for i in $(seq 1 $MAX_RETRIES); do
    git pull --rebase || { echo "Rebase failed — resolve conflicts first."; exit 1; }
    if git push "$@" 2>&1; then
        exit 0
    fi
    if [ "$i" -lt "$MAX_RETRIES" ]; then
        echo "Push rejected (attempt $i/$MAX_RETRIES) — CI likely pushed. Retrying in 3s..."
        sleep 3
    fi
done

echo "Push failed after $MAX_RETRIES attempts. Try again manually."
exit 1
