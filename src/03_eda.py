import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_PATH = PROJECT_ROOT / "data" / "clean_bike_sharing.csv"
IMAGES_DIR = PROJECT_ROOT / "images"
IMAGES_DIR.mkdir(exist_ok=True)

BIKE_GREEN = "#52B788"
DARK_GREEN = "#2D6A4F"
LIGHT_GREEN = "#B7E4C7"


def save_plot(filename: str) -> None:
    plt.tight_layout()
    plt.savefig(IMAGES_DIR / filename, dpi=300, bbox_inches="tight")
    plt.close()


if __name__ == "__main__":
    df = pd.read_csv(DATA_PATH)

    print("Dataset shape:")
    print(df.shape)

    print("\nColumns:")
    print(df.columns.tolist())

    target = "Rented_Bike_Count"

    print("\nTarget statistics:")
    print(df[target].describe())

    plt.figure(figsize=(8, 5))
    sns.histplot(df[target], bins=40, color=LIGHT_GREEN)
    plt.title("Rozkład liczby wypożyczeń rowerów")
    plt.xlabel("Liczba wypożyczeń")
    plt.ylabel("Liczba obserwacji")
    save_plot("01_rented_bike_count_distribution.png")

    hourly_avg = df.groupby("Hour")[target].mean()

    plt.figure(figsize=(9, 5))
    sns.lineplot(
        x=hourly_avg.index,
        y=hourly_avg.values,
        marker="o",
        color=DARK_GREEN
    )
    plt.title("Średnia liczba wypożyczeń według godziny")
    plt.xlabel("Godzina")
    plt.ylabel("Średnia liczba wypożyczeń")
    plt.xticks(range(0, 24))
    save_plot("02_average_rentals_by_hour.png")

    season_avg = df.groupby("Seasons")[target].mean().sort_values(ascending=False)

    season_labels = {
        "Spring": "Wiosna",
        "Summer": "Lato",
        "Autumn": "Jesień",
        "Winter": "Zima"
    }

    season_avg.index = season_avg.index.map(season_labels)

    plt.figure(figsize=(8, 5))
    sns.barplot(
        x=season_avg.index,
        y=season_avg.values,
        color=BIKE_GREEN
    )
    plt.title("Średnia liczba wypożyczeń według pory roku")
    plt.xlabel("Pora roku")
    plt.ylabel("Średnia liczba wypożyczeń")
    save_plot("03_average_rentals_by_season.png")

    plt.figure(figsize=(8, 5))
    sns.scatterplot(
        data=df,
        x="TemperatureC",
        y=target,
        alpha=0.4,
        color=BIKE_GREEN
    )
    plt.title("Temperatura a liczba wypożyczeń")
    plt.xlabel("Temperatura")
    plt.ylabel("Liczba wypożyczeń")
    save_plot("04_temperature_vs_rentals.png")

    functioning_avg = df.groupby("Functioning_Day")[target].mean().sort_values(ascending=False)

    functioning_labels = {
        "Yes": "Tak",
        "No": "Nie"
    }

    functioning_avg.index = functioning_avg.index.map(functioning_labels)

    plt.figure(figsize=(7, 5))
    sns.barplot(
        x=functioning_avg.index,
        y=functioning_avg.values,
        color=LIGHT_GREEN
    )
    plt.title("Średnia liczba wypożyczeń według działania systemu")
    plt.xlabel("Czy system działał")
    plt.ylabel("Średnia liczba wypożyczeń")
    save_plot("05_average_rentals_by_functioning_day.png")

    numeric_df = df.select_dtypes(include=["int64", "float64"])

    plt.figure(figsize=(11, 8))
    sns.heatmap(
        numeric_df.corr(),
        cmap="Greens",
        linewidths=0.5
    )
    plt.title("Mapa korelacji zmiennych numerycznych")
    save_plot("06_correlation_heatmap.png")
