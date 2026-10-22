#!/bin/bash
# prepare rewrite prompts and mark units as rewriting
cd "$(dirname "$0")/.."
for f in "$@"; do sed "s/{FILE}/$f/g" work/rewrite_prompt.md > work/context/rewrite-$f.prompt; done
python3 scripts/pipeline.py start "$@"
