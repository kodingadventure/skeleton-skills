# skeleton-skills

## 0.2.0

### Minor Changes

- [#3](https://github.com/kodingadventure/skeleton-skills/pull/3) [`cf95c2d`](https://github.com/kodingadventure/skeleton-skills/commit/cf95c2de4f7e77753475a9af086243b0799a50dd) Thanks [@budiadiono](https://github.com/budiadiono)! - `refine-docs`: the Docs Layout gains an optional Wiki section (flow pages, feature index, preserved behaviour) and a `Required` column in the deep-context tier. `refine-docs` routes flow content to the wiki without writing it, and takes a commit range (`HEAD~3..HEAD`); with a clean tree and no argument it asks which recent commits to document.

- [#3](https://github.com/kodingadventure/skeleton-skills/pull/3) [`85604c2`](https://github.com/kodingadventure/skeleton-skills/commit/85604c2fe849ee623b00ee36e56aec389478c23e) Thanks [@budiadiono](https://github.com/budiadiono)! - New skill `update-wiki` (workflow group, optional): writes the wiki from committed changes — flow pages across code units, the feature index and, if the repo keeps one, a page of behaviour kept wrong on purpose. Reads every path from the Docs Layout's Wiki section; install it with `refine-docs`.

- [#3](https://github.com/kodingadventure/skeleton-skills/pull/3) [`e7d0f52`](https://github.com/kodingadventure/skeleton-skills/commit/e7d0f52d59fd38249cb4da15261d33e0e4cdce5e) Thanks [@budiadiono](https://github.com/budiadiono)! - `whatnext`: after a commit that changed behaviour, it now suggests updating the docs — once for a plan's whole commit range after its last phase, or right away for a commit outside a plan — with `update-wiki` if installed, else `refine-docs`. It also flags code units the Docs Layout says must each have a glossary but don't.

### Patch Changes

- [#3](https://github.com/kodingadventure/skeleton-skills/pull/3) [`3f4170d`](https://github.com/kodingadventure/skeleton-skills/commit/3f4170d0657817509ff7569d7cec65c6b1fe1d83) Thanks [@budiadiono](https://github.com/budiadiono)! - `whatnext`: for committed code with no test, it now suggests adding tests for that code instead of a test-first skill, and never names a skill that is not installed. `resume-here` and `discuss`: every message, question included, is in the workspace language, even in a repo whose committed files are English-only.

- [#3](https://github.com/kodingadventure/skeleton-skills/pull/3) [`b8785d3`](https://github.com/kodingadventure/skeleton-skills/commit/b8785d3e7e0390c482ad92ee1ad7f017b118e0d5) Thanks [@budiadiono](https://github.com/budiadiono)! - `whatnext`: when no installed skill fits, the answer now leaves out the `Invoke` line entirely instead of writing `Invoke: none`.

- [#3](https://github.com/kodingadventure/skeleton-skills/pull/3) [`229e330`](https://github.com/kodingadventure/skeleton-skills/commit/229e3303f197e184faa0639ba2eaa2bbe60255ec) Thanks [@budiadiono](https://github.com/budiadiono)! - `whatnext`: when a commit changed behaviour without a test beside it, it now asks for the missing tests before suggesting the docs update, and keeps asking for them even after a later commit documented the change.

## 0.1.1

### Patch Changes

- [`236e4e7`](https://github.com/kodingadventure/skeleton-skills/commit/236e4e7b2099508cbc23047239811e78691e064e) Thanks [@budiadiono](https://github.com/budiadiono)! - `review-page`: the page template is reformatted; pages look and behave the same.
