import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

PREDICTIONS_PATH = PROJECT_ROOT / "models" / "predictions.csv"
RESULTS_PATH = PROJECT_ROOT / "models" / "model_results.csv"
IMAGES_DIR = PROJECT_ROOT / "images"
IMAGES_DIR.mkdir(exist_ok=True)

BIKE_GREEN = "#52B788"
DARK_GREEN = "#2D6A4F"


if __name__ == "__main__":
    predictions = pd.read_csv(PREDICTIONS_PATH)
    results = pd.read_csv(RESULTS_PATH)

    model_labels = {
        "Linear Regression": "Regresja liniowa",
        "Random Forest": "Las losowy"
    }

    results["Model"] = results["Model"].replace(model_labels)

    # 1. Wartości rzeczywiste a przewidywane
    plt.figure(figsize=(7, 6))
    sns.scatterplot(
        data=predictions,
        x="Actual",
        y="Predicted",
        alpha=0.4,
        color=BIKE_GREEN
    )

    min_value = min(predictions["Actual"].min(), predictions["Predicted"].min())
    max_value = max(predictions["Actual"].max(), predictions["Predicted"].max())

    plt.plot(
        [min_value, max_value],
        [min_value, max_value],
        color=DARK_GREEN,
        linestyle="--",
        linewidth=2
    )

    plt.title("Wartości rzeczywiste a przewidywane")
    plt.xlabel("Rzeczywista liczba wypożyczeń")
    plt.ylabel("Przewidywana liczba wypożyczeń")
    plt.tight_layout()
    plt.savefig(
        IMAGES_DIR / "07_actual_vs_predicted.png",
        dpi=300,
        bbox_inches="tight"
    )
    plt.close()

    # 2. Porównanie modeli według RMSE
    plt.figure(figsize=(8, 5))
    ax = sns.barplot(
        data=results,
        x="Model",
        y="RMSE",
        color=DARK_GREEN
    )

    plt.title("Porównanie modeli według RMSE")
    plt.xlabel("Model")
    plt.ylabel("RMSE")
    plt.xticks(rotation=15, ha="right")

    for container in ax.containers:
        ax.bar_label(container, fmt="%.2f", padding=3)

    plt.tight_layout()
    plt.savefig(
        IMAGES_DIR / "08_model_comparison_rmse.png",
        dpi=300,
        bbox_inches="tight"
    )
    plt.close()

    # 3. Porównanie modeli według R2
    plt.figure(figsize=(8, 5))
    ax = sns.barplot(
        data=results,
        x="Model",
        y="R2",
        color=BIKE_GREEN
    )

    plt.title("Porównanie modeli według R2")
    plt.xlabel("Model")
    plt.ylabel("R2")
    plt.ylim(0, 1)
    plt.xticks(rotation=15, ha="right")

    for container in ax.containers:
        ax.bar_label(container, fmt="%.3f", padding=3)

    plt.tight_layout()
    plt.savefig(
        IMAGES_DIR / "09_model_comparison_r2.png",
        dpi=300,
        bbox_inches="tight"
    )
    plt.close()
