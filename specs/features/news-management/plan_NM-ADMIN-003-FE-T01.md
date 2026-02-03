# NM-ADMIN-003-FE-T01 — Implementation Plan

**Source ticket**: `specs/features/news-management/tickets.md` → **NM-ADMIN-003-FE-T01**  
**Related user story**: **NM-ADMIN-003** (from `specs/features/news-management/user-stories.md`)  
**Plan version**: v1.0 — (Claude, 2026-02-03T18:05:31+01:00)  
**Traceability**: All tasks must include inline references to `NM-ADMIN-003-FE-T01` and `NM-ADMIN-003` scenario names/tags.

---

## 1) Context & Objective

### Ticket Summary
Enable admins to access the edit form for any article, updating the existing NewsEditPage permission logic.

### Impacted Tests or Business Flows
- `Scenario: Admin edits a published article`
- `Scenario: Admin edits a neighbor's draft`

---

## 2) Scope

### In Scope
- Admins can navigate to `/noticias/:id/editar` for any article
- Reuse `NewsEditPage` with admin permission check
- Changes immediately visible if article is published

---

## 3) Atomic Task Breakdown

### Task 1: Update NewsEditPage Permissions

- **Purpose**: Allow admin access to any article. References `NM-ADMIN-003-FE-T01`.
- **Artifacts impacted**:
  - `frontend/src/features/news/pages/NewsEditPage.tsx` (UPDATE)
  - `frontend/src/features/news/pages/NewsEditPage.test.tsx` (UPDATE)
- **BDD Acceptance**:

```gherkin
Scenario: Admin can edit any article
  Given I am logged in as ADMIN
  When I navigate to /noticias/:id/editar for any article
  Then I can edit the article

Scenario: Vecino cannot edit others' articles
  Given I am logged in as VECINO
  When I navigate to /noticias/:id/editar for another's article
  Then I receive 403 error
```

---

## 4) Definition of Done

- [ ] Admin can access edit page for any article
- [ ] Vecino restrictions still enforced
- [ ] Updated tests for admin path
