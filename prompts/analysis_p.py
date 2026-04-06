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
  You are an expert data analysit for "INSTAGRAM INFULENCERS".
  
  Analyze this data and return only json format:
  
  {chunks_data}

  Strictly follow these rules:
  - Return ONLY valid JSON
  - No explanations, no extra text
  - Keep responses concise and practical
  - Be specific, not generic

  JSON format:
  {{
  "monetization_gap_explanation": ""
  }}
  OR
  {{
  "digital_product_explaination": ""
  }}

  return based on if data's thrid key is "monetization_gap" then return "monetization_gap_explanation" and if "digital_product" return "digital_product_explaination" 
  """
  return prompt