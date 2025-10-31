# tao_bai_tap_pdf.py
# Tạo file PDF mẫu (bai_tap.pdf) - yêu cầu reportlab
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import datetime
import os

OUT = "bai_tap.pdf"

def create_pdf(path=OUT):
    c = canvas.Canvas(path, pagesize=A4)
    width, height = A4
    c.setFont("Helvetica", 14)
    c.drawString(60, height - 80, "Bài tập lớn - Hệ thống quản lý (Sample)")
    c.setFont("Helvetica", 11)
    body = [
        "Người thực hiện: Thảo",
        "Môn: Thiết kế hệ thống",
        "",
        "Nội dung (mẫu):",
        "1. Mục tiêu: Tạo file PDF mẫu để ký điện tử dạng text (visible).",
        "2. Phần mô tả: Đây là file PDF mẫu được tạo tự động bởi script tao_bai_tap_pdf.py.",
        "",
        "Nội dung chi tiết có thể được thay thế bằng nội dung thực tế của bạn.",
        "",
        "KẾT THÚC TÀI LIỆU (phần ký sẽ được thêm bởi ky_bai_tap.py).",
    ]
    y = height - 110
    for line in body:
        c.drawString(60, y, line)
        y -= 18
        if y < 100:
            c.showPage()
            y = height - 60
    # footer with generation timestamp
    c.setFont("Helvetica-Oblique", 9)
    c.drawString(60, 30, f"Generated: {datetime.datetime.now().isoformat()}")
    c.save()
    print(f"Created: {path}")

if __name__ == '__main__':
    create_pdf()
