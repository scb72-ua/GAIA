# NM-PUBLIC-002-FE-T01 — Implementation Plan

**Source ticket**: `specs/features/news-management/tickets.md` → **NM-PUBLIC-002-FE-T01**  
**Related user story**: **NM-PUBLIC-002** (from `specs/features/news-management/user-stories.md`)  
**Plan version**: v1.0 — (Claude, 2026-02-03T18:05:31+01:00)  
**Traceability**: All tasks must include inline references to `NM-PUBLIC-002-FE-T01` and `NM-PUBLIC-002` scenario names/tags.

---

## 1) Context & Objective

### Ticket Summary
Implement the news article detail page with full content display, proper error handling for 404, and accessibility compliance.

### Impacted Services/Modules
- `frontend/src/features/news/pages/` — NewsDetailPage
- `frontend/src/features/news/components/` — NewsArticle
- `frontend/src/app/router/` — Route registration

### Impacted Tests or Business Flows
- `Scenario: Public visitor reads published article`
- `Scenario: Article does not exist`
- `Scenario: Article detail is accessible`

---

## 2) Scope

### In Scope
- Route: `/noticias/:id`
- `useQuery` hook for fetching article detail
- Display: title (h1), content, author, publication date
- Back link to news list
- 404 error page: "Noticia no encontrada"
- Loading skeleton

### Out of Scope
- Share buttons
- Comments section

---

## 3) Detailed Work Plan (TDD + BDD)

### 3.1 NFR Hooks

#### Accessibility
- Single `<h1>` for title
- Semantic HTML (`<article>`, `<p>`)
- Focus management on page load

#### Connectivity & Routing
- Entry: From news list card click
- Exit: Back link to `/noticias`

---

## 4) Atomic Task Breakdown

### Task 1: Create NewsArticle Component

- **Purpose**: Display full article content. References `NM-PUBLIC-002-FE-T01`.
- **Artifacts impacted**:
  - `frontend/src/features/news/components/NewsArticle.tsx` (NEW)
  - `frontend/src/features/news/components/NewsArticle.test.tsx` (NEW)
- **BDD Acceptance**:

```gherkin
Scenario: NewsArticle displays full content
  Given article data with title, content, author, date
  When I render NewsArticle
  Then I see title as h1
  And I see full content in paragraphs
  And I see author name
  And I see date formatted DD/MM/YYYY
```

---

### Task 2: Create NewsDetailPage

- **Purpose**: Page with data fetching and error handling. References `NM-PUBLIC-002-FE-T01`.
- **Artifacts impacted**:
  - `frontend/src/features/news/pages/NewsDetailPage.tsx` (NEW)
  - `frontend/src/features/news/pages/NewsDetailPage.test.tsx` (NEW)
  - `frontend/src/features/news/api/newsApi.ts` (UPDATE)
- **BDD Acceptance**:

```gherkin
Scenario: Page displays article
  Given API returns article data
  When I navigate to /noticias/:id
  Then I see the full article

Scenario: Page shows 404 error
  Given API returns 404
  When I navigate to /noticias/invalid
  Then I see "Noticia no encontrada"

Scenario: Page shows loading state
  Given API is pending
  When I navigate to /noticias/:id
  Then I see loading skeleton
```

---

### Task 3: Add Route

- **Purpose**: Register route for detail page. References `NM-PUBLIC-002-FE-T01`.
- **Artifacts impacted**:
  - `frontend/src/app/router/index.tsx` (UPDATE)

---

## 5) Verification Plan

```bash
# Run tests
npm run test -- --filter NewsDetail

# Manual verification
npm run dev
# Navigate to article from list
# Test with invalid ID for 404
```

---

## 6) Definition of Done

- [ ] NewsArticle component with tests
- [ ] NewsDetailPage with data fetching
- [ ] Route registered at `/noticias/:id`
- [ ] 404 page displays correctly
- [ ] Loading skeleton works
- [ ] A11y: Single h1, semantic HTML
