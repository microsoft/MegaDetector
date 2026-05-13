# Auditor report — round 3

## Context

Round 2 closed with `STATUS: NEEDS-MORE NEW=5` from the inquisitor, who
enumerated 5 trim-cascade residual sites (2 NEW finding clusters) in
auditor-owned files. The inquisitor offered two protocol-valid closes;
the round-3 plan selected **path (2) — tight 5-line cascade-cleanup**.
Both items APPROVED by round-3 inquisitor (`inquisitor_approvals.md`).
This report records the applied edits.

Commit: `a41abfed8e2e0ac612a1d356212e613f69f22e76` — touches only `README.md` and
`src/megadetector_ai/detector.py` (the two files cited by the round-2
NEW findings). All 5 sites edited as planned, verbatim.

## Changes Applied

<a name="ITEM-AUD-301"></a>
### ITEM-AUD-301 — README.md: trim-cascade residuals (3 sites)

**`README.md:54`** — drop "licensing flexibility" tagline that has no
referent after the round-2 trim (all 5 documented V6 variants are
AGPL-3.0 per the canonical Model Variants table at L64–70).
- Before: `The latest release focuses on **efficiency**, **modern architectures**, and **licensing flexibility** — **SMALLER, FASTER, BETTER**.`
- After: `The latest release focuses on **efficiency** and **modern architectures** — **SMALLER, FASTER, BETTER**.`

**`README.md:280`** (Version History V6.0 row) — replace stale param
range and license annotation with values matching the canonical Model
Variants table.
- Before: `| **V6.0** (current) | 2024 | YOLOv9/v10, RT-DETR | 2.3M–76M | Multiple variants, MIT/Apache options |`
- After: `| **V6.0** (current) | 2024 | YOLOv9/v10, RT-DETR | 2.3M–58.1M | YOLOv9/v10 + RT-DETR variants (AGPL-3.0) |`
- Numbers: 58.1M = `MDV6-yolov9-e`, the new max in the trimmed table.
  76M referred to the removed `MDV6-apa-rtdetr-e`.

**`README.md:340`** (License footer) — resolve internal contradiction:
sentence sent reader to Model Variants table to verify "per-variant
licensing" of MIT/Apache-2.0/AGPL-3.0, but that table now contains
only AGPL-3.0 rows. Reframed link target as "details" (param counts,
recall, mAP50) rather than "per-variant licensing".
- Before: `The MegaDetector code is released under the [MIT License](LICENSE). Individual model weights are released under MIT, Apache-2.0, or AGPL-3.0 — see the [Model Variants](#model-variants) table for per-variant licensing.`
- After: `The MegaDetector code is released under the [MIT License](LICENSE). Individual model weights documented in this repository are released under AGPL-3.0 — see the [Model Variants](#model-variants) table for details.`
- The repo code MIT clause at the start of the sentence is unchanged
  (`LICENSE` in repo root is still MIT). The `#model-variants`
  anchor still resolves to the same H3 at L62.

<a name="ITEM-AUD-302"></a>
### ITEM-AUD-302 — src/megadetector_ai/detector.py: trim-cascade residuals (2 sites)

**`detector.py:16`** (V6 docstring summary) — fix intra-docstring
contradiction. The bullet list at L22–27 enumerates 5 variants whose
max-param entry is `MDV6-yolov9-e` (58.1M per README table); the
summary line said 76M (referred to the removed `MDV6-apa-rtdetr-e`).
- Before: `variants are available, ranging from 2.3M to 76M parameters.`
- After: `variants are available, ranging from 2.3M to 58.1M parameters.`

**`detector.py:44–46`** (V5 docstring comparative claim) — drop
"permissive license options" clause that has no referent on the
`MegaDetectorV6` class's constructable surface (all 5 variants the
user can instantiate via `version=` are AGPL-3.0). Genuine
comparative claims ("smaller, faster") preserved — both independently
true (V6 compact 2.3M vs V5 139.9M; V6 inference latency also lower).
- Before: `We recommend V6 for new projects — it is smaller, faster, and offers permissive license options.` (across 3 lines after wrapping)
- After: `We recommend V6 for new projects — it is smaller and faster.` (across 2 lines after wrapping)

## Tests Added/Updated

None. All five edits are docstring / Markdown text — no behavioral
surface, no tests to add or update.

Verification commands run after the edits:

| Command | Result |
|---|---|
| `grep -nE "76M\|MIT/Apache\|licensing flexibility" README.md src/megadetector_ai/detector.py` | zero hits |
| `grep -nE "permissive license" README.md src/megadetector_ai/detector.py` | 1 hit at `README.md:5` — the explicitly-deferred site (refers to repo code MIT + PyTorch Wildlife framework MIT, NOT to model weights; preserved per plan's "Out of scope" section and unmodified across rounds 1–3) |
| `python -c 'import ast; ast.parse(open("src/megadetector_ai/detector.py").read())'` | OK |
| `uvx ruff check src/megadetector_ai/detector.py` | All checks passed |
| `grep -n "#model-variants" README.md` | 1 inbound reference at L340 (anchor target H3 at L62 unchanged) |

## Cross-Scope Findings

None. The reviewer-owned files (`training.py`, `training_utils.py`,
`cli.py`, `__init__.py`, `examples/config_training.yaml`) were
verified clean in round 2 and surfaced no new behavioral concerns on
the round-3 read-through. The 5 sites addressed here are purely
docstring / docs text with no behavioral cross-impact.

## Skipped

The following items were considered and explicitly deferred (consistent
with the round-3 plan's "Out of scope" section). None are blocking;
all were verified clean or non-applicable in round 2 and surface no
new concerns:

- **`README.md:5`** "available under permissive licenses" — refers to
  the repo code (MIT) and the PyTorch Wildlife framework (MIT), not
  model weights. Factually accurate; not flagged by the round-2
  inquisitor; rewording would expand scope unnecessarily.
- **`docs/audit_report.md`** — historical artifact summarizing round 1
  findings; not user-facing, not flagged in round 2.
- **`megadetector.md`** — verified clean in round 2; no variant
  enumeration to cascade-fix.
- **`docs/training_guide.md`** — verified clean in round 2; the
  `weights: null` doc lag explicitly waived in rounds 1 and 2 as
  non-blocking (training itself raises a clear runtime error when the
  field is unset, per the round-2 reviewer fix).
- **`pyproject.toml`** / **`environment.yaml`** — verified clean in
  round 2; no factual claims to cascade-fix.

## Status

All 5 cited NEW-finding sites from `round_02/inquisitor_review.md` are
resolved. The doc-vs-doc factual cascade introduced by the round-2
V6-variant trim is now fully closed. Round 4 expected to be a no-op
verification round.

STATUS: DONE COMMIT=a41abfed8e2e0ac612a1d356212e613f69f22e76
