#!/usr/bin/env python3
"""Extract statusline fields from Claude Code's JSON payload (stdin)
and emit shell-quoted KEY=VALUE assignments on stdout."""

import json
import shlex
import sys
import time

try:
    d = json.load(sys.stdin)
except Exception:
    d = {}


def q(k, v):
    print(f"{k}={shlex.quote(str(v) if v is not None else '')}")


def pct(v):
    """Round a percentage to a whole-number string; '' if not numeric."""
    try:
        return str(int(round(float(v))))
    except (TypeError, ValueError):
        return ""


q("cwd", d.get("cwd") or d.get("workspace", {}).get("current_dir") or "")
q("model", (d.get("model") or {}).get("display_name") or "")
q("effort", ((d.get("effort") or {}).get("level") or "").lower())
q("thinking_on", "1" if (d.get("thinking") or {}).get("enabled") else "")
q("fast_mode", "1" if d.get("fast_mode") else "")

cw = d.get("context_window") or {}
q("ctx_pct", pct(cw.get("used_percentage")))


def fmt_k(n):
    try:
        n = int(n)
    except Exception:
        return ""
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M".replace(".0M", "M")
    if n >= 10_000:
        return f"{n // 1000}k"
    if n >= 1000:
        return f"{n / 1000:.1f}k".replace(".0k", "k")
    return f"{n}"


ctx_tokens = (cw.get("total_input_tokens") or 0) + (cw.get("total_output_tokens") or 0)
q("ctx_tokens", fmt_k(ctx_tokens) if ctx_tokens else "")

rl = d.get("rate_limits") or {}
fh = rl.get("five_hour") or {}
sd = rl.get("seven_day") or {}
q("session_pct", pct(fh.get("used_percentage")))
q("week_pct", pct(sd.get("used_percentage")))


def rel(ts):
    if not ts:
        return ""
    try:
        secs = int(ts) - int(time.time())
    except Exception:
        return ""
    if secs <= 0:
        return "now"
    if secs < 3600:
        return f"{secs // 60}m"
    if secs < 86400:
        h = secs // 3600
        m = (secs % 3600) // 60
        return f"{h}h{m:02d}m" if secs < 36000 else f"{h}h"
    d_ = secs // 86400
    h = (secs % 86400) // 3600
    return f"{d_}d{h}h" if secs < 7 * 86400 else f"{d_}d"


q("session_reset", rel(fh.get("resets_at")))
q("week_reset", rel(sd.get("resets_at")))
