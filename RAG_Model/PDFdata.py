from llama_index.core.readers import StringIterableReader
import regex as re
from io import BytesIO, StringIO
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

def getDataFromPDF(pdf_paths):

    rag_docs = []
    for pdf_path in pdf_paths:
        pdf_data = open(pdf_path, 'rb').read()

        text_paras = []
        parser = PDFParser(BytesIO(pdf_data))
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        for page in PDFPage.create_pages(doc):
            output_string = StringIO()
            device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            interpreter.process_page(page)
            page_text = output_string.getvalue()
            text_paras.extend(re.split(r'\n\s*\n', page_text))

        rag_docs_data = StringIterableReader().load_data(text_paras)
        rag_docs.extend(rag_docs_data)

    return rag_docs