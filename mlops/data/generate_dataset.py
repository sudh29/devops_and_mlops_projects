"""
Data generator for Predictive Equipment Maintenance dataset.
Uses Python standard library for zero-dependency dataset generation,
with pandas fallback if available.
"""
import csv
import math
import random
from pathlib import Path

def generate_data_records(n_samples: int = 5000, random_seed: int = 42):
    random.seed(random_seed)
    records = []

    for _ in range(n_samples):
        air_temp = round(random.gauss(300.0, 2.0), 2)
        process_temp = round(air_temp + random.gauss(10.0, 1.0), 2)
        rotational_speed = round(random.gauss(1500.0, 180.0), 1)
        torque = round(random.gauss(40.0, 10.0), 2)
        tool_wear = round(random.uniform(0.0, 240.0), 1)

        # Power output calculation (kW)
        power = (2 * math.pi * rotational_speed * torque) / 60000.0

        # Failure logic
        temp_diff = process_temp - air_temp
        heat_failure = (temp_diff < 8.6) and (rotational_speed < 1380.0)
        power_failure = (power < 3.5) or (power > 9.0)
        tool_failure = (tool_wear > 200.0) and (random.random() > 0.8)

        failure = 1 if (heat_failure or power_failure or tool_failure) else 0

        records.append({
            "air_temperature_k": air_temp,
            "process_temperature_k": process_temp,
            "rotational_speed_rpm": rotational_speed,
            "torque_nm": torque,
            "tool_wear_min": tool_wear,
            "failure": failure
        })

    return records

def generate_data(n_samples: int = 5000, random_seed: int = 42):
    try:
        import pandas as pd
        records = generate_data_records(n_samples, random_seed)
        return pd.DataFrame(records)
    except ImportError:
        return generate_data_records(n_samples, random_seed)

def save_csv(records, output_path: Path):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "air_temperature_k",
        "process_temperature_k",
        "rotational_speed_rpm",
        "torque_nm",
        "tool_wear_min",
        "failure"
    ]
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

if __name__ == "__main__":
    out_dir = Path(__file__).resolve().parent
    out_path = out_dir / "sensor_data.csv"
    data = generate_data_records(n_samples=5000)
    save_csv(data, out_path)
    failure_count = sum(r["failure"] for r in data)
    print(f"[SUCCESS] Generated {len(data)} telemetry records saved to: {out_path}")
    print(f"Total Failures: {failure_count} ({failure_count / len(data):.2%})")
