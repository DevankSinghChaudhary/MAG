from chunks import chunks
from data import ask, improved_output, cycle
from prompts import analysis_prompt, chunks
from models import call_analysis, chunks_model

def main():
    raw_data = ask()

    prompt = analysis_prompt(raw_data)

    ai_output = call_analysis(prompt)

    output = improved_output(ai_output)
    chunks_data = chunks(output)


if __name__ == "__main__":
    output = main()