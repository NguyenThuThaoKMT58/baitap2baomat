import hashlib
import hmac
import json
from PyPDF2 import PdfReader

INPUT_PDF = "bai_tap.pdf"
SIGNED_PDF = "bai_tap_signed.pdf"
SIGNATURE_FILE = "bai_tap.sig"
SECRET_KEY_FILE = "secret.key"

# Hàm đọc khóa bí mật
def load_secret_key(filename):
    with open(filename, "rb") as f:
        return f.read().strip()

# Hàm tính SHA256 của file
def sha256_file(filepath):
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

# Hàm tạo HMAC
def hmac_sha256(secret, message):
    return hmac.new(secret, message.encode(), hashlib.sha256).hexdigest()

# Hàm trích xuất chữ ký hiển thị từ PDF (kiểm tra có dòng chữ ký)
def extract_visible_text(filepath):
    reader = PdfReader(filepath)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

# Hàm xác minh chữ ký
def verify():
    secret_key = load_secret_key(SECRET_KEY_FILE)

    with open(SIGNATURE_FILE, "r", encoding="utf-8") as f:
        sig = json.load(f)

    original_hash = sha256_file(INPUT_PDF)
    check_hmac = hmac_sha256(secret_key, original_hash)
    last_text = extract_visible_text(SIGNED_PDF)

    print("Verification results:")
    print(f" - SHA256 matches original? {'YES' if sig['sha256']==original_hash else 'NO'}")
    print(f" - HMAC matches? {'YES' if sig['hmac']==check_hmac else 'NO'}")
    print(f" - Visible signature text in signed PDF? {'YES' if 'Người ký' in last_text else 'NO'}")

    if (sig['sha256'] == original_hash) and (sig['hmac'] == check_hmac):
        print("✅ Signature verification SUCCESS.")
    else:
        print("❌ Signature verification FAILED.")

if __name__ == "__main__":
    verify()
