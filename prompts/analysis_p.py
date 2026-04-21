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
  You are an expert creator strategist specializing in "create once, sell anytime" digital products.

  Analyze the following creator data and identify ONLY the most critical, actionable monetization gaps:

  {structured_data}

  CRITICAL INSTRUCTIONS:

  1. QUALITY OVER QUANTITY: Identify only 1-3 genuine monetization gaps. If only one real gap exists, return just one.
  2. DIGITAL PRODUCTS ONLY: Focus exclusively on digital products (courses, templates, ebooks, workbooks, guides, frameworks).
  3. AUTHENTIC GAPS: Each gap must reflect a real, specific opportunity - not forced or generic.
  4. DIRECT CONVERSATION: When listing gaps/products, write as if speaking directly to this creator about THEIR specific situation.

  {to_avoid}
  {to_avoid_name}
  {to_add}

  JSON format (STRICT):
  {{
    "niche_clarity": "1-2 sentence evaluation of how clear their niche positioning is",
    "target_audience": "1-2 sentence description of who they serve and what they need",
    "monetization_gaps": [
      "Only 1-3 real gaps. Each should be specific to THIS creator's content and audience."
    ],
    "digital_product_ideas": [
      "Only 1-3 product ideas that match the gaps above. Each must feel natural to their audience."
    ]
  }}

  Remember: Return ONLY valid JSON with double quotes. No explanations. No generic filler. No forcing 5 ideas if 2 are better.
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
  You are a strategic advisor writing directly to a creator about their business opportunities.

  Data to convert:
  {items}

  INSTRUCTIONS (READ CAREFULLY):

  1. CONVERSATIONAL TONE: Write as if you're having a genuine conversation with this specific creator.
  2. NO GENERIC LANGUAGE: Every sentence should feel personalized to their niche, audience, and current approach.
  3. HONEST ASSESSMENT: Be direct and authentic. If it's a real gap, explain it clearly. Don't overcomplicate.
  4. ACTIONABLE: Each recommendation should be concrete and implementable for THEIR situation specifically.
  5. NAME FORMAT: No word "Gap" in the name. Use the actual product/opportunity name (e.g., "Email Course", "Templates Library", not "Email Course Gap").

  TONE EXAMPLES:

  Observation (What's missing):
    You're creating amazing [content type], but your audience has no way to go deeper beyond free content. Right now, they engage, then disappear.

  Impact (Why it matters):
    This means you're leaving money on the table while your engaged audience is actively looking for the next step. Every person who could become a customer instead just scrolls past.

  Recommendation (What to do):
    Create a [specific product type] that takes your [specific content theme] to the next level. Price it at [realistic range], and promote it to your most engaged followers. This single product could generate [realistic revenue impact].

  JSON FORMAT:
  {{
    "Gap_name": "Name of the digital product/opportunity (no 'Gap' word)",
    "Observation": "What's missing from their current approach (talking directly to them)",
    "Impact": "Why this matters specifically for their business and audience",
    "Recommendation": "Concrete, specific action they can take (mention the product, audience segment, pricing approach)"
  }}

  RULES:
  - Return ONLY valid JSON
  - Use double quotes only
  - Be specific to THIS creator, not generic
  - Make it feel like real advice from someone who understands their business
  - No buzzwords, no fluff
  """
  return prompt