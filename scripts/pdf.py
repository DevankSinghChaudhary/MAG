import os
from jinja2 import Template


def jinjaPdf(result_pdf):
    if not result_pdf:
        raise ValueError("Nothing in Jinja!!")
    result = result_pdf

    basedir = os.path.dirname(__file__)
    path  = os.path.join(basedir, "template.html")

    with open(path, encoding="utf-8") as file:
        pdf = Template(file.read())
        htmlcontent = pdf.render(result=result)
        return htmlcontent