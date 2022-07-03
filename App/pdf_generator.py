from borb.pdf import Document
from borb.pdf.page.page import Page
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.page_layout.page_layout import PageLayout
from borb.pdf.pdf import PDF
from borb.pdf.canvas.layout.image.barcode import Barcode, BarcodeType  
from borb.pdf.canvas.layout.layout_element import LayoutElement
from borb.pdf.canvas.layout.text.paragraph import Paragraph  
from borb.pdf.canvas.color.color import HexColor  
from decimal import Decimal  
from borb.pdf.canvas.layout.table.flexible_column_width_table import FlexibleColumnWidthTable

def main():
    """ Wesh c'est une main fonction
    """
    # Create empty Document
    pdf = Document()

    # Create empty Page
    page = Page()

    # Add Page to Document
    pdf.add_page(page)

    # Create PageLayout
    layout: PageLayout = SingleColumnLayout(page)

    layout.add(
        Paragraph("Brand Seeker", 
            font_color=HexColor("#6d64e8"), 
            font_size=Decimal(20)
        )
    )

    qr_code: LayoutElement = Barcode(
        data="https://github.com/HumanBojack/BrandSeeker",
        width=Decimal(64),
        height=Decimal(64),
        type=BarcodeType.QR,
    )

    layout.add(
        FlexibleColumnWidthTable(number_of_columns=2, number_of_rows=1)
        .add(qr_code)
        .add(
            Paragraph(
                """
                500 South Buenos Eres Street
                Brand Seeker CA
                91521-0991 USA
                """,
                padding_top=Decimal(12),
                respect_newlines_in_text=True,
                font_color=HexColor("#666666"),
                font_size=Decimal(10),
            )
        )
        .no_borders()
    )
    # Future content-rendering-code to be inserted here
    
    # Attempt to store PDF
    with open("output.pdf", "wb") as pdf_file_handle:
        PDF.dumps(pdf_file_handle, pdf)

if __name__ == '__main__':
  main()