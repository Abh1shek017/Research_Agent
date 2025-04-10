import requests
import os
from tqdm import tqdm
from PyPDF2 import PdfReader

def download_pdf(url: str, save_path: str = "papers") -> str:
    """Downloads a PDF from the given URL and saves it with a .pdf extension in the specified folder."""
    os.makedirs(save_path, exist_ok=True)

    # Always ensure the filename ends with .pdf
    filename = url.split('/')[-1]
    if not filename.endswith('.pdf'):
        filename += ".pdf"

    file_path = os.path.join(save_path, filename)

    response = requests.get(url, stream=True)

    # Check for valid response
    if response.status_code != 200 or "application/pdf" not in response.headers.get("Content-Type", ""):
        raise ValueError(f"Failed to download PDF: {url}")

    total_size = int(response.headers.get('content-length', 0))

    with open(file_path, 'wb') as f, tqdm(
        desc=f"📥 Downloading {filename}",
        total=total_size,
        unit='B',
        unit_scale=True
    ) as bar:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                bar.update(len(chunk))

    return file_path

def extract_text(pdf_path: str) -> str:
    """Extracts text from a given PDF file."""
    text = []
    with open(pdf_path, 'rb') as f:
        reader = PdfReader(f)
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text.append(extracted)
    return "\n".join(text)
