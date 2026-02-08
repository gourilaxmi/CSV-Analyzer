from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PIL import Image


class Chart(FigureCanvas):
    def __init__(self, parent=None):
        self.fig = Figure(figsize=(8, 6))
        super().__init__(self.fig)
        self.setParent(parent)
    
    def plot_image(self, image_path):
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        
        try:
            img = Image.open(image_path)
            ax.imshow(img)
            ax.axis('off')
            self.draw()
        except Exception as e:
            ax.text(0.5, 0.5, f'Error loading image:\n{str(e)}', 
                   ha='center', va='center', transform=ax.transAxes)
            self.draw()