from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()
client = OpenAI(
  base_url = "https://integrate.api.nvidia.com/v1",
  api_key = os.getenv("NVIDIA_API_KEY2")
)

def ai_pdf(pdfPrompt):
  completion = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[{"role":"system","content":"Always Return JSON format without any additional formatting. No '\u2011' or any encoding"},
              {"role":"user","content":pdfPrompt}],
    temperature=1,
    top_p=1,
    max_tokens=2000,
    stream=False
  )
  return completion.choices[0].message.content