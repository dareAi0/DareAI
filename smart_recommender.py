
import random

def generate_recommendation(findings, risky_txns):
    recommendations = []
    if findings:
        recommendations.append("🔍 يوصى بمراجعة السكربتات التالية بسبب استخدام أوامر قد تكون خطرة:")
        recommendations.extend([f"⚠️ {f}" for f in findings])

    if not risky_txns.empty:
        recommendations.append("\n📊 يوصى بمراقبة هذه المعاملات البنكية بعناية:")
        for _, row in risky_txns.iterrows():
            msg = f"🚨 معاملة {row['transaction_type']} بمبلغ {row['amount']} إلى {row['recipient_account_id']} قد تكون جزءًا من نشاط مشبوه."
            recommendations.append(msg)

    if not recommendations:
        return ["✅ لا توجد توصيات أمنية حالياً. كل شيء يبدو آمناً."]
    else:
        return recommendations
