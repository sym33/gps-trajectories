"""Recalculate the public TGIS contrasts and floors from group-level values."""

import csv
from collections import defaultdict
from math import isclose
from pathlib import Path
from statistics import mean

import numpy as np
from scipy.stats import t


EVIDENCE = Path(__file__).resolve().parent / "evidence"
FLOOR_KEY = ("cohort", "condition", "variant", "reference")


def rows(filename):
    with (EVIDENCE / filename).open(newline="") as source:
        return list(csv.DictReader(source))


def close(expected, actual):
    assert isclose(float(expected), float(actual), rel_tol=0, abs_tol=1e-7), (expected, actual)


def metric_means():
    output = defaultdict(list)
    for row in sorted(rows("geolife_group_means.csv"), key=lambda row: row["group"]):
        key = (row["condition"], row["target"], int(row["cell_m"]), row["method"])
        output[key].append(float(row["mean_loss"]))
    return {key: np.array(values) for key, values in output.items()}


def verify_source(means):
    comparisons = defaultdict(list)
    for row in rows("geolife_comparisons.csv"):
        comparisons[row["condition"], row["target"], int(row["cell_m"])].append(row)
    rng = np.random.default_rng(20261017)
    primary = 0
    for key, contrasts in sorted(comparisons.items()):
        count = len(means[(*key, "linear")])
        draws = rng.integers(count, size=(20_000, count))
        for row in contrasts:
            method = means[(*key, row["method"])]
            gain = means[(*key, row["control"])] - method
            is_primary = row["primary"] == "True"
            tail = 0.025 / 24 if is_primary else 0.025
            low, high = np.quantile(gain[draws].mean(axis=1), [tail, 1 - tail])
            for field, actual in (("mean_loss", method.mean()), ("mean_gain", gain.mean()), ("ci_low", low), ("ci_high", high)):
                close(row[field], actual)
            if is_primary:
                supported = low > 0 and gain.mean() >= (10 if key[1] == "regional_time" else 100)
                assert supported == (row["practical_supported"] == "True")
                primary += 1
    assert primary == 24
    return sum(map(len, comparisons.values()))


def verify_grid(means):
    contrasts = rows("geolife_grid_width_contrasts.csv")
    assert len(contrasts) == 36
    count = 14
    tail = 0.025 / len(contrasts)
    draws = np.random.default_rng(20261126).integers(count, size=(100_000, count))
    critical = t.ppf(1 - tail, count - 1)
    for row in contrasts:
        key = row["condition"], "regional_time", int(row["cell_m"])
        gain = means[(*key, "linear")] - means[(*key, "pchip")]
        average = gain.mean()
        low, high = np.quantile(gain[draws].mean(axis=1), [tail, 1 - tail])
        half_width = critical * gain.std(ddof=1) / np.sqrt(count)
        for field, actual in (
            ("mean_gain_s", average), ("bootstrap_low_s", low), ("bootstrap_high_s", high),
            ("paired_t_low_s", average - half_width), ("paired_t_high_s", average + half_width),
        ):
            close(row[field], actual)
        supported = min(low, average - half_width) > 0 and average >= 10
        assert supported == (row["both_support_improvement"] == "True")
    return len(contrasts)


def verify_floors():
    by_condition = defaultdict(list)
    for row in rows("distance_floor_group_aggregates.csv"):
        by_condition[tuple(row[field] for field in FLOOR_KEY)].append(row)
    for row in rows("distance_floor_summary.csv"):
        groups = by_condition.pop(tuple(row[field] for field in FLOOR_KEY))
        floor = mean(float(group["mean_error_floor_m"]) for group in groups)
        linear = mean(float(group["linear_MAE_m"]) for group in groups)
        assert int(row["groups"]) == len(groups)
        assert int(row["windows"]) == sum(int(group["windows"]) for group in groups)
        for field, actual in (
            ("mean_error_floor_m", floor), ("linear_MAE_m", linear),
            ("maximum_possible_mean_gain_m", linear - floor),
            ("fraction_linear_MAE_structurally_unavoidable", floor / linear if linear else 0),
            ("fraction_cases_positive_floor", mean(float(group["fraction_positive"]) for group in groups)),
            ("fraction_cases_floor_above100m", mean(float(group["fraction_above_100_m"]) for group in groups)),
        ):
            close(row[field], actual)
    assert not by_condition
    return len(rows("distance_floor_summary.csv"))


if __name__ == "__main__":
    means = metric_means()
    source, grid, floors = verify_source(means), verify_grid(means), verify_floors()
    print(f"Reproduced {source} GeoLife contrasts, {grid} grid-width contrasts and {floors} distance-floor summaries.")
