"""
Data Drift and Distribution Shift Detector.
Performs two-sample Kolmogorov-Smirnov (KS) tests between reference training
distributions and production inference traffic.
"""
import csv
import json
import math
from pathlib import Path
from typing import Dict, Any, List

def compute_mean_std(values: List[float]):
    if not values:
        return 0.0, 0.0
    mean = sum(values) / len(values)
    variance = sum((x - mean) ** 2 for x in values) / max(len(values) - 1, 1)
    return mean, math.sqrt(variance)

def two_sample_ks_statistic(sample1: List[float], sample2: List[float]):
    """Pure python calculation of the 2-sample KS supremum statistic."""
    s1 = sorted(sample1)
    s2 = sorted(sample2)
    n1, n2 = len(s1), len(s2)

    all_vals = sorted(list(set(s1 + s2)))
    max_diff = 0.0
    i1, i2 = 0, 0

    for v in all_vals:
        while i1 < n1 and s1[i1] <= v:
            i1 += 1
        while i2 < n2 and s2[i2] <= v:
            i2 += 1
        cdf1 = i1 / n1
        cdf2 = i2 / n2
        diff = abs(cdf1 - cdf2)
        if diff > max_diff:
            max_diff = diff

    # Approximate p-value based on asymptotic distribution
    en = math.sqrt((n1 * n2) / (n1 + n2))
    lambda_val = (en + 0.12 + 0.11 / en) * max_diff
    p_val = max(min(2.0 * math.exp(-2.0 * lambda_val * lambda_val), 1.0), 0.0)

    return max_diff, p_val

class DataDriftDetector:
    def __init__(self, reference_records: List[Dict[str, Any]], alpha: float = 0.05):
        self.reference_records = reference_records
        self.alpha = alpha
        self.features = [
            k for k in reference_records[0].keys() if k not in ["failure", "id"]
        ]

    def detect_drift(self, current_records: List[Dict[str, Any]]) -> Dict[str, Any]:
        report = {
            "drift_detected": False,
            "alpha_threshold": self.alpha,
            "metrics_per_feature": {},
            "drifted_features_count": 0,
            "total_features": len(self.features)
        }

        drifted_count = 0
        for feat in self.features:
            ref_vals = [float(r[feat]) for r in self.reference_records]
            curr_vals = [float(r[feat]) for r in current_records]

            ks_stat, p_val = two_sample_ks_statistic(ref_vals, curr_vals)
            is_drifted = bool(p_val < self.alpha)

            if is_drifted:
                drifted_count += 1

            ref_mean, _ = compute_mean_std(ref_vals)
            curr_mean, _ = compute_mean_std(curr_vals)

            report["metrics_per_feature"][feat] = {
                "ks_statistic": round(ks_stat, 4),
                "p_value": round(p_val, 6),
                "drift_detected": is_drifted,
                "reference_mean": round(ref_mean, 3),
                "current_mean": round(curr_mean, 3)
            }

        report["drifted_features_count"] = drifted_count
        report["drift_detected"] = drifted_count > 0
        return report

    def save_report(self, report: Dict[str, Any], output_path: Path):
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
        print(f"[DRIFT REPORT] Saved to {output_path}")

def run_drift_check():
    import sys
    sys.path.append(str(Path(__file__).resolve().parent.parent))
    from data.generate_dataset import generate_data_records

    reference_data = generate_data_records(n_samples=2000, random_seed=42)

    # Simulate production data with thermal drift (sensor overheating)
    drifted_prod_data = generate_data_records(n_samples=500, random_seed=999)
    for r in drifted_prod_data:
        r["air_temperature_k"] = round(r["air_temperature_k"] + 8.5, 2)

    detector = DataDriftDetector(reference_records=reference_data)
    report = detector.detect_drift(drifted_prod_data)

    print(f"Overall Drift Detected: {report['drift_detected']}")
    print(f"Features Drifted: {report['drifted_features_count']} / {report['total_features']}")
    for feat, m in report["metrics_per_feature"].items():
        flag = "[DRIFT!]" if m["drift_detected"] else "[OK]"
        print(f"  {flag} {feat:25s} | p-val: {m['p_value']:.4f} | KS: {m['ks_statistic']}")

    report_path = Path(__file__).resolve().parent / "drift_report.json"
    detector.save_report(report, report_path)
    return report

if __name__ == "__main__":
    run_drift_check()
