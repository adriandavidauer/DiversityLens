"""
Intersectional demographic analysis for DiversityLens CSV output.
Produces heatmaps and tables showing combined demographic distributions.
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd

CSV_PATH = "demographic_results.csv"

# --- Load ---
df = pd.read_csv(CSV_PATH)
total = len(df)
print(f"Total faces: {total}\n")


# --- 1. Gender x Race heatmap ---
gender_race = df.groupby(["gender", "race"]).size().unstack(fill_value=0)
gender_race_pct = (gender_race / total * 100).round(1)

print("=== Gender × Race (%) ===")
print(gender_race_pct.to_string())
print()

fig, ax = plt.subplots(figsize=(8, 4))
im = ax.imshow(gender_race_pct.values, cmap="YlOrRd", aspect="auto")

ax.set_xticks(range(len(gender_race_pct.columns)))
ax.set_xticklabels(gender_race_pct.columns, rotation=30, ha="right")
ax.set_yticks(range(len(gender_race_pct.index)))
ax.set_yticklabels(gender_race_pct.index)
ax.set_xlabel("Race")
ax.set_ylabel("Gender")
ax.set_title("Gender × Race Distribution (% of total)")

for i in range(len(gender_race_pct.index)):
    for j in range(len(gender_race_pct.columns)):
        val = gender_race_pct.values[i, j]
        ax.text(j, i, f"{val}%", ha="center", va="center", fontsize=9,
                color="black" if val < 20 else "white")

plt.colorbar(im, ax=ax, label="% of total")
plt.tight_layout()
plt.savefig("heatmap_gender_race.png", dpi=150)
print("Saved: heatmap_gender_race.png")


# --- 2. Gender x Age Group heatmap ---
# Bin ages into groups
bins = [0, 18, 30, 45, 60, 120]
labels = ["<18", "18–30", "31–45", "46–60", "60+"]
df["age_group"] = pd.cut(df["age"], bins=bins, labels=labels, right=False)

gender_age = df.groupby(["gender", "age_group"], observed=True).size().unstack(fill_value=0)
gender_age_pct = (gender_age / total * 100).round(1)

print("=== Gender × Age Group (%) ===")
print(gender_age_pct.to_string())
print()

fig, ax = plt.subplots(figsize=(8, 4))
im = ax.imshow(gender_age_pct.values, cmap="YlGnBu", aspect="auto")

ax.set_xticks(range(len(gender_age_pct.columns)))
ax.set_xticklabels(gender_age_pct.columns)
ax.set_yticks(range(len(gender_age_pct.index)))
ax.set_yticklabels(gender_age_pct.index)
ax.set_xlabel("Age Group")
ax.set_ylabel("Gender")
ax.set_title("Gender × Age Group Distribution (% of total)")

for i in range(len(gender_age_pct.index)):
    for j in range(len(gender_age_pct.columns)):
        val = gender_age_pct.values[i, j]
        ax.text(j, i, f"{val}%", ha="center", va="center", fontsize=9,
                color="black" if val < 20 else "white")

plt.colorbar(im, ax=ax, label="% of total")
plt.tight_layout()
plt.savefig("heatmap_gender_age.png", dpi=150)
print("Saved: heatmap_gender_age.png")


# --- 3. Race x Age Group heatmap ---
race_age = df.groupby(["race", "age_group"], observed=True).size().unstack(fill_value=0)
race_age_pct = (race_age / total * 100).round(1)

print("=== Race × Age Group (%) ===")
print(race_age_pct.to_string())
print()

fig, ax = plt.subplots(figsize=(9, 5))
im = ax.imshow(race_age_pct.values, cmap="PuBuGn", aspect="auto")

ax.set_xticks(range(len(race_age_pct.columns)))
ax.set_xticklabels(race_age_pct.columns)
ax.set_yticks(range(len(race_age_pct.index)))
ax.set_yticklabels(race_age_pct.index)
ax.set_xlabel("Age Group")
ax.set_ylabel("Race")
ax.set_title("Race × Age Group Distribution (% of total)")

for i in range(len(race_age_pct.index)):
    for j in range(len(race_age_pct.columns)):
        val = race_age_pct.values[i, j]
        ax.text(j, i, f"{val}%", ha="center", va="center", fontsize=9,
                color="black" if val < 15 else "white")

plt.colorbar(im, ax=ax, label="% of total")
plt.tight_layout()
plt.savefig("heatmap_race_age.png", dpi=150)
print("Saved: heatmap_race_age.png")


# --- 4. Top 10 intersectional combos (Gender + Race + Age) ---
triple = df.groupby(["gender", "race", "age_group"], observed=True).size().reset_index(name="count")
triple["pct"] = (triple["count"] / total * 100).round(1)
triple = triple.sort_values("count", ascending=False)

print("=== Top 10 Gender × Race × Age Group combinations ===")
print(triple.head(10).to_string(index=False))
print()

# Bar chart of top 10
top10 = triple.head(10).copy()
top10["label"] = top10["gender"] + "\n" + top10["race"] + "\n" + top10["age_group"].astype(str)

fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.bar(range(len(top10)), top10["pct"], color="steelblue")
ax.set_xticks(range(len(top10)))
ax.set_xticklabels(top10["label"], fontsize=8)
ax.set_ylabel("% of total faces")
ax.set_title("Top 10 Intersectional Groups (Gender × Race × Age)")
ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("%.1f%%"))

for bar, pct in zip(bars, top10["pct"]):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1,
            f"{pct}%", ha="center", va="bottom", fontsize=8)

plt.tight_layout()
plt.savefig("intersectional_top10.png", dpi=150)
print("Saved: intersectional_top10.png")

print("\nDone. 4 files saved.")
