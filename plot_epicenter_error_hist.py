"""
Plot epicenter error histogram.
"""

import sys
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

from eews_analyzer import EEWSAnalyzer


def plot_epicenter_error_histogram(analyzer, output_file="outputs/epicenter_error_hist.png", bins=20, dpi=300):
    """
    Create histogram of epicenter errors.

    Args:
        analyzer: EEWSAnalyzer instance with loaded data
        output_file: Output filename
        bins: Number of histogram bins
        dpi: Resolution in dots per inch
    """
    if not hasattr(analyzer, "df_analyzed"):
        analyzer.calculate_errors()

    df = analyzer.df_analyzed.dropna(subset=["Epicenter_Error_km"])

    Path(output_file).parent.mkdir(exist_ok=True, parents=True)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(df["Epicenter_Error_km"], bins=bins, color="steelblue", edgecolor="black", alpha=0.8)

    mean_err = df["Epicenter_Error_km"].mean()
    median_err = df["Epicenter_Error_km"].median()
    ax.axvline(mean_err, color="red", linestyle="--", linewidth=2, label=f"Mean: {mean_err:.2f} km")
    ax.axvline(median_err, color="green", linestyle="--", linewidth=2, label=f"Median: {median_err:.2f} km")

    ax.set_xlabel("Epicenter Error (km)", fontweight="bold")
    ax.set_ylabel("Number of Events", fontweight="bold")
    ax.set_title("Epicenter Error Histogram", fontweight="bold")
    ax.grid(True, alpha=0.3)
    ax.legend()

    fig.tight_layout()
    fig.savefig(output_file, dpi=dpi, bbox_inches="tight")
    plt.close(fig)

    print(f"Epicenter error histogram saved to: {output_file}")


if __name__ == "__main__":
    # Use command-line arguments or defaults
    if len(sys.argv) == 6:
        data_file = sys.argv[1]
        min_mag = float(sys.argv[2])
        max_depth = float(sys.argv[3])
        target_year = int(sys.argv[4])
        bins = int(sys.argv[5])
    else:
        data_file = "EEW_ALL-2014-2025.txt"
        min_mag = 5.0
        max_depth = 40.0
        target_year = 2025
        bins = 20

    print("\n" + "=" * 70)
    print("EPICENTER ERROR HISTOGRAM PLOTTER")
    print("=" * 70)
    print("\nConfiguration:")
    print(f"   Data File: {data_file}")
    print(f"   Magnitude >= {min_mag}")
    print(f"   Depth <= {max_depth} km")
    print(f"   Year == {target_year}")
    print(f"   Bins = {bins}")
    print("=" * 70 + "\n")

    analyzer = EEWSAnalyzer(data_file)
    analyzer.load_data()

    original_count = len(analyzer.df)
    analyzer.df["Origin_Time"] = pd.to_datetime(analyzer.df["Origin_Time"], errors="coerce")
    analyzer.df = analyzer.df[analyzer.df["Origin_Time"].dt.year == target_year]
    analyzer.df = analyzer.df[
        (analyzer.df["Cat_Mag"] >= min_mag)
        & (analyzer.df["Cat_Depth"] <= max_depth)
    ]
    filtered_count = len(analyzer.df)

    print(f"Filtered {filtered_count} events from {original_count} total events\n")

    analyzer.calculate_errors()
    plot_epicenter_error_histogram(analyzer, bins=bins)
    print("\nDone!")
