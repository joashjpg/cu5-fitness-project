# StepUp - A Step Goal Early-Warning Predictor

Predicts whether you'll reach 10,000 steps today, using only the **time of day** and your **steps so far**. If you're likely to fall short, the demo suggests short walks spread over the rest of the day to give you the best chance of reaching the goal.

Data science capstone project. The model and write-up are in the notebooks, and the demo is a small Flask API plus a single-page frontend.

## Data

[Fitbit Fitness Tracker Data](https://www.kaggle.com/datasets/arashnic/fitbit) (Kaggle, `arashnic/fitbit`), folder `Fitabase Data 4.12.16-5.12.16`. Two files are used:

- `minuteStepsNarrow_merged.csv`: steps per minute (core file)
- `dailyActivity_merged.csv`: daily totals, used for cross-checking the minute data

After cleaning, the training table covers 30 users and 30 dates (12 April to 11 May 2016). Each row is one user, one day and one checkpoint (every 30 minutes from 8:00am to 9:30pm).

## Results (test set: the last 6 dates)

| | Always predict 0 | Pace rule | Logistic Regression | Random Forest |
|---|---|---|---|---|
| Accuracy | 0.638 | 0.724 | 0.751 | **0.768** |
| Precision | 0.000 | 0.646 | 0.737 | **0.893** |
| Recall | 0.000 | 0.521 | 0.483 | 0.408 |
| F1 | 0.000 | 0.577 | 0.583 | 0.560 |
| Wrong "you'll make it" | 0 | 343 | 207 | **59** |

ROC AUC: Random Forest 0.775, Logistic Regression 0.743. The Random Forest is used in the app because the costly mistake for a warning tool is a wrong "you're fine". See `02_modeling.ipynb` (Sections 7 and 10) for the full interpretation and limitations.

## Project structure

```
├── 01_eda_cleaning.ipynb     # cleaning and EDA, exports the processed files
├── 02_modeling.ipynb         # features, split, baselines, models, evaluation
├── app.py                    # Flask API (loads the saved model)
├── index.html                # demo frontend
├── data/
│   ├── raw/                  # original Kaggle files (not included in the repo)
│   ├── processed_daily.csv
│   └── processed_minute_steps.csv
└── models/
    ├── rf_model.joblib       # trained Random Forest
    └── progress_curve.json   # typical-day progress curve
```

## How to run the demo

1. Install the dependencies:
   ```
   pip install flask flask-cors joblib pandas scikit-learn
   ```
2. From the project folder, start the API:
   ```
   python app.py
   ```
   It runs at `http://127.0.0.1:5000`.
3. Open `index.html` in a browser. Set the time and your steps so far, or drag the dot on the chart.

The `models/` folder must exist. If it doesn't, run `02_modeling.ipynb` down to Section 9 to create it. Load the model with the same scikit-learn version that trained it.

## Re-running the notebooks

Install `jupyter matplotlib seaborn` as well. Download the two raw files listed above into `data/raw/`, then run `01_eda_cleaning.ipynb` followed by `02_modeling.ipynb`. Run each notebook from top to bottom.

## API

- `POST /predict` with `{"minute_of_day": 840, "steps_so_far": 4000}` returns `probability`, `will_reach`, `steps_remaining` and `in_trained_range`.
- `GET /curve` returns the typical-day progress curve used by the chart.

## Limitations

Small, self-selected dataset (30 users, 2016). The same users appear in train and test, so scores may be optimistic for a new user. Only two features are used, and early-morning predictions are close to guessing. The goal is fixed at 10,000 steps, and the walk plan assumes about 100 steps a minute. Details are in the notebook.

## AI assistance

The frontend (`index.html`) and the API boilerplate (`app.py`) were built with AI assistance. The cleaning, feature engineering, split, baselines and evaluation code were written by me, with a few small snippets and explanations from AI tools, which are marked in the notebook.
