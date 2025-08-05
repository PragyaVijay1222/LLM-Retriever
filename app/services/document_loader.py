import fitz  
import requests
from io import BytesIO

def load_pdf_from_url(url: str) -> str:
    response = requests.get(url)
    doc = fitz.open(stream=BytesIO(response.content), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text