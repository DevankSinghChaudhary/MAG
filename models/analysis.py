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
      messages=[{"role":"system","content":"DONT REPEATE ANY MONETISATION GAP/DIGITAL PRODUCT. Always Return JSON format without any additional formatting. No '\u2011' or any encoding. (NEVER GIVE ADVISE OF STARTING ANY KIND OF SAAS, NOT EVEN ONLINE WEB PORTAL OF ANY HABIT TRAKER ETC). CRITICAL: Only suggest creator-owned DIGITAL products. NEVER physical products, merchandise, tangible goods, or affiliate/reseller opportunities. Keep in mind this audit is mainly for outreaching influencer for monetising thier audience via creator-owned digital products. ENSURE ALL PRODUCT IDEAS ARE IN DISTINCT CATEGORIES - DO NOT SUGGEST OVERLAPPING OR DUPLICATE CATEGORIES LIKE 'COURSE' AND 'VIDEO COURSE'."},
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
    messages=[{"role":"system","content":"DONT REPEATE ANY MONETISATION GAP/DIGITAL PRODUCT. Always Return JSON format without any additional formatting. No '\u2011' or any encoding. (NEVER GIVE ADVISE OF STARTING ANY KIND OF SAAS, NOT EVEN ONLINE WEB PORTAL OF ANY HABIT TRAKER ETC). CRITICAL: Only suggest creator-owned DIGITAL products. NEVER physical products, merchandise, tangible goods, or affiliate/reseller opportunities. Keep in mind this audit is mainly for outreaching influencer for monetising thier audience via creator-owned digital products. ENSURE ALL PRODUCT IDEAS ARE IN DISTINCT CATEGORIES - DO NOT SUGGEST OVERLAPPING OR DUPLICATE CATEGORIES LIKE 'COURSE' AND 'VIDEO COURSE'."},
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
    messages=[{"role":"system","content":"DONT REPEATE ANY MONETISATION GAP/DIGITAL PRODUCT. Always Return JSON format without any additional formatting. No '\u2011' or any encoding. (NEVER GIVE ADVISE OF STARTING ANY KIND OF SAAS, NOT EVEN ONLINE WEB PORTAL OF ANY HABIT TRAKER ETC). CRITICAL: Only recommend creator-owned DIGITAL products. NEVER physical products, merchandise, tangible goods, or affiliate/reseller opportunities. Keep in mind this audit is mainly for outreaching influencer for monetising thier audience via creator-owned digital products. ENSURE ALL PRODUCT IDEAS ARE IN DISTINCT CATEGORIES - DO NOT SUGGEST OVERLAPPING OR DUPLICATE CATEGORIES LIKE 'COURSE' AND 'VIDEO COURSE'."},
              {"role":"user","content": pdfPrompt}],
    temperature=0.5,
    top_p=0.95,
    max_tokens=10000,
    extra_body={"chat_template_kwargs":{"enable_thinking":True},"reasoning_budget":10000},
    stream=False
  )
  return completion.choices[0].message.content


def test_carousel_model(prompt):
  completion = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[{"role":"system","content":"You are an expert in creating engaging social media content strategies. Always return JSON format without any additional formatting. Focus on practical, step-by-step plans for content creation. CRITICAL: The 7-day carousel must be for a creator-owned DIGITAL product ONLY. NEVER create content for physical products, merchandise, or affiliate/reseller opportunities. ENSURE ALL PRODUCT IDEAS ARE IN DISTINCT CATEGORIES - DO NOT SUGGEST OVERLAPPING OR DUPLICATE CATEGORIES LIKE 'COURSE' AND 'VIDEO COURSE'."},
              {"role":"user","content":prompt}],
    temperature=0.8,
    top_p=0.95,
    max_tokens=3000,
    stream=False
  )
  return completion.choices[0].message.content