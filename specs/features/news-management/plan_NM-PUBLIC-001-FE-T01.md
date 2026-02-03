# NM-PUBLIC-001-FE-T01 — Implementation Plan

**Source ticket**: `specs/features/news-management/tickets.md` → **NM-PUBLIC-001-FE-T01**  
**Related user story**: **NM-PUBLIC-001** (from `specs/features/news-management/user-stories.md`)  
**Plan version**: v1.0 — (Claude, 2026-02-03T18:05:31+01:00)  
**Traceability**: All tasks must include inline references to `NM-PUBLIC-001-FE-T01` and `NM-PUBLIC-001` scenario names/tags.

---

## 1) Context & Objective

### Ticket Summary
Implement the public news list page with pagination, empty state, and loading skeleton. This is the first UI component for the News Management feature, allowing visitors to browse published community news.

### Impacted Entities/Tables
- None (frontend only)

### Impacted Services/Modules
- `frontend/src/features/news/` — New feature module
- `frontend/src/app/router/` — Route registration

### Impacted Tests or Business Flows
- `Scenario: Public visitor views news list`
- `Scenario: No published news available`
- `Scenario: News list is accessible`

---

## 2) Scope

### In Scope
- Route: `/noticias`
- `useQuery` hook for fetching news list
- `NewsList` component with card layout
- `NewsCard` component showing: title, excerpt, author name, publication date (DD/MM/YYYY)
- Empty state: "No hay noticias publicadas"
- Loading skeleton during fetch
- Pagination controls
- Link to detail page for each article

### Out of Scope
- Search bar
- Category filters
- Admin-only features

### NFR Requirements
- **A11y**: Semantic `<main>` landmark, heading hierarchy (h2/h3), keyboard navigable
- **i18n**: UI strings in Spanish (Castilian)
- **Brand**: Use design tokens from brand-guidelines.md

---

## 3) Detailed Work Plan (TDD + BDD)

### 3.1 Test-First Sequencing

1. Write component tests for `NewsCard`
2. Write component tests for `NewsList`
3. Write page tests for `NewsListPage`
4. Implement components to pass tests

### 3.2 NFR Hooks

#### Accessibility
- Use semantic HTML (`<main>`, `<article>`, `<h2>`)
- Ensure keyboard navigation
- Use proper ARIA labels

#### Brand & Visuals
- Use Tailwind + shadcn/ui
- Follow brand color tokens
- Consistent spacing (space-y-4)

#### Connectivity & Routing
- Entry: From header navigation "Noticias"
- Exit: Click on card → `/noticias/:id`

---

## 4) Atomic Task Breakdown

### Task 1: Create News Feature Structure

- **Purpose**: Set up the news feature module. References `NM-PUBLIC-001-FE-T01`.
- **Artifacts impacted**:
  - `frontend/src/features/news/` (NEW directory)
  - `frontend/src/features/news/types.ts` (NEW)
  - `frontend/src/features/news/api/newsApi.ts` (NEW)

**Deliverables**:
```typescript
// frontend/src/features/news/types.ts
// [Feature: News Management] [Story: NM-PUBLIC-001] [Ticket: NM-PUBLIC-001-FE-T01]
export interface NewsListItem {
  id: string;
  title: string;
  excerpt: string;
  author_name: string;
  published_at: string;
}

export interface NewsListResponse {
  items: NewsListItem[];
  total: number;
  page: number;
  page_size: number;
}
```

---

### Task 2: Create NewsCard Component

- **Purpose**: Reusable card for displaying news in lists. References `NM-PUBLIC-001-FE-T01`.
- **Artifacts impacted**:
  - `frontend/src/features/news/components/NewsCard.tsx` (NEW)
  - `frontend/src/features/news/components/NewsCard.test.tsx` (NEW)
- **Test types**: Component tests (Vitest + RTL)
- **BDD Acceptance**:

```gherkin
Scenario: NewsCard displays all required fields
  Given a news item with title, excerpt, author, and date
  When I render NewsCard
  Then I see the title as a heading
  And I see the excerpt text
  And I see the author name
  And I see the date formatted as DD/MM/YYYY
  And the card links to /noticias/:id
```

---

### Task 3: Create NewsList Component

- **Purpose**: List container with empty and loading states. References `NM-PUBLIC-001-FE-T01`.
- **Artifacts impacted**:
  - `frontend/src/features/news/components/NewsList.tsx` (NEW)
  - `frontend/src/features/news/components/NewsList.test.tsx` (NEW)
- **Test types**: Component tests
- **BDD Acceptance**:

```gherkin
Scenario: NewsList renders cards for each item
  Given 5 news items
  When I render NewsList
  Then I see 5 NewsCard components

Scenario: NewsList shows empty state
  Given 0 news items
  When I render NewsList
  Then I see "No hay noticias publicadas"

Scenario: NewsList shows loading skeleton
  Given data is loading
  When I render NewsList with isLoading=true
  Then I see skeleton placeholders
```

---

### Task 4: Create NewsListPage

- **Purpose**: Page component with data fetching. References `NM-PUBLIC-001-FE-T01`.
- **Artifacts impacted**:
  - `frontend/src/features/news/pages/NewsListPage.tsx` (NEW)
  - `frontend/src/features/news/pages/NewsListPage.test.tsx` (NEW)
  - `frontend/src/app/router/index.tsx` (UPDATE)
- **Test types**: Component tests with mocked API
- **BDD Acceptance**:

```gherkin
Scenario: Page fetches and displays news
  Given the API returns 5 published articles
  When I navigate to /noticias
  Then I see the news list with 5 cards

Scenario: Page is accessible
  Given I am using a screen reader
  When I navigate to /noticias
  Then the page has a main landmark
  And articles have proper heading structure
```

---

### Task 5: Add Route and Navigation

- **Purpose**: Register route and add navigation link. References `NM-PUBLIC-001-FE-T01`.
- **Artifacts impacted**:
  - `frontend/src/app/router/index.tsx` (UPDATE)
  - Navigation component (UPDATE if exists)

---

## 5) Verification Plan

```bash
# Run component tests
cd frontend
npm run test -- --filter news

# Run in browser
npm run dev
# Navigate to http://localhost:5188/noticias

# Accessibility check
# Use browser DevTools Lighthouse or axe extension
```

---

## 6) Definition of Done

- [ ] News feature module created
- [ ] NewsCard component with tests
- [ ] NewsList component with tests
- [ ] NewsListPage with data fetching
- [ ] Route registered at `/noticias`
- [ ] Empty state displays correctly
- [ ] Loading skeleton displays correctly
- [ ] A11y requirements met (semantic HTML, keyboard nav)
- [ ] UI strings in Spanish
