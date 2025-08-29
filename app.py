# app.py
import streamlit as st
import pandas as pd
import joblib
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE
import lime
import lime.lime_tabular
import time
import warnings

warnings.filterwarnings('ignore')

# --- Page Configuration ---
st.set_page_config(
    page_title="Fraud Detection Command Center",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Machine Learning Model Setup ---
# This section replaces train.py. It loads, cleans, and trains the model in memory.
@st.cache_resource
def load_and_train_model():
    print("Loading data and training model for the first time...")
    try:
        data = pd.read_csv('bank_fraud_dataset.csv', index_col=0)
    except FileNotFoundError:
        st.error("FATAL: 'bank_fraud_dataset.csv' not found. Please place it in the same folder as this script.")
        st.stop()

    feature_names = [
        'aon', 'daily_decr30', 'daily_decr90', 'rental30', 'rental90',
        'last_rech_date_ma', 'last_rech_date_da', 'last_rech_amt_ma',
        'cnt_ma_rech30', 'fr_ma_rech30', 'sumamnt_ma_rech30',
        'medianamnt_ma_rech30', 'medianmarechprebal30', 'cnt_ma_rech90',
        'fr_ma_rech90', 'sumamnt_ma_rech90', 'medianamnt_ma_rech90',
        'medianmarechprebal90', 'cnt_da_rech30', 'fr_da_rech30',
        'cnt_da_rech90', 'fr_da_rech90', 'cnt_loans30', 'amnt_loans30',
        'maxamnt_loans30', 'medianamnt_loans30', 'cnt_loans90', 'amnt_loans90',
        'maxamnt_loans90', 'medianamnt_loans90', 'payback30', 'payback90'
    ]
    X = data[feature_names]
    y = data['label']

    for col in X.columns:
        X[col] = pd.to_numeric(X[col], errors='coerce')
        if X[col].isnull().any():
            X[col] = X[col].fillna(X[col].median())
    
    X_resampled, y_resampled = SMOTE(random_state=42).fit_resample(X, y)
    
    scaler = StandardScaler().fit(X_resampled)
    X_scaled = scaler.transform(X_resampled)
    
    model = GradientBoostingClassifier(n_estimators=200, max_depth=10, random_state=42).fit(X_scaled, y_resampled)
    
    # Create the LIME explainer
    lime_explainer = lime.lime_tabular.LimeTabularExplainer(
        training_data=X_resampled.values,
        mode='classification',
        feature_names=feature_names,
        class_names=['Not Fraud', 'Fraud'],
        discretize_continuous=True
    )
    
    print("Model training and resource loading complete.")
    return model, scaler, feature_names, X, lime_explainer

# Load all ML resources. This will only run once.
model, scaler, feature_names, simulation_data, lime_explainer = load_and_train_model()

# --- Prediction and Explanation Functions ---
# These functions replace the API. They are called directly from the UI.
def predict_fraud(transaction_df):
    transaction_scaled = scaler.transform(transaction_df)
    prediction = model.predict(transaction_scaled)[0]
    confidence_scores = model.predict_proba(transaction_scaled)[0]
    is_fraud = bool(prediction)
    confidence = float(confidence_scores[1] if is_fraud else confidence_scores[0])
    return {"fraud": is_fraud, "confidence": round(confidence, 4)}

def explain_prediction(transaction_df):
    transaction_scaled = scaler.transform(transaction_df)
    def predict_fn(x):
        # The scaler expects a DataFrame, so we recreate it
        x_df = pd.DataFrame(x, columns=feature_names)
        return model.predict_proba(scaler.transform(x_df))

    explanation = lime_explainer.explain_instance(
        transaction_df.iloc[0].values,
        predict_fn,
        num_features=10
    )
    return explanation.as_list()

# --- Session State Initialization ---
if 'flagged_transactions' not in st.session_state:
    st.session_state.flagged_transactions = pd.DataFrame(columns=['timestamp', 'aon', 'sumamnt_ma_rech30', 'amnt_loans30', 'confidence'])
if 'metrics' not in st.session_state:
    st.session_state.metrics = {'total': 0, 'fraud': 0}

# --- UI Layout ---
st.title("🛡️ Fraud Detection Command Center")
st.caption("Live monitoring and investigation of suspicious transaction activity.")

col_live, col_investigate = st.columns([2, 1.5])

with col_live:
    st.header("📈 Live Transaction Monitoring")
    mcol1, mcol2, mcol3 = st.columns(3)
    total_placeholder = mcol1.empty()
    fraud_placeholder = mcol2.empty()
    rate_placeholder = mcol3.empty()
    st.subheader("🚨 Flagged Fraud Alerts")
    alerts_placeholder = st.empty()

with col_investigate:
    st.header("🔬 Investigate a Transaction (LIME)")
    with st.container(border=True):
        with st.form("explain_form"):
            st.write("Enter transaction details below to generate a risk analysis.")
            form_cols = st.columns(3)
            inputs = {}
            for i, feature in enumerate(feature_names):
                inputs[feature] = form_cols[i % 3].number_input(f"{feature}", value=0.0, format="%.2f", key=feature)
            submitted = st.form_submit_button("Analyze Transaction", use_container_width=True)
        if submitted:
            # Convert inputs to a DataFrame
            input_df = pd.DataFrame([inputs])
            # Get the explanation directly from our function
            explanation = explain_prediction(input_df)
            
            st.subheader("Transaction Risk Analysis")
            st.write("Top features contributing to the prediction:")
            for feature, weight in explanation:
                if weight > 0:
                    st.markdown(f"- `{feature}`: <span style='color:red;'>Increases fraud risk</span>", unsafe_allow_html=True)
                else:
                    st.markdown(f"- `{feature}`: <span style='color:green;'>Decreases fraud risk</span>", unsafe_allow_html=True)

# --- Main Loop for Live Updates ---
while True:
    transaction_df = simulation_data.sample(1)
    
    pred = predict_fraud(transaction_df)
    
    st.session_state.metrics['total'] += 1
    if pred.get("fraud"):
        st.session_state.metrics['fraud'] += 1
        transaction = transaction_df.iloc[0]
        new_entry = pd.DataFrame([{'timestamp': pd.to_datetime('now').strftime('%H:%M:%S'), 'aon': int(transaction['aon']), 'sumamnt_ma_rech30': transaction['sumamnt_ma_rech30'], 'amnt_loans30': transaction['amnt_loans30'], 'confidence': pred['confidence']}])
        st.session_state.flagged_transactions = pd.concat([st.session_state.flagged_transactions, new_entry], ignore_index=True)

    with total_placeholder.container(border=True): st.metric("Total Transactions", st.session_state.metrics['total'])
    with fraud_placeholder.container(border=True): st.metric("Flagged as Fraud", st.session_state.metrics['fraud'])
    with rate_placeholder.container(border=True):
        fraud_rate = (st.session_state.metrics['fraud'] / st.session_state.metrics['total']) * 100 if st.session_state.metrics['total'] > 0 else 0
        st.metric("Fraud Rate", f"{fraud_rate:.2f}%")
    
    with alerts_placeholder:
        st.dataframe(st.session_state.flagged_transactions.tail(10), use_container_width=True)
    
    time.sleep(2)