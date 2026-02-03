# NM-ADMIN-001-BE-T01 — Implementation Plan

**Source ticket**: `specs/features/news-management/tickets.md` → **NM-ADMIN-001-BE-T01**  
**Related user story**: **NM-ADMIN-001** (from `specs/features/news-management/user-stories.md`)  
**Plan version**: v1.0 — (Claude, 2026-02-03T18:05:31+01:00)  
**Traceability**: All tasks must include inline references to `NM-ADMIN-001-BE-T01` and `NM-ADMIN-001` scenario names/tags.

---

## 1) Context & Objective

### Ticket Summary
Implement the `POST /api/v1/news/{id}/publish` endpoint for Admins to publish draft articles. This completes the news publication workflow.

### Impacted Entities/Tables
- `news` table (update status, published_at)

### Impacted Services/Modules
- `backend/app/application/news/` — PublishNewsUseCase
- `backend/app/presentation/news/` — Router extension

### Impacted Tests or Business Flows
- `Scenario: Admin publishes a draft`
- `Scenario: Vecino cannot publish articles`
- `Scenario: Unauthenticated user cannot publish`
- `Scenario: Article is already published`
- `Scenario: Publication is audited`

---

## 2) Scope

### In Scope
- `POST /api/v1/news/{id}/publish` (requires auth: ADMIN only)
- Change `status` to `published`, set `published_at=now`
- 403 for non-admin roles
- 401 for unauthenticated
- 400 if already published
- 404 if article not found
- Audit log: `news.published` event

### Out of Scope
- Scheduled publishing

---

## 3) Atomic Task Breakdown

### Task 1: Create PublishNewsUseCase

- **Purpose**: Business logic for publishing. References `NM-ADMIN-001-BE-T01`.
- **Artifacts impacted**:
  - `backend/app/application/news/publish.py` (NEW)
  - `backend/tests/unit/test_publish_news.py` (NEW)
- **BDD Acceptance**:

```gherkin
Scenario: Publish draft article
  Given a draft article exists
  When admin calls PublishNewsUseCase
  Then status changes to 'published'
  And published_at is set to now
  And audit event 'news.published' is logged

Scenario: Already published returns error
  Given a published article exists
  When admin calls PublishNewsUseCase
  Then AlreadyPublishedError is raised
```

---

### Task 2: Add Publish Endpoint

- **Purpose**: Expose admin-only publish action. References `NM-ADMIN-001-BE-T01`.
- **Artifacts impacted**:
  - `backend/app/presentation/news/router.py` (UPDATE)
  - `backend/tests/api/test_news_publish.py` (NEW)
- **BDD Acceptance**:

```gherkin
Scenario: POST /api/v1/news/{id}/publish works for admin
  Given I am authenticated as ADMIN
  And a draft article exists
  When I POST /api/v1/news/{id}/publish
  Then I receive 200 OK
  And article is now published

Scenario: 403 for VECINO
  Given I am authenticated as VECINO
  When I POST /api/v1/news/{id}/publish
  Then I receive 403 Forbidden

Scenario: 400 if already published
  Given article is already published
  When I POST /api/v1/news/{id}/publish
  Then I receive 400 with message "La noticia ya está publicada"
```

---

## 4) Definition of Done

- [ ] PublishNewsUseCase with tests
- [ ] API endpoint with admin-only RBAC
- [ ] 400 for already-published cases
- [ ] Audit log verified
