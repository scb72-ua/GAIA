# NM-VECINO-002-FE-T01 — Implementation Plan

**Source ticket**: `specs/features/news-management/tickets.md` → **NM-VECINO-002-FE-T01**  
**Related user story**: **NM-VECINO-002** (from `specs/features/news-management/user-stories.md`)  
**Plan version**: v1.0 — (Claude, 2026-02-03T18:05:31+01:00)  
**Traceability**: All tasks must include inline references to `NM-VECINO-002-FE-T01` and `NM-VECINO-002` scenario names/tags.

---

## 1) Context & Objective

### Ticket Summary
Implement the news edit form for neighbors editing their own drafts. Reuse the NewsForm component from the create flow.

### Impacted Tests or Business Flows
- `Scenario: Neighbor edits their own draft`
- `Scenario: Neighbor cannot edit published articles`

---

## 2) Scope

### In Scope
- Route: `/noticias/:id/editar` (protected)
- Fetch existing draft data with `useQuery`
- Pre-populate form with current values
- Submit via `useMutation`
- Success: toast "Cambios guardados"
- Handle 403: redirect with message
- Handle 404: show error

### Out of Scope
- Version history

---

## 3) Atomic Task Breakdown

### Task 1: Create NewsEditPage

- **Purpose**: Edit page reusing NewsForm. References `NM-VECINO-002-FE-T01`.
- **Artifacts impacted**:
  - `frontend/src/features/news/pages/NewsEditPage.tsx` (NEW)
  - `frontend/src/features/news/pages/NewsEditPage.test.tsx` (NEW)
  - `frontend/src/features/news/api/newsApi.ts` (UPDATE) — updateNews mutation
- **BDD Acceptance**:

```gherkin
Scenario: Form pre-populated with data
  Given I navigate to /noticias/:id/editar
  When page loads
  Then form is filled with current title and content

Scenario: Success shows toast
  Given I submit valid changes
  When API returns success
  Then I see toast "Cambios guardados"

Scenario: 403 redirects with message
  Given I try to edit someone else's draft
  When API returns 403
  Then I see "Solo los administradores pueden editar noticias publicadas"
```

---

### Task 2: Add Route

- **Purpose**: Register edit route. References `NM-VECINO-002-FE-T01`.
- **Artifacts impacted**:
  - `frontend/src/app/router/index.tsx` (UPDATE)

---

## 4) Definition of Done

- [ ] NewsEditPage fetches and pre-populates
- [ ] Reuses NewsForm component
- [ ] Error handling for 403/404
- [ ] Route registered
