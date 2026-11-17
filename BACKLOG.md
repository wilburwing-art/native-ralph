# native-ralph session backlog

The queue for one-item-per-session work. Written 2026-11-17 from measurements on that date: 11 tracked files of markdown (the skill at `skill/SKILL.md`, 5 templates under `skill/templates/`, `docs/primitive-comparison.md`, README, CLAUDE.md); 8 commits (latest 2026-05-03); no code and no tests; 0 unpushed. The working tree holds another session's in-flight edit: `skill/SKILL.md` changed by about 61 lines (a sixth option, a launchd agent registered on the routines spine) and `README.md` by 2 lines, `.claude/commands/prime.md` modified, and two command files (`install.md`, `reset-state.md`) deletions that are staged in the index. The README and CLAUDE.md still say "5 primitives". Re-measure before starting an item, because the counts move.

**How to read it**

- Take the first unticked item in "Queue" from the top that is not marked "Needs owner". One item per session.
- Estimates are hours for one session. Check by running the skill on one real "loop on X" request and reading the brief it produces.

## Queue

- [ ] **1. Land the sixth-option edit.** ~1 h. Review the `skill/SKILL.md` and `README.md` diffs with the session that wrote them, confirm the two staged deletions are intended, and commit by named path. Done: `git status` is clean and the README names the same options as the skill.

- [ ] **2. Reconcile README, CLAUDE.md and the comparison doc with the skill.** ~1 h. They say 5 primitives and describe a 12-step chooser; the skill now carries a sixth option. Done: option count, step count and table rows match `skill/SKILL.md`, each checked by reading it that session.

- [ ] **3. Write the sixth template.** ~2 h. A launchd-on-the-routines-spine template belongs beside the five under `skill/templates/`, with fields and real failure modes (an agent that is installed but not loaded; a job that reads gitignored data a cloud routine cannot see). Done: the template exists with the three required sections and the skill points at it.

- [ ] **4. Failure-mode audit.** ~2 h. CLAUDE.md requires failure modes to be real observed incidents. Done: each failure-mode line in the five templates cites a date or a repo where it happened, or is removed.

- [ ] **5. A routing eval.** ~3 h. Write 10 real past "loop on X" requests and the primitive each should route to, and run the skill on each. Done: the table of expected versus chosen primitive is in `docs/` and mismatches become edits to the chooser.

## Needs owner

- **Whether the two staged command deletions are intended.** They belong to another session.
- **Which primitive each past request should have used** for item 5; only the owner knows the intent.
