# User Stories — News Management

## Introduction

This document defines the user stories for the **News Management** feature. These stories enable neighborhood residents to stay informed and contribute news through a centralized web portal.

### Linked Objectives (from `feature-descr.md`)

| Objective | KPI | Target |
|-----------|-----|--------|
| Increase community awareness | Monthly unique visitors | 100+ (Q1) |
| Enable neighbor contributions | News drafts per month | 5+ (Q2) |
| Ensure content quality | % submissions published | >80% (Q2) |
| Reduce admin burden | Time to publish | <5 min (Q1) |

### Roles

| Role | Code | Permissions |
|------|------|-------------|
| Public Visitor | `PUBLIC` | Read published news |
| Neighbor | `VECINO` | Read + Create drafts + Edit own drafts |
| Administrator | `ADMIN` | Full CRUD + Publish/Unpublish |

---

## User Stories

### NM-PUBLIC-001: View Published News List

**As a** public visitor,  
**I want to** see a list of published news articles,  
**So that** I can stay informed about what is happening in my neighborhood.

#### Acceptance Criteria

```gherkin
Feature: View Published News List

  # Happy Path
  Scenario: Public visitor views news list
    Given the system has 5 published news articles
    When I navigate to the news list page without authentication
    Then I see a paginated list of published news articles
    And articles are sorted by publication date descending
    And each article shows title, excerpt, author name, and publication date

  # Edge Case: Empty list
  Scenario: No published news available
    Given there are no published news articles
    When I navigate to the news list page
    Then I see an empty state message "No hay noticias publicadas"

  # Edge Case: Draft articles hidden
  Scenario: Draft articles are not visible to public
    Given there are 3 published and 2 draft news articles
    When I navigate to the news list page without authentication
    Then I see only 3 articles in the list

  # Performance
  Scenario: News list loads within performance budget
    Given the system has 100 published news articles
    When I request the news list API
    Then the response is returned within 300ms (P95)

  # Accessibility
  Scenario: News list is accessible
    Given I am using a screen reader
    When I navigate to the news list page
    Then all articles have proper heading structure (h2/h3)
    And the list has a semantic <main> landmark
    And date format is DD/MM/YYYY
```

---

### NM-PUBLIC-002: View News Article Detail

**As a** public visitor,  
**I want to** read the full content of a news article,  
**So that** I can get complete information about a topic.

#### Acceptance Criteria

```gherkin
Feature: View News Article Detail

  # Happy Path
  Scenario: Public visitor reads published article
    Given a published news article with ID "abc123" exists
    When I navigate to /news/abc123
    Then I see the full article with title, content, author, and publication date
    And I see a link to return to the news list

  # Edge Case: Article not found
  Scenario: Article does not exist
    Given no article with ID "nonexistent" exists
    When I navigate to /news/nonexistent
    Then I receive a 404 error
    And I see a friendly error message "Noticia no encontrada"

  # Security: Draft articles not accessible
  Scenario: Draft article not accessible to public
    Given a draft news article with ID "draft123" exists
    When I navigate to /news/draft123 without authentication
    Then I receive a 404 error
    And the draft content is not exposed

  # Performance
  Scenario: Article detail loads within performance budget
    Given a published news article exists
    When I request the article detail API
    Then the response is returned within 200ms (P95)

  # Accessibility
  Scenario: Article detail is accessible
    Given I am viewing an article
    Then the article has a single <h1> for the title
    And content uses semantic paragraph elements
    And the page has proper focus management
```

---

### NM-VECINO-001: Create News Draft

**As a** registered neighbor (Vecino),  
**I want to** create a news draft,  
**So that** I can share information with my community pending moderation.

#### Acceptance Criteria

```gherkin
Feature: Create News Draft

  # Happy Path
  Scenario: Neighbor creates a news draft
    Given I am authenticated as a Vecino
    When I submit a news draft with title "Reunión de vecinos" and content "El sábado..."
    Then the draft is saved with status "draft"
    And I receive confirmation "Noticia guardada como borrador"
    And the draft is not visible in the public news list
    And the creation event is logged with my user ID

  # Validation: Required fields
  Scenario: Draft requires title and content
    Given I am authenticated as a Vecino
    When I submit a news draft without a title
    Then I receive a validation error "El título es obligatorio"
    
  Scenario: Draft requires content
    Given I am authenticated as a Vecino
    When I submit a news draft without content
    Then I receive a validation error "El contenido es obligatorio"

  # Security: Authentication required
  Scenario: Unauthenticated user cannot create draft
    Given I am not authenticated
    When I attempt to create a news draft
    Then I receive a 401 Unauthorized error

  # Security: Public role cannot create
  Scenario: Public visitor cannot access creation form
    Given I am not authenticated
    When I navigate to the news creation form
    Then I am redirected to the login page

  # Observability
  Scenario: Draft creation is audited
    Given I am authenticated as a Vecino
    When I create a news draft
    Then an audit log entry is created with:
      | field       | value          |
      | action      | news.created   |
      | user_id     | my user ID     |
      | news_status | draft          |
      | timestamp   | current time   |
```

