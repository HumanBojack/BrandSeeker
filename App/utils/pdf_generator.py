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
from datetime import date
import cv2
import typing
import random
import shutil
import os
import unicodedata

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

def load_frames(video_path, output_dict):

    # Path to tmp file
    tmp_path = 'tmp'

    try:
        shutil.rmtree(tmp_path)
    except OSError as e:
        pass
    
    os.makedirs('tmp', exist_ok=True)

    # Create a capture from video and get fps, number of frames and calculate video length 
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) 
    length = frame_count/fps

    # create all list needed
    frame_seq_list = []
    brand_list = []
    confidence_list = []
    bbxs = []
    path_list = []
    path_cropped_list= []

    # Get values needed from filtered dict
    for key, value in output_dict.items():
        # brand
        brand_list.append(key)
        # median confidence
        confidence_list.append(value[1])
        # frame
        frame_seq_list.append(value[2])
        # bbx
        bbxs.append(value[3])

    # Save frames and cropped frames with bbx axes
    for i, elem in enumerate(frame_seq_list):

        bbx = [max(0, int(bbxs[i][1])), max(0, int(bbxs[i][3])), max(0, int(bbxs[i][0])), max(0, int(bbxs[i][2]))] # ymin, ymax, xmin, xmax
        cap.set(1, elem)  # Where frame_no is the frame you want
        ret, frame = cap.read()  # Read the frame

        if ret:
            cropped_frame = frame[bbx[0]:bbx[1], bbx[2]:bbx[3]]
            cv2.imwrite('tmp/frame_'+str(frame_seq_list[i])+'.jpg', frame)
            cv2.imwrite('tmp/frame_'+str(frame_seq_list[i])+'_cropped.jpg', cropped_frame)
            path_list.append('tmp/frame_'+str(frame_seq_list[i])+'.jpg')
            path_cropped_list.append('tmp/frame_'+str(frame_seq_list[i])+'_cropped.jpg')
    
    # Release capture
    cap.release()

    # Normalise all caracters and replace space with underscore for the saved pdf name
    video_name = normalize(video_path)
    frame_time = [int(item / fps) for item in frame_seq_list]
    frame_minutes = [int(item/60) for item in frame_time]
    frame_seconds = [int(item%60) for item in frame_time]

    return video_name, length, confidence_list, brand_list, path_list, path_cropped_list, frame_minutes, frame_seconds

def normalize(path):
    string = os.path.basename(path).split(".")[0].replace(" ", "_")
    string = unicodedata.normalize('NFD', string).encode('ascii', 'ignore')
    string = string.decode("utf-8")
    return string

def pdf_generator(video_path, output_dict, save_dir):
    """
        _summary_: This function render the pdf 
    
        args: video_path: [str] | path to the video
              output_dict: [dict] | output dictionnary after brandseeker algorithm output filter
    
        return: video_name.pdf
    """
    # Write frames and return a path list
    video_name, length, confidence_list, brand_list, path_list, path_cropped_list, frame_minutes, frame_seconds = load_frames(video_path, output_dict)
    
    # Video length in m, s
    minutes = int(length/60)
    seconds = int(length%60)
    
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
    # Add qr code
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
            str(video_name[:45]), font_color=HexColor("#283592"), font_size=Decimal(16)
        )
    )
    # Subtitles
    layout.add(
        Paragraph(
            "Date: "+str(date.today().strftime("%B %d, %Y")),
            font_color=HexColor("#e01b84"),
            font_size=Decimal(11)
        )
    )
    layout.add(
        Paragraph(
            "Duration: "+ str(minutes) + 'm ' + str(seconds) + 's',
            font_color=HexColor("#e01b84"),
            font_size=Decimal(11),
        )
    )
    # Add each pictures
    for i in range(0, len(path_list)):
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
                    Path(path_list[i]),
                    width=Decimal(128),
                    height=Decimal(128),
                ),
                row_span=2,
            )
        )
        .add(
            Paragraph(
                brand_list[i],
                font_color=HexColor("e01b84"),
                font="Helvetica-Bold",
                padding_bottom=Decimal(10),
            )
        )
        .add(
            UnorderedList()
            .add(Paragraph("Time: " + str(frame_minutes[i]) + 'm ' + (str(frame_seconds[i])) + 's'))
            .add(Paragraph("Median confidence: " + str(confidence_list[i])))
            .add(Paragraph("Detected bounding box: "))
            .add(Image(Path(path_cropped_list[i],                    
                        width=Decimal(64),
                        height=Decimal(32))))
        )
        .no_borders()
    )

    for i in range(0, int(pdf.get_document_info().get_number_of_pages())):
        add_colored_artwork_bottom_right_corner(pdf.get_page(i))
        add_gray_artwork_upper_right_corner(pdf.get_page(i))

    with open(save_dir + '/' + str(video_name) + '.pdf', "wb") as pdf_file_handle:
        PDF.dumps(pdf_file_handle, pdf)
