# Ideal Function Mapping Project

## Overview

This project implements a full data pipeline that:

- Loads training, ideal, and test datasets
- Uses Least Squares (Sum of Squared Errors) to select best-fitting ideal functions
- Maps test data points to selected functions using statistical deviation constraints
- Stores all results in a SQLite database
- Visualizes results using Bokeh

---

## Methodology

### 1. Function Selection (Least Squares)
Each training function is compared with all 50 ideal functions using:

\[
SSE = \sum (y_{train} - y_{ideal})^2
\]

The 4 ideal functions with the lowest SSE values are selected.

---

### 2. Mapping Rule

A test point is assigned to an ideal function if:

\[
|y_{test} - y_{ideal}| \le \sqrt{2} \cdot max\_deviation
\]

---

## Architecture

ideal_function_project/
│
├── data/
│   ├── train.csv
│   ├── test.csv
│   └── ideal.csv
│
├── database/
│   └── ideal_functions.db
│
├── models/
│   ├── database.py
│   ├── data_loader.py
│   ├── base_loader.py
│   ├── exceptions.py
│   ├── function_selector.py
│   ├── mapper.py
│   └── visualizer.py
│   └──__init__.py
│
├── tests/
│   ├── test_loader.py
│   ├── test_selector.py
│   └── test_mapper.py
│   └── test_visualizer.py
│   └── test_database.py
│
├── main.py
├── requirements.txt
└── README.md


---

## Database Structure

- training_data
- ideal_functions
- mapped_test_data

---

## Visualization

The system generates 3 interactive Bokeh plots:

1. Training vs Ideal functions
2. Test data mapping visualization
3. Full combined overview

---

## Technologies Used

- Python 3.x
- Pandas
- NumPy
- SQLAlchemy
- SQLite
- Bokeh
- Pytest

---

## Testing

Run tests:

```bash
pytest