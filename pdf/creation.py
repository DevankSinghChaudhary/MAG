import json
from models import ai_pdf
from prompts import pdf_prompt
from data import improved_output


def resultpdf(results):
    item = []
    for items in results:
        pdfPrompt = pdf_prompt(items)
        raw_result = ai_pdf(pdfPrompt)
        result = improved_output(raw_result)
        result2 = json.loads(result)
        item.append(result2)
    return item


def txt(result_pdf):
    if not result_pdf:
        raise ValueError("Nothing for TXT Insertion!")
    for items in result_pdf:
        stritems = str(items)
        with open("result.txt","w", encoding="utf-8") as file:
            file.write(stritems)