def analysis_prompt(raw_data):
  if not raw_data:
    raise ValueError("No raw data for AI!")
  prompt = f"""
  You are an expert creator strategist.

  Analyze the following creator data and provide actionable insights:

  {raw_data}

  Strictly follow these rules:
  - Return ONLY valid JSON
  - No explanations, no extra text
  - Keep responses concise and practical
  - Be specific, not generic

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
  
  
  NOTE: ABOVE IS JUST EXAMPLE, IT MUST NOT INFLUENCE REPORT DATA EXCEPT TONE.
  Gap_name = Name of gap. e.g: Course Gap, Planner Gap, Content Gap etc 
  """
  return prompt