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
from borb.pdf.canvas.layout.image.image import Image
from borb.pdf.canvas.layout.table.table import TableCell  
from borb.pdf.canvas.layout.table.fixed_column_width_table import FixedColumnWidthTable
from borb.pdf.canvas.layout.list.unordered_list import UnorderedList
from pathlib import Path
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.shape.shape import Shape
from borb.pdf.page.page_size import PageSize
from borb.pdf.canvas.line_art.line_art_factory import LineArtFactory
import typing
import random

def add_gray_artwork_upper_right_corner(page: Page):
    """
    This method will add a gray artwork of squares and triangles in the upper right corner
    of the given Page
    """
    grays: typing.List[HexColor] = [
        HexColor("A9A9A9"),
        HexColor("D3D3D3"),
        HexColor("DCDCDC"),
        HexColor("E0E0E0"),
        HexColor("E8E8E8"),
        HexColor("F0F0F0"),
    ]
    ps: typing.Tuple[Decimal, Decimal] = PageSize.A4_PORTRAIT.value
    N: int = 4
    M: Decimal = Decimal(32)
    
    # Draw triangles
    for i in range(0, N):
        x: Decimal = ps[0] - N * M + i * M
        y: Decimal = ps[1] - (i + 1) * M
        rg: HexColor = random.choice(grays)
        Shape(
            points=[(x + M, y), (x + M, y + M), (x, y + M)],
            stroke_color=rg,
            fill_color=rg,
        ).layout(page, Rectangle(x, y, M, M))
        
    # Draw squares
    for i in range(0, N - 1):
        for j in range(0, N - 1):
            if j > i:
                continue
            x: Decimal = ps[0] - (N - 1) * M + i * M
            y: Decimal = ps[1] - (j + 1) * M
            rg: HexColor = random.choice(grays)
            Shape(
                points=[(x, y), (x + M, y), (x + M, y + M), (x, y + M)],
                stroke_color=rg,
                fill_color=rg,
            ).layout(page, Rectangle(x, y, M, M))

def add_colored_artwork_bottom_right_corner(page: Page):
    """
    This method will add a blue/purple artwork of lines 
    and squares to the bottom right corner
    of the given Page
    """
    ps: typing.Tuple[Decimal, Decimal] = PageSize.A4_PORTRAIT.value
    
    # Square
    Shape(
      points=[
          (ps[0] - 32, 40),
          (ps[0], 40),
          (ps[0], 40 + 32),
          (ps[0] - 32, 40 + 32),
      ],
      stroke_color=HexColor("d53067"),
      fill_color=HexColor("d53067"),
    ).layout(page, Rectangle(ps[0] - 32, 40, 32, 32))
    
    # Square
    Shape(
      points=[
          (ps[0] - 64, 40),
          (ps[0] - 32, 40),
          (ps[0] - 32, 40 + 32),
          (ps[0] - 64, 40 + 32),
      ],
      stroke_color=HexColor("eb3f79"),
      fill_color=HexColor("eb3f79"),
    ).layout(page, Rectangle(ps[0] - 64, 40, 32, 32))
    
    # Triangle
    Shape(
      points=[
          (ps[0] - 96, 40),
          (ps[0] - 64, 40),
          (ps[0] - 64, 40 + 32),
      ],
      stroke_color=HexColor("e01b84"),
      fill_color=HexColor("e01b84"),
    ).layout(page, Rectangle(ps[0] - 96, 40, 32, 32))
        
    # Line
    r: Rectangle = Rectangle(Decimal(0), Decimal(32), ps[0], Decimal(8))
    Shape(
      points=LineArtFactory.rectangle(r),
      stroke_color=HexColor("283592"),
      fill_color=HexColor("283592"),
    ).layout(page, r)

def pdf_generator():

    # Create empty Document
    pdf = Document()

    # Create empty Page
    page = Page()

    IMAGE_PATH = Path(r'App\images\uber-eats-1024x682.jpg')

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
                50 Rue de la gamelle
                Brand Seeker CA
                59000 FR
                """,
                padding_top=Decimal(12),
                respect_newlines_in_text=True,
                font_color=HexColor("#666666"),
                font_size=Decimal(10),
            )
        )
        .no_borders()
    )
    # Title
    layout.add(
        Paragraph(
            "Video name", font_color=HexColor("#283592"), font_size=Decimal(34)
        )
    )

    # Subtitle
    layout.add(
        Paragraph(
            "Date: ",
            font_color=HexColor("#e01b84"),
            font_size=Decimal(11),
        )
    )
    layout.add(
        Paragraph(
            "Length: ",
            font_color=HexColor("#e01b84"),
            font_size=Decimal(11),
        )
    )
    for i in range(0,3):
        layout.add(
        FixedColumnWidthTable(
            number_of_rows=2,
            number_of_columns=2,
            column_widths=[Decimal(0.3), Decimal(0.7)],
        )
        .add(
            # Add the frame
            TableCell(
                Image(
                    IMAGE_PATH,
                    width=Decimal(128),
                    height=Decimal(128),
                ),
                row_span=2,
            )
        )
        .add(
            Paragraph(
                "Frames and confidence",
                font_color=HexColor("e01b84"),
                font="Helvetica-Bold",
                padding_bottom=Decimal(10),
            )
        )
        .add(
            UnorderedList()
            .add(Paragraph("Frame nb : [confidence value]"))
        )
        .no_borders()
    )
    # Future content-rendering-code to be inserted here
    add_colored_artwork_bottom_right_corner(page)
    add_gray_artwork_upper_right_corner(page)
    # Attempt to store PDF
    with open("App/output.pdf", "wb") as pdf_file_handle:
        PDF.dumps(pdf_file_handle, pdf)

pdf_generator()