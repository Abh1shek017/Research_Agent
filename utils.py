import requests
import os
from tqdm import tqdm
from PyPDF2 import PdfReader

def download_pdf(url: str, save_path: str = "papers") -> str:
    """Downloads a PDF with progress bar"""
    os.makedirs(save_path, exist_ok=True)
    filename = os.path.join(save_path, url.split('/')[-1])
    
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    with open(filename, 'wb') as f, tqdm(
        desc=filename,
        total=total_size,
        unit='B',
        unit_scale=True
    ) as bar:
        for chunk in response.iter_content(chunk_size=1024):
            f.write(chunk)
            bar.update(len(chunk))
    
    return filename
def extract_text(pdf_path: str) -> str:
    """Extracts text from PDF"""
    text = []
    with open(pdf_path, 'rb') as f:
        reader = PdfReader(f)
        for page in reader.pages:
            text.append(page.extract_text())
    return "\n".join(text)