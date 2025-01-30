# Methods of Advanced Data Engineering 
# **Data-Driven Analysis of Employment Conditions and Food Security in the United States**

<img src="https://raw.githubusercontent.com/snsamia/MADE-WIN2024/main/images/flag.jpg" width="800" height="466">

## **Table of Contents**
- [Introduction](#introduction)
- [Data Sources](#data-sources)
- [ETL Pipeline](#etl-pipeline)
- [Exploratory Data Analysis (EDA)](#exploratory-data-analysis-eda)
- [Findings](#findings)
- [Conclusion & Future Work](#conclusion--future-work)
- [References](#references)

---

## **Introduction**
Food insecurity remains a critical issue in the United States, impacting millions of households annually. Employment conditions, including **wages, job type, working hours, and job benefits**, directly influence a household’s ability to access nutritious food consistently. 

This project explores the **relationship between employment metrics and food security indicators** using **2022 data** from the **Medical Expenditure Panel Survey (MEPS)**. The study aims to identify trends and correlations that can inform policy decisions.

---

## **Data Sources**
The analysis integrates two primary datasets:

1. **Job and Employment Conditions Dataset (HC-237, MEPS 2022) [1]**  
   This dataset provides employment-related details, including **job type, weekly hours worked, gross pay, daily wages, and employer-provided insurance.** Structured in a tabular format, each row corresponds to an individual respondent, while columns represent employment attributes.

2. **Food Security Dataset (HC-240, MEPS 2022) [2]**  
   This dataset includes household-level insights into food security, covering **affordability concerns, meal skipping, and household food stability.** The dataset captures information on whether individuals experienced food shortages or had to skip meals due to financial constraints.

Both datasets were merged using **dwelling\_unit\_id** as the common identifier.

---

## **ETL Pipeline**
The **ETL (Extract, Transform, Load) pipeline** ensures data integrity and usability. The workflow consists of:

1. **Data Ingestion:** Datasets were downloaded from **AHRQ MEPS**.
2. **Preprocessing:** Data cleaning, missing value handling, and standardization.
3. **Data Merging:** Employment and food security datasets were merged.
4. **Storage & Export:** The processed data was stored in an **SQLite database** and exported as **CSV**.

### **ETL Pipeline Workflow**
<img src="https://github.com/snsamia/MADE-WIN2024/blob/main/images/pipeline.png" width="800" height="466">

---

## **Exploratory Data Analysis (EDA)**
EDA was performed to understand the **distribution of employment metrics and their relationship with food security**.

- **Income Distribution:** A histogram of gross pay reveals a **significant income disparity** among respondents.
- **Work Hours:** Weekly working hours vary, with most individuals working **40 hours per week**.
- **Food Security Metrics:** Frequency distributions illustrate **concerns about food shortages and meal skipping**.
- **Correlation Heatmap:** Examines statistical relationships between income, employment, and food security.

### **Sample Correlation Heatmap**

<img src="https://github.com/snsamia/MADE-WIN2024/blob/main/images/correlation.png" width="800" height="466">

---

## **Findings**
### **Key Insights**
- **Higher gross pay significantly reduces food insecurity.**  
  Individuals with **higher wages** are less likely to worry about food shortages or skip meals.
- **Lower working hours correlate with greater food insecurity.**  
  Those who work **fewer hours per week** tend to experience **greater food insecurity**.
- **Food security indicators (e.g., meal skipping and food worries) show strong negative correlations with income levels.**

---

## **Conclusion & Future Work**
This study demonstrates a clear link between **employment stability and food security**. The findings emphasize the role of **wages, job benefits, and working hours** in mitigating food insecurity. These insights can help **policymakers design targeted interventions** to support vulnerable households.

### **Limitations**
Despite the valuable insights, there are **several limitations** in this analysis:
- **Data Completeness:** Some missing values were dropped, which might introduce bias in the final dataset.
- **Static Data:** The dataset covers only 2022 and does not reflect **real-time economic fluctuations** such as inflation or policy changes.
- **Self-Reported Data:** Responses may be influenced by **subjective biases** and **errors in data collection**.

### **Future Enhancements**
- **Predictive Modeling:** Implementing **machine learning models** to forecast food insecurity trends based on employment changes.
- **Real-Time Data Integration:** Incorporating live employment and economic datasets to **enhance analytical accuracy**.
- **Policy Evaluation:** Assessing the effectiveness of **government aid programs** in reducing food insecurity.

---

## **References**
[1] Medical Expenditure Panel Survey (MEPS) - HC-237: Job and Employment Conditions Dataset. [URL]  
[2] Medical Expenditure Panel Survey (MEPS) - HC-240: Food Security Dataset. [URL]  






## Exercises
During the semester you will need to complete exercises using [Jayvee](https://github.com/jvalue/jayvee). You **must** place your submission in the `exercises` folder in your repository and name them according to their number from one to five: `exercise<number from 1-5>.jv`.

In regular intervals, exercises will be given as homework to complete during the semester. Details and deadlines will be discussed in the lecture, also see the [course schedule](https://made.uni1.de/).

### Exercise Feedback
We provide automated exercise feedback using a GitHub action (that is defined in `.github/workflows/exercise-feedback.yml`). 

To view your exercise feedback, navigate to Actions → Exercise Feedback in your repository.

The exercise feedback is executed whenever you make a change in files in the `exercise` folder and push your local changes to the repository on GitHub. To see the feedback, open the latest GitHub Action run, open the `exercise-feedback` job and `Exercise Feedback` step. You should see command line output that contains output like this:

```sh
Found exercises/exercise1.jv, executing model...
Found output file airports.sqlite, grading...
Grading Exercise 1
	Overall points 17 of 17
	---
	By category:
		Shape: 4 of 4
		Types: 13 of 13
```
