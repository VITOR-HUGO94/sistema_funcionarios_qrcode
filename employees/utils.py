# employees/utils.py
import re
import pypdf

def extract_date_from_pdf(file_or_path):
    """
    Extrai a data de emissão de um PDF textual (não escaneado).
    Aceita tanto um path (string) quanto um file-like (ex.: FieldFile).
    Retorna a string encontrada (ex: '01/01/2025' ou '1 de janeiro de 2025') ou None.
    """
    try:
        # pypdf aceita file-like objects
        reader = pypdf.PdfReader(file_or_path)
        text = ""
        for page in reader.pages:
            t = page.extract_text()
            if t:
                text += t

        padroes = [
            r'\b\d{2}/\d{2}/\d{4}\b',                # 01/01/2025
            r'\b\d{1,2}\s*(?:º|º?)?\s*de\s+[a-zç]+\s+de\s+\d{4}\b',  # 1 de janeiro de 2025 (com ou sem º)
            r'\b\d{1,2}\s+[a-zç]+\s+\d{4}\b',        # 1 janeiro 2025
        ]

        for padrao in padroes:
            match = re.search(padrao, text, re.IGNORECASE)
            if match:
                return match.group(0)

        return None

    except Exception as e:
        # Não interromper o fluxo; logue para troubleshooting
        print("Erro ao ler PDF para extração de data:", e)
        return None
