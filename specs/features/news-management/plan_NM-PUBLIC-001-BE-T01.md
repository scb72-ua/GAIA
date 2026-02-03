# NM-PUBLIC-001-BE-T01 — Implementation Plan

**Source ticket**: `specs/features/news-management/tickets.md` → **NM-PUBLIC-001-BE-T01**  
**Related user story**: **NM-PUBLIC-001** (from `specs/features/news-management/user-stories.md`)  
**Plan version**: v1.0 — (Claude, 2026-02-03T18:05:31+01:00)  
**Traceability**: All tasks must include inline references to `NM-PUBLIC-001-BE-T01` and `NM-PUBLIC-001` scenario names/tags.

---

## 1) Context & Objective

### Ticket Summary
Implement the `GET /api/v1/news` endpoint to list published news articles with pagination. This is the first backend endpoint for the News Management feature, enabling public visitors to browse community news.

### Impacted Entities/Tables
- `news` table (read-only)
- `users` table (join for author_name)

### Impacted Services/Modules
- `backend/app/domain/news/` — News entity, repository interface
- `backend/app/application/news/` — ListPublishedNewsUseCase
- `backend/app/infrastructure/news/` — SQLAlchemyNewsRepository
- `backend/app/presentation/news/` — Router, DTOs

### Impacted Tests or Business Flows
- `Scenario: Public visitor views news list`
- `Scenario: No published news available`
- `Scenario: Draft articles are not visible to public`
- `Scenario: News list loads within performance budget`

---

## 2) Scope

### In Scope
- `GET /api/v1/news` endpoint (public, no auth)
- Query params: `page` (default 1), `page_size` (default 10, max 50)
- Response: `{ items: [...], total: int, page: int, page_size: int }`
- Each item: `id`, `title`, `excerpt`, `author_name`, `published_at`
- Filter: only `status='published'`
- Sort: `published_at DESC`
- Empty list returns `{ items: [], total: 0, page: 1, page_size: 10 }`

### Out of Scope
- Search functionality
- Category/tag filtering
- Authentication (endpoint is public)

### Assumptions
- Database schema from NM-PUBLIC-001-DB-T01 is complete
- FastAPI app structure exists in `backend/app/main.py`

---

## 3) Detailed Work Plan (TDD + BDD)

### 3.1 Test-First Sequencing

1. **Unit tests** for `ListPublishedNewsUseCase` (mock repository)
2. **Integration tests** for `SQLAlchemyNewsRepository` (real DB)
3. **API tests** for `GET /api/v1/news` endpoint

### 3.2 NFR Hooks

#### Performance
- P95 < 300ms target
- Use DB index on `published_at DESC`
- Limit `page_size` to max 50

#### Observability
- Structured logging with `request_id`
- Log query execution time

---

## 4) Atomic Task Breakdown

### Task 1: Create News Domain Layer

- **Purpose**: Define the News entity and repository interface. References `NM-PUBLIC-001-BE-T01`.
- **Prerequisites**: Backend folder structure exists
- **Artifacts impacted**:
  - `backend/app/domain/news/entity.py` (NEW)
  - `backend/app/domain/news/repository.py` (NEW)
- **Test types**: None (interfaces only)

**Deliverables**:
```python
# backend/app/domain/news/entity.py
# [Feature: News Management] [Story: NM-PUBLIC-001] [Ticket: NM-PUBLIC-001-BE-T01]
@dataclass
class News:
    id: UUID
    title: str
    content: str
    excerpt: Optional[str]
    author_id: UUID
    author_name: str  # Denormalized for display
    status: str  # 'draft' | 'published'
    created_at: datetime
    updated_at: datetime
    published_at: Optional[datetime]

# backend/app/domain/news/repository.py
class NewsRepository(Protocol):
    def list_published(self, page: int, page_size: int) -> tuple[list[News], int]: ...
```

---

### Task 2: Create ListPublishedNewsUseCase

- **Purpose**: Implement business logic for listing published news. References `NM-PUBLIC-001-BE-T01`.
- **Artifacts impacted**:
  - `backend/app/application/news/list_published.py` (NEW)
  - `backend/tests/unit/test_list_published_news.py` (NEW)
- **Test types**: Unit tests (mock repository)
- **BDD Acceptance**:

```gherkin
Scenario: List published news with pagination
  Given the repository returns 5 published articles
  When I call ListPublishedNewsUseCase with page=1, page_size=10
  Then I receive a list of 5 articles
  And the total count is 5

Scenario: Empty list when no published news
  Given the repository returns 0 articles
  When I call ListPublishedNewsUseCase
  Then I receive an empty list
  And the total count is 0
```

---

### Task 3: Create SQLAlchemyNewsRepository

- **Purpose**: Implement repository with real database queries. References `NM-PUBLIC-001-BE-T01`.
- **Artifacts impacted**:
  - `backend/app/infrastructure/news/repository.py` (NEW)
  - `backend/app/infrastructure/news/models.py` (NEW) — SQLAlchemy model
  - `backend/tests/integration/test_news_repository.py` (NEW)
- **Test types**: Integration tests (real DB)
- **BDD Acceptance**:

```gherkin
Scenario: Only published articles returned
  Given 3 published and 2 draft articles in DB
  When I call repository.list_published()
  Then I receive only 3 articles
  And all articles have status='published'

Scenario: Articles sorted by published_at DESC
  Given 3 articles published at different times
  When I call repository.list_published()
  Then articles are ordered newest first
```

---

### Task 4: Create News Router and DTOs

- **Purpose**: Expose the API endpoint. References `NM-PUBLIC-001-BE-T01`.
- **Artifacts impacted**:
  - `backend/app/presentation/news/router.py` (NEW)
  - `backend/app/presentation/news/schemas.py` (NEW)
  - `backend/app/main.py` (UPDATE) — Mount router
  - `backend/tests/api/test_news_list.py` (NEW)
- **Test types**: API tests
- **BDD Acceptance**:

```gherkin
Scenario: GET /api/v1/news returns published articles
  Given 5 published articles exist
  When I GET /api/v1/news
  Then I receive 200 OK
  And response contains items array with 5 articles
  And each item has id, title, excerpt, author_name, published_at

Scenario: Pagination works correctly
  Given 25 published articles exist
  When I GET /api/v1/news?page=2&page_size=10
  Then I receive items for page 2
  And total equals 25

Scenario: Empty state returns empty array
  Given 0 published articles exist
  When I GET /api/v1/news
  Then I receive 200 OK
  And items is empty array
  And total equals 0
```

---

## 5) Verification Plan

```bash
# Run unit tests
cd backend
pytest tests/unit/test_list_published_news.py -v

# Run integration tests (requires DB)
docker compose up -d db
pytest tests/integration/test_news_repository.py -v

# Run API tests
pytest tests/api/test_news_list.py -v

# Manual verification
curl http://localhost:8005/api/v1/news | jq
```

---

## 6) Definition of Done

- [ ] Domain entity and repository interface created
- [ ] Use case implemented with unit tests
- [ ] Repository implemented with integration tests
- [ ] Router and DTOs created with API tests
- [ ] All tests pass
- [ ] P95 < 300ms verified
