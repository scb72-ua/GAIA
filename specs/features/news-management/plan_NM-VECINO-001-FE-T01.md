# NM-VECINO-001-FE-T01 — Implementation Plan

**Source ticket**: `specs/features/news-management/tickets.md` → **NM-VECINO-001-FE-T01**  
**Related user story**: **NM-VECINO-001** (from `specs/features/news-management/user-stories.md`)  
**Plan version**: v1.0 — (Claude, 2026-02-03T18:05:31+01:00)  
**Traceability**: All tasks must include inline references to `NM-VECINO-001-FE-T01` and `NM-VECINO-001` scenario names/tags.

---

## 1) Context & Objective

### Ticket Summary
Implement the news creation form for authenticated neighbors. This is the first protected frontend page requiring auth guards.

### Impacted Services/Modules
- `frontend/src/features/news/pages/` — NewsCreatePage
- `frontend/src/features/news/components/` — NewsForm
- `frontend/src/app/router/` — Protected route

### Impacted Tests or Business Flows
- `Scenario: Neighbor creates a news draft`
- `Scenario: Draft requires title and content`
- `Scenario: Public visitor cannot access creation form`

---

## 2) Scope

### In Scope
- Route: `/noticias/nueva` (protected: VECINO or ADMIN)
- Redirect to login if unauthenticated
- Form fields: title (required), content textarea (required)
- Client-side validation with Zod
- Submit via `useMutation`
- Success: toast "Noticia guardada como borrador", redirect
- Error handling: display validation errors

### Out of Scope
- Rich text editor (MVP uses textarea)
- Image upload

---

## 3) Detailed Work Plan (TDD + BDD)

### 3.1 NFR Hooks

#### Accessibility
- Labels above inputs
- Error announcements for screen readers

#### Connectivity & Routing
- Entry: From navigation "Nueva Noticia" button (visible to VECINO/ADMIN)
- Exit: On success → `/noticias` or `/noticias/:id`

---

## 4) Atomic Task Breakdown

### Task 1: Create NewsForm Component

- **Purpose**: Reusable form for create/edit. References `NM-VECINO-001-FE-T01`.
- **Artifacts impacted**:
  - `frontend/src/features/news/components/NewsForm.tsx` (NEW)
  - `frontend/src/features/news/components/NewsForm.test.tsx` (NEW)
  - `frontend/src/features/news/schemas/newsSchema.ts` (NEW) — Zod schema
- **BDD Acceptance**:

```gherkin
Scenario: Form validates required fields
  Given empty form
  When I submit
  Then I see error "El título es obligatorio"
  And I see error "El contenido es obligatorio"

Scenario: Form submits valid data
  Given title and content filled
  When I submit
  Then onSubmit is called with form data
```

---

### Task 2: Create NewsCreatePage

- **Purpose**: Protected page for creating news. References `NM-VECINO-001-FE-T01`.
- **Artifacts impacted**:
  - `frontend/src/features/news/pages/NewsCreatePage.tsx` (NEW)
  - `frontend/src/features/news/pages/NewsCreatePage.test.tsx` (NEW)
  - `frontend/src/features/news/api/newsApi.ts` (UPDATE) — createNews mutation
- **BDD Acceptance**:

```gherkin
Scenario: Authenticated user can create
  Given I am logged in as VECINO
  When I navigate to /noticias/nueva
  Then I see the news creation form

Scenario: Success shows toast and redirects
  Given I submit valid form
  When API returns success
  Then I see toast "Noticia guardada como borrador"
  And I am redirected to /noticias
```

---

### Task 3: Add Protected Route

- **Purpose**: Guard route for authenticated users. References `NM-VECINO-001-FE-T01`.
- **Artifacts impacted**:
  - `frontend/src/app/router/index.tsx` (UPDATE)
  - `frontend/src/app/router/ProtectedRoute.tsx` (NEW or UPDATE)
- **BDD Acceptance**:

```gherkin
Scenario: Unauthenticated redirected to login
  Given I am not logged in
  When I navigate to /noticias/nueva
  Then I am redirected to /login

Scenario: PUBLIC role denied
  Given I am logged in as PUBLIC
  When I navigate to /noticias/nueva
  Then I am redirected or shown access denied
```

---

## 5) Definition of Done

- [ ] NewsForm with Zod validation
- [ ] NewsCreatePage with mutation
- [ ] Protected route configured
- [ ] Success toast and redirect work
- [ ] A11y: Labels above inputs
