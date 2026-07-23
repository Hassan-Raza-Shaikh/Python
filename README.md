# Computational Mathematics & Artificial Intelligence Utilities

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-11557C?style=for-the-badge&logo=python&logoColor=white)

A Python code repository showcasing core mathematical algorithms, numerical solvers, linear algebra processes, and artificial neural network layers.

## Setup

Install the core dependencies for the standalone scripts with:

```bash
pip install -r requirements.txt
```

The root `requirements.txt` covers the main scripts in this repository. Some notebooks and lab folders use extra packages such as `pandas`, `scikit-learn`, `seaborn`, `torch`, `tensorflow`, and Jupyter-related tools, so you may need to install those separately depending on which notebook you open.

## Implemented Algorithms
- **Neural Networks**: Backpropagation logic (`backpropagation.py`).
- **Graph Algorithms**: Google's PageRank algorithm (`page_rank.py`).
- **Linear Algebra Solvers**: 
  - Gram-Schmidt orthonormalisation (`gram_schemit_process.py`).
  - Gaussian Elimination matrix solver (`gaussian_elimination.py`).
  - Matrix reflections (`reflecting_matrix.py`).
- **Data Visualisation**: Custom data analytics dashboards utilizing Matplotlib and Plotly.

## Suggested Organization

This repo would be easier to navigate if you split it into a few top-level groups:

- `scripts/` for standalone `.py` files.
- `notebooks/` for `.ipynb` files.
- `data/` for CSV, JSON, text, and generated files.
- `labs/` or `courses/` for the AI course folders.

If you want to keep the current layout, a smaller improvement is to add one requirements file for the root scripts and separate environment files for the notebook-heavy folders.
