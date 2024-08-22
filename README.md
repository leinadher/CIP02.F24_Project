# 📱 Data scraping and analysis of largest Swiss phone resellers

**Authors:** Daniel Herrera, Ramon Burkhard & Jack Brown

**Date:** 13/05/2024

---

## 1. Project Overview

The project involves full Extraction-Transform-Load (ETL) process, from the retrieval of the raw data via web scraping in Python from 3 different Swiss electronics resellers to the analysis and reporting of the transformed and stored data. Because it is a group effort, data from the three resellers has been transformed to follow a group-agreed standardization and structure, prior to loading onto the final database. The three sources are **Galaxus**, **Interdiscount** and **MediaMarkt**.

As the repository is maintained by myself, I have only included my own segment of the code, corresponding to the **Interdiscount** online store, as well as the final assembled dataset and exploratory data analysis in a Jupyter Notebook.

## 2. Repository structure:

- 📁 'exploration': Contains the assembled dataset as well as the EDA report under `ExploratoryDataAnalysis.ipynb`.
- 📁 'ETL_interdiscount': Contains the ETL sequence split into its phases for the reseller Interdiscount.
- 📄 `README.md`: This readme file.

## 3. Additional notes

- 🕸️ In all three cases, data is scraped from the website using Selenium for Python.
- 🐼 The raw data is transformed and manipulated with Pandas dataframes.
- 🔄 The data is merged into one cohesive dataset.
- 🗄️ It is loaded onto a shared SQL database using the MariaDB library.
- 📊 An exploratory analysis and report are undertaken with the data in a Jupyter Notebook.