---

### NM-VECINO-002: Edit Own Draft

**As a** registered neighbor (Vecino),  
**I want to** edit my own unpublished drafts,  
**So that** I can improve my submission before moderation.

#### Acceptance Criteria

```gherkin
Feature: Edit Own Draft

  # Happy Path
  Scenario: Neighbor edits their own draft
    Given I am authenticated as a Vecino
    And I have a draft news article with ID "mydraft"
    When I update the title to "Reunión actualizada"
    Then the draft is updated successfully
    And I receive confirmation "Cambios guardados"

  # Security: Cannot edit other's drafts
  Scenario: Neighbor cannot edit another neighbor's draft
    Given I am authenticated as Vecino "vecino1"
    And Vecino "vecino2" has a draft article
    When I attempt to edit vecino2's draft
    Then I receive a 403 Forbidden error

  # Security: Cannot edit published articles
  Scenario: Neighbor cannot edit published articles
    Given I am authenticated as a Vecino
    And my article has been published by an Admin
    When I attempt to edit the published article
    Then I receive a 403 Forbidden error
    And I see a message "Solo los administradores pueden editar noticias publicadas"

  # Edge Case: Draft no longer exists
  Scenario: Draft was deleted
    Given I am authenticated as a Vecino
    And my draft was deleted by an Admin
    When I attempt to edit the draft
    Then I receive a 404 error
```

---

### NM-ADMIN-001: Publish News Article

**As an** administrator,  
**I want to** publish a draft news article,  
**So that** it becomes visible to all community members.

#### Acceptance Criteria

```gherkin
Feature: Publish News Article

  # Happy Path
  Scenario: Admin publishes a draft
    Given I am authenticated as an Admin
    And a draft news article with ID "draft123" exists
    When I publish the article
    Then the article status changes to "published"
    And the publication date is recorded
    And the article appears in the public news list
    And I receive confirmation "Noticia publicada"

  # Security: Only Admin can publish
  Scenario: Vecino cannot publish articles
    Given I am authenticated as a Vecino
    And I have a draft article
    When I attempt to publish the article
    Then I receive a 403 Forbidden error

  Scenario: Unauthenticated user cannot publish
    Given I am not authenticated
    When I attempt to publish an article via API
    Then I receive a 401 Unauthorized error

  # Edge Case: Already published
  Scenario: Article is already published
    Given I am authenticated as an Admin
    And article "pub123" is already published
    When I attempt to publish it again
    Then I receive a message "La noticia ya está publicada"

  # Observability
  Scenario: Publication is audited
    Given I am authenticated as an Admin
    When I publish a draft article
    Then an audit log entry is created with:
      | field       | value           |
      | action      | news.published  |
      | user_id     | my admin ID     |
      | news_id     | the article ID  |
      | timestamp   | current time    |
```

---

### NM-ADMIN-002: Unpublish News Article

**As an** administrator,  
**I want to** unpublish a news article,  
**So that** I can remove incorrect or inappropriate content from public view.

#### Acceptance Criteria

```gherkin
Feature: Unpublish News Article

  # Happy Path
  Scenario: Admin unpublishes an article
    Given I am authenticated as an Admin
    And a published news article with ID "pub123" exists
    When I unpublish the article
    Then the article status changes to "draft"
    And the article is removed from the public news list
    And the public can no longer access /news/pub123
    And I receive confirmation "Noticia despublicada"

  # Security: Only Admin can unpublish
  Scenario: Vecino cannot unpublish articles
    Given I am authenticated as a Vecino
    When I attempt to unpublish any article via API
    Then I receive a 403 Forbidden error

  # Edge Case: Already draft
  Scenario: Article is already a draft
    Given I am authenticated as an Admin
    And article "draft123" is a draft
    When I attempt to unpublish it
    Then I receive a message "La noticia ya es un borrador"

  # Observability
  Scenario: Unpublication is audited
    Given I am authenticated as an Admin
    When I unpublish an article
    Then an audit log entry is created with action "news.unpublished"
```

