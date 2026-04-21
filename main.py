import json
import asyncio
from chunks import chunks
from pdf import resultpdf
from pdf.reportlab_pdf import create_pdf
from data import ask, improved_output
from prompts import analysis_prompt, chunks_prompt, to_avoid_name, to_avoid, to_add, analyze, test_carousel_prompt
from models import call_analysis, chunks_model, test_carousel_model


def main():
    raw_data = ask()
    structured_data = analyze(raw_data)

    prompt = analysis_prompt(structured_data, to_avoid, to_avoid_name, to_add)

    ai_output = call_analysis(prompt)

    output = improved_output(ai_output)
    data = json.loads(output)

    chunks_data = chunks(data)
    return raw_data, structured_data, data, chunks_data
    return raw_data, structured_data, data, chunks_data
    
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
    raw_data, structured_data, data, chunks_data = main()
    print(chunks_data)
    results = asyncio.run(run_all(chunks_data))
    result_pdf = resultpdf(results)
    print(result_pdf)
    
    # Generate test carousel
    carousel_prompt = test_carousel_prompt(raw_data, structured_data, data)
    carousel_output = test_carousel_model(carousel_prompt)
    carousel_data = json.loads(improved_output(carousel_output))
    print("Carousel data:", carousel_data)
    
    name = raw_data["name"]
    followers = raw_data.get("followers")
    create_pdf(result_pdf, name, followers=followers, carousel_data=carousel_data)

    
