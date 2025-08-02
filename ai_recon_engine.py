
import os
import pandas as pd

def scan_code_directory(path=".", extension=".py"):
    findings = []
    # المعايير: البحث عن أوامر تعتبر خطيرة أو تستخدم في الهجمات مثل os.system أو eval أو subprocess
    RISKY_PATTERNS = [
        ("os.system", "استخدام أوامر النظام مباشرة"),
        ("eval(", "تنفيذ نصوص برمجية مباشرة"),
        ("subprocess", "تشغيل أوامر خارجية"),
        ("pickle.load", "تحميل كائنات غير موثوقة - RCE محتمل"),
        ("exec(", "تنفيذ كود ديناميكي (exec)"),
    ]

    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith(extension) and "venv" not in root:
                with open(os.path.join(root, file), "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    for pattern, reason in RISKY_PATTERNS:
                        if pattern in content:
                            findings.append(f"{file} يحتوي على {reason}: {pattern}")
    return findings

def scan_transactions(file_path="src/transactions_modified.csv"):
    if not os.path.exists(file_path):
        return pd.DataFrame(columns=["transaction_type", "amount", "status", "recipient_account_id"])
    df = pd.read_csv(file_path)
    # المعايير: اعتبار المعاملات ذات المبلغ > 50000 بأنها مرتفعة الخطورة
    flagged = df[df['amount'] > 50000]
    return flagged[["transaction_type", "amount", "status", "recipient_account_id"]]

def main():
    print("📂 تفتيش الكود:")
    code_findings = scan_code_directory()
    if code_findings:
        for item in code_findings:
            print(f"[!] {item}")
    else:
        print("✅ لا توجد أنماط خطرة في الكود.")

    print("\n📊 تفتيش المعاملات:")
    txns = scan_transactions()
    if not txns.empty:
        print("⚠️ تم رصد المعاملات التالية كمشبوهة:")
        print(txns.to_string(index=False))
    else:
        print("✅ لا توجد معاملات مشبوهة حسب المعايير المعتمدة.")

if __name__ == "__main__":
    main()
