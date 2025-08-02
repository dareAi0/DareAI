
import streamlit as st
import pandas as pd
from ai_recon_engine import scan_code_directory, scan_transactions
from smart_recommender import generate_recommendation

# ========== الصفحة 1: تحليل سلوك المعاملات ==========
def transaction_behavior_page():
    st.title("🧠 تحليل سلوك المعاملات")
    df = pd.read_csv("src/transactions_modified.csv")
    df.dropna(inplace=True)

    def calculate_risk(row):
        score = 0.0
        if row['amount'] > 50000: score += 0.3
        if row['transaction_type'] in ['international', 'crypto']: score += 0.3
        if row['status'] == 'failed': score += 0.2
        if 'suspicious' in str(row['recipient_account_id']).lower(): score += 0.2
        return round(score, 2)

    df['Risk_Score'] = df.apply(calculate_risk, axis=1)
    df['Severity'] = df['Risk_Score'].apply(lambda x: '🔴 مرتفع' if x >= 0.6 else '🟡 متوسط' if x >= 0.3 else '🟢 منخفض')
    st.dataframe(df)

# ========== الصفحة 2: محاكاة هجوم على المعاملات ==========
def simulate_attack_page():
    st.title("🧪 محاكاة هجوم على المعاملات")
    if st.button("🔁 تنفيذ معاملة مشبوهة"):
        data = [{
            "transaction_type": "crypto",
            "amount": 100000,
            "status": "failed",
            "transaction_date": pd.Timestamp.now(),
            "recipient_account_id": "suspicious_9988"
        }]
        df_sim = pd.DataFrame(data)
        df_sim['Risk_Score'] = df_sim.apply(lambda row: 1.0, axis=1)
        df_sim['Severity'] = '🔴 مرتفع'
        st.dataframe(df_sim)
        st.error("🚨 تم رصد معاملة مشبوهة!")

# ========== الصفحة 3: لوحة الهاكر الأخلاقي ==========
def whitehat_dashboard():
    st.title("🧠 WhiteHat AI | لوحة الهاكر الأخلاقي")

    st.subheader("📂 تحليل الكود")
    code_findings = scan_code_directory()
    if code_findings:
        for finding in code_findings:
            st.warning(f"⚠️ {finding}")
    else:
        st.success("✅ لا توجد أنماط خطيرة في ملفات الكود")

    st.subheader("💸 تحليل المعاملات البنكية")
    risky_txns = scan_transactions()
    if not risky_txns.empty:
        st.error("🚨 معاملات عالية الخطورة تم رصدها:")
        st.dataframe(risky_txns)
    else:
        st.success("✅ لا توجد معاملات مشبوهة حالياً")

    st.subheader("🧠 توصيات أمنية ذكية")
    recommendations = generate_recommendation(code_findings, risky_txns)
    for rec in recommendations:
        st.info(rec)

# ========== التنقل ==========
def main():
    st.sidebar.title("🚨 WhiteHat Navigation")
    page = st.sidebar.radio("اختر الواجهة:", ["تحليل المعاملات", "محاكاة هجوم", "لوحة الهاكر الأخلاقي"])

    if page == "تحليل المعاملات":
        transaction_behavior_page()
    elif page == "محاكاة هجوم":
        simulate_attack_page()
    elif page == "لوحة الهاكر الأخلاقي":
        whitehat_dashboard()

main()
