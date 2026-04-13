<img width="1905" height="878" alt="RFM Dashboard 1" src="https://github.com/user-attachments/assets/7aeba3fd-338c-4f44-9d30-2198d5f64875" />
<img width="1906" height="878" alt="RFM Dashboard 2" src="https://github.com/user-attachments/assets/b1e5edb0-210a-4205-afe6-24c8463e02c4" />
# rfm-customer-segmentation
```markdown
# 🛍️ E-Commerce Customer Segmentation (RFM) Dashboard

A full-stack data analytics application that segments e-commerce customers based on their purchasing behavior using RFM (Recency, Frequency, Monetary) modeling. 

## 🎯 Business Value
Instead of treating all customers equally, this dashboard allows marketing and sales teams to identify highly profitable "Champions," re-engage "At Risk" users, and understand the core metrics driving revenue. It transforms raw transaction logs into actionable, segmented cohorts.

## 🏗️ Architecture & Features

* **Data Engine (`rfm_engine.py`):** Generates realistic synthetic transaction data and calculates complex RFM quantiles using `pandas` and `numpy`.
* **Interactive UI (`app.py`):** A responsive, SaaS-grade web application built with `Streamlit`.
* **Dynamic Theming:** Custom CSS implementation featuring a seamless toggle between a high-contrast Dark Mode and a clean Light Mode.
* **Advanced Visualizations:** Utilizes `plotly.express` for hierarchical Treemaps, multi-variable Scatter Plots, and spending Histograms.

## ⚙️ The Tech Stack
* **Language:** Python 3.10
* **Data Processing:** `pandas`, `numpy`
* **Frontend:** `streamlit`
* **Visualization:** `plotly`

## 🚀 Running It Locally

If you want to clone this repository and run the pipeline on your local machine, follow these steps:

**1. Clone the repository:**
```bash
git clone [https://github.com/your-username/rfm-customer-segmentation.git](https://github.com/your-username/rfm-customer-segmentation.git)
cd rfm-customer-segmentation
```

**2. Install dependencies:**
```bash
pip install pandas numpy streamlit plotly
```

**3. Generate the data:**
```bash
python rfm_engine.py

**4. Launch the dashboard:**
```bash
streamlit run app.py
```
```
