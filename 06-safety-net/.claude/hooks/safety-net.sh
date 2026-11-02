#!/bin/bash
# Stop hook: enforce the safety net.
#
# Claude cannot end its turn until the full gate (format + lint + types + tests)
# is green. On failure we print the output to stderr and exit 2, which Claude
# Code feeds back to the model so it keeps working instead of stopping.

# Run from the station root regardless of where the hook is invoked.
cd "$(dirname "$0")/../.." || exit 0

out=$(make check 2>&1)
status=$?

if [ "$status" -ne 0 ]; then
    echo "SAFETY NET FAILED -- fix these before finishing:" >&2
    echo "$out" >&2
    exit 2
fi

exit 0
