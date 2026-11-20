# AdaptiveExitLab — measured local run

Real trained two-stage MLP on synthetic numeric alerts, validation-selected confidence. Fraction exiting is not a measured latency speedup.

## Results

```json
{
  "adaptive": {
    "accuracy": 0.82,
    "precision": 0.801980198019802,
    "recall": 0.8350515463917526,
    "f1": 0.8181818181818183,
    "average_precision": 0.8595332128222047,
    "fp": 20,
    "fn": 16,
    "cases": 200
  },
  "full_depth": {
    "accuracy": 0.805,
    "precision": 0.7959183673469388,
    "recall": 0.8041237113402062,
    "f1": 0.8,
    "average_precision": 0.8398101217798026,
    "fp": 20,
    "fn": 19,
    "cases": 200
  },
  "selected_confidence": 0.6,
  "early_exit_fraction": 0.9200000166893005,
  "late_rows_computed": 16,
  "checks": [
    "Late stage only executes uncertain rows"
  ],
  "scope": "Real trained two-stage MLP on synthetic numeric alerts, validation-selected confidence. Fraction exiting is not a measured latency speedup."
}
```

Local experiment assertions passed. This does not establish production readiness or performance on real customer data. Source fingerprints and dependency versions are in results.json.
