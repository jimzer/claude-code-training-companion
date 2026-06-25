---
description: Security rules for production code
paths:
  - "services/**/*.py"
  - "libs/**/*.py"
---

# Security Rules

## Authentication & Authorization
- Never bypass auth middleware, even in tests
- Use the shared auth library from `libs/auth`
- All endpoints require authentication unless explicitly marked public
- Use role-based access control (RBAC) for authorization

## Data Handling
- Never log PII (emails, names, SSNs, etc.)
- Sanitize all user input before processing
- Use parameterized queries, never string concatenation for SQL
- Encrypt sensitive fields at rest using `libs/crypto`

## Secrets
- Never hardcode secrets, tokens, or API keys
- Use environment variables via pydantic-settings
- Never commit `.env` files
- Rotate secrets if accidentally exposed

## Dependencies
- Pin all dependency versions exactly
- Run `safety check` before adding new dependencies
- No dependencies with known CVEs
- Prefer well-maintained packages (>1000 GitHub stars, recent commits)
