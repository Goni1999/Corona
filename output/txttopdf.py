from PyPDF2 import PdfWriter, PdfReader

def add_js_to_pdf(pdf_path, output_pdf):
    reader = PdfReader(pdf_path)
    writer = PdfWriter()

    # Add all pages from the existing PDF
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        writer.add_page(page)

    # JavaScript code to execute on PDF open
    js_code = "app.alert('This is an example alert');"
    writer.add_js(js_code)

    # Save the modified PDF with JavaScript
    with open(output_pdf, 'wb') as f:
        writer.write(f)

    print(f"JavaScript added to PDF {output_pdf}")

add_js_to_pdf("input.pdf", "output11.pdf")
