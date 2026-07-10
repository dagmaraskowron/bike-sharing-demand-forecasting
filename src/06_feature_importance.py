import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_PATH = PROJECT_ROOT / "data" / "bike_sharing_features.csv"
MODEL_PATH = PROJECT_ROOT / "models" / "best_model.joblib"
IMAGES_DIR = PROJECT_ROOT / "images"
IMAGES_DIR.mkdir(exist_ok=True)

TARGET_COLUMN = "Rented_Bike_Count"

BIKE_GREEN = "#52B788"
DARK_GREEN = "#2D6A4F"


def prepare_data(df: pd.DataFrame):
    X = df.drop(columns=[TARGET_COLUMN])
    X = pd.get_dummies(X, drop_first=True)

    return X


if __name__ == "__main__":
    df = pd.read_csv(DATA_PATH)
    X = prepare_data(df)

    model = joblib.load(MODEL_PATH)

    if not hasattr(model, "feature_importances_"):
        raise AttributeError("Selected model does not provide feature_importances_.")

    importances = pd.DataFrame({
        "Feature": X.columns,
        "Importance": model.feature_importances_
    }).sort_values(by="Importance", ascending=False)

    print("Top 15 most important features:")
    print(importances.head(15))

    importances.to_csv(
        PROJECT_ROOT / "models" / "feature_importance.csv",
        index=False
    )

    top_features = importances.head(7).copy()

    feature_labels = {
        "TemperatureC": "Temperatura",
        "Hour": "Godzina",
        "Functioning_Day_Yes": "Działający system",
        "Solar_Radiation_MJ_m2": "Promieniowanie słoneczne",
        "Humiditypercent": "Wilgotność",
        "Rainfallmm": "Opady deszczu",
        "IsEveningPeak": "Godziny wieczorne",
        "Seasons_Winter": "Zima",
        "DayOfWeek": "Dzień tygodnia",
        "Dew_point_temperatureC": "Punkt rosy",
        "Wind_speed_m_s": "Prędkość wiatru",
        "Visibility_10m": "Widoczność",
        "Snowfall_cm": "Opady śniegu",
        "IsMorningPeak": "Godziny poranne",
        "Month": "Miesiąc"
    }

    top_features["Feature_Label"] = top_features["Feature"].map(feature_labels)
    top_features["Feature_Label"] = top_features["Feature_Label"].fillna(
        top_features["Feature"]
    )

    plt.figure(figsize=(9, 6))
    ax = sns.barplot(
        data=top_features,
        x="Importance",
        y="Feature_Label",
        color=BIKE_GREEN
    )

    plt.title("Najważniejsze cechy modelu")
    plt.xlabel("Ważność cechy")
    plt.ylabel("")

    for container in ax.containers:
        ax.bar_label(container, fmt="%.3f", padding=3)

    plt.tight_layout()
    plt.savefig(
        IMAGES_DIR / "06_feature_importance.png",
        dpi=300,
        bbox_inches="tight"
    )
    plt.close()

