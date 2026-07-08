from pypdf import PdfReader


def extract_text(file, filename):

    if filename.endswith(".txt"):
        content = file.read()
        return content.decode("utf-8")


    elif filename.endswith(".pdf"):

        reader = PdfReader(file)

        text = ""

        for page in reader.pages:
            text += page.extract_text() or ""

        return text


    else:
        raise ValueError(
            "Only .txt and .pdf files are supported"
        )