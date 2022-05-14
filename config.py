from pathlib import Path


file_dir = Path("config.py").parent.absolute()
data_dir = str(file_dir) + '/input/'
export_dir = str(file_dir) + '/output/'