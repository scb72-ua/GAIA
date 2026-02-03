# NM-VECINO-001-BE-T01 — Implementation Plan

**Source ticket**: `specs/features/news-management/tickets.md` → **NM-VECINO-001-BE-T01**  
**Related user story**: **NM-VECINO-001** (from `specs/features/news-management/user-stories.md`)  
**Plan version**: v1.0 — (Claude, 2026-02-03T18:05:31+01:00)  
**Traceability**: All tasks must include inline references to `NM-VECINO-001-BE-T01` and `NM-VECINO-001` scenario names/tags.

---

## 1) Context & Objective

### Ticket Summary
Implement the `POST /api/v1/news` endpoint for authenticated Vecinos/Admins to create news drafts. This is the first authenticated endpoint, requiring JWT validation and RBAC enforcement.

### Impacted Entities/Tables
- `news` table (insert)

### Impacted Services/Modules
- `backend/app/application/news/` — CreateNewsDraftUseCase
- `backend/app/presentation/news/` — Router, CreateNewsRequest schema
- `backend/app/domain/audit/` — Audit event interface
- `backend/app/infrastructure/audit/` — Audit logger

### Impacted Tests or Business Flows
- `Scenario: Neighbor creates a news draft`
- `Scenario: Draft requires title and content`
- `Scenario: Unauthenticated user cannot create draft`
- `Scenario: Draft creation is audited`

---

## 2) Scope

### In Scope
- `POST /api/v1/news` endpoint (requires auth: VECINO or ADMIN)
- Request body: `title` (required), `content` (required)
- Auto-set: `status=draft`, `author_id=current_user`, `created_at=now`
- Generate excerpt from first 200 chars of content
- Validation: 400 with field-specific messages
- Auth: 401 for unauthenticated, 403 for PUBLIC role
- Audit log: `news.created` event

### Out of Scope
- Image upload
- Scheduling

### Assumptions
- Auth feature provides JWT validation middleware
- Auth feature provides `get_current_user` dependency

---

## 3) Detailed Work Plan (TDD + BDD)

### 3.1 NFR Hooks

#### Security
- JWT validation required
- RBAC: VECINO or ADMIN role only
- PUBLIC role receives 403

#### Observability
- Audit log entry: `news.created`
- Include user_id, news_id, status, timestamp

---

## 4) Atomic Task Breakdown

### Task 1: Add create method to Repository

- **Purpose**: Extend repository for insert operations. References `NM-VECINO-001-BE-T01`.
- **Artifacts impacted**:
  - `backend/app/domain/news/repository.py` (UPDATE)
  - `backend/app/infrastructure/news/repository.py` (UPDATE)
- **BDD Acceptance**:

```gherkin
Scenario: Create news draft
  Given valid news data
  When I call repository.create(news)
  Then the news is persisted with status='draft'
  And the generated ID is returned
```

---

### Task 2: Create Audit Domain Interface

- **Purpose**: Define audit logging contract. References `NM-VECINO-001-BE-T01`.
- **Artifacts impacted**:
  - `backend/app/domain/audit/` (NEW directory)
  - `backend/app/domain/audit/events.py` (NEW)
  - `backend/app/infrastructure/audit/logger.py` (NEW)

---

### Task 3: Create CreateNewsDraftUseCase

- **Purpose**: Business logic for draft creation with audit. References `NM-VECINO-001-BE-T01`.
- **Artifacts impacted**:
  - `backend/app/application/news/create_draft.py` (NEW)
  - `backend/tests/unit/test_create_news_draft.py` (NEW)
- **BDD Acceptance**:

```gherkin
Scenario: Create draft with valid data
  Given user with VECINO role
  And valid title and content
  When I call CreateNewsDraftUseCase
  Then news is saved with status='draft'
  And excerpt is generated from content
  And audit event 'news.created' is logged

Scenario: Reject empty title
  Given valid content but empty title
  When I call CreateNewsDraftUseCase
  Then ValidationError is raised for 'title'
```

---

### Task 4: Create POST Endpoint

- **Purpose**: Expose authenticated endpoint. References `NM-VECINO-001-BE-T01`.
- **Artifacts impacted**:
  - `backend/app/presentation/news/router.py` (UPDATE)
  - `backend/app/presentation/news/schemas.py` (UPDATE)
  - `backend/tests/api/test_news_create.py` (NEW)
- **BDD Acceptance**:

```gherkin
Scenario: POST /api/v1/news creates draft
  Given I am authenticated as VECINO
  When I POST with valid title and content
  Then I receive 201 Created
  And response contains news ID

Scenario: 401 for unauthenticated
  Given no auth token
  When I POST /api/v1/news
  Then I receive 401 Unauthorized

Scenario: 403 for PUBLIC role
  Given I am authenticated as PUBLIC
  When I POST /api/v1/news
  Then I receive 403 Forbidden

Scenario: 400 for validation errors
  Given I am authenticated as VECINO
  When I POST with empty title
  Then I receive 400 with error for 'title'
```

---

## 5) Definition of Done

- [ ] Repository create method implemented
- [ ] Audit interface and logger created
- [ ] Use case with unit tests
- [ ] API endpoint with tests (auth + validation)
- [ ] Audit log verified
