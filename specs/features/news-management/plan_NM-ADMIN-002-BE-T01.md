# NM-ADMIN-002-BE-T01 — Implementation Plan

**Source ticket**: `specs/features/news-management/tickets.md` → **NM-ADMIN-002-BE-T01**  
**Related user story**: **NM-ADMIN-002** (from `specs/features/news-management/user-stories.md`)  
**Plan version**: v1.0 — (Claude, 2026-02-03T18:05:31+01:00)  
**Traceability**: All tasks must include inline references to `NM-ADMIN-002-BE-T01` and `NM-ADMIN-002` scenario names/tags.

---

## 1) Context & Objective

### Ticket Summary
Implement the `POST /api/v1/news/{id}/unpublish` endpoint for Admins to unpublish articles.

### Impacted Tests or Business Flows
- `Scenario: Admin unpublishes an article`
- `Scenario: Vecino cannot unpublish articles`
- `Scenario: Article is already a draft`
- `Scenario: Unpublication is audited`

---

## 2) Scope

### In Scope
- `POST /api/v1/news/{id}/unpublish` (ADMIN only)
- Change `status` to `draft`, clear `published_at`
- 403 for non-admin roles
- 400 if already draft
- 404 if not found
- Audit log: `news.unpublished` event

---

## 3) Atomic Task Breakdown

### Task 1: Create UnpublishNewsUseCase

- **Artifacts impacted**:
  - `backend/app/application/news/unpublish.py` (NEW)
  - `backend/tests/unit/test_unpublish_news.py` (NEW)
- **BDD Acceptance**:

```gherkin
Scenario: Unpublish published article
  Given a published article
  When admin unpublishes
  Then status='draft' and published_at=None

Scenario: Already draft returns error
  Given a draft article
  When admin unpublishes
  Then AlreadyDraftError raised
```

---

### Task 2: Add Unpublish Endpoint

- **Artifacts impacted**:
  - `backend/app/presentation/news/router.py` (UPDATE)
  - `backend/tests/api/test_news_unpublish.py` (NEW)

---

## 4) Definition of Done

- [ ] UnpublishNewsUseCase with tests
- [ ] API endpoint with admin-only RBAC
- [ ] Audit log verified
