# Real Estate Data Analysis Project

This project involves scraping real estate data, cleaning and preprocessing it, performing feature engineering, and training machine learning models to predict property prices.

## Directory Structure


## Files Description

### `/scraping`

This directory contains all the scripts and notebooks required for data scraping, cleaning, feature engineering, and model training.

#### `data_ingestion.py`

This script scrapes real estate advertisements from Unegui.mn and exports the data to `cleaned_data.csv`.

#### `data_visualization_and_plotting.py`

This script is used to visualize the data. It is not crucial for the main pipeline but provides useful insights through data visualization.

#### `cleaning_module.ipynb`

This Jupyter notebook contains the data preprocessing steps. It is an important part of the pipeline where the raw data is cleaned and prepared for analysis. **Please take a look at this.**

#### `feature_engineering_module.ipynb`

This Jupyter notebook handles feature engineering. New features are created and existing ones are transformed to improve the performance of machine learning models. **Please take a look at this.**

#### `training_module.ipynb`

This Jupyter notebook is used for training machine learning models. It includes the steps to train and evaluate the models. **Please take a look at this.**

#### `data_aos_modified.csv`

This file contains the manually cleaned and modified data.

## Instructions

1. **Data Ingestion**: Run the `data_ingestion.py` script to scrape data from Unegui.mn and save it to `cleaned_data.csv`.

2. **Data Visualization**: Use `data_visualization_and_plotting.py` to visualize the data and gain insights.

3. **Data Cleaning**: Open `cleaning_module.ipynb` in Jupyter Notebook and follow the steps to clean the data. Save the cleaned data to `cleaned_data_cleaned.csv`.

4. **Feature Engineering**: Open `feature_engineering_module.ipynb` in Jupyter Notebook and perform feature engineering. Save the engineered data to `cleaned_data_engineered.csv`.

5. **Model Training**: Open `training_module.ipynb` in Jupyter Notebook and train the machine learning model. Evaluate the model using Mean Absolute Error and R-squared metrics.

## Notes

- Ensure all necessary libraries are installed. You can install them using the following command:
  ```bash
  pip install requests beautifulsoup4 pandas matplotlib seaborn scikit-learn
