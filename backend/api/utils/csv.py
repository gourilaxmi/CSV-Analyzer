import pandas as pd
import numpy as np
import logging
logger = logging.getLogger(__name__)

class DataAnalysisError(Exception):
    pass

class CSVProcessor:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.identify_columns()

    def identify_columns(self):
        """Separates numeric and categorical columns for targeted processing."""
        self.numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        self.categorical_cols = self.df.select_dtypes(exclude=[np.number]).columns.tolist()

    def clean_data(self):
        # replace Nan with median for numerical and unknown for categorical values
        for col in self.numeric_cols:
            if self.df[col].isnull().any():
                self.df[col] = self.df[col].fillna(self.df[col].median())
        
        for col in self.categorical_cols:
            if self.df[col].isnull().any():
                self.df[col] = self.df[col].fillna("Unknown")

    def handle_outliers(self, strategy="cap") -> dict:
        # use iqr to find if outliers exist. if they exist boxplot is plotted. 
        outlier_counts = {}

        for col in self.numeric_cols:
            q1, q3 = self.df[col].quantile([0.25, 0.75])
            iqr = q3 - q1
            
            if iqr == 0:
                continue

            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
            
            mask = (self.df[col] < lower_bound) | (self.df[col] > upper_bound)

            if mask.any():
                outlier_counts[col] = int(mask.sum())
                if strategy == "cap":
                    # Capping ensures extreme values don't skew the final averages
                    self.df[col] = self.df[col].clip(lower_bound, upper_bound)

        self.outlier_counts = outlier_counts
        return outlier_counts

    def get_stats(self) -> dict:
        return self.df[self.numeric_cols].describe().round(2).to_dict()
    
    def equip_dist(self) -> dict:
        # frequency of each equipment type
        if "Type" not in self.df.columns:
            return {}
        return self.df["Type"].value_counts().to_dict()
    
    def equip_averages(self) -> dict:
        # finding mean of each numerical parameter for each type of equipment
        if "Type" not in self.df.columns or not self.numeric_cols:
            return {}
        
        averages = self.df.groupby("Type")[self.numeric_cols].mean().round(2)
        return averages.to_dict(orient='index')


def process_csv(file_path: str):

    try:
        df = pd.read_csv(file_path)
    except Exception:
        logger.exception(f"Fatal error: Could not read CSV file at {file_path}")
        raise

    processor = CSVProcessor(df)

    try:
        processor.clean_data()
        processor.handle_outliers(strategy="cap")
    except Exception:
        logger.exception("Preprocessing of data couldn't be completed.")
        raise

    return (
        processor.df,
        {
            "total_rows": len(processor.df),
            "stats": processor.get_stats(),
            "outliers": processor.outlier_counts,
            "equip_dist": processor.equip_dist(),
            "equip_averages": processor.equip_averages(),
            "columns": processor.df.columns.tolist(),
        },
    )