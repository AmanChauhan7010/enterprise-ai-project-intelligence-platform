"""
XGBoost Machine Learning Engine for Project Risk Classification.
Trains, evaluates, persists, and performs inference on enterprise project risk profiles.
"""
import os
from typing import Dict, Tuple, Any, List, Optional
import pandas as pd
import numpy as np
import joblib
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from utils.logger import get_logger

logger = get_logger(__name__)

FEATURES = [
    "Budget",
    "Actual_Cost",
    "Progress",
    "Sprint_Velocity",
    "Team_Size",
    "Open_Bugs",
    "Remaining_Days"
]

TARGET_MAP = {"Low": 0, "Medium": 1, "High": 2}
TARGET_MAP_INV = {0: "Low", 1: "Medium", 2: "High"}
MODEL_PATH = "models/xgb_risk_model.joblib"


class RiskPredictionEngine:
    """
    Encapsulates XGBoost model training and real-time inference logic.
    """
    def __init__(self, model_path: str = MODEL_PATH):
        self.model_path = model_path
        self.model: Optional[XGBClassifier] = None
        self.feature_names = FEATURES

    def train_and_persist(self, data_path: str = "data/projects.csv") -> Tuple[XGBClassifier, Dict[str, float]]:
        """
        Trains the XGBoost risk classification model on synthetic historical project data.
        
        Args:
            data_path (str): Path to projects CSV.
            
        Returns:
            Tuple[XGBClassifier, Dict[str, float]]: Trained model instance and evaluation metrics.
        """
        logger.info(f"Loading historical project data from {data_path} for XGBoost training...")
        if not os.path.exists(data_path):
            raise FileNotFoundError(f"Project dataset not found at {data_path}")

        df = pd.read_csv(data_path)
        
        # Verify required features exist
        missing_cols = [c for c in self.feature_names + ["Risk"] if c not in df.columns]
        if missing_cols:
            raise ValueError(f"Dataset missing essential columns: {missing_cols}")

        X = df[self.feature_names].copy()
        y = df["Risk"].map(TARGET_MAP)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

        logger.info("Fitting XGBClassifier pipeline...")
        self.model = XGBClassifier(
            n_estimators=120,
            learning_rate=0.08,
            max_depth=4,
            subsample=0.85,
            colsample_bytree=0.85,
            random_state=42,
            eval_metric="mlogloss"
        )
        self.model.fit(X_train, y_train)

        y_pred = self.model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        logger.info(f"XGBoost training completed. Test Accuracy: {acc * 100:.2f}%")

        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        joblib.dump(self.model, self.model_path)
        logger.info(f"Saved trained risk model artifact to {self.model_path}")

        metrics = {
            "accuracy": float(acc),
            "train_samples": len(X_train),
            "test_samples": len(X_test)
        }
        return self.model, metrics

    def load_model(self) -> XGBClassifier:
        """
        Loads persisted XGBoost model artifact from disk.
        
        Returns:
            XGBClassifier: Loaded model instance.
        """
        if self.model is not None:
            return self.model

        if not os.path.exists(self.model_path):
            logger.warning(f"Model artifact not found at {self.model_path}. Auto-training...")
            self.train_and_persist()

        self.model = joblib.load(self.model_path)
        return self.model

    def predict(self, input_features: Dict[str, float]) -> Tuple[str, Dict[str, float], pd.DataFrame]:
        """
        Performs real-time inference for a project feature profile.
        
        Args:
            input_features (Dict[str, float]): Feature key-value pairs.
            
        Returns:
            Tuple[str, Dict[str, float], pd.DataFrame]: Predicted label, probabilities dict, feature importances.
        """
        model = self.load_model()
        
        input_df = pd.DataFrame([input_features])[self.feature_names]
        
        probs_raw = model.predict_proba(input_df)[0]
        pred_idx = int(np.argmax(probs_raw))
        pred_label = TARGET_MAP_INV[pred_idx]

        probs_dict = {TARGET_MAP_INV[i]: float(probs_raw[i]) for i in range(len(probs_raw))}

        # Extract feature importances
        importances = model.feature_importances_
        df_imp = pd.DataFrame({
            "Feature": self.feature_names,
            "Importance": importances
        }).sort_values(by="Importance", ascending=False)

        return pred_label, probs_dict, df_imp


if __name__ == "__main__":
    engine = RiskPredictionEngine()
    engine.train_and_persist()
