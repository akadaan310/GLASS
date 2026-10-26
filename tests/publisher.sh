#!/bin/sh
set -eu
bin=$(realpath "$1")
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
git init -q --bare --initial-branch=main "$tmp/remote.git"
git init -q --initial-branch=main "$tmp/work"
git -C "$tmp/work" config user.name Glass-Test
git -C "$tmp/work" config user.email glass-test@example.invalid
git -C "$tmp/work" remote add origin "$tmp/remote.git"
printf 'seed\n' > "$tmp/work/seed.txt"
git -C "$tmp/work" add seed.txt
git -C "$tmp/work" commit -qm seed
git -C "$tmp/work" push -q origin main
printf 'atlas\n' > "$tmp/work/atlas.json"
"$bin" "$tmp/work" "$tmp/receipt.json" atlas.json
test "$(git -C "$tmp/work" rev-parse HEAD)" = "$(git --git-dir="$tmp/remote.git" rev-parse main)"
git -C "$tmp/work" switch -qc temp
if "$bin" "$tmp/work" "$tmp/refused.json" atlas.json; then exit 1; fi
git -C "$tmp/work" switch -q main
printf 'pending\n' >> "$tmp/work/atlas.json"
git -C "$tmp/work" remote set-url origin "$tmp/unreachable.git"
if "$bin" "$tmp/work" "$tmp/pending.json" atlas.json; then exit 1; fi
test -s "$tmp/pending.json"
printf 'PASS main publication, branch guard, transport queue receipt\n'
