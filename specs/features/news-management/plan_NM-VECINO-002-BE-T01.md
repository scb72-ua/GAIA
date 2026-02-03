# NM-VECINO-002-BE-T01 — Implementation Plan

**Source ticket**: `specs/features/news-management/tickets.md` → **NM-VECINO-002-BE-T01**  
**Related user story**: **NM-VECINO-002** (from `specs/features/news-management/user-stories.md`)  
**Plan version**: v1.0 — (Claude, 2026-02-03T18:05:31+01:00)  
**Traceability**: All tasks must include inline references to `NM-VECINO-002-BE-T01` and `NM-VECINO-002` scenario names/tags.

---

## 1) Context & Objective

### Ticket Summary
Implement the `PUT /api/v1/news/{id}` endpoint for Vecinos to edit their own unpublished drafts. This introduces ownership-based authorization.

### Impacted Tests or Business Flows
- `Scenario: Neighbor edits their own draft`
- `Scenario: Neighbor cannot edit another neighbor's draft`
- `Scenario: Neighbor cannot edit published articles`
- `Scenario: Draft was deleted`

---

## 2) Scope

### In Scope
- `PUT /api/v1/news/{id}` endpoint (requires auth: VECINO or ADMIN)
- Vecino: can only edit if `author_id == current_user AND status == draft`
- Request body: `title`, `content` (at least one required)
- Validation: 400 for empty required fields
- 403 if Vecino tries to edit others' drafts or published articles
- 404 if article not found
- Update `updated_at` timestamp

### Out of Scope
- Bulk edit
- Admin edit (separate ticket NM-ADMIN-003)

---

## 3) Atomic Task Breakdown

### Task 1: Create EditOwnDraftUseCase

- **Purpose**: Business logic with ownership validation. References `NM-VECINO-002-BE-T01`.
- **Artifacts impacted**:
  - `backend/app/application/news/edit_draft.py` (NEW)
  - `backend/tests/unit/test_edit_own_draft.py` (NEW)
- **BDD Acceptance**:

```gherkin
Scenario: Vecino edits own draft
  Given I own a draft article
  When I call EditOwnDraftUseCase
  Then article is updated
  And updated_at is refreshed

Scenario: Cannot edit others' drafts
  Given another user owns the draft
  When I call EditOwnDraftUseCase
  Then ForbiddenError is raised

Scenario: Cannot edit published articles
  Given I own a published article
  When I call EditOwnDraftUseCase
  Then ForbiddenError is raised
```

---

### Task 2: Add PUT Endpoint

- **Purpose**: Expose edit endpoint. References `NM-VECINO-002-BE-T01`.
- **Artifacts impacted**:
  - `backend/app/presentation/news/router.py` (UPDATE)
  - `backend/app/presentation/news/schemas.py` (UPDATE)
  - `backend/tests/api/test_news_edit.py` (NEW)
- **BDD Acceptance**:

```gherkin
Scenario: PUT /api/v1/news/{id} works for owner
  Given I own a draft article
  When I PUT with updated content
  Then I receive 200 OK

Scenario: 403 for non-owner
  Given another user owns the article
  When I PUT /api/v1/news/{id}
  Then I receive 403 Forbidden

Scenario: 404 for missing article
  When I PUT /api/v1/news/nonexistent
  Then I receive 404 Not Found
```

---

## 4) Definition of Done

- [ ] EditOwnDraftUseCase with ownership checks
- [ ] API endpoint with tests
- [ ] 403 for ownership/status violations
