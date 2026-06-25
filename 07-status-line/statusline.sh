#!/bin/sh
# Claude Code statusLine: robbyrussell prompt + model + thinking + plan % usage.
# All data comes from the JSON payload Claude Code provides on stdin -- no
# external CLI calls, so this is fast (< 50 ms typical).
#
# Layout:
#   line 1: ➜ <dir> git:(<branch>) ✗
#   line 2: 🤖 <model> · 🧪 <effort> · 🧠 <ctx>% · ⏱ 5h <X>% (in 3h) · 📅 week <Y>% (in 2d)

RESET='\033[0m'
BOLD_GREEN='\033[1;32m'
CYAN='\033[0;36m'
BOLD_BLUE='\033[1;34m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[0;33m'
MAGENTA='\033[0;35m'
GREEN='\033[0;32m'
GREY='\033[0;90m'
BOLD='\033[1m'

PY=/usr/bin/python3

input=$(cat)

# Extract all fields via sibling parser; emits shell-quoted KEY=VALUE lines.
# Resolve the parser relative to this script so the station is portable.
SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
eval "$(printf '%s' "$input" | "$PY" "$SCRIPT_DIR/statusline-parse.py")"

# --- robbyrussell prompt ---------------------------------------------------
if [ -n "$cwd" ]; then dir=$(basename "$cwd"); else dir=$(basename "$(pwd)"); fi
arrow="${BOLD_GREEN}➜${RESET}"
dirname="${CYAN}${dir}${RESET}"

git_part=""
repo_dir="${cwd:-$(pwd)}"
if git -C "$repo_dir" rev-parse --is-inside-work-tree --no-optional-locks 2>/dev/null | grep -q true 2>/dev/null; then
  branch=$(git -C "$repo_dir" symbolic-ref --short HEAD 2>/dev/null \
    || git -C "$repo_dir" rev-parse --short HEAD 2>/dev/null)
  if [ -n "$branch" ]; then
    if git -C "$repo_dir" status --porcelain --no-optional-locks 2>/dev/null | grep -q .; then
      dirty="${BLUE})${RESET} ${YELLOW}✗${RESET}"
    else
      dirty="${BLUE})${RESET}"
    fi
    git_part=" ${BOLD_BLUE}git:(${RED}${branch}${dirty}"
  fi
fi

# Color a percentage: <50 green, 50-79 yellow, 80+ red.
color_pct() {
  pct="$1"
  n="${pct%\%}"
  case "$n" in ''|*[!0-9]*) printf '%s%s%s' "$GREY" "$pct" "$RESET"; return;; esac
  if [ "$n" -ge 80 ]; then printf '%s%s%s' "$RED" "$pct" "$RESET"
  elif [ "$n" -ge 50 ]; then printf '%s%s%s' "$YELLOW" "$pct" "$RESET"
  else printf '%s%s%s' "$GREEN" "$pct" "$RESET"
  fi
}

# --- assemble line 2 ------------------------------------------------------
parts=""
sep=" ${GREY}·${RESET} "
add() { [ -n "$parts" ] && parts="${parts}${sep}"; parts="${parts}$1"; }

if [ -n "$model" ]; then
  fast=""
  [ -n "$fast_mode" ] && fast=" ${YELLOW}⚡${RESET}"
  add "${BOLD}🤖 ${model}${RESET}${fast}"
fi

if [ -n "$effort" ] || [ -n "$thinking_on" ]; then
  if [ -n "$effort" ]; then
    label="$effort"
  elif [ -n "$thinking_on" ]; then
    label="on"
  fi
  add "${MAGENTA}🧪 ${label}${RESET}"
fi

if [ -n "$ctx_pct" ]; then
  tok=""; [ -n "$ctx_tokens" ] && tok=" ${GREY}(${ctx_tokens})${RESET}"
  add "🧠 $(color_pct "${ctx_pct}%")${tok}"
fi

if [ -n "$session_pct" ]; then
  rt=""; [ -n "$session_reset" ] && rt=" ${GREY}(in ${session_reset})${RESET}"
  add "⏱ 5h $(color_pct "${session_pct}%")${rt}"
fi

if [ -n "$week_pct" ]; then
  rt=""; [ -n "$week_reset" ] && rt=" ${GREY}(in ${week_reset})${RESET}"
  add "📅 week $(color_pct "${week_pct}%")${rt}"
fi

# --- output ---------------------------------------------------------------
printf "%b %b%b\n" "$arrow" "$dirname" "$git_part"
[ -n "$parts" ] && printf "%b\n" "$parts"
