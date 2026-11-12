# Preserved behaviour page

Optional. Written only when the Wiki table has a `Preserved behaviour` row. It lists behaviour
that is known to be wrong or inconsistent and deliberately not fixed yet. It is not limited to
migrations: any known gap that was left on purpose belongs here, each entry with the test that
locks it.

## Page shape

An opening paragraph that states the rule for fixing an entry: change the test that locks the
behaviour in the same commit; make sure no older client that is still in use depends on the old
behaviour; delete the entry. Ids are never reused, so a deleted entry leaves a gap in the
numbers.

Then one line:

```markdown
Open entries: <n>. Last checked against the code: <YYYY-MM-DD>.
```

Then one section per area, with one entry per behaviour. The id is `<PREFIX>-NNN`; choose the
prefix per area (for example `PB-API`) and take the next unused number.

## Entry fields

Seven fields, in this order:

- **Where:** the route, command or screen, and who can reach it.
- **Current behaviour:** what happens, from the caller's side.
- **Mechanism:** the function and file that cause it, and the check that is missing or wrong.
- **Why it is kept:** the reason it has not been fixed.
- **Wanted behaviour:** what should happen instead.
- **Locked by:** the test that locks the current behaviour (name and file), or `(no test)`.
- **Severity:** one word, for example `security`, `data`, `error-shape` or `cosmetic`.

## Example entry

The names below are invented.

```markdown
### PB-API-001 — Any member can close any ticket

- **Where:** `POST /tickets/:id/close`. Called by the support screen. Needs a signed-in member.
- **Current behaviour:** A member who does not own the ticket sends its id. The API answers `200`
  and the ticket is closed.
- **Mechanism:** `closeTicket` in `src/tickets/close.ts` loads the ticket and checks only its
  status. It never compares the caller with `ticket.ownerId`. `assignTicket` does compare them.
- **Why it is kept:** The behaviour was copied from the previous system; the fix is scheduled
  after the release.
- **Wanted behaviour:** Close answers `403` when the caller does not own the ticket.
- **Locked by:** `closes a ticket owned by someone else` in `tests/tickets.test.ts`.
- **Severity:** security
```
