import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

#setting globalcolor to viridis
plt.rcParams['axes.prop_cycle'] = plt.cycler(color=sns.color_palette("viridis", 10))

class CSVPlots:
    def __init__(self, df, output_dir, equip_dist=None, equip_averages=None):
        self.df = df
        self.output_dir = output_dir
        self.outlier_counts = {} 
        self.equip_dist = equip_dist or {}
        self.equip_averages = equip_averages or {}
        os.makedirs(output_dir, exist_ok=True)
        sns.set_theme(style="ticks")

    def save_plot(self, filename):
        # save charts to charts in media folder
        path = os.path.join(self.output_dir, filename)
        plt.tight_layout()
        plt.savefig(path, dpi=300, bbox_inches='tight')
        plt.close('all')
        return path
    
    def boxplots(self):
        # box plots if oultiers exist
        outlier_plots = []
        
        for col, count in self.outlier_counts.items():
            if col not in self.df.columns: 
                continue
            
            plt.figure(figsize=(10, 4))
            
            sns.boxplot(x=self.df[col], orient="h", color=sns.color_palette("viridis")[3])
            
            plt.title(f"Outlier Distribution: {col} ({count} outliers detected)")
            sns.despine() 
            
            save_path = self.save_plot(f"outlier_{col}.png")
            outlier_plots.append(save_path)
            
        return outlier_plots

    def pie_chart(self):
        # pie chart for equipment type distribution
        if not self.equip_dist:
            return None
        
        labels = list(self.equip_dist.keys())
        sizes = list(self.equip_dist.values())
        
        plt.figure(figsize=(10, 10))
        
        colors = sns.color_palette('viridis', n_colors=len(labels))
        
        plt.pie(
            sizes, 
            labels=labels, 
            autopct='%1.1f%%',
            startangle=90,
            colors=colors,
        )
        
        plt.title('Equipment Type Distribution', fontsize=14, fontweight='bold')
        return self.save_plot("equip_dist_pie.png")

    def equipment_averages_chart(self):
        # bar charts for mean of each parameter for each equipment type
        if not self.equip_averages:
            return []
        
        avg_plots = []
        equipment_types = list(self.equip_averages.keys())
        fields = list(self.equip_averages[equipment_types[0]].keys()) if equipment_types else []

        for field in fields:
            plt.figure(figsize=(10, 5))
            
            values = [self.equip_averages[et].get(field, 0) for et in equipment_types]
            
            colors = sns.color_palette("viridis", len(equipment_types))
            
            bars = plt.bar(equipment_types, values, color=colors)
            
            plt.bar_label(bars, fmt='%.2f', padding=3)
            
            plt.title(f'Average {field} per Equipment Type')
            plt.ylabel('Value')
            sns.despine()
            
            avg_plots.append(self.save_plot(f"avg_{field}.png"))
        
        return avg_plots

    def corr_matrix(self):
        # corr matrix to find correlation between parameters
        numeric_df = self.df.select_dtypes(include=['number'])
        
        if numeric_df.shape[1] < 2: 
            return None
        
        plt.figure(figsize=(10, 8))
        
        sns.heatmap(
            numeric_df.corr(), 
            annot=True, 
            cmap='viridis', 
            fmt=".2f",
            square=True
        )
        
        plt.title('Parameter Correlation Matrix', fontsize=14, fontweight='bold')
        return self.save_plot("correlation_matrix.png")

    def plots(self):
        
        plots_pdf = []
        
        pie_path = self.pie_chart()
        if pie_path:
            plots_pdf.append(pie_path)
        
        plots_pdf.extend(self.equipment_averages_chart())
        plots_pdf.extend(self.boxplots())
        
        corr_path = self.corr_matrix()
        if corr_path:
            plots_pdf.append(corr_path)
        
        return plots_pdf

def visualization_csv(df, output_dir, outlier_counts=None, equip_dist=None, equip_averages=None):
    
    viz = CSVPlots(df, output_dir, equip_dist, equip_averages)
    if outlier_counts:
        viz.outlier_counts = outlier_counts
    return viz