import json
import asyncio
from chunks import chunks
from data import ask, improved_output
from prompts import analysis_prompt, chunks_prompt
from models import call_analysis, chunks_model


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
    print("##============================================================##")
    print(chunks_data)
    results = asyncio.run(run_all(chunks_data))
    print("##============================================================##")
    print(results)
    print("##============================================================##")
    print(len(chunks_data))
    print(len(results))