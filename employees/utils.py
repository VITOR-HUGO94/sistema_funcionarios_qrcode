import re
import pypdf

def extract_date_from_pdf(file_path):
    """
    Extrai a data de emissão de um PDF textual (não escaneado).
    Retorna None se não encontrar.
    """
    try:
        reader = pypdf.PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""

        # Expressões comuns de data: 01/01/2025, 1º de janeiro de 2025, etc.
        padroes = [
            r'\b\d{2}/\d{2}/\d{4}\b',                # 01/01/2025
            r'\b\d{1,2} de [a-zç]+ de \d{4}\b',      # 1 de janeiro de 2025
        ]

        for padrao in padroes:
            match = re.search(padrao, text, re.IGNORECASE)
            if match:
                return match.group(0)

        return None

    except Exception as e:
        print("Erro ao ler PDF:", e)
        return None
