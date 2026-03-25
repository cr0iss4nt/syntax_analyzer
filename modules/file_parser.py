from striprtf.striprtf import rtf_to_text
from pathlib import Path
import pdfplumber
import docx2txt

def parse_txt(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
        return content

def parse_rtf(filename):
    with open(filename) as f:
        content = f.read()
        text = rtf_to_text(content)
        return text

def parse_pdf(filename):
    text = ''
    with pdfplumber.open(filename) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + '\n'
    return text

def parse_docx(filename):
    text = docx2txt.process(filename)
    return text

def parse_file(filename):
    path = Path(filename)
    match path.suffix:
        case '.rtf':
            return parse_rtf(filename)
        case '.txt':
            return parse_txt(filename)
        case '.pdf':
            return parse_pdf(filename)
        case '.docx':
            return parse_docx(filename)
        case _:
            return ""