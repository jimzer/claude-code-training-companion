#!/bin/bash
# Headless mode teaser.
#
# `claude -p "<prompt>"` runs ONE prompt non-interactively, prints the result to
# stdout, and exits. That makes Claude Code a normal Unix filter: pipe data in,
# get text out, compose it with anything. This one-liner turns a staged diff into
# a commit message.
#
# Usage: stage some changes, then `bash headless.sh`

git diff --staged | claude -p "Write a one-line conventional-commit message for this diff. Output only the message, nothing else."
