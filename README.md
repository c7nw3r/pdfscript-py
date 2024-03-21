# pdfscript-py

PDFScript is an open source software library for script based PDF generation
using a rendering evaluation graph. The graph nodes are used to evaluate the
bounding boxes of each renderable before it gets rendered. The evaluation
graphs enables **pdfscript-py** to auto-adjust the renderables within the boundaries of a page.

## Quickstart

A PDF script is initiated by calling one of the static methods e.g. "a4".
The static method call opens a new PDFScriptStream, which is used to create
an evaluation graph. By calling one of the **render** functions on the script stream, the PDF
pages gets rendered.

```
script = PDFScript.a4()
script.text("Hello world")

script.render_as_file("simple.pdf")
bytes = script.render_as_stream()
``` 

A PDFScriptStream automatically takes care of the boundaries of a PDF page format (e.g. a4).
If a row or column overflows the available space, the text automatically wraps to the available space.

For example the following script creates an evaluation graph which leads to multiple lines.
```
script = PDFScript.a4()
script.text("Lorem ipsum dolor sit amet, consectetur adipisici elit, sed eiusmod tempor incidunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquid ex ea commodi consequat. Quis aute iure reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint obcaecat cupiditat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")
``` 

## Header and Footer

By using the **withHeader** and **withFooter** function, it is possible to create a header and/or footer content for each page.
PDFScript automatically takes care of the page format boundary adjustments.

```
script = PDFScript.a4()

header = script.with_header()
header.text("Header Text")

footer = script.with_footer()
footer.text("Footer Text")
``` 

## Table

PDFScript provides a flexible way of table rendering. By default, PDFScript auto adjusts each
column by giving each column the same amount of space.

```
script = PDFScript.a4()

table = script.table()
table_row1 = table.row()
table_row1.col().text("Column 1")
table_row1.col().text("Column 2")

table_row2 = table.row()
table_row2.col().text("Column 3")
table_row2.col().text("Column 4")
``` 

## Image
PDFScript renders a jpg or png image by calling **image** with an image source, width and height argument.
The image source can be a url, a byte array or a supplier of an input stream.
```
script = PDFScript.a4()
script.image(path, ImageStyle(width=50, height=30))
```

## Paragraph
A paragraph groups multiple renderables and separates them from other elements by a newline before and after the paragraph.
```
script = PDFScript.a4()
script.paragraph("Lorem ipsum dolor sit amet, consectetur adipisici elit, sed eiusmod tempor incidunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquid ex ea commodi consequat. Quis aute iure reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint obcaecat cupiditat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")
```

## Bold
By using the bold renderable a text can be styled in a bold manner. The specific font is selected automatically.
When using a non standard font the bold style font have to be registered.
```
script = PDFScript.a4()
script.bold("Text")
```

## Canvas
A canvas supports to draw elements on an absolute position without adjusting the current position of the element flow.
So by the use of a canvas it is possible to draw elements in a free way onto the pdf.

Each function within the *withCanvas* block accepts the x and y coordinates on the pdf. While the x coordinate starts
on the left of the page, the y coordinate starts on the bottom. A negative x value can be used to start on the right
and a negative y value can be used to start from the top.

```
script = PDFScript.a4()
canvas = script.with_canvas()
canvas.draw_line(100, 100, 200, 200)
```

## Unit Testing
PDFScript supports pixel perfect PDF rendering unit tests by using the **AuditInterceptor**.
The **AuditInterceptor** collects the raw PDF instructions so that a unit test simple asserts the
actual raw commands with the expected commands. (collected from a previous pdf rendering run)

```
class TextTest(TestCase):

    def test_paragraph(self):
        interceptor = AuditInterceptor()

        script = PDFScript.a4()
        script.text("Text")

        script.render_as_stream(interceptor)
        interceptor.verify("test_paragraph.txt")
```
