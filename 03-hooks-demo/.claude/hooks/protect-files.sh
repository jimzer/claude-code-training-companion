#!/bin/bash
# Protect sensitive files from being read or modified by Claude

# Read JSON input from stdin (Claude Code passes hook context via stdin)
TOOL_INPUT=$(cat /dev/stdin)

# List of protected file patterns
PROTECTED_PATTERNS=(
    ".env"
    ".env.local"
    ".env.production"
    "credentials"
    "secrets"
)

# Check if the tool input references a protected file
for pattern in "${PROTECTED_PATTERNS[@]}"; do
    if echo "$TOOL_INPUT" | grep -qi "$pattern"; then
        echo "BLOCKED: Access to files matching '$pattern' is not allowed." >&2
        echo "These files contain sensitive information (API keys, passwords, etc.)" >&2
        echo "and should not be read or modified by AI assistants." >&2
        exit 2
    fi
done

exit 0
