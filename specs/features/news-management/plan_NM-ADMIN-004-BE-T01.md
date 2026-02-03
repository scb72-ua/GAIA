# NM-ADMIN-004-BE-T01 — Implementation Plan

**Source ticket**: `specs/features/news-management/tickets.md` → **NM-ADMIN-004-BE-T01**  
**Related user story**: **NM-ADMIN-004** (from `specs/features/news-management/user-stories.md`)  
**Plan version**: v1.0 — (Claude, 2026-02-03T18:05:31+01:00)  
**Traceability**: All tasks must include inline references to `NM-ADMIN-004-BE-T01` and `NM-ADMIN-004` scenario names/tags.

---

## 1) Context & Objective

### Ticket Summary
Implement the `DELETE /api/v1/news/{id}` endpoint for Admins to permanently delete articles.

### Impacted Tests or Business Flows
- `Scenario: Admin deletes an article`
- `Scenario: Vecino cannot delete articles`
- `Scenario: Article does not exist`
- `Scenario: Deletion is audited`

---

## 2) Scope

### In Scope
- `DELETE /api/v1/news/{id}` (ADMIN only)
- Hard delete from database
- 403 for non-admin roles
- 404 if not found
- Audit log: `news.deleted` event with article metadata snapshot

### Out of Scope
- Soft delete
- Trash/restore

---

## 3) Atomic Task Breakdown

### Task 1: Add delete method to Repository

- **Artifacts impacted**:
  - `backend/app/domain/news/repository.py` (UPDATE)
  - `backend/app/infrastructure/news/repository.py` (UPDATE)

---

### Task 2: Create DeleteNewsUseCase

- **Artifacts impacted**:
  - `backend/app/application/news/delete.py` (NEW)
  - `backend/tests/unit/test_delete_news.py` (NEW)
- **BDD Acceptance**:

```gherkin
Scenario: Admin deletes article
  Given an article exists
  When admin deletes
  Then article is removed from DB
  And audit log contains article metadata

Scenario: Non-existent returns NotFound
  Given no article exists
  When admin deletes
  Then NotFoundError raised
```

---

### Task 3: Add DELETE Endpoint

- **Artifacts impacted**:
  - `backend/app/presentation/news/router.py` (UPDATE)
  - `backend/tests/api/test_news_delete.py` (NEW)
- **BDD Acceptance**:

```gherkin
Scenario: DELETE /api/v1/news/{id} works for admin
  Given I am ADMIN
  When I DELETE
  Then I receive 204 No Content

Scenario: 403 for VECINO
  Given I am VECINO
  When I DELETE
  Then I receive 403 Forbidden
```

---

## 4) Definition of Done

- [ ] DeleteNewsUseCase with tests
- [ ] API endpoint with admin-only RBAC
- [ ] Audit log with metadata snapshot
