# NM-ADMIN-004-FE-T01 — Implementation Plan

**Source ticket**: `specs/features/news-management/tickets.md` → **NM-ADMIN-004-FE-T01**  
**Related user story**: **NM-ADMIN-004** (from `specs/features/news-management/user-stories.md`)  
**Plan version**: v1.0 — (Claude, 2026-02-03T18:05:31+01:00)  
**Traceability**: All tasks must include inline references to `NM-ADMIN-004-FE-T01` and `NM-ADMIN-004` scenario names/tags.

---

## 1) Context & Objective

### Ticket Summary
Implement the delete action with confirmation dialog for admins.

### Impacted Tests or Business Flows
- `Scenario: Admin deletes an article`
- `Scenario: Deletion requires confirmation`

---

## 2) Scope

### In Scope
- "Eliminar" button (destructive variant) in admin news view
- Confirmation dialog: "¿Seguro que desea eliminar esta noticia?"
- `useMutation` for delete action
- Success: toast "Noticia eliminada", remove from list / redirect
- Handle 404: toast "Noticia no encontrada"

---

## 3) Atomic Task Breakdown

### Task 1: Create DeleteButton Component

- **Artifacts impacted**:
  - `frontend/src/features/news/components/DeleteButton.tsx` (NEW)
  - `frontend/src/features/news/components/DeleteButton.test.tsx` (NEW)
  - `frontend/src/features/news/api/newsApi.ts` (UPDATE) — deleteNews mutation
- **BDD Acceptance**:

```gherkin
Scenario: Confirmation dialog appears
  Given I click Eliminar
  Then I see dialog "¿Seguro que desea eliminar esta noticia?"

Scenario: Cancel does nothing
  Given dialog is open
  When I click Cancel
  Then dialog closes and article remains

Scenario: Confirm deletes article
  Given dialog is open
  When I confirm
  Then article is deleted
  And I see toast "Noticia eliminada"
```

---

### Task 2: Style as Destructive

- Use shadcn `AlertDialog` for confirmation
- Use `destructive` variant for button
- A11y: Focus trap, Escape to cancel

---

## 4) Definition of Done

- [ ] DeleteButton with confirmation dialog
- [ ] AlertDialog from shadcn
- [ ] Destructive styling
- [ ] A11y: focus trap, escape to cancel
