# Product-Recommendations-using-Customer-Behavior-Analysis
Enhancing the online retail experience by **analyzing customer behavior**, **predicting next purchases**, and **recommending products** using **Association Rule Mining** and **Markov Chains**.

---

## Project Objective

The objective of this project is to enhance the online retail shopping experience by:

- Gaining insights into **customer behavior**.
- **Predicting** the user's **next purchase** based on historical data.
- Providing **personalized recommendations** using advanced data mining techniques.

---

## Libraries Used

| Library   | Purpose                         |
|-----------|----------------------------------|
| numpy     | Data manipulation                |
| pandas    | Data manipulation                |
| matplotlib| Data visualization               |
| seaborn   | Data visualization               |
| mlxtend   | Association Rule Mining          |
| fastapi   | Building APIs                    |
| uvicorn   | Model deployment server          |
| streamlit | Building interactive web UI      |
| requests  | Connecting UI with API           |

---

## Data Source

- **Dataset**: Brazilian E-commerce Public Dataset (provided by [Olist](https://www.olist.com/))
- **Size**: 100k+ orders (2016-2018)
- **Dimensions**: Order status, pricing, payments, freight performance, customer locations, product attributes, customer reviews, and geolocation data.

The dataset allows viewing an order from multiple perspectives and provides rich customer behavior information.

---

## Database Schema

Each table (orders, customers, products, payments, reviews, sellers, geolocation) is explored individually. Required preprocessing and cleaning steps are applied using visualizations for better understanding.

---

## Exploratory Data Analysis (EDA)

- Performed individual analysis on each dataset.
- Insights into customer buying patterns, product categories, churn rates, and sales performance.
- Data visualizations were generated using Matplotlib and Seaborn.

---

## Churn Analysis

- **97% of customers churn** after a single purchase.
- Despite the high churn, over **3,000 repeat customers** remain, offering substantial analysis opportunities for recommendations.

---

## Web Application

An interactive web app was built using **FastAPI** (backend) and **Streamlit** (frontend).

**Home Page** features:
- **Login Section**: User inputs Unique Customer ID.
- **Trending Products Section**: Top-selling products are shown.

### Recommendation Logic

Depending on the user's purchase history, one of three recommendation cases is triggered:

#### Case 1: Cold Start

- **New user** (no purchase history).
- Top 5 trending products are recommended.

#### Case 2: Sequence Chain

- **Returning user** with purchases forming a **sequence**.
- Remaining products in the chain are recommended using:
  - Association Rule Mining (Antecedent ➔ Consequent)
  - Markov Chains (P(Consequent | Antecedent))

If no items remain, fallback to **Cold Start**.

#### Case 3: Cross-Category Sell

- **Returning user** with purchases **outside the sequence**.
- Association Rules applied on **product categories**.
- Top 5 products from the recommended category are suggested.

Fallback to **Cold Start** if no suitable category found.

---

## Deployment

- **FastAPI** used to build APIs.
- **Uvicorn** server for backend deployment.
- **Streamlit** frontend connects to backend using **requests**.

---

## Conclusion & Future Work

- The recommendation engine works accurately but suffers from **high latency** due to:
  - Large dataset size.
  - Time complexity of association rule generation.
  - Sequence chain building.

**Future Improvements**:
- **Parallelize** the recommendation generation for micro-second response times.
- **Dynamically update** database with new purchases to refine recommendations over time.
- **Optimize Markov Chain and Association Rule algorithms** for scalability.

---

## Project Structure

```
├── datasets/
│   ├── olist_customers_dataset.csv
│   ├── olist_geolocation_dataset.csv
│   └── ... (other datasets)
├── main.py               # Backend API code (FastAPI)
├── app.py                # Frontend UI (Streamlit) (ARM)
├── apps.py               # Frontend UI (Streamlit) (Markov Chain)
├── README.md             # Project description
├── requirements.txt      # Python dependencies
```

---

## Contact

For any queries or collaboration opportunities:

- **Name**: Shreya Kabra
- **GitHub**: [shreyakabra](https://github.com/shreyakabra)

---
