# CLAUDE.md

Guidance for Claude Code when working in this repository.

## Project overview

Thesis project (Universidad Católica Boliviana, Ingeniería Mecatrónica): a software
prototype based on multimodal transformers to optimize the planning and management of
occupational health and safety programs (PGSST) under Bolivia's NTS-009/23 standard.

- `docs/thesis/` — LaTeX thesis document (Spanish). Main entry point: `main.tex`.
  - `chapters/` — content: `marcoref.tex` (introduction/referential framework),
    `marcoteorico.tex` (theoretical framework), `marcopractico/` (proposal),
    `additional_material/apendices/` and `additional_material/anexos/` (appendices/annexes).
  - `images/` — figures, mostly TikZ `.tex` sources organized per chapter.
  - `packages/`, `preambles/` — `ucbimt.sty` (UCB title pages), `tikz-uml.sty`, preamble.
  - `bibliography/referencias.bib` — biblatex (ISO 690) bibliography.
  - `slides/` — `perfil.tex` defense slides (beamer).
- `prototypes/` — exploratory prototypes: `danger_detection` (computer vision),
  `iper` (risk matrix), `gui`, `images`.
- `docs/ref`, `docs/proto_thesis`, `docs/psst_references` — local reference material, gitignored.

## Building the thesis

Compile with `pdflatex` + `biber` (biblatex is used — never `\bibliography`/bibtex):

```
pdflatex main.tex && biber main && pdflatex main.tex && pdflatex main.tex
```

LaTeX build artifacts (`.aux`, `.bbl`, `.log`, …) are gitignored, but the compiled
`main.pdf` and `slides/perfil.pdf` ARE tracked — rebuild and include them when the
sources change.

## Commit style

Conventional Commits, in English, lowercase, imperative mood, no trailing period:

```
type(scope): short description
```

- Types: `feat`, `fix`, `docs`, `perf`, `refactor`, `chore`.
- Scope is optional but preferred, e.g. `docs(thesis): ...`, `feat(prototypes): ...`,
  `chore(deps): ...`.
- Keep commits atomic: one logical block of related files per commit.
- Thesis content/writing changes use the `docs(thesis)` type+scope; prototype code uses
  `feat`/`fix` with a `prototypes` scope.
- No AI attribution: never add `Co-Authored-By: Claude ...` trailers, "Generated with
  Claude Code" lines, or any other AI attribution to commit messages or PR descriptions.
