# NM-ADMIN-002-FE-T01 — Implementation Plan

**Source ticket**: `specs/features/news-management/tickets.md` → **NM-ADMIN-002-FE-T01**  
**Related user story**: **NM-ADMIN-002** (from `specs/features/news-management/user-stories.md`)  
**Plan version**: v1.0 — (Claude, 2026-02-03T18:05:31+01:00)  
**Traceability**: All tasks must include inline references to `NM-ADMIN-002-FE-T01` and `NM-ADMIN-002` scenario names/tags.

---

## 1) Context & Objective

### Ticket Summary
Implement the unpublish action button for admins.

### Impacted Tests or Business Flows
- `Scenario: Admin unpublishes an article`
- `Scenario: Article is already a draft`

---

## 2) Scope

### In Scope
- "Despublicar" button (visible only for published articles)
- `useMutation` for unpublish action
- Success: toast "Noticia despublicada"
- Handle 400 (already draft): toast with message

---

## 3) Atomic Task Breakdown

### Task 1: Create UnpublishButton Component

- **Artifacts impacted**:
  - `frontend/src/features/news/components/UnpublishButton.tsx` (NEW)
  - `frontend/src/features/news/components/UnpublishButton.test.tsx` (NEW)
  - `frontend/src/features/news/api/newsApi.ts` (UPDATE)
- **BDD Acceptance**:

```gherkin
Scenario: Button visible for published articles
  Given article status is 'published'
  Then I see "Despublicar" button

Scenario: Success shows toast
  When I click Despublicar and API succeeds
  Then I see toast "Noticia despublicada"
```

---

## 4) Definition of Done

- [ ] UnpublishButton component with tests
- [ ] Button only visible for published status
- [ ] Toast notifications work
