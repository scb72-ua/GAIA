# NM-PUBLIC-001-DB-T01 — Implementation Plan

**Source ticket**: `specs/features/news-management/tickets.md` → **NM-PUBLIC-001-DB-T01**  
**Related user story**: **NM-PUBLIC-001** (from `specs/features/news-management/user-stories.md`)  
**Plan version**: v1.0 — (Claude, 2026-02-03T18:02:12+01:00)  
**Traceability**: All tasks must include inline references to `NM-PUBLIC-001-DB-T01` and, where relevant, `NM-PUBLIC-001` scenario names/tags.

---

## 1) Context & Objective

### Ticket Summary
Create the `news` table in PostgreSQL with all required columns to support the full news lifecycle (draft → published). This is the **foundational database ticket** for the News Management feature — all backend and frontend tickets depend on this schema being in place.

### Impacted Entities/Tables
- **NEW**: `news` table
- **REFERENCED**: `users` table (FK constraint for `author_id`) — *assumed to exist from Auth feature*

### Impacted Services/Modules
- `backend/alembic/` — Migration scripts
- `specs/DataModel.md` — ERD documentation (to be created)

### Impacted Tests or Business Flows
This ticket provides the data foundation for all NM-PUBLIC-001 scenarios:
- `Scenario: Public visitor views news list` — requires published news rows
- `Scenario: No published news available` — requires empty table or draft-only rows
- `Scenario: Draft articles are not visible to public` — requires `status` column with ENUM values

---

## 2) Scope

### In Scope
- Create `news` table with columns:
  - `id` (UUID, PK, default `gen_random_uuid()`)
  - `title` (VARCHAR(255), NOT NULL)
  - `content` (TEXT, NOT NULL)
  - `excerpt` (VARCHAR(500), nullable)
  - `author_id` (UUID, FK to `users.id`, NOT NULL)
  - `status` (VARCHAR(20), CHECK constraint: 'draft' | 'published', default 'draft')
  - `created_at` (TIMESTAMPTZ, NOT NULL, default NOW())
  - `updated_at` (TIMESTAMPTZ, NOT NULL, default NOW())
  - `published_at` (TIMESTAMPTZ, nullable)
- Create indexes:
  - `idx_news_published_at_desc` on `(published_at DESC NULLS LAST)` for list queries
  - `idx_news_status` on `(status)` for filtering
- FK constraint: `news.author_id` → `users.id` (ON DELETE RESTRICT)
- Reversible Alembic migration (upgrade + downgrade)

### Out of Scope
- Seed data (separate ticket if needed)
- SQLAlchemy ORM model (covered in NM-PUBLIC-001-BE-T01)
- API endpoints (covered in NM-PUBLIC-001-BE-T01)

### Assumptions
1. **Users table exists** — The Auth feature has created the `users` table with `id` (UUID PK). If not, this ticket will need to create a minimal users table first.
2. **PostgreSQL 14+** — Using `gen_random_uuid()` for UUID generation.
3. **Alembic is configured** — `backend/alembic/` structure exists with proper `alembic.ini` and `env.py`.
4. **docker-compose.yml exists** — Container infrastructure is in place.

### Open Questions
1. **Users table status?** — Does the users table exist? If not, should this ticket create a minimal version?
2. **Soft delete?** — The ticket specifies hard delete later, but should we add `deleted_at` column now for future soft-delete capability?

> **NOTE**: Given the project is greenfield, this plan assumes we must first set up the containerized environment (docker-compose.yml) and Alembic configuration before running migrations.

---

## 3) Detailed Work Plan (TDD + BDD)

### 3.0 Prerequisites Check

Before any database work, verify the containerized environment is ready:

1. **Docker Compose Check**: Verify `docker-compose.yml` exists with PostgreSQL service
2. **Start containers**: `docker compose up -d`
3. **Health check**: `docker compose ps` — PostgreSQL must be `healthy`
4. **Alembic setup**: Verify `backend/alembic/` exists with proper config

> ⚠️ **STOP if any prerequisite fails**. The infrastructure must be created first.

### 3.1 Test-First Sequencing

Since this is a DB-only ticket, the "tests" are:
1. **Migration executes successfully** (upgrade)
2. **Rollback works** (downgrade)
3. **Schema matches specification** (columns, types, constraints, indexes)

These will be verified via:
- Alembic commands (`alembic upgrade head`, `alembic downgrade -1`)
- SQL introspection queries

### 3.2 NFR Hooks

#### Security/Privacy
- `author_id` FK ensures news is always linked to a valid user
- No PII stored directly in news table (author info via FK join)
- ON DELETE RESTRICT prevents orphaned news if users are deleted

#### Performance
- Index `idx_news_published_at_desc` optimizes `ORDER BY published_at DESC` queries (expected P95 < 300ms)
- Index `idx_news_status` optimizes `WHERE status = 'published'` filtering

#### Observability
- Alembic migration creates audit trail via version table
- `created_at`, `updated_at`, `published_at` timestamps enable lifecycle tracking

---

## 4) Atomic Task Breakdown

### Task 1: Create Project Infrastructure (if needed)

- **Purpose**: Ensure the containerized environment exists before any DB work. References `NM-PUBLIC-001-DB-T01` prerequisite.
- **Prerequisites**: None (first task)
- **Artifacts impacted**:
  - `docker-compose.yml` (NEW if not exists)
  - `backend/` directory structure (NEW if not exists)
  - `backend/alembic/` configuration (NEW if not exists)
- **Test types**: Manual verification
- **BDD Acceptance**:

```gherkin
Given the repository root directory
When I run `docker compose ps`
Then I see a PostgreSQL container in "healthy" state
And the database is accessible on port 5455 (host) / 5432 (container)
```

**Deliverables**:
```
docker-compose.yml (if not exists):
  - db service: postgres:16-alpine
  - ports: "5455:5432"
  - environment: POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB
  - healthcheck configured
  
backend/
  ├── alembic/
  │   ├── versions/        # Migration scripts
  │   ├── env.py           # Alembic environment config
  │   └── script.py.mako   # Migration template
  ├── alembic.ini          # Alembic config pointing to DB URL
  └── app/
      └── core/
          └── config.py    # Database settings (if not exists)
```

---

### Task 2: Create Users Table (if not exists)

- **Purpose**: The `news.author_id` FK requires a `users` table. This is a minimal stub if Auth feature hasn't created it yet. References `NM-PUBLIC-001-DB-T01` dependency.
- **Prerequisites**: Task 1 complete (docker-compose up, Alembic configured)
- **Artifacts impacted**:
  - `backend/alembic/versions/YYYYMMDD_HHMM_create_users_table.py` (NEW, if needed)
  - `specs/DataModel.md` (NEW/UPDATE)
- **Test types**: Migration verification
- **BDD Acceptance**:

```gherkin
Given the database has no users table
When I run `alembic upgrade head`
Then the users table is created with:
  | column     | type         | constraints |
  | id         | UUID         | PK, default gen_random_uuid() |
  | email      | VARCHAR(255) | UNIQUE, NOT NULL |
  | name       | VARCHAR(255) | NOT NULL |
  | role       | VARCHAR(20)  | CHECK: 'PUBLIC'|'VECINO'|'ADMIN', default 'VECINO' |
  | created_at | TIMESTAMPTZ  | NOT NULL, default NOW() |
```

> **NOTE**: This is a minimal stub. The full Auth feature will extend this table.

---

### Task 3: Create News Table Migration

- **Purpose**: Create the core `news` table as specified in `NM-PUBLIC-001-DB-T01`. This is the primary deliverable of this ticket.
- **Prerequisites**: Task 1 and Task 2 complete (users table exists)
- **Artifacts impacted**:
  - `backend/alembic/versions/YYYYMMDD_HHMM_create_news_table.py` (NEW)
- **Test types**: Migration verification (upgrade + downgrade)
- **BDD Acceptance**:

```gherkin
# Scenario: Migration creates news table
Given the database has the users table
When I run `alembic upgrade head`
Then the news table is created with:
  | column       | type          | constraints                              |
  | id           | UUID          | PK, default gen_random_uuid()            |
  | title        | VARCHAR(255)  | NOT NULL                                 |
  | content      | TEXT          | NOT NULL                                 |
  | excerpt      | VARCHAR(500)  | nullable                                 |
  | author_id    | UUID          | FK → users.id, NOT NULL, ON DELETE RESTRICT |
  | status       | VARCHAR(20)   | CHECK: 'draft'|'published', default 'draft' |
  | created_at   | TIMESTAMPTZ   | NOT NULL, default NOW()                  |
  | updated_at   | TIMESTAMPTZ   | NOT NULL, default NOW()                  |
  | published_at | TIMESTAMPTZ   | nullable                                 |

# Scenario: Migration creates indexes
Given the news table exists
Then the following indexes exist:
  | index name                  | columns                        |
  | idx_news_published_at_desc  | (published_at DESC NULLS LAST) |
  | idx_news_status             | (status)                       |
  | idx_news_author_id          | (author_id)                    |

# Scenario: Migration is reversible
Given the news table exists
When I run `alembic downgrade -1`
Then the news table is dropped
And the indexes are dropped
```

**Migration script structure**:
```python
# [Feature: News Management] [Story: NM-PUBLIC-001] [Ticket: NM-PUBLIC-001-DB-T01]
def upgrade():
    op.create_table(
        'news',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('content', sa.Text, nullable=False),
        sa.Column('excerpt', sa.String(500), nullable=True),
        sa.Column('author_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='RESTRICT'), nullable=False),
        sa.Column('status', sa.String(20), nullable=False, server_default='draft'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('published_at', sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint("status IN ('draft', 'published')", name='ck_news_status'),
    )
    op.create_index('idx_news_published_at_desc', 'news', [sa.text('published_at DESC NULLS LAST')])
    op.create_index('idx_news_status', 'news', ['status'])
    op.create_index('idx_news_author_id', 'news', ['author_id'])

def downgrade():
    op.drop_index('idx_news_author_id', table_name='news')
    op.drop_index('idx_news_status', table_name='news')
    op.drop_index('idx_news_published_at_desc', table_name='news')
    op.drop_table('news')
```

---

### Task 4: Update DataModel.md

- **Purpose**: Document the new schema in the specs directory. References `NM-PUBLIC-001-DB-T01` deliverable.
- **Prerequisites**: Task 3 complete (news table created)
- **Artifacts impacted**:
  - `specs/DataModel.md` (NEW or UPDATE)
- **Test types**: None (documentation)
- **BDD Acceptance**:

```gherkin
Given Task 3 is complete
When I view specs/DataModel.md
Then I see the news table documented with:
  - All columns, types, and constraints
  - Relationship to users table
  - Mermaid ER diagram showing news ↔ users relationship
```

**DataModel.md structure**:
```markdown
# Data Model

## Entity Relationship Diagram

​```mermaid
erDiagram
    USERS ||--o{ NEWS : "authors"
    
    USERS {
        uuid id PK
        string email UK
        string name
        string role
        timestamptz created_at
    }
    
    NEWS {
        uuid id PK
        string title
        text content
        string excerpt
        uuid author_id FK
        string status
        timestamptz created_at
        timestamptz updated_at
        timestamptz published_at
    }
​```

## Tables

### users
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK, default gen_random_uuid() | Unique identifier |
| ... | ... | ... | ... |

### news
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK, default gen_random_uuid() | Unique identifier |
| title | VARCHAR(255) | NOT NULL | News headline |
| content | TEXT | NOT NULL | Full article content |
| excerpt | VARCHAR(500) | nullable | Auto-generated preview (first 200 chars) |
| author_id | UUID | FK → users.id, NOT NULL | Article author |
| status | VARCHAR(20) | CHECK: draft/published, default 'draft' | Publication status |
| created_at | TIMESTAMPTZ | NOT NULL, default NOW() | Creation timestamp |
| updated_at | TIMESTAMPTZ | NOT NULL, default NOW() | Last update timestamp |
| published_at | TIMESTAMPTZ | nullable | When article was published |

### Indexes
| Table | Index Name | Columns | Purpose |
|-------|------------|---------|---------|
| news | idx_news_published_at_desc | (published_at DESC NULLS LAST) | Optimize list queries |
| news | idx_news_status | (status) | Filter by status |
| news | idx_news_author_id | (author_id) | FK lookup optimization |
```

---

### Task 5: Update ArchitecturalModel.md

- **Purpose**: Document the database component in the architecture. References `NM-PUBLIC-001-DB-T01`.
- **Prerequisites**: Task 4 complete
- **Artifacts impacted**:
  - `specs/ArchitecturalModel.md` (NEW or UPDATE)
- **Test types**: None (documentation)
- **BDD Acceptance**:

```gherkin
Given Task 4 is complete
When I view specs/ArchitecturalModel.md
Then I see the database layer documented with:
  - PostgreSQL as the database
  - Alembic for migrations
  - Connection details from environment variables
```

---

## 5) Verification Plan

### Automated Verification

```bash
# 1. Start database container
cd /home/sebas/UA/GCS/GAIA
docker compose up -d db
docker compose ps  # Verify "healthy" status

# 2. Run migrations
cd backend
alembic upgrade head

# 3. Verify tables exist
docker compose exec db psql -U postgres -d gaia -c "\dt"
# Expected: users, news tables listed

# 4. Verify news table schema
docker compose exec db psql -U postgres -d gaia -c "\d news"
# Expected: All columns with correct types and constraints

# 5. Verify indexes
docker compose exec db psql -U postgres -d gaia -c "\di"
# Expected: idx_news_published_at_desc, idx_news_status, idx_news_author_id

# 6. Test rollback
alembic downgrade -1
docker compose exec db psql -U postgres -d gaia -c "\dt"
# Expected: news table NOT listed

# 7. Re-apply migration
alembic upgrade head
```

### Manual Verification (for user)

1. **Check docker-compose.yml** — Database service is defined with health check
2. **Check migration file** — `backend/alembic/versions/*_create_news_table.py` exists
3. **Check DataModel.md** — ERD diagram renders correctly
4. **Check ArchitecturalModel.md** — Database layer documented

---

## 6) Definition of Done

- [ ] `docker-compose.yml` exists with PostgreSQL service
- [ ] `backend/alembic/` is configured and working
- [ ] Users table migration exists (if not present from Auth feature)
- [ ] News table migration created with all columns, constraints, and indexes
- [ ] Migration is reversible (downgrade tested)
- [ ] `specs/DataModel.md` updated with news table ERD
- [ ] `specs/ArchitecturalModel.md` updated with database layer
- [ ] Ticket marked as complete in `tickets.md`
