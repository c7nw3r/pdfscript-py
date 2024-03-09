from unittest import TestCase

from pdfscript.__spi__.styles import TextStyle
from pdfscript.pdf_script import PDFScript
from pdfscript.stream.interceptor.audit_interceptor import AuditInterceptor
from pdfscript.stream.listener.bbox_listener import BBoxListener
from test import get_local_dir


class TextTest(TestCase):

    def test_paragraph(self):
        bbox_listener = BBoxListener("text")
        interceptor = AuditInterceptor()

        script = PDFScript.a4()
        script.text("Test asdf" * 30, listener=bbox_listener)

        script.render_as_file("simple.pdf", interceptor)
        interceptor.verify(f"{get_local_dir(__file__)}/test_paragraph.txt")

    def test_paragraph_with_custom_font(self):
        interceptor = AuditInterceptor()

        script = PDFScript.a4()
        script.text("Test asdf" * 20, TextStyle(font_name="Times-Bold", font_size=20))

        script.render_as_file("simple.pdf", interceptor)
        interceptor.verify(f"{get_local_dir(__file__)}/test_paragraph_with_custom_font_justified.txt")

    def test_paragraph_with_header_and_footer(self):
        interceptor = AuditInterceptor()

        script = PDFScript.a4()
        header = script.with_header()
        header.text("Test asdf" * 10)

        footer = script.with_footer()
        footer.text("Test asdf" * 10)

        script.text("Test asdf" * 20, TextStyle(font_size=16))

        script.render_as_file("simple.pdf", interceptor)
        interceptor.verify(f"{get_local_dir(__file__)}/test_paragraph_with_header_and_footer.txt")

    def test_long_text(self):
        bbox_listener = BBoxListener("text")
        interceptor = AuditInterceptor()

        script = PDFScript.a4()
        script.paragraph("The Wikimedia Foundation, Inc., abbreviated WMF, is an American 501(c)(3) nonprofit organization headquartered in San Francisco, California, and registered there as a charitable foundation. It is best known as the host of Wikipedia, the seventh most visited website in the world. However, the foundation also hosts 14 other related content projects. It also supports the development of MediaWiki, the wiki software that underpins them all.The Wikimedia Foundation was established, in 2003 in St. Petersburg, Florida, by Jimmy Wales as a nonprofit way to fund Wikipedia, Wiktionary, and other crowdsourced wiki projects. (Until then, they had been hosted by Bomis, Wales's for-profit company.) The Foundation finances itself mainly through millions of small donations from Wikipedia readers, collected through email campaigns and annual fundraising banners placed on Wikipedia and its sister projects. These are complemented by grants from philanthropic organizations and tech companies, and starting in 2022, by services income from Wikimedia Enterprise.", listener=bbox_listener)
        script.paragraph("The Wikimedia Foundation, Inc., abbreviated WMF, is an American 501(c)(3) nonprofit organization headquartered in San Francisco, California, and registered there as a charitable foundation. It is best known as the host of Wikipedia, the seventh most visited website in the world. However, the foundation also hosts 14 other related content projects. It also supports the development of MediaWiki, the wiki software that underpins them all.The Wikimedia Foundation was established, in 2003 in St. Petersburg, Florida, by Jimmy Wales as a nonprofit way to fund Wikipedia, Wiktionary, and other crowdsourced wiki projects. (Until then, they had been hosted by Bomis, Wales's for-profit company.) The Foundation finances itself mainly through millions of small donations from Wikipedia readers, collected through email campaigns and annual fundraising banners placed on Wikipedia and its sister projects. These are complemented by grants from philanthropic organizations and tech companies, and starting in 2022, by services income from Wikimedia Enterprise.", listener=bbox_listener)
        script.paragraph("The Wikimedia Foundation, Inc., abbreviated WMF, is an American 501(c)(3) nonprofit organization headquartered in San Francisco, California, and registered there as a charitable foundation. It is best known as the host of Wikipedia, the seventh most visited website in the world. However, the foundation also hosts 14 other related content projects. It also supports the development of MediaWiki, the wiki software that underpins them all.The Wikimedia Foundation was established, in 2003 in St. Petersburg, Florida, by Jimmy Wales as a nonprofit way to fund Wikipedia, Wiktionary, and other crowdsourced wiki projects. (Until then, they had been hosted by Bomis, Wales's for-profit company.) The Foundation finances itself mainly through millions of small donations from Wikipedia readers, collected through email campaigns and annual fundraising banners placed on Wikipedia and its sister projects. These are complemented by grants from philanthropic organizations and tech companies, and starting in 2022, by services income from Wikimedia Enterprise.", listener=bbox_listener)
        script.paragraph("The Wikimedia Foundation, Inc., abbreviated WMF, is an American 501(c)(3) nonprofit organization headquartered in San Francisco, California, and registered there as a charitable foundation. It is best known as the host of Wikipedia, the seventh most visited website in the world. However, the foundation also hosts 14 other related content projects. It also supports the development of MediaWiki, the wiki software that underpins them all.The Wikimedia Foundation was established, in 2003 in St. Petersburg, Florida, by Jimmy Wales as a nonprofit way to fund Wikipedia, Wiktionary, and other crowdsourced wiki projects. (Until then, they had been hosted by Bomis, Wales's for-profit company.) The Foundation finances itself mainly through millions of small donations from Wikipedia readers, collected through email campaigns and annual fundraising banners placed on Wikipedia and its sister projects. These are complemented by grants from philanthropic organizations and tech companies, and starting in 2022, by services income from Wikimedia Enterprise.", listener=bbox_listener)

        script.render_as_file("simple.pdf", interceptor)
        interceptor.verify(f"{get_local_dir(__file__)}/test_long_text.txt")

    def test_long_paragraphs(self):
        bbox_listener = BBoxListener("text")
        interceptor = AuditInterceptor()

        script = PDFScript.a4()
        script.paragraph("Wikimedia Commons – repository of images, sounds, videos, and general media")
        script.paragraph("Wikispecies – taxonomic catalog of species")

        script.render_as_file("simple.pdf", interceptor)
        interceptor.verify(f"{get_local_dir(__file__)}/test_long_paragraphs.txt")

    def test_text_overflow(self):
        bbox_listener = BBoxListener("text")
        interceptor = AuditInterceptor()

        script = PDFScript.a4()
        script.paragraph("This is an example text. " * 200)

        script.render_as_file("simple.pdf", interceptor)
        interceptor.verify(f"{get_local_dir(__file__)}/test_text_overflow.txt")
