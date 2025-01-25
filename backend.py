import os
import PyPDF2

from llama_index import GPTSimpleVectorIndex, Document

os.environ["OPENAI_API_KEY"] = "..."


def read_pdf(file_path):
    """reads a PDF and extracts its text."""
    with open(file_path, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


# Path to your PDF file
pdf_path = "test.pdf"

# Extract text and create a document
pdf_text = read_pdf(pdf_path)
documents = [Document(pdf_text)]

# Build the index
index = GPTSimpleVectorIndex.from_documents(documents)

# (Optional) Save the index for later use
index.save_to_disk("pdf_index.json")

# Query the index to summarize the PDF content
response = index.query("Summarize the main points of the document.")
print(response)