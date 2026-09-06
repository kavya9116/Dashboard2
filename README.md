# Café Behavioral Analytics Dashboard

An interactive **customer behavioral analytics dashboard** built with Python, Pandas, Plotly, and Streamlit to analyze customer experience, engagement, adoption, retention, task success, and ordering behavior for a café website.

## Project Overview

The objective of this project is to analyze how users interact with a café website and identify areas that influence the overall user experience and business performance.

The project uses behavioral and feedback data to calculate key UX and business metrics and presents the results through an interactive Streamlit dashboard.

The dataset used in this project is **synthetic data** created for analysis and demonstration purposes.

## Key Areas of Analysis

The dashboard analyzes the following areas:

### Happiness

* Net Promoter Score (NPS)
* Customer Satisfaction Score (CSAT)
* System Usability Scale (SUS)
* Customer Effort Score (CES)

### Engagement

* Sessions
* User interactions
* Engagement time
* Meaningful-value events

### Adoption

* Core action completion
* Feature usage
* Order completion behavior

### Retention

* Day-7 return rate
* Returning user behavior
* Visit patterns

### Task Success

* Task completion rate
* Task attempts
* Task errors
* Task Error Rate

### Time to First Value

* Signup Time
* First Value Time
* Time to First Value (TTFV)

### Customer & Order Analysis

* Customer visits
* Sessions
* Orders
* Quantity sold
* Revenue
* Average order value
* Product performance

## HEART Framework

The project uses the **HEART framework** to organize the user experience analysis:

| HEART Dimension | Metrics                        |
| --------------- | ------------------------------ |
| Happiness       | NPS, CSAT, SUS                 |
| Engagement      | Sessions and user interactions |
| Adoption        | Core action completion         |
| Retention       | Day-7 return rate              |
| Task Success    | Task completion and error rate |

Additional UX metrics such as **TTFV, CES, and Task Error Rate** are used to provide deeper insight into user behavior.

## Technology Stack

* **Python**
* **Pandas** — data processing and analysis
* **OpenPyXL** — Excel data handling
* **Plotly** — interactive visualizations
* **Streamlit** — dashboard development

## Project Structure

```text
Cafe-Behavioral-Analytics/
│
├── dashboard.py
├── requirements.txt
├── README.md
└── Cafe_Analysis_Performed.xlsx
```

## Dataset

The project uses:

**`Cafe_Analysis_Performed.xlsx`**

The workbook contains data related to:

* Happiness
* Engagement
* Adoption
* Retention
* Task Success
* Customer/Visitor behavior
* Orders

The data is synthetic and does not represent real customer information.

## How to Run the Dashboard

### 1. Clone the repository

```bash
git clone <repository-url>
cd Cafe-Behavioral-Analytics
```

### 2. Install the required libraries

```bash
pip install -r requirements.txt
```

### 3. Run the Streamlit application

```bash
streamlit run dashboard.py
```

The dashboard will open in your browser.

## Analysis Workflow

```text
Excel Dataset
      ↓
Pandas
      ↓
Data Processing & Analysis
      ↓
KPI Calculation
      ↓
Interactive Visualizations
      ↓
Streamlit Dashboard
      ↓
Insights & Recommendations
```

## Key Metrics

### NPS

NPS is calculated as:

**% Promoters − % Detractors**

* 0–6 → Detractors
* 7–8 → Passives
* 9–10 → Promoters

### CSAT

CSAT measures customer satisfaction on a **1–5 scale**.

Responses of **4 or above** are considered satisfied.

### SUS

SUS is calculated using the standard 10-question scoring method and converted to a **0–100 scale**.

### CES

CES measures the effort required to complete an interaction on a **1–7 scale**.

A lower score indicates lower effort and a better experience.

### TTFV

Time to First Value measures the time between:

**Signup Time → First Value Time**

### Task Error Rate

Task Error Rate is calculated as:

**Total Errors ÷ Total Task Attempts × 100**

### Day-7 Retention

Day-7 retention measures whether users returned within the specified 7-day period.

## Project Goal

The final dashboard is designed to help identify:

* How satisfied users are
* How easily users interact with the website
* Whether users complete important actions
* Where users encounter errors
* How quickly users reach meaningful value
* Whether users return to the website
* Which products and customer behaviors contribute to business performance

The analysis can then be used to identify **UX problems, behavioral patterns, risks, and potential improvements**.

## Disclaimer

This project is created for **educational and portfolio purposes**. The dataset is synthetic and is intended to demonstrate the application of behavioral analytics and dashboard development techniques.
