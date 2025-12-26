from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def generate_pdf(path, filename, steps, before, after):
    c = canvas.Canvas(path, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "AI Data Cleaning Report")

    c.setFont("Helvetica", 12)
    c.drawString(50, height - 90, f"File: {filename}")
    c.drawString(50, height - 120, f"Rows before cleaning: {before}")
    c.drawString(50, height - 150, f"Rows after cleaning: {after}")

    c.drawString(50, height - 190, "Steps Applied:")
    y = height - 220
    for step in steps:
        c.drawString(70, y, f"- {step}")
        y -= 25

    c.save()
