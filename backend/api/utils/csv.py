import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)

class DataAnalysisError(Exception):
    pass

class CSVProcessor:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.columns()

    def columns(self):
        self.numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        self.categorical_cols = self.df.select_dtypes(exclude=[np.number]).columns.tolist()

    def clean_data(self):
        for col in self.numeric_cols:
            if self.df[col].isnull().any():
                self.df[col] = self.df[col].fillna(self.df[col].median())
        
        for col in self.categorical_cols:
            if self.df[col].isnull().any():
                self.df[col] = self.df[col].fillna("Unknown")

    def handle_outliers(self, strategy="cap"):
        outlier = {}

        for col in self.numeric_cols:
            q1, q3 = self.df[col].quantile([0.25, 0.75])
            iqr = q3 - q1
            if iqr == 0:
                continue

            lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
            mask = (self.df[col] < lower) | (self.df[col] > upper)

            if mask.any():
                outlier[col] = int(mask.sum())
                if strategy == "cap":
                    self.df[col] = self.df[col].clip(lower, upper)

        self.outlier_counts = outlier
        return outlier


    def get_stats(self):
        return self.df[self.numeric_cols].describe().round(2).to_dict()
    
    def equipment_distribution(self):
        if "Type" not in self.df.columns:
            return {}
        return self.df["Type"].value_counts().to_dict()


def process_csv(file_path: str):
    try:
        df = pd.read_csv(file_path)
    except Exception:
        logger.exception("Could not read CSV file")
        raise

    processor = CSVProcessor(df)

    try:
        processor.clean_data()
        processor.handle_outliers()
    except Exception:
        logger.exception("Data cleanup failed")
        raise

    return (
        processor.df,
        {
            "total_rows": len(processor.df),
            "stats": processor.get_stats(),
            "outliers": processor.outlier_counts,
            "equipment_distribution": processor.equipment_distribution(),
            "columns": processor.df.columns.tolist(),
        },
    )
