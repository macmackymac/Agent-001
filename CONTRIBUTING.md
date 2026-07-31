# Contributing to APPA

Thank you for your interest in contributing to APPA.

APPA is the flagship AI platform developed by **Sinag Lab**. Our goal is to build a modular, enterprise-ready productivity assistant powered by agentic AI.

---

# Development Principles

We value:

- Simplicity over complexity
- Readable code
- Modular architecture
- Security by design
- Reusable components
- Comprehensive documentation

---

# Branch Strategy

Main branches:

```
main
```

Stable production code.

```
APPA
```

Primary development branch.

Feature branches:

```
feature/<feature-name>
```

Examples:

```
feature/google-calendar
feature/memory
feature/rag
feature/mcp
```

Bug fixes:

```
bugfix/<issue>
```

---

# Commit Message Convention

Use short and descriptive commits.

Examples:

```
feat: add Gmail integration
```

```
fix: resolve OAuth callback issue
```

```
docs: update roadmap
```

```
refactor: move tools into services package
```

---

# Code Style

- Use descriptive function names.
- Keep functions focused on a single responsibility.
- Prefer modular files over very large modules.
- Avoid duplicate logic.
- Add docstrings for public functions.
- Keep comments meaningful.

---

# Pull Requests

Before opening a pull request:

- Test locally.
- Ensure Streamlit deploys successfully.
- Update documentation if needed.
- Update CHANGELOG.md for user-visible changes.

---

# Project Structure

```
APPA
│
├── assets/
├── auth/
├── core/
├── docs/
├── personas/
├── services/
├── streamlit_app.py
├── README.md
├── CHANGELOG.md
└── ROADMAP.md
```

---

# Reporting Issues

When reporting a bug, include:

- Description
- Steps to reproduce
- Expected behavior
- Actual behavior
- Screenshots (if applicable)
- Error messages
- Environment details

---

# Vision

Every contribution should move APPA closer to becoming an intelligent productivity platform capable of serving individuals, teams, and enterprises.
