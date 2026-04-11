import json
import asyncio
from scripts import jinjaPdf
from chunks import chunks
from pdf import resultpdf, txt
from data import ask, improved_output
from prompts import analysis_prompt, chunks_prompt
from models import call_analysis, chunks_model
from weasyprint import HTML


def main():
    raw_data = ask()

    prompt = analysis_prompt(raw_data)

    ai_output = call_analysis(prompt)

    output = improved_output(ai_output)
    data = json.loads(output)

    chunks_data = chunks(data)
    return chunks_data
    
async def chunks_call(chunks_data):
    chunksPrompt = chunks_prompt(chunks_data)
    output = await asyncio.to_thread(chunks_model, chunksPrompt)
    return output


async def run_all(chunks_data):
    task = []
    for items in chunks_data:
        task.append(chunks_call(items))
    result = await asyncio.gather(*task)
    return result


if __name__ == "__main__":
    chunks_data = main()
    print(chunks_data)
    results = asyncio.run(run_all(chunks_data))
    result_pdf = resultpdf(results)
    content = jinjaPdf(result_pdf)
    HTML(string=content).write_pdf("Audit_Example.pdf")

    
