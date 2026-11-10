**Public check**, every line of it:

- Holds only what the code, the repo's docs, or the issue itself already show. Workspace paths and names, decision numbers, findings, plans, other projects, customers, and people stay out.
- Carries no secrets, tokens, internal hosts, or personal data.
- Names a commit only when it is on the public remote: run `git fetch`, check that `git branch -r --contains <hash>` lists a branch of the issue's repo, and that `gh repo view <owner/name> --json isPrivate` says `false`. In doubt, leave the hash out.
- Writes `@name` only for someone you mean to notify, and describes a vulnerability's details nowhere.
