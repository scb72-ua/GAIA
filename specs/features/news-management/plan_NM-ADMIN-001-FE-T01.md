# NM-ADMIN-001-FE-T01 — Implementation Plan

**Source ticket**: `specs/features/news-management/tickets.md` → **NM-ADMIN-001-FE-T01**  
**Related user story**: **NM-ADMIN-001** (from `specs/features/news-management/user-stories.md`)  
**Plan version**: v1.0 — (Claude, 2026-02-03T18:05:31+01:00)  
**Traceability**: All tasks must include inline references to `NM-ADMIN-001-FE-T01` and `NM-ADMIN-001` scenario names/tags.

---

## 1) Context & Objective

### Ticket Summary
Implement the publish action button for admins in the news management view. This requires an admin panel scaffold if not already present.

### Impacted Services/Modules
- `frontend/src/features/news/components/` — PublishButton
- Admin news list/detail view

### Impacted Tests or Business Flows
- `Scenario: Admin publishes a draft`
- `Scenario: Article is already published`

---

## 2) Scope

### In Scope
- "Publicar" button visible only for drafts
- `useMutation` for publish action
- Success: toast "Noticia publicada", update UI state
- Handle 400 (already published): toast with message
- Button hidden for already-published articles

### Out of Scope
- Bulk publish

---

## 3) Atomic Task Breakdown

### Task 1: Create PublishButton Component

- **Purpose**: Admin action button. References `NM-ADMIN-001-FE-T01`.
- **Artifacts impacted**:
  - `frontend/src/features/news/components/PublishButton.tsx` (NEW)
  - `frontend/src/features/news/components/PublishButton.test.tsx` (NEW)
  - `frontend/src/features/news/api/newsApi.ts` (UPDATE) — publishNews mutation
- **BDD Acceptance**:

```gherkin
Scenario: Button visible for draft articles
  Given article status is 'draft'
  When I render PublishButton
  Then I see "Publicar" button

Scenario: Button hidden for published articles
  Given article status is 'published'
  When I render PublishButton
  Then button is not visible

Scenario: Publish success shows toast
  Given I click Publicar
  When API returns success
  Then I see toast "Noticia publicada"
  And article status updates to 'published'
```

---

### Task 2: Integrate in Admin View

- **Purpose**: Add button to admin news list/detail. References `NM-ADMIN-001-FE-T01`.
- **Artifacts impacted**:
  - Admin news components (UPDATE)
- **Note**: May require creating admin panel scaffold if not present

---

## 4) Definition of Done

- [ ] PublishButton component with tests
- [ ] Mutation invalidates and refetches
- [ ] Toast notifications work
- [ ] Button only visible for drafts
