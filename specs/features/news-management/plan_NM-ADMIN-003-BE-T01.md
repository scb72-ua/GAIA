# NM-ADMIN-003-BE-T01 — Implementation Plan

**Source ticket**: `specs/features/news-management/tickets.md` → **NM-ADMIN-003-BE-T01**  
**Related user story**: **NM-ADMIN-003** (from `specs/features/news-management/user-stories.md`)  
**Plan version**: v1.0 — (Claude, 2026-02-03T18:05:31+01:00)  
**Traceability**: All tasks must include inline references to `NM-ADMIN-003-BE-T01` and `NM-ADMIN-003` scenario names/tags.

---

## 1) Context & Objective

### Ticket Summary
Extend the PUT endpoint to allow Admins to edit any article regardless of ownership or status.

### Impacted Tests or Business Flows
- `Scenario: Admin edits a published article`
- `Scenario: Admin edits a neighbor's draft`
- `Scenario: Edit is audited`

---

## 2) Scope

### In Scope
- Extend `PUT /api/v1/news/{id}` to allow ADMIN role to edit any article
- Validation: 400 for empty required fields
- Update `updated_at` timestamp
- Audit log: `news.updated` event

---

## 3) Atomic Task Breakdown

### Task 1: Extend EditNewsUseCase

- **Purpose**: Add admin path that bypasses ownership check. References `NM-ADMIN-003-BE-T01`.
- **Artifacts impacted**:
  - `backend/app/application/news/edit_draft.py` (UPDATE)
  - `backend/tests/unit/test_edit_news_admin.py` (NEW)
- **BDD Acceptance**:

```gherkin
Scenario: Admin can edit any article
  Given an article owned by another user
  And I am ADMIN
  When I call EditNewsUseCase
  Then article is updated successfully

Scenario: Admin can edit published articles
  Given a published article
  And I am ADMIN
  When I call EditNewsUseCase
  Then article is updated and remains published
```

---

### Task 2: Update API Tests

- **Artifacts impacted**:
  - `backend/tests/api/test_news_edit.py` (UPDATE)

---

## 4) Definition of Done

- [ ] ADMIN can edit any article
- [ ] Audit log for updates
- [ ] Tests for admin path
