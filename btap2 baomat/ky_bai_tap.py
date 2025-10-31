import hashlib
import hmac
import json
import datetime
import os
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from io import BytesIO

# ----------------------------
# Cấu hình cơ bản
# ----------------------------
INPUT_PDF = "bai_tap.pdf"
SIGNED_PDF = "bai_tap_signed.pdf"
SIG_FILE = "bai_tap.sig"
SECRET_KEY_FILE = "secret.key"
SIGNER_NAME = "Thảo"
VISIBLE_TEXT = f"Người ký: {SIGNER_NAME}"

# ----------------------------
# Tạo khóa bí mật nếu chưa có
# ----------------------------
if not os.path.exists(SECRET_KEY_FILE):
    import secrets
    key = secrets.token_bytes(32)
    with open(SECRET_KEY_FILE, "wb") as f:
        f.write(key)
    print("🔑 Đã tạo khóa bí mật mới (secret.key).")

# ----------------------------
# Hàm tiện ích
# ----------------------------
def load_secret_key():
    """Đọc khóa bí mật từ file"""
    with open(SECRET_KEY_FILE, "rb") as f:
        return f.read().strip()

def sha256_file(path):
    """Tính hash SHA256 của file"""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
    return h.hexdigest()

def hmac_sha256(key, message_hex):
    """Tính HMAC-SHA256"""
    msg = message_hex.encode("utf-8")
    return hmac.new(key, msg, hashlib.sha256).hexdigest()

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def create_overlay(text, page_width, page_height):
    """Tạo lớp chữ ký hiển thị ở cuối trang PDF (có hỗ trợ Unicode)"""
    packet = BytesIO()
    c = canvas.Canvas(packet, pagesize=(page_width, page_height))

    # Đăng ký font Unicode (Arial hoặc DejaVuSans hỗ trợ tiếng Việt)
    font_path = "C:\\Windows\\Fonts\\arial.ttf"  # có sẵn trên Windows
    pdfmetrics.registerFont(TTFont("ArialUnicode", font_path))
    c.setFont("ArialUnicode", 12)

    # Thêm chữ ký ở cuối trang
    c.drawString(60, 40, text)
    c.save()
    packet.seek(0)
    return packet

# ----------------------------
# Hàm ký PDF
# ----------------------------
def sign_pdf():
    if not os.path.exists(INPUT_PDF):
        print("❌ Không tìm thấy file gốc (bai_tap.pdf). Hãy tạo trước khi ký.")
        return

    # 1. Đọc khóa và tính hash
    key = load_secret_key()
    file_hash = sha256_file(INPUT_PDF)
    signature_hmac = hmac_sha256(key, file_hash)

    # 2. Đọc file PDF gốc
    reader = PdfReader(INPUT_PDF)
    writer = PdfWriter()
    num_pages = len(reader.pages)

    # 3. Tạo overlay chữ ký cho trang cuối
    last_page = reader.pages[-1]
    page_width = float(last_page.mediabox.width)
    page_height = float(last_page.mediabox.height)
    overlay_pdf = create_overlay(VISIBLE_TEXT, page_width, page_height)
    overlay_reader = PdfReader(overlay_pdf)
    overlay_page = overlay_reader.pages[0]

    # 4. Sao chép các trang và ghép chữ ký vào trang cuối
    for i in range(num_pages - 1):
        writer.add_page(reader.pages[i])
    base_last = reader.pages[-1]
    base_last.merge_page(overlay_page)
    writer.add_page(base_last)

    # 5. Ghi PDF đã ký
    with open(SIGNED_PDF, "wb") as f_out:
        writer.write(f_out)

    # 6. Tạo file chữ ký JSON
    sig_obj = {
        "signed_by": SIGNER_NAME,
        "timestamp": datetime.datetime.now().isoformat(),
        "sha256": file_hash,
        "hmac": signature_hmac
    }
    with open(SIG_FILE, "w", encoding="utf-8") as f:
        json.dump(sig_obj, f, ensure_ascii=False, indent=2)

    print("✅ Đã ký thành công!")
    print(f"PDF đã ký: {SIGNED_PDF}")
    print(f"Tệp chữ ký: {SIG_FILE}")

# ----------------------------
# Chạy trực tiếp
# ----------------------------
if __name__ == "__main__":
    sign_pdf()
