# Auditor plan — round 3

## Context
Round 2's inquisitor returned `STATUS: NEEDS-MORE NEW=5` (clustered as
**2 NEW findings**, one per owned file). Both findings are direct
trim-cascade residuals from the round-2 fix that pruned the V6 variant
list from 9 rows to the 5 supported by PW 1.2.4.2. The two paths the
inquisitor offered were:

1. **Conservative close** — defer as editorial consolidation, return
   NOTHING-TO-DO.
2. **Tight close** — apply a 5-line cascade-cleanup, removing the last
   factual lag points.

I'm taking path (2). Reasons:

- All 5 sites are in my owned files (`README.md`, `detector.py`).
- The findings are squarely "docs accuracy" — core structural scope.
- `README.md:340` is an internal contradiction (link target undermines
  adjacent claim), not just staleness.
- `README.md:280` advertises a max param count (76M) that no longer
  appears anywhere in the canonical variant table.
- `detector.py:16` contradicts the bullet list two lines below in the
  same docstring.
- Each fix is a 1–3-word edit with an unambiguous corrected value
  drawn directly from the post-round-2 table — zero design judgement,
  zero risk of regression.
- These are NOT invented items: the inquisitor enumerated them
  literally in `round_02/inquisitor_review.md#missed-issues-new-this-round`.

Nothing else is proposed: round 2 closed the runtime cascade and round 1
closed all user-blocking items. No new structural concerns in
`pyproject.toml`, `environment.yaml`, `megadetector.md`,
`docs/training_guide.md`, or `docs/audit_report.md` after re-reading.

## Items

<a name="ITEM-AUD-301"></a>
### ITEM-AUD-301 — `README.md`: trim-cascade residuals (3 sites)

**What**
- **L54**: `**efficiency**, **modern architectures**, and **licensing flexibility** — **SMALLER, FASTER, BETTER**.`
  → `**efficiency** and **modern architectures** — **SMALLER, FASTER, BETTER**.`
- **L280** (Version History table, V6.0 row): `2.3M–76M | Multiple variants, MIT/Apache options`
  → `2.3M–58.1M | YOLOv9/v10 + RT-DETR variants (AGPL-3.0)`
- **L340** (License footer): `Individual model weights are released under MIT, Apache-2.0, or AGPL-3.0 — see the [Model Variants](#model-variants) table for per-variant licensing.`
  → `Individual model weights documented in this repository are released under AGPL-3.0 — see the [Model Variants](#model-variants) table for details.`

**Why**

L54: After the round-2 trim, all 5 documented V6 variants are AGPL-3.0.
"Licensing flexibility" no longer has a referent in the immediately-
following table or any other section of the README. Dropping it leaves
two umbrella claims ("efficiency", "modern architectures") that the
Highlights block (lines 56–60) and the Model Variants table (lines
64–70) both substantiate.

L280: Both halves of this cell are factually stale. Max param count
in the trimmed Model Variants table (line 64–70) is 58.1M
(`MDV6-yolov9-e`). The previous max-bearing variant was the now-
removed `MDV6-apa-rtdetr-e` (76M). The "MIT/Apache options" annotation
referred to variants no longer documented. New cell aligns with the
canonical table on both numbers and licensing.

L340: This is the only internal contradiction among the three sites.
The sentence sends the reader to the Model Variants table to verify
"per-variant licensing" of MIT / Apache-2.0 / AGPL-3.0, but that table
now contains only AGPL-3.0 rows. The fixed sentence (a) drops the two
license names that have no referent in the table and (b) reframes the
link target as "details" (param counts, recall, mAP50) rather than
"per-variant licensing", which it can no longer be.

The MegaDetector *code* sentence at the start of line 340 ("released
under the [MIT License](LICENSE)") stays untouched — `LICENSE` in the
repo root is still MIT and the project framing at line 5
("available under permissive licenses") refers to repo code +
PyTorch Wildlife framework, both MIT, both still accurate.

**Risk** Zero behavioral risk. Single-pass text edits, no link
restructuring, no anchor changes (`#model-variants` still resolves to
the same H3 at line 62).

**Verification**
1. `grep -n "76M\|MIT/Apache\|licensing flexibility" README.md` →
   zero hits after the edit.
2. `grep -n "#model-variants" README.md` → still exactly one inbound
   reference at L340.
3. Visual inspection of L54, L280, L340 against the canonical Model
   Variants table at L64–70.

<a name="ITEM-AUD-302"></a>
### ITEM-AUD-302 — `src/megadetector_ai/detector.py`: trim-cascade residuals (2 sites)

**What**
- **L16** (V6 docstring summary): `Multiple model variants are available, ranging from 2.3M to 76M parameters.`
  → `Multiple model variants are available, ranging from 2.3M to 58.1M parameters.`
- **L44–46** (V5 docstring comparative claim): `We recommend V6 for new projects — it is smaller, faster, and offers permissive license options.`
  → `We recommend V6 for new projects — it is smaller and faster.`

**Why**

L16: The same docstring's bullet list at lines 22–27 enumerates the 5
supported variants. The max-param variant in that list is
`MDV6-yolov9-e` (58.1M per the README's Model Variants table). 76M
referred to the now-removed `MDV6-apa-rtdetr-e`. Intra-docstring
contradiction is the kind of thing a user would notice in an IDE hover
the first time they autocomplete `MegaDetectorV6(`.

L44–46: After the round-2 docstring trim two lines above (variant
bullets), no V6 variant the user can construct via this class has a
permissive license — they're all AGPL-3.0. The "permissive license
options" claim now has zero referent on this class's surface. Dropping
the phrase leaves the genuine comparative claims ("smaller, faster")
intact; both are independently true (V6 compact is 2.3M vs V5's
139.9M; V6 inference latency is also lower).

**Risk** Zero behavioral risk. Docstring-only edits. No type signature,
no class hierarchy, no example block touched. `pass` body unchanged.
`help(MegaDetectorV6)` and `help(MegaDetectorV5)` will be the only
observable diff.

**Verification**
1. `grep -n "76M\|permissive license" src/megadetector_ai/detector.py`
   → zero hits after the edit.
2. `python -c "from megadetector_ai.detector import MegaDetectorV6, MegaDetectorV5; help(MegaDetectorV6); help(MegaDetectorV5)"`
   → both docstrings render without contradicting their own bullet
   lists.
3. `ruff check src/megadetector_ai/detector.py` → clean.

## Out of scope (explicitly deferred)

The following items were considered and rejected as over-fitting:

- **`README.md:5`** "available under permissive licenses" — refers to
  the repo code (MIT) and the PyTorch Wildlife framework (MIT), not
  to model weights. Not flagged by the inquisitor; rewording would
  expand scope unnecessarily.
- **`docs/audit_report.md`** — historical artifact summarizing
  round 1 findings; not flagged in round 2 and not a user-facing doc.
- **`megadetector.md`** — verified clean in round 2; no variant
  enumeration to cascade-fix.
- **`docs/training_guide.md`** — verified clean in round 2; the
  `weights: null` doc lag explicitly waived by both round 1 and
  round 2 auditor reports as non-blocking.
- **`pyproject.toml`** / **`environment.yaml`** — verified clean in
  round 2; no factual claims to cascade.

## Cross-Scope Findings

None. The reviewer-owned files (`training.py`, `training_utils.py`,
`cli.py`, `__init__.py`, `examples/config_training.yaml`) were
verified clean in round 2 and the round-3 read-through surfaced no
behavioral issues. The 5 sites in this plan are all docstring / doc
text — purely structural, no behavioral cross-impact.

STATUS: PLAN-READY
