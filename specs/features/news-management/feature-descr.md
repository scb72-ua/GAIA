# Feature Description — News Management

## 0) Feature Name & Summary

**Feature Name:** `News Management`

**Executive Summary (3–5 lines):**  
- **Problem:** Community members lack a centralized, easy-to-access source for neighborhood news and announcements. Information spreads informally, leading to uninformed neighbors and missed events.  
- **Opportunity:** Provide a simple web-based news portal where residents can stay informed and contribute content, strengthening community engagement.  
- **Expected Outcome:** Increased neighborhood participation, faster information dissemination, and reduced reliance on informal communication channels.

**Fit with Vision / Product Goal:**  
This feature is the **core MVP capability** of the Neighborhood News Management System. It directly addresses the primary vision of informing neighbors and announcing community events through a simple, accessible web platform.

---

## 1) Description of the Feature

The News Management feature enables the neighborhood community to share and consume news and announcements through a web-based platform. 

**Core capabilities:**
- **Public visitors** can browse and read published news without authentication
- **Authenticated neighbors (Vecino)** can create news drafts for community announcements
- **Administrators** can moderate content, publish/unpublish news, and manage all submissions

The feature supports the full news lifecycle: draft creation → moderation → publication → viewing.

---

## 2) Users/Roles & Impacted Personas

| Role/Persona | Key Objectives | Tasks / Jobs-to-be-done | Current Pain | Stakeholders |
|---|---|---|---|---|
| **Public Visitor** | Stay informed | Browse news list, read full articles | Information scattered across WhatsApp groups, word-of-mouth | — |
| **Neighbor (Vecino)** | Share local information | Create news drafts, view own submissions | No formal channel to contribute information | Community Board |
| **Administrator** | Ensure quality content | Moderate submissions, publish/unpublish, edit news | Manual coordination, no oversight tools | Community Board, Legal (content liability) |

> **Note:** Neighbors who create content must be registered users. Admins are a subset of registered neighbors with elevated permissions.

---

## 3) Problem / Opportunity Statement

**Context:** The informal neighborhood association currently relies on fragmented communication (WhatsApp groups, paper flyers, verbal announcements) to inform residents about news and events. This results in missed announcements and uneven information distribution.

**Problem Statement:** Our neighborhood residents experience frustration when trying to find community information, which causes missed events, reduced participation, and a fragmented sense of community.

**Why Now:** The association is formalizing its digital presence. A centralized news platform is the foundational capability required before expanding to events, incidents, or other community features.

---

## 4) Objectives & Business Outcomes

| Objective / Outcome | KPI / Metric | Baseline | Target | Time Horizon | Measurement Method |
|---|---|---|---|---|---|
| Increase community awareness | Monthly unique visitors to news section | 0 | 100+ | Q1 post-launch | Analytics (page views) |
| Enable neighbor contributions | News drafts submitted per month | 0 | 5+ | Q2 | Backend count query |
| Ensure content quality | % of submissions published | N/A | >80% | Q2 | Admin dashboard |
| Reduce admin burden | Time to publish a news item | Unknown | <5 min | Q1 | User feedback |

---

## 5) Scope (In/Out)

**In scope:**
- News list view (public, paginated, sorted by date descending)
- News detail view (public)
- News creation (authenticated Neighbors/Admins, draft state)
- News publication workflow (Admin-only)
- News editing (Admin-only for all news; Neighbor for own drafts while unpublished)
- RBAC enforcement (Public < Vecino < Admin)

**Out of scope (to prevent scope creep):**
- Comments on news articles (future feature)
- Rich media uploads (images/videos beyond text) — MVP uses text only
- Push notifications or email alerts
- Multi-language support (Spanish-only for MVP)
- News categories/tags (future enhancement)
- Search functionality (future enhancement)

**Key Assumptions:**
- Authentication system (JWT-based) will be implemented as a prerequisite or parallel feature
- Neighbors must explicitly register; there is no self-service admin promotion
- Initial deployment is local/internal; public internet exposure TBD

**Dependencies / Blockers:**
- User authentication & authorization feature must exist
- Database and API infrastructure ready

---

## 6) Non-Functional Requirements (NFRs)

### 6.1 Security & Privacy
- **Personal Data (PII):** News author name stored; minimized to display name only.
- **Encryption/Hashing:** All API traffic over HTTPS (TLS 1.2+). User passwords hashed with bcrypt/argon2.
- **Access Control (RBAC):** 
  - Public: read published news
  - Vecino: read + create drafts
  - Admin: full CRUD + publish/unpublish
- **Compliance:** GDPR-aware (residents in Spain). Content liability on Admin approval.
- **Audit & Sensitive Logs:** Log news creation, publication, and deletion events with user ID and timestamp. Retain logs for 1 year.

### 6.2 Performance
- **Performance Budgets:** News list API P95 < 300ms; News detail API P95 < 200ms.
- **Load/Throughput Limits:** Expected peak: 50 concurrent readers.
- **Query/Index Efficiency:** Index on `published_at DESC` for list queries; index on `id` for detail lookup.

### 6.3 Availability & Reliability
- **SLO/SLA/SLI:** Target 99% monthly uptime (acceptable for community app).
- **Graceful Degradation:** If DB is unavailable, return cached news list if possible.
- **Backup & Recovery / RTO-RPO:** Daily DB backups; RTO < 24h; RPO < 24h.

### 6.4 Accessibility (a11y) & Internationalization (i18n)
- **Accessibility:** WCAG 2.1 AA target. Semantic HTML, keyboard navigation, sufficient contrast.
- **Languages/Locales:** UI in Spanish (Castilian). Dates formatted as DD/MM/YYYY.

### 6.5 Observability
- **Metrics:** API latency, error rate, news created/published counts.
- **Logs:** Structured JSON logs with correlation ID per request.
- **Traces:** Standard request tracing with `request_id`.
- **Alerts:** Alert if error rate > 5% or P95 latency > 1s for 5 minutes.

---

## Annexes

### Open Questions / Assumptions
1. **Author names:** Should author display names be shown publicly, or kept anonymous? → *Assumption: Show author name for transparency.*
2. **Draft editing window:** Can Neighbors edit their drafts after submission but before publication? → *Assumption: Yes, until Admin publishes.*
3. **Unpublish workflow:** Can Admins unpublish already-published news? → *Assumption: Yes, for corrections or inappropriate content.*

### Risks & Mitigations
| Risk | Impact | Mitigation |
|------|--------|------------|
| Low adoption | Feature unused | Promote via existing community channels |
| Inappropriate content | Legal/reputation risk | Admin moderation required before publication |
| Performance under load | Poor UX | Paginate lists, optimize queries |

### Success / Fail-fast Criteria
- **Success signal:** >50 unique visitors within first month; >3 news items published.
- **Fail signal:** <10 visitors after 1 month; no news published after 2 weeks.
