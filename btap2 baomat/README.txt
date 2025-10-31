Hướng dẫn nhanh (tiếng Việt)
----------------------------
Thư mục chứa các file:
  - tao_bai_tap_pdf.py   : tạo bai_tap.pdf (PDF gốc)
  - ky_bai_tap.py       : ký file (tạo bai_tap_signed.pdf và bai_tap.sig)
  - verify_pdf.py       : verify chữ ký đơn giản
  - private_key.pem     : file "secret" (dùng làm HMAC key)
  - cert.pem            : file chứng chỉ dummy
  - requirements.txt    : dependencies (reportlab, PyPDF2)

Các bước chạy (trong cùng một thư mục, ví dụ /mnt/data/sign_package):
  1) Tạo môi trường ảo (khuyến nghị) và cài dependencies:
     python -m venv venv
     source venv/bin/activate   # (Windows: venv\Scripts\activate)
     pip install -r requirements.txt

  2) Tạo PDF gốc:
     python tao_bai_tap_pdf.py
     -> tạo 'bai_tap.pdf'

  3) Ký PDF (thêm chữ ký hiển thị ở cuối trang và tạo file bai_tap.sig):
     python ky_bai_tap.py
     -> tạo 'bai_tap_signed.pdf' và 'bai_tap.sig'

  4) Kiểm tra chữ ký:
     python verify_pdf.py

Ghi chú:
  - Đây là 'ký logic đơn giản' (HMAC với secret text). Không phải chữ ký số theo tiêu chuẩn PKI.
  - Chữ ký hiển thị là dạng text ('Người ký: Thảo') được overlay lên trang cuối.
