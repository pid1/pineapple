# AGENTS.md

## Sadr

### Build and test
- No test suite exists. The check is that the app generates a PDF from example_resume.md and that `pdftotext` extracts its text.
- With uv: `uv sync --locked`, then `uv run python pineapple.py example_resume.md -o /tmp/example.pdf`. Passing means exit 0 and a PDF.
- With devenv: `devenv shell -- python pineapple.py example_resume.md -o /tmp/example.pdf`. Passing means exit 0 and a PDF.
- CI runs only Semgrep (`.github/workflows/semgrep.yml`). The required check on `main` is `semgrep/ci`.

### Toolchain
- uv installs the Python and the packages that pyproject.toml and uv.lock pin.
- devenv.nix takes Python, reportlab and markdown from the nixpkgs in devenv.lock. It ignores pyproject.toml and uv.lock.