---

### NM-ADMIN-003: Edit Any News Article

**As an** administrator,  
**I want to** edit any news article (draft or published),  
**So that** I can correct errors or update information.

#### Acceptance Criteria

```gherkin
Feature: Edit Any News Article

  # Happy Path: Edit published article
  Scenario: Admin edits a published article
    Given I am authenticated as an Admin
    And a published article with ID "pub123" exists
    When I update the content
    Then the changes are saved
    And the updated content is immediately visible to the public
    And I receive confirmation "Cambios guardados"

  # Happy Path: Edit draft article
  Scenario: Admin edits a neighbor's draft
    Given I am authenticated as an Admin
    And Vecino "vecino1" has a draft article
    When I update the title
    Then the changes are saved successfully

  # Security: Only Admin can edit published
  Scenario: Vecino cannot edit published articles
    Given I am authenticated as a Vecino
    And there is a published article
    When I attempt to edit it
    Then I receive a 403 Forbidden error

  # Validation
  Scenario: Cannot save with empty required fields
    Given I am authenticated as an Admin
    When I clear the title and save
    Then I receive a validation error "El título es obligatorio"

  # Observability
  Scenario: Edit is audited
    Given I am authenticated as an Admin
    When I edit any article
    Then an audit log entry is created with action "news.updated"
```

---

### NM-ADMIN-004: Delete News Article

**As an** administrator,  
**I want to** delete a news article,  
**So that** I can remove obsolete or inappropriate content permanently.

#### Acceptance Criteria

```gherkin
Feature: Delete News Article

  # Happy Path
  Scenario: Admin deletes an article
    Given I am authenticated as an Admin
    And a news article with ID "news123" exists
    When I delete the article
    Then the article is permanently removed
    And the article no longer appears in any list
    And I receive confirmation "Noticia eliminada"

  # Security: Only Admin can delete
  Scenario: Vecino cannot delete articles
    Given I am authenticated as a Vecino
    When I attempt to delete any article via API
    Then I receive a 403 Forbidden error

  # UX: Confirmation required
  Scenario: Deletion requires confirmation
    Given I am authenticated as an Admin
    When I click delete on an article
    Then I see a confirmation dialog "¿Seguro que desea eliminar esta noticia?"
    And the article is only deleted after confirmation

  # Edge Case: Article not found
  Scenario: Article does not exist
    Given I am authenticated as an Admin
    When I attempt to delete a non-existent article
    Then I receive a 404 error

  # Observability
  Scenario: Deletion is audited
    Given I am authenticated as an Admin
    When I delete an article
    Then an audit log entry is created with action "news.deleted"
    And the log includes the deleted article's metadata
```

---

## Story Summary

| ID | Title | Role | Priority |
|----|-------|------|----------|
| NM-PUBLIC-001 | View Published News List | Public | Must |
| NM-PUBLIC-002 | View News Article Detail | Public | Must |
| NM-VECINO-001 | Create News Draft | Vecino | Must |
| NM-VECINO-002 | Edit Own Draft | Vecino | Should |
| NM-ADMIN-001 | Publish News Article | Admin | Must |
| NM-ADMIN-002 | Unpublish News Article | Admin | Should |
| NM-ADMIN-003 | Edit Any News Article | Admin | Should |
| NM-ADMIN-004 | Delete News Article | Admin | Should |

---

## Traceability Matrix

| Story ID | Objective Addressed | NFR Coverage |
|----------|---------------------|--------------|
| NM-PUBLIC-001 | Increase community awareness | Performance (P95 <300ms), Accessibility (WCAG AA) |
| NM-PUBLIC-002 | Increase community awareness | Performance (P95 <200ms), Accessibility |
| NM-VECINO-001 | Enable neighbor contributions | Security (Auth), Observability (Audit logs) |
| NM-VECINO-002 | Enable neighbor contributions | Security (RBAC ownership) |
| NM-ADMIN-001 | Ensure content quality, Reduce admin burden | Observability (Audit logs) |
| NM-ADMIN-002 | Ensure content quality | Observability (Audit logs) |
| NM-ADMIN-003 | Reduce admin burden | Security (RBAC), Observability |
| NM-ADMIN-004 | Ensure content quality | Security (RBAC), Observability |
