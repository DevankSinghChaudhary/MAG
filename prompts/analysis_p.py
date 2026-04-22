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
  3. NO PHYSICAL PRODUCTS: Never suggest or include physical products, merchandise, or tangible goods.
  4. NO AFFILIATE PRODUCTS: Do NOT suggest existing affiliate products they use. Do NOT suggest ANY new affiliate products or promotions. Only creator-owned digital products.
  5. AUTHENTIC GAPS: Each gap must reflect a real, specific opportunity - not forced or generic.
  6. DIRECT CONVERSATION: When listing gaps/products, write as if speaking directly to this creator about THEIR specific situation.

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
      "Only 1-3 creator-owned digital product ideas. NO physical products. NO affiliate products. Each must feel natural to their audience."
    ]
  }}

  Remember: Return ONLY valid JSON with double quotes. No explanations. No generic filler. No forcing 5 ideas if 2 are better. CRITICAL: Every digital product must be creator-owned content, NOT affiliate or reseller products, and NEVER physical goods.
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
  6. NO PHYSICAL PRODUCTS: Never recommend physical products, merchandise, or tangible goods.
  7. NO AFFILIATE PRODUCTS: Never recommend affiliate products or reseller opportunities. Only creator-owned digital products.

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
  - The recommended product must be a creator-owned digital product (course, template, guide, etc.)
  - Never recommend physical products or affiliate/reseller opportunities
  """
  return prompt


def test_carousel_prompt(raw_data, structured_data, gaps_data):
  if not raw_data or not structured_data or not gaps_data:
    raise ValueError("No data for test carousel generation!")
  
  # Pick the first product idea to focus on
  product_ideas = gaps_data.get("digital_product_ideas", [])
  selected_product = product_ideas[0] if product_ideas else "Digital Course"
  
  prompt = f"""
  You are an expert social media strategist creating a 7-day carousel content series for digital product promotion.

  FOCUS PRODUCT: {selected_product}

  Based on the creator's data, create a 7-day carousel workbook that tells a complete story around this ONE product. Structure it as:

  DAYS 1-2: AUDIENCE DEMAND ANALYSIS
  - Analyze what the audience really needs
  - Build curiosity and desire
  - No selling, just understanding their pain points

  DAYS 3-5: FREE VALUE DELIVERY  
  - Provide genuine value related to the product
  - Show expertise and build trust
  - Position yourself as the solution provider

  DAYS 6-7: CONVERSION
  - Present the product as the natural next step
  - Create urgency and scarcity
  - Guide them to purchase

  Creator Data:
  Raw Data: {raw_data}
  Structured Data: {structured_data}
  Gaps Data: {gaps_data}

  REQUIREMENTS:
  1. Focus ENTIRELY on the product: {selected_product}
  2. Each day must have: focus, content_idea (slide breakdown), hook, call_to_action
  3. Content should flow as a cohesive 7-day story
  4. Use clean, professional language - no rich formatting like "48hour" or "15minute"
  5. Make it conversational and engaging for PDF rendering
  6. The product must be a creator-owned digital product - NO physical products, NO affiliate products

  JSON FORMAT:
  {{
    "carousel_title": "Catchy title for the 7-day carousel series about {selected_product}",
    "selected_product": "{selected_product}",
    "day_1": {{
      "focus": "Audience demand analysis objective",
      "content_idea": "Detailed slide breakdown for carousel",
      "hook": "Attention-grabbing opening line",
      "call_to_action": "What to ask viewers to do"
    }},
    "day_2": {{
      "focus": "Continue audience demand analysis",
      "content_idea": "Detailed slide breakdown for carousel", 
      "hook": "Attention-grabbing opening line",
      "call_to_action": "What to ask viewers to do"
    }},
    "day_3": {{
      "focus": "Start free value delivery",
      "content_idea": "Detailed slide breakdown for carousel",
      "hook": "Attention-grabbing opening line", 
      "call_to_action": "What to ask viewers to do"
    }},
    "day_4": {{
      "focus": "Continue free value delivery",
      "content_idea": "Detailed slide breakdown for carousel",
      "hook": "Attention-grabbing opening line",
      "call_to_action": "What to ask viewers to do"
    }},
    "day_5": {{
      "focus": "Peak free value delivery",
      "content_idea": "Detailed slide breakdown for carousel",
      "hook": "Attention-grabbing opening line",
      "call_to_action": "What to ask viewers to do"
    }},
    "day_6": {{
      "focus": "Begin conversion phase",
      "content_idea": "Detailed slide breakdown for carousel",
      "hook": "Attention-grabbing opening line",
      "call_to_action": "What to ask viewers to do"
    }},
    "day_7": {{
      "focus": "Final conversion push",
      "content_idea": "Detailed slide breakdown for carousel",
      "hook": "Attention-grabbing opening line",
      "call_to_action": "What to ask viewers to do"
    }}
  }}

  Return ONLY valid JSON with clean text. No special formatting or rich text.
  """
  return prompt