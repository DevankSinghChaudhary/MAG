from openai import OpenAI
from dotenv import load_dotenv
import os


load_dotenv()
client = OpenAI(
  base_url = "https://integrate.api.nvidia.com/v1",
  api_key = os.getenv("NVIDIA_API_KEY")
)
def call_analysis(prompt):
    completion = client.chat.completions.create(
      model="openai/gpt-oss-120b",
      messages=[{"role":"system","content":"DONT REPEATE ANY MONETISATION GAP/DIGITAL PRODUCT. Always Return JSON format without any additional formatting. No '\u2011' or any encoding. (NEVER GIVE ADVISE OF STARTING ANY KIND OF SAAS, NOT EVEN ONLINE WEB PORTAL OF ANY HABIT TRAKER ETC). Keep in mind this audit is mainly for outreaching influencer for monetising thier audience via digital products."},
                {"role":"user","content":prompt}],
      temperature=1,
      top_p=0.95,
      max_tokens=2000,
      stream=False
    )
    return completion.choices[0].message.content

def chunks_model(chunksPrompt):
  completion = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[{"role":"system","content":"DONT REPEATE ANY MONETISATION GAP/DIGITAL PRODUCT. Always Return JSON format without any additional formatting. No '\u2011' or any encoding. (NEVER GIVE ADVISE OF STARTING ANY KIND OF SAAS, NOT EVEN ONLINE WEB PORTAL OF ANY HABIT TRAKER ETC). Keep in mind this audit is mainly for outreaching influencer for monetising thier audience via digital products."},
              {"role":"user","content":chunksPrompt}],
    temperature=1,
    top_p=1,
    max_tokens=2000,
    stream=False
  )
  return completion.choices[0].message.content


def pdfCreation(pdfPrompt):
  completion = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[{"role":"system","content":"DONT REPEATE ANY MONETISATION GAP/DIGITAL PRODUCT. Always Return JSON format without any additional formatting. No '\u2011' or any encoding. (NEVER GIVE ADVISE OF STARTING ANY KIND OF SAAS, NOT EVEN ONLINE WEB PORTAL OF ANY HABIT TRAKER ETC). Keep in mind this audit is mainly for outreaching influencer for monetising thier audience via digital products."},
              {"role":"user","content": pdfPrompt}],
    temperature=0.5,
    top_p=0.95,
    max_tokens=10000,
    extra_body={"chat_template_kwargs":{"enable_thinking":True},"reasoning_budget":10000},
    stream=False
  )
  return completion.choices[0].message.content