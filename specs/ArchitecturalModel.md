# Architectural Model

This document describes the high-level architecture of the GAIA application.

## System Context (C4 Level 1)

```plantuml
@startuml C4_SystemContext
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Context.puml

title GAIA - System Context Diagram

Person(public, "Public Visitor", "Views published news")
Person(vecino, "Vecino (Neighbor)", "Creates drafts, views news")
Person(admin, "Administrator", "Full CRUD, publish/unpublish")

System(gaia, "GAIA", "Sistema de Gestión de Noticias Vecinales\nNeighborhood News Management System")

Rel(public, gaia, "Reads published news", "HTTPS")
Rel(vecino, gaia, "Creates/edits drafts", "HTTPS + JWT")
Rel(admin, gaia, "Manages all content", "HTTPS + JWT")

@enduml
```

---

## Container Diagram (C4 Level 2)

```plantuml
@startuml C4_Container
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Container.puml

title GAIA - Container Diagram

Person(user, "User", "Public/Vecino/Admin")

System_Boundary(gaia, "GAIA System") {
    Container(frontend, "Frontend SPA", "React, Vite, TanStack Query", "User interface")
    Container(backend, "Backend API", "FastAPI, Python 3.11+", "REST API, business logic")
    ContainerDb(database, "Database", "PostgreSQL 16", "Stores users, news")
}

Rel(user, frontend, "Uses", "HTTPS")
Rel(frontend, backend, "Calls", "HTTPS/JSON")
Rel(backend, database, "Reads/Writes", "PostgreSQL")

@enduml
```

---

## Backend Component Diagram (C4 Level 3)

The backend follows **Clean / Hexagonal Architecture** with strict layer dependencies:

```plantuml
@startuml C4_Component_Backend
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Component.puml

title GAIA Backend - Component Diagram

Container_Boundary(backend, "Backend API") {
    Component(presentation, "Presentation Layer", "FastAPI Routers, Pydantic DTOs", "HTTP handlers, request/response mapping")
    Component(application, "Application Layer", "Use Cases", "Business orchestration, transactions")
    Component(domain, "Domain Layer", "Entities, Repository Interfaces", "Core business logic, contracts")
    Component(infrastructure, "Infrastructure Layer", "SQLAlchemy, Adapters", "Database access, external services")
}

ContainerDb(database, "PostgreSQL", "Database")

Rel(presentation, application, "Calls")
Rel(application, domain, "Uses")
Rel(application, infrastructure, "Uses (via interfaces)")
Rel(infrastructure, domain, "Implements interfaces from")
Rel(infrastructure, database, "Reads/Writes")

@enduml
```

### Layer Rules

| Layer | Location | Dependencies | Forbidden |
|-------|----------|--------------|-----------|
| **Domain** | `backend/app/domain/` | None | Must not import from other layers |
| **Application** | `backend/app/application/` | Domain | Must not import infrastructure |
| **Infrastructure** | `backend/app/infrastructure/` | Domain, Application | - |
| **Presentation** | `backend/app/presentation/` | Domain (DTOs), Application | Must not import infrastructure |

---

## Database Layer

| Component | Technology | Configuration |
|-----------|------------|---------------|
| Database Engine | PostgreSQL 16 | Docker container `gaia-db` |
| Host Port | 5455 | Mapped to container 5432 |
| Migrations | Alembic | `backend/alembic/` |
| ORM | SQLAlchemy 2.x | Async support available |

### Connection Configuration

Database URL is configured via environment variable:
```
DATABASE_URL=postgresql://postgres:postgres@localhost:5455/gaia
```

For Docker-internal connections:
```
DATABASE_URL=postgresql://postgres:postgres@db:5432/gaia
```

---

## Authentication & Authorization

| Aspect | Implementation |
|--------|----------------|
| Authentication | JWT tokens (to be implemented in Auth feature) |
| Authorization | Role-Based Access Control (RBAC) |
| Roles | `PUBLIC`, `VECINO`, `ADMIN` |

---

## Infrastructure Services

| Service | Container Name | Port | Health Check |
|---------|---------------|------|--------------|
| PostgreSQL | `gaia-db` | 5455:5432 | `pg_isready` |
| Backend API | `gaia-backend` | 8005:8000 | `/health` endpoint |
