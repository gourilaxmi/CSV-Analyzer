import matplotlib.pyplot as plt
import seaborn as sns
import os

class CSVPlots:
    def __init__(self, df, output_dir):
        self.df = df
        self.output_dir = output_dir
        self.outlier_counts = {} 
        os.makedirs(output_dir, exist_ok=True)
        sns.set_theme(style="ticks")

    def save_plot(self, filename):
        path = os.path.join(self.output_dir, filename)
        plt.tight_layout()
        plt.savefig(path, dpi=300, bbox_inches='tight')
        plt.close('all')
        return path

    def histogram(self):
        paths = []
        numeric_cols = self.df.select_dtypes(include=['number']).columns
        for col in numeric_cols:
            plt.figure(figsize=(10, 6))
            sns.histplot(self.df[col], color='skyblue')
            plt.title(f'{col}')
            paths.append(self.save_plot(f"{col}_dist.png"))
        return paths
    
    def boxplots(self):
        paths = []
        for col, count in self.outlier_counts.items():
            if col not in self.df: continue
            plt.figure(figsize=(8, 4))
            sns.boxplot(x=self.df[col], orient="h")
            plt.title(f"Outlier Distribution: {col}")
            paths.append(self.save_plot(f"{col}_boxplot.png"))
        return paths

    def corr_matrix(self):
        if len(self.df.select_dtypes(include=['number']).columns) < 2: return None
        plt.figure(figsize=(12, 10))
        sns.heatmap(self.df.corr(numeric_only=True), annot=True, cmap='coolwarm', fmt=".2f")
        plt.title('Correlation Matrix')
        return self.save_plot("correlation_matrix.png")

    def plots(self):
        
        all_paths = []
        all_paths.extend(self.histogram())
        all_paths.extend(self.boxplots())
        corr_path = self.corr_matrix()
        if corr_path:
            all_paths.append(corr_path)
        return all_paths

def visualization_csv(df, output_dir, outlier_counts=None):
    viz = CSVPlots(df, output_dir)
    if outlier_counts:
        viz.outlier_counts = outlier_counts
    return viz