import pandas as pd
import joblib
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_PATH = PROJECT_ROOT / "data" / "bike_sharing_features.csv"
MODELS_DIR = PROJECT_ROOT / "models"
MODELS_DIR.mkdir(exist_ok=True)

MODEL_PATH = MODELS_DIR / "best_model.joblib"
PREDICTIONS_PATH = MODELS_DIR / "predictions.csv"

TARGET_COLUMN = "Rented_Bike_Count"


def prepare_data(df: pd.DataFrame):
    X = df.drop(columns=[TARGET_COLUMN])
    y = df[TARGET_COLUMN]

    X = pd.get_dummies(X, drop_first=True)

    return X, y


def evaluate_model(y_true, y_pred):

    mae = mean_absolute_error(y_true, y_pred)
    rmse = mean_squared_error(y_true, y_pred) ** 0.5
    r2 = r2_score(y_true, y_pred)

    return mae, rmse, r2


if __name__ == "__main__":
    df = pd.read_csv(DATA_PATH)

    X, y = prepare_data(df)

    print("Features shape:")
    print(X.shape)

    print("\nTarget statistics:")
    print(y.describe())

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    models = {
        "Linear Regression": LinearRegression(),
        "Random Forest": RandomForestRegressor(
            n_estimators=150,
            random_state=42,
            n_jobs=-1
        )
    }

    results = []
    best_model = None
    best_model_name = None
    best_rmse = float("inf")
    best_predictions = None

    for model_name, model in models.items():
        print(f"\n{model_name}")
        print("-" * 50)

        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        mae, rmse, r2 = evaluate_model(y_test, y_pred)

        print(f"MAE: {mae:.2f}")
        print(f"RMSE: {rmse:.2f}")
        print(f"R2: {r2:.4f}")

        results.append({
            "Model": model_name,
            "MAE": mae,
            "RMSE": rmse,
            "R2": r2
        })

        if rmse < best_rmse:
            best_rmse = rmse
            best_model = model
            best_model_name = model_name
            best_predictions = y_pred

    results_df = pd.DataFrame(results)
    results_df.to_csv(MODELS_DIR / "model_results.csv", index=False)

    predictions_df = pd.DataFrame({
        "Actual": y_test.values,
        "Predicted": best_predictions
    })

    predictions_df.to_csv(PREDICTIONS_PATH, index=False)

    joblib.dump(best_model, MODEL_PATH)

    print("\nModel comparison:")
    print(results_df)

    print("\nBest model:")
    print(best_model_name)

    print(f"\nBest model saved to: {MODEL_PATH}")
    print(f"Predictions saved to: {PREDICTIONS_PATH}")