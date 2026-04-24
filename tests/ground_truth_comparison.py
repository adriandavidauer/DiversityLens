"""
Ground-Truth Comparison Script for UTKFace Dataset
Compares DiversityLens predictions against UTKFace filename annotations.

UTKFace filename format: [age]_[gender]_[race]_[date&time].jpg
  Gender: 0 = Male, 1 = Female
  Race:   0 = White, 1 = Black, 2 = Asian, 3 = Indian, 4 = Others
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# === UTKFace label mappings ===
UTK_GENDER_MAP = {0: "Man", 1: "Woman"}
UTK_RACE_MAP = {0: "white", 1: "black", 2: "asian", 3: "indian", 4: "others"}

# DeepFace race labels → UTKFace race labels (mapping)
DEEPFACE_TO_UTK_RACE = {
    "white": "white",
    "black": "black",
    "asian": "asian",
    "indian": "indian",
    "middle eastern": "others",
    "latino hispanic": "others",
}


def parse_utk_filename(filepath: str) -> dict | None:
    """Extract ground-truth labels from UTKFace filename."""
    filename = Path(filepath).name
    parts = filename.split("_")
    if len(parts) < 4:
        return None
    try:
        age = int(parts[0])
        gender_code = int(parts[1])
        race_code = int(parts[2])
        if gender_code not in UTK_GENDER_MAP or race_code not in UTK_RACE_MAP:
            return None
        return {
            "gt_age": age,
            "gt_gender": UTK_GENDER_MAP[gender_code],
            "gt_race": UTK_RACE_MAP[race_code],
        }
    except (ValueError, IndexError):
        return None


def run_comparison(csv_path: str):
    """Run full ground-truth comparison analysis."""
    print("=" * 60)
    print("DiversityLens Ground-Truth Comparison — UTKFace")
    print("=" * 60)

    # Load predictions
    df = pd.read_csv(csv_path)
    print(f"\nTotal predictions loaded: {len(df)}")

    # Parse ground-truth from filenames
    gt_data = df["file"].apply(parse_utk_filename)
    valid_mask = gt_data.notna()
    print(f"Successfully parsed ground-truth: {valid_mask.sum()}")
    print(f"Failed to parse: {(~valid_mask).sum()}")

    df = df[valid_mask].copy()
    gt_df = pd.DataFrame(gt_data[valid_mask].tolist())
    df = pd.concat([df.reset_index(drop=True), gt_df.reset_index(drop=True)], axis=1)

    # === 1. GENDER ACCURACY ===
    print("\n" + "=" * 60)
    print("1. GENDER CLASSIFICATION")
    print("=" * 60)

    gender_acc = accuracy_score(df["gt_gender"], df["gender"])
    print(f"\nOverall Accuracy: {gender_acc:.1%}")

    print("\nClassification Report:")
    print(classification_report(df["gt_gender"], df["gender"], digits=3))

    print("Confusion Matrix:")
    gender_labels = ["Man", "Woman"]
    gender_cm = confusion_matrix(df["gt_gender"], df["gender"], labels=gender_labels)
    gender_cm_df = pd.DataFrame(gender_cm, index=gender_labels, columns=gender_labels)
    print(gender_cm_df.to_string())

    # === 2. RACE ACCURACY ===
    print("\n" + "=" * 60)
    print("2. RACE CLASSIFICATION")
    print("=" * 60)

    # Map DeepFace predictions to UTK categories
    df["pred_race_mapped"] = df["race"].str.lower().map(DEEPFACE_TO_UTK_RACE)
    race_valid = df.dropna(subset=["pred_race_mapped"])
    print(f"\nMapped predictions: {len(race_valid)} / {len(df)}")

    race_acc = accuracy_score(race_valid["gt_race"], race_valid["pred_race_mapped"])
    print(f"Overall Accuracy: {race_acc:.1%}")

    print("\nClassification Report:")
    race_labels = ["white", "black", "asian", "indian", "others"]
    print(classification_report(
        race_valid["gt_race"], race_valid["pred_race_mapped"],
        labels=race_labels, digits=3, zero_division=0
    ))

    print("Confusion Matrix:")
    race_cm = confusion_matrix(
        race_valid["gt_race"], race_valid["pred_race_mapped"],
        labels=race_labels
    )
    race_cm_df = pd.DataFrame(race_cm, index=race_labels, columns=race_labels)
    print(race_cm_df.to_string())

    # Per-race accuracy
    print("\nPer-Race Accuracy:")
    for label in race_labels:
        mask = race_valid["gt_race"] == label
        if mask.sum() > 0:
            acc = accuracy_score(
                race_valid.loc[mask, "gt_race"],
                race_valid.loc[mask, "pred_race_mapped"]
            )
            print(f"  {label:20s}: {acc:.1%}  (n={mask.sum()})")

    # === 3. AGE ESTIMATION ===
    print("\n" + "=" * 60)
    print("3. AGE ESTIMATION")
    print("=" * 60)

    age_error = df["age"] - df["gt_age"]
    mae = age_error.abs().mean()
    mse = (age_error ** 2).mean()
    rmse = np.sqrt(mse)
    median_ae = age_error.abs().median()

    print(f"\nMean Absolute Error (MAE):   {mae:.2f} years")
    print(f"Median Absolute Error:       {median_ae:.2f} years")
    print(f"Root Mean Square Error:      {rmse:.2f} years")
    print(f"Mean Error (bias):           {age_error.mean():.2f} years")

    # Age error by age group
    print("\nMAE by Age Group:")
    bins = [0, 7, 14, 21, 28, 35, 42, 49, 56, 63, 70, 120]
    labels_age = ["0-7", "8-14", "15-21", "22-28", "29-35",
                  "36-42", "43-49", "50-56", "57-63", "64-70", "70+"]
    df["gt_age_group"] = pd.cut(df["gt_age"], bins=bins, labels=labels_age, right=False)

    age_group_stats = df.groupby("gt_age_group", observed=False).apply(
        lambda g: pd.Series({
            "n": len(g),
            "MAE": (g["age"] - g["gt_age"]).abs().mean() if len(g) > 0 else 0,
            "Mean Error": (g["age"] - g["gt_age"]).mean() if len(g) > 0 else 0,
        })
    )
    print(age_group_stats.to_string(float_format="%.2f"))

    # === 4. SUMMARY TABLE ===
    print("\n" + "=" * 60)
    print("4. SUMMARY")
    print("=" * 60)
    print(f"\n{'Metric':<35} {'Value':>10}")
    print("-" * 47)
    print(f"{'Total faces analyzed':<35} {len(df):>10}")
    print(f"{'Gender accuracy':<35} {gender_acc:>10.1%}")
    print(f"{'Race accuracy':<35} {race_acc:>10.1%}")
    print(f"{'Age MAE':<35} {mae:>10.2f}")
    print(f"{'Age RMSE':<35} {rmse:>10.2f}")

    return df


if __name__ == "__main__":
    csv_file = sys.argv[1] if len(sys.argv) > 1 else "Demographic_Results.csv"
    result_df = run_comparison(csv_file)
