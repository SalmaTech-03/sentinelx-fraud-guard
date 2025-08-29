<div align="center">

# 🛡️ SentinelX Fraud Guard 🛡️

### A Real-Time Fraud Detection Command Center with Explainable AI


</div>

---

<table>
<tr>
<td width="65%">

**SentinelX Fraud Guard** is an advanced, end-to-end machine learning project that demonstrates a complete MLOps workflow. It simulates a live stream of financial transactions, uses a Gradient Boosting model to detect potential fraud in real-time, and provides clear, human-readable explanations for every prediction using LIME (Local Interpretable Model-agnostic Explanations).

The entire system is built as a robust, all-in-one web application, showcasing a modern approach to building and deploying interactive AI-powered tools.


---

## ✨ Core Features

*   **📈 Live Monitoring Dashboard:** A real-time interface displays incoming transactions and flags suspicious activity instantly.
*   **📊 Dynamic Metrics:** Key performance indicators (KPIs) like Total Transactions, Flagged Fraud, and the overall Fraud Rate are updated live.
*   **🔬 Explainable AI (XAI):** Go beyond predictions. The "Investigate" panel uses **LIME** to break down the model's reasoning, showing exactly which features contributed to a transaction being flagged.
*   **⚙️ All-in-One Architecture:** A single, powerful Streamlit application handles data preprocessing, in-memory model training, real-time predictions, and the interactive user interface.
*   **👨‍💻 Professional UI:** A clean, modern "Command Center" UI designed for an intuitive user experience, perfect for a fraud analyst.

---

## 🛠️ Technology Stack

This project was built using a modern, data-centric Python stack.

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white)
![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)

*   **Language & Framework:** Python, Streamlit
*   **Data & Machine Learning:** Pandas, Scikit-learn, Imbalanced-learn, LIME
*   **Version Control & Deployment:** Git, GitHub, Streamlit Community Cloud

---

## 🚀 How to Run Locally

This project is fully self-contained and easy to set up.

#### 1. Clone the Repository
```bash
git clone https://github.com/YourUsername/sentinelx-fraud-guard.git
cd sentinelx-fraud-guard
---

#### 2. Install Dependencies
All required libraries are listed in the requirements.txt file.

```bash

pip install -r requirements.txt

#### 3. Run the Application
Launch the Streamlit app with a single command. The first run will take a moment to train the model in memory.

```bash 

streamlit run app.py
---
