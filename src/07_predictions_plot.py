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

    plt.figure(figsize=(7, 6))
    sns.scatterplot(
        data=predictions,
        x="Actual",
        y="Predicted",
        alpha=0.4,
        color=BIKE_GREEN
    )
    plt.title("Actual vs Predicted Bike Rentals")
    plt.xlabel("Actual rented bike count")
    plt.ylabel("Predicted rented bike count")
    plt.tight_layout()
    plt.savefig(
        IMAGES_DIR / "07_actual_vs_predicted.png",
        dpi=300,
        bbox_inches="tight"
    )
    plt.close()

    plt.figure(figsize=(8, 5))
    sns.barplot(
        data=results,
        x="Model",
        y="RMSE",
        color=DARK_GREEN
    )
    plt.title("Model Comparison by RMSE")
    plt.xlabel("Model")
    plt.ylabel("RMSE")
    plt.xticks(rotation=15, ha="right")
    plt.tight_layout()
    plt.savefig(
        IMAGES_DIR / "08_model_comparison_rmse.png",
        dpi=300,
        bbox_inches="tight"
    )
    plt.close()

    plt.figure(figsize=(8, 5))
    sns.barplot(
        data=results,
        x="Model",
        y="R2",
        color=BIKE_GREEN
    )
    plt.title("Model Comparison by R2 Score")
    plt.xlabel("Model")
    plt.ylabel("R2")
    plt.ylim(0, 1)
    plt.xticks(rotation=15, ha="right")
    plt.tight_layout()
    plt.savefig(
        IMAGES_DIR / "09_model_comparison_r2.png",
        dpi=300,
        bbox_inches="tight"
    )
    plt.close()

    print("Prediction plots saved.")