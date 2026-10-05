# HRCEV-Lite

Lightweight testing code for **Prediction Reliability Assessment in Adversarial
Hyperspectral Classification via Hierarchical Evidence Fusion**.

[中文说明](README_zh.md)

This preliminary release runs the V13 result-support calibrator and hierarchical
fusion on a small, real, precomputed Pavia University evidence subset. It provides
a CPU example of fitting, inference and offline evaluation. A GPU, PyTorch and
the raw hyperspectral image are not needed for this example.

The core implementation is copied without modification from
`result_calibration_v13.py`. The lightweight interface adds validation, explicit
feature selection and a command-line workflow. It estimates **Trust**, residual
**Uncertainty** and diagnostic **Conflict**. Trust + disbelief + Uncertainty = 1.
Conflict is a separate diagnostic and is not part of that normalization.

## Release scope

| Included now | Planned for the complete release |
| --- | --- |
| Original V13 calibration and fusion implementation | Raw-patch-to-evidence processing and primary classifier training |
| 2,000 real development evidence records | Full reference/development/test setup and preprocessing |
| 1,120 real evaluation records, with targets in a separate file | Full three-dataset, nine-attack experiment scripts and baselines |
| CLI, input schema, offline metrics and tests | Complete results, trained artifacts and data-access instructions |

The complete release is planned after paper acceptance, subject to third-party
dataset redistribution terms. This repository does not reproduce the paper's
three-dataset aggregate metrics. The demo fits a new calibrator on the small
development subset; it does not contain the paper's full-data fitted calibrator.

## Quick start

Use Python 3.10–3.12 in a fresh environment. From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python run_demo.py
python -m unittest discover -s tests -v
```

The demo uses one CPU thread for fitting and inference. It writes:

- `outputs/demo/demo_calibrator.joblib` — locally fitted demo model
- `outputs/demo/predictions.csv` — sample ID, confidence and four output scores
- `outputs/demo/metrics.json` — per-condition, pooled and macro metrics for the subset

Outputs are ignored by Git. The example data are bundled, so no data download,
original experiment directory or machine-specific path is required.

## Separate commands and your own evidence tables

For the CLI, install the package from this checkout:

```bash
python -m pip install .
hrcev-lite fit --development examples/development.csv --model outputs/model.joblib
hrcev-lite predict --input examples/evaluation_inputs.csv --model outputs/model.joblib --output outputs/predictions.csv
hrcev-lite evaluate --predictions outputs/predictions.csv --targets examples/evaluation_targets.csv --output outputs/metrics.json
```

`python -m hrcev_lite` provides the same installed CLI. See
[the input schema](docs/INPUT_SCHEMA.md) for using your own tables.
Fit on labeled development data, then freeze the calibrator before evaluating
unseen test records. Prediction consumes diagnostic features and the predicted
class only. It never selects `correct`, ground-truth labels, attack names or budgets
as model features. Those fields are used only in development supervision or
offline evaluation. Locally saved joblib models should only be loaded from trusted
sources and with compatible dependency versions.

## What the small dataset contains

The development subset contains 80 rows per condition from eight attacks at three
budgets and one clean condition. The evaluation subset contains 40 rows per
condition from nine attacks at the same budgets and one clean condition.
Budgets are 0.005, 0.010 and 0.020. Square Attack is excluded from development.

Sampling is uniform within each condition, with fixed seeds, without filtering
on correctness or score. Development and evaluation have disjoint underlying
pixel IDs, checked against the full source caches. Multiple attacked records can
refer to the same evaluation pixel; rows are not independent image replicates.
The files contain derived scalar diagnostics and class indices, not raw images.
Pavia University dataset information is available from the
[original dataset page](https://www.ehu.eus/ccwintco/index.php/Hyperspectral_Remote_Sensing_Scenes).
Source filenames, hashes and sampling details are in
[`examples/provenance.json`](examples/provenance.json).

`base_conflict` is the pre-V13 conflict diagnostic. For the cached evaluation rows,
it comes from `v10_conflict`, not the already fused V13 `conflict`. Feeding the final
conflict back into the model would apply the diagnostic formula twice.

## Metrics

Errors are the positive class for error-detection AUROC and AUPR, using 1 − Trust
as the detection score. MSP uses 1 − classifier confidence. AURC is the mean
cumulative error after sorting by decreasing support. Ties retain input row order.
Top-20% accuracy retains `ceil(0.2 * n)` rows within each evaluated group.

Macro metrics average the attack/budget groups with equal weight and exclude the
clean reference condition. Pooled metrics are reported separately. An AUROC/AUPR
is `null` for a condition containing only one correctness class; the number of
defined conditions is reported. Small-subset metrics can differ substantially
from complete-benchmark metrics and are not substitutes for the reported paper
results.

## Project layout

```text
src/hrcev_lite/calibration.py  unchanged V13 core
src/hrcev_lite/api.py          validated fit and inference interface
src/hrcev_lite/evaluation.py   offline subset metrics
src/hrcev_lite/cli.py          command-line entry point
examples/                     small real evidence tables and provenance
tests/                        numerical, split and no-label-inference checks
docs/INPUT_SCHEMA.md          input/output contract
docs/RELEASE_NOTES.md          staged release and validation record
```

The manuscript title identifies the associated work. Publication details and a
formal citation will be added when available. No journal acceptance or DOI is
claimed by this preliminary release. See [NOTICE](NOTICE) for licensing status.
