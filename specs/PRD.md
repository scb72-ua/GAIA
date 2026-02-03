# Sistema de Gestión de Noticias Vecinales

## Visión de Producto

Sistema web full-stack para una **asociación vecinal informal** que permite:
- Informar a los vecinos mediante noticias
- Anunciar eventos comunitarios
- Levantar incidencias del barrio
- Gestionar contenido de forma simple por administradores

### Usuarios
- **Público**: lee noticias sin autenticación
- **Vecino**: lector + creador de contenido (noticias en borrador)
- **Admin**: crea, edita, modera y publica noticias

### Stack Técnico
- Frontend: React
- Backend: FastAPI
- Base de datos: PostgreSQL

---

## Features

### 1. News Management (Gestión de Noticias)

A centralized web portal for neighborhood news and announcements.

> **Full Spec:** [feature-descr.md](file:///home/sebas/UA/GCS/GAIA/specs/features/news-management/feature-descr.md)

#### 1.1 Actors (Roles)

| Role | Code | Description |
|------|------|-------------|
| Public Visitor | `PUBLIC` | Unauthenticated user. Can read published news. |
| Neighbor | `VECINO` | Registered resident. Can read + create news drafts. |
| Administrator | `ADMIN` | Elevated neighbor. Full CRUD + publish/unpublish. |

#### 1.2 Access Levels

| Action | Public | Vecino | Admin |
|--------|--------|--------|-------|
| View published news list | ✅ | ✅ | ✅ |
| View news detail | ✅ | ✅ | ✅ |
| Create news draft | ❌ | ✅ | ✅ |
| Edit own draft (before publish) | ❌ | ✅ | ✅ |
| Edit any news | ❌ | ❌ | ✅ |
| Publish/Unpublish news | ❌ | ❌ | ✅ |
| Delete news | ❌ | ❌ | ✅ |

#### 1.3 Requirements & Constraints

- **Security:** TLS required; JWT authentication; bcrypt/argon2 password hashing
- **RBAC:** Enforced at API level (no frontend-only checks)
- **Performance:** News list P95 < 300ms; detail P95 < 200ms
- **Accessibility:** WCAG 2.1 AA target
- **Audit:** Log creation, publication, deletion events with user ID

---

## Historias de Usuario (MVP)

### HU-1 Listado de noticias
Como visitante público,  
quiero ver una lista de noticias publicadas,  
para mantenerme informado de lo que ocurre en el barrio.

**Criterios de aceptación**
- Solo se muestran noticias publicadas
- Ordenadas por fecha descendente
- No requiere login

---

### HU-2 Crear noticia (borrador)
Como vecino autenticado,  
quiero crear una noticia en borrador,  
para compartir información con la comunidad.

**Criterios de aceptación**
- Título y contenido obligatorios
- Estado inicial: borrador
- Vecinos y admins pueden crear

---

### HU-3 Publicar noticia
Como administrador,  
quiero publicar una noticia,  
para que sea visible a los vecinos.

**Criterios de aceptación**
- Cambio de estado a publicado
- Fecha de publicación registrada
- Visible en el listado público

---

### HU-4 Ver detalle de noticia
Como visitante público,  
quiero ver el detalle de una noticia,  
para leer el contenido completo.

**Criterios de aceptación**
- Acceso desde listado
- Error 404 si no existe o no está publicada

---

### HU-5 Editar noticia
Como administrador,  
quiero editar una noticia,  
para actualizar o corregir información.

**Criterios de aceptación**
- Edición de título y contenido
- Cambios visibles si ya estaba publicada

---

## Backlog Priorizado (MoSCoW)

| ID  | Historia                     | Prioridad | Dependencias |
|-----|------------------------------|-----------|--------------|
| HU-1| Listado de noticias           | Must      | Backend news |
| HU-4| Detalle de noticia            | Must      | HU-1         |
| HU-2| Crear noticia (borrador)      | Must      | Auth         |
| HU-3| Publicar noticia              | Must      | HU-2         |
| HU-5| Editar noticia                | Should    | HU-2, HU-3   |

---

## Expansión Técnica – HU-2

| Ticket | Tarea técnica |
|------|---------------|
| T2.1 | Endpoint POST /news (FastAPI) |
| T2.2 | Modelo News en PostgreSQL     |
| T2.3 | Autorización JWT rol admin    |
| T2.4 | Formulario React (crear)      |

### Criterios Gherkin
```gherkin
Given soy un vecino autenticado
When creo una noticia con título y contenido
Then se guarda como borrador
And no es visible públicamente
```
