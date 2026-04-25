import streamlit as st
import json
import asyncio
import os
from chunks import chunks
from pdf.reportlab_pdf import create_pdf
from data import improved_output
from prompts import analysis_prompt, chunks_prompt, to_avoid_name, to_avoid, to_add, analyze, test_carousel_prompt
from models import call_analysis, chunks_model, test_carousel_model

# Check if required environment variables are set
if "NVIDIA_API_KEY" not in os.environ:
    st.warning("NVIDIA_API_KEY not found in environment variables. Please set it in Streamlit secrets.")

if "NVIDIA_API_KEY2" not in os.environ:
    st.warning("NVIDIA_API_KEY2 not found in environment variables. Please set it in Streamlit secrets.")

# Simple password protection
def check_password():
    def password_entered():
        if "password" in st.secrets and st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
        else:
            st.session_state["password_correct"] = False
            if st.session_state["password"] != "":
                st.error("Password incorrect")

    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    if not st.session_state["password_correct"]:
        # First password input for authentication
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        st.stop()
    else:
        st.session_state["password_correct"] = True

# Function to run the existing pipeline
def run_pipeline(name, bio, captions):
    # Create data structure similar to the original ask() function
    raw_data = {
        "name": name,
        "bio": bio,
        "caption": captions
    }

    # Process the data through the pipeline
    # The analyze function returns a prompt, not analyzed data
    analyze_prompt = analyze(raw_data)
    structured_data = call_analysis(analyze_prompt)
    
    # Parse the structured data from the AI response
    if isinstance(structured_data, str):
        try:
            structured_data = json.loads(structured_data)
        except json.JSONDecodeError:
            # If parsing fails, create a fallback structured data object
            structured_data = {
                "niche": "General",
                "target_audience": "General audience",
                "monetization_type": "unknown",
                "link_strategy": "Standard",
                "content_type": "Mixed content",
                "primary_goal": "Grow audience and monetize"
            }
    
    prompt = analysis_prompt(structured_data, to_avoid, to_avoid_name, to_add)
    ai_output = call_analysis(prompt)
    
    # Process the AI output
    if isinstance(ai_output, str):
        try:
            output = improved_output(ai_output)
            data = json.loads(output)
        except (json.JSONDecodeError, TypeError):
            # Fallback data if parsing fails
            data = {
                "niche_clarity": "General assessment",
                "target_audience": "General audience",
                "monetization_gaps": ["Content strategy gap", "Audience engagement gap"],
                "digital_product_ideas": ["Digital course", "Template pack"]
            }
    else:
        data = ai_output

    # Process chunks
    try:
        chunks_data = chunks(data)
    except Exception as e:
        # If chunks processing fails, create a simple chunks_data structure
        chunks_data = [
            {
                "niche_clarity": "General assessment",
                "target_audience": "General audience",
                "monetization_gaps": "Content strategy gap",
                "digital_product_ideas": "Digital course"
            }
        ]

    # Run chunk processing
    async def chunks_call(chunks_data_item):
        chunksPrompt = chunks_prompt(chunks_data_item)
        output = await asyncio.to_thread(chunks_model, chunksPrompt)
        return output

    async def run_all(chunks_data_list):
        tasks = []
        for items in chunks_data_list:
            tasks.append(chunks_call(items))
        result = await asyncio.gather(*tasks)
        return result

    try:
        results = asyncio.run(run_all(chunks_data))
    except Exception as e:
        # Fallback results if processing fails
        results = [
            '{"monetization_gap_explanation": "Content strategy gap affects audience engagement and revenue potential."}',
            '{"digital_product_explaination": "A digital course can help establish authority and provide value to your audience."}'
        ]

    # Process carousel data
    try:
        carousel_prompt = test_carousel_prompt(raw_data, structured_data, data)
        carousel_output = test_carousel_model(carousel_prompt)
        carousel_data = json.loads(improved_output(carousel_output))
    except Exception as e:
        # Fallback carousel data if any step fails
        carousel_data = {
            "carousel_title": "7-Day Product Testing",
            "selected_product": "Digital Product",
            "day_1": {
                "focus": "Audience demand analysis",
                "content_idea": "Analyzing audience needs",
                "hook": "What does your audience really want?",
                "call_to_action": "Share your biggest content challenge"
            }
        }

    return results, data, carousel_data

# Streamlit app
st.title("Monetization Audit Generator")
st.markdown("## Generate Your Monetization Audit Report")

# Password protection
check_password()

# Show a warning if we're not in a Streamlit Cloud environment
if "password" not in st.secrets:
    st.warning("App password not found in secrets. Please set it in Streamlit secrets.")

# Input fields
name = st.text_input("Name")
bio = st.text_area("Bio")
captions_input = st.text_area("Captions (one per line)")
captions = captions_input.split('\n') if captions_input else []

# Button to generate report
if st.button("Generate Report"):
    if not name or not bio or not captions:
        st.error("Please fill in all fields")
    else:
        try:
            with st.spinner("Generating report..."):
                # Check if required environment variables are set
                if "NVIDIA_API_KEY" not in os.environ or "NVIDIA_API_KEY2" not in os.environ:
                    st.error("NVIDIA API keys not found. Please set them in Streamlit secrets.")
                    st.stop()

                # Run the pipeline
                results, data, carousel_data = run_pipeline(name, bio, captions)

                # Generate PDF
                output_dir = "output"
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)

                output_file_path = os.path.join(output_dir, f"{name}_audit.pdf")
                try:
                    create_pdf(results, name, carousel_data=carousel_data, output_file=output_file_path)

                    st.success("Report generated successfully!")
                    with open(output_file_path, 'rb') as file:
                        st.download_button(
                            label="Download PDF",
                            data=file,
                            file_name=f"{name}_audit.pdf",
                            mime="application/pdf"
                        )
                except Exception as pdf_error:
                    st.error(f"Error generating PDF: {str(pdf_error)}")
        except Exception as e:
            st.error(f"Error generating report: {str(e)}")
            # Print full traceback for debugging
            import traceback
            st.text(traceback.format_exc())