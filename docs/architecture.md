# NOVA Scout — Architecture

**Version:** 0.1.0
**Status:** Architecture Lock
**Last updated:** 2026-10-02

---

## 1. Purpose

NOVA Scout (Niche Opportunity & Validation Analyzer) is a research and validation system designed to discover, investigate, compare, and monitor international microproduct opportunities.

The system exists to answer a practical question:

> Is there enough evidence to justify spending a small amount of time and money building this product?

NOVA Scout does not make the final business decision.

It collects evidence, organizes it, analyzes it, exposes uncertainty, and produces a traceable opportunity profile.

The human remains responsible for the final decision.

---

## 2. Core Principle

NOVA Scout must not operate as a black-box score generator.

The fundamental pipeline is:

SOURCE
   ↓
RAW DATA
   ↓
NORMALIZATION
   ↓
EVIDENCE
   ↓
ANALYSIS
   ↓
OPPORTUNITY PROFILE
   ↓
REPORT
   ↓
HUMAN DECISION

Every important analytical conclusion should be traceable to one or more pieces of evidence.

---

## 3. Architectural Goals

The architecture must prioritize:

1. Simplicity during the MVP.
2. Clear separation of responsibilities.
3. Testability.
4. Traceable evidence.
5. Reproducible analysis.
6. Preservation of raw collected data.
7. Replaceable data sources.
8. Incremental automation.
9. Low operational complexity.
10. Future support for autonomous scheduled research.

The project should grow by adding capabilities rather than repeatedly rewriting its foundation.

---

## 4. High-Level Architecture

```text
NOVA SCOUT
│
├── CLI / UI
│
├── APPLICATION
│
├── DOMAIN
│
├── SOURCES
│
├── EVIDENCE
│
├── ANALYSIS
│
├── REPORTS
│
└── STORAGE / FILES
```

## 5. Architectural Layers

### 5.1 Interface Layer

Responsible for interaction with the user.

Initial interface:

```text
nova
```

Examples:

    nova --help
    nova status
    nova idea add "Example Product"
    nova idea list
    nova scan 001
    nova report 001

The CLI must remain thin.

Business logic must not be implemented directly inside CLI commands.

### 5.2 Application Layer

Responsible for orchestrating use cases.

Examples:

    OpportunityService
    ResearchService
    ReportService

The application layer coordinates domain objects, repositories, sources, and analyzers.
### 5.3 Domain Layer

Contains the core concepts of NOVA Scout.

Initial concepts:

```text
Opportunity
Evidence
Research
OpportunityProfile
```

The domain should not depend directly on:

```text
CLI
HTTP clients
SQLite
specific marketplaces
environment variables
```

### 5.4 Infrastructure Layer

Contains implementation details such as:

```text
SQLite
HTTP clients
API connectors
file storage
schedulers
logging
```

Infrastructure should implement interfaces required by the application/domain rather than becoming the domain itself.
