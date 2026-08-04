import os
from pathlib import Path

# Create __init__ files to make them proper packages
init_paths = [
    "__init__.py",
    "core/__init__.py",
    "core/domain/__init__.py",
    "core/ports/__init__.py",
    "core/use_cases/__init__.py",
    "fusion/__init__.py",
    "confidence/__init__.py",
    "preprocessing/__init__.py",
    "explainability/__init__.py",
    "config/__init__.py",
]

base = Path(r"C:\Users\DELL\OneDrive\Desktop\intern\acfe")
for p in init_paths:
    f = base / p
    f.parent.mkdir(parents=True, exist_ok=True)
    f.touch(exist_ok=True)
    
print("Initialized packages.")
