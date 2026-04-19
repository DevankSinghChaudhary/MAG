def analyze(raw_data):
  if not raw_data:
    raise ValueError("No raw data for AI!")
  prompt = f"""
    You are a precise social media business analyst.

    Your task is to analyze a creator's bio and captions and extract structured business context.

    ---

    Return ONLY valid JSON with this exact structure:

    {{
      "niche": "...",
      "target_audience": "...",
      "monetization_type": "...",
      "link_strategy": "...",
      "content_type": "...",
      "primary_goal": "..."
    }}

    ---

    FIELD RULES:

    - niche: 3-6 words describing domain
    - target_audience: specific audience + intent
    - monetization_type: choose ONE:
      "affiliate-heavy", "digital-products", "brand-deals", "mixed", "none", "unknown"

    - link_strategy: describe how links are used
    - content_type: describe style of content
    - primary_goal: main business goal

    ---

    STRICT RULES:

    - Return ONLY JSON
    - Use double quotes
    - No extra text
    - If unsure, use "unknown"
    - Do NOT guess aggressively

    ---
    DATA:
    {raw_data}
    """
  return prompt

def analysis_prompt(structured_data, to_avoid, to_avoid_name, to_add):
  if not structured_data:
    raise ValueError("No raw data for AI!")
  prompt = f"""
  You are an expert creator strategist.

  Analyze the following creator data and provide actionable insights:

  {structured_data}

  Strictly follow these rules:
  - Return ONLY valid JSON
  - No explanations, no extra text
  - Keep responses concise and practical
  - Be specific, not generic

  {to_avoid}


  {to_avoid_name}

  
  {to_add}
  JSON format:
  {{
    "niche_clarity": "Evaluate how clear the niche is in 1-2 sentences",
    "target_audience": "Describe the ideal audience in 1-2 sentences",
    "monetization_gaps": [
      "List 3-5 specific missed monetization opportunities"
    ],
    "digital_product_ideas": [
      "List 3-5 highly relevant product ideas tailored to this creator"
    ]
  }}

  Specifically all keys and values with double qoutes (""), not single qoute ('') 
  """
  return prompt


def chunks_prompt(chunks_data):
  if not chunks_data:
    raise ValueError("No chunks data for AI!")
  prompt = f"""
  Convert this into a professional report statement:

  {chunks_data}

    Make it:
    - Clear
    - Concise
    - Professional tone

  JSON format:
  {{
    "monetization_gap_explanation": ""
  }}
  OR
  {{
    "digital_product_explaination": ""
  }}

  return based on if data's key is "monetization_gap" then return "monetization_gap_explanation" and if "digital_product" return "digital_product_explaination" 
  """
  return prompt

def pdf_prompt(items):
  if not items:
    raise ValueError("No data for pdf creation!!")
  prompt = f"""
  YOU ARE PROFESSIONAL SENIOR DATA ANALYST
  Convert this into professional report of the creator:

  {items}

  Your report will be used in the ADUIT.pdf directly, so make it like its talking to the creator itself.
  Not static report.

  Make it:
    - Clear
    - Professional Tone
    - Talking to creator directly

  Don't add but:
    - "Gap" in gap name like: "Homeschool Curriculum Gap" < Wrong
    - "Homeschool Curriculum" < Right

  JSON FORMAT YOU WILL DELIVER:
  {{
    "Gap_name": ""
    "Observation": "",
    "Impact": "",
    "Recommendation": ""
  }}


  EXAMPLE OF TONE OF EACH VALUE:
  Observation
    The current monetization strategy relies heavily on one-time transactions, which limits long-term revenue stability and reduces customer lifetime value. There is no clear mechanism in place to retain users or generate predictable, recurring income.

  Impact
    This approach creates inconsistent revenue streams and increases dependency on continuous customer acquisition. Over time, this can lead to higher marketing costs and reduced overall profitability.

  Recommendation
    Introduce a recurring revenue model, such as a subscription-based offering or membership tier, that provides ongoing value to users. This could include exclusive content, premium features, or community access. Implementing such a model would improve revenue predictability and strengthen customer retention. 
  
    
    MAKE OBSERVATION, IMPACT, RECOMMENDATION IMPACTFUL AND CONNECTING TO THEM.
  
  NOTE: ABOVE IS JUST EXAMPLE, IT MUST NOT INFLUENCE REPORT DATA EXCEPT TONE.
  Gap_name = Name of gap. e.g: Course Gap, Planner Gap, Content Gap etc 
  """
  return prompt