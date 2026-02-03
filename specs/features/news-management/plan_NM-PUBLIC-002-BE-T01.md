# NM-PUBLIC-002-BE-T01 — Implementation Plan

**Source ticket**: `specs/features/news-management/tickets.md` → **NM-PUBLIC-002-BE-T01**  
**Related user story**: **NM-PUBLIC-002** (from `specs/features/news-management/user-stories.md`)  
**Plan version**: v1.0 — (Claude, 2026-02-03T18:05:31+01:00)  
**Traceability**: All tasks must include inline references to `NM-PUBLIC-002-BE-T01` and `NM-PUBLIC-002` scenario names/tags.

---

## 1) Context & Objective

### Ticket Summary
Implement the `GET /api/v1/news/{id}` endpoint to retrieve a single published news article. Draft articles must return 404 to prevent data leakage.

### Impacted Entities/Tables
- `news` table (read-only)
- `users` table (join for author_name)

### Impacted Services/Modules
- `backend/app/application/news/` — GetPublishedNewsDetailUseCase
- `backend/app/presentation/news/` — Router extension, NewsDetailDTO

### Impacted Tests or Business Flows
- `Scenario: Public visitor reads published article`
- `Scenario: Article does not exist`
- `Scenario: Draft article not accessible to public`
- `Scenario: Article detail loads within performance budget`

---

## 2) Scope

### In Scope
- `GET /api/v1/news/{id}` endpoint (public, no auth)
- Response: `id`, `title`, `content`, `author_name`, `published_at`
- Return 404 if article not found OR if `status != published`
- Security: Draft content MUST NOT be exposed in error response

### Out of Scope
- Related articles
- Comments

---

## 3) Detailed Work Plan (TDD + BDD)

### 3.1 Test-First Sequencing

1. **Unit tests** for `GetPublishedNewsDetailUseCase`
2. **Integration tests** for repository `get_by_id` method
3. **API tests** for endpoint

### 3.2 NFR Hooks

#### Performance
- P95 < 200ms target
- Use indexed lookup by `id`

#### Security
- 404 for both "not found" and "draft" (no information disclosure)

---

## 4) Atomic Task Breakdown

### Task 1: Add get_by_id to Repository

- **Purpose**: Extend repository interface. References `NM-PUBLIC-002-BE-T01`.
- **Artifacts impacted**:
  - `backend/app/domain/news/repository.py` (UPDATE)
  - `backend/app/infrastructure/news/repository.py` (UPDATE)
  - `backend/tests/integration/test_news_repository.py` (UPDATE)
- **BDD Acceptance**:

```gherkin
Scenario: Get published article by ID
  Given a published article with ID "abc123"
  When I call repository.get_published_by_id("abc123")
  Then I receive the article

Scenario: Draft article returns None
  Given a draft article with ID "draft123"
  When I call repository.get_published_by_id("draft123")
  Then I receive None

Scenario: Non-existent ID returns None
  Given no article with ID "nonexistent"
  When I call repository.get_published_by_id("nonexistent")
  Then I receive None
```

---

### Task 2: Create GetPublishedNewsDetailUseCase

- **Purpose**: Business logic for retrieving article detail. References `NM-PUBLIC-002-BE-T01`.
- **Artifacts impacted**:
  - `backend/app/application/news/get_detail.py` (NEW)
  - `backend/tests/unit/test_get_news_detail.py` (NEW)
- **BDD Acceptance**:

```gherkin
Scenario: Returns article when published
  Given repository returns a published article
  When I call use case
  Then I receive the article

Scenario: Raises NotFound when article is draft
  Given repository returns None (draft or missing)
  When I call use case
  Then NotFoundError is raised
```

---

### Task 3: Add Detail Endpoint

- **Purpose**: Expose GET /api/v1/news/{id}. References `NM-PUBLIC-002-BE-T01`.
- **Artifacts impacted**:
  - `backend/app/presentation/news/router.py` (UPDATE)
  - `backend/app/presentation/news/schemas.py` (UPDATE)
  - `backend/tests/api/test_news_detail.py` (NEW)
- **BDD Acceptance**:

```gherkin
Scenario: GET /api/v1/news/{id} returns article
  Given a published article exists
  When I GET /api/v1/news/{id}
  Then I receive 200 OK with full article

Scenario: 404 for non-existent article
  When I GET /api/v1/news/nonexistent
  Then I receive 404 Not Found

Scenario: 404 for draft article (no leak)
  Given a draft article exists
  When I GET /api/v1/news/{draft_id}
  Then I receive 404 Not Found
  And response does not contain draft content
```

---

## 5) Verification Plan

```bash
# Run tests
pytest tests/unit/test_get_news_detail.py -v
pytest tests/integration/test_news_repository.py -v
pytest tests/api/test_news_detail.py -v

# Manual verification
curl http://localhost:8005/api/v1/news/{valid_id} | jq
curl http://localhost:8005/api/v1/news/invalid-id  # Should return 404
```

---

## 6) Definition of Done

- [ ] Repository extended with `get_published_by_id`
- [ ] Use case implemented with unit tests
- [ ] API endpoint created with tests
- [ ] 404 returned for drafts (no data leak)
- [ ] P95 < 200ms verified
