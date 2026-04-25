import streamlit as st
import json
import asyncio
import os
from chunks import chunks
from pdf.reportlab_pdf import create_pdf
from data import improved_output
from prompts import analysis_prompt, chunks_prompt, to_avoid_name, to_avoid, to_add, analyze, test_carousel_prompt
from models import call_analysis, chunks_model, test_carousel_model

# Simple password protection
def check_password():
    def password_entered():
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
        else:
            st.session_state["password_correct"] = False
            st.error("Password incorrect")

    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    if not st.session_state["password_correct"]:
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
    structured_data = analyze(raw_data)
    prompt = analysis_prompt(structured_data, to_avoid, to_avoid_name, to_add)
    ai_output = call_analysis(prompt)
    output = improved_output(ai_output)
    data = json.loads(output) if isinstance(output, str) else output
    
    # Process chunks
    chunks_data = chunks(data)
    
    # Run chunk processing
    async def chunks_call(chunks_data):
        chunksPrompt = chunks_prompt(chunks_data)
        output = await asyncio.to_thread(chunks_model, chunksPrompt)
        return output

    async def run_all(chunks_data):
        tasks = []
        for items in chunks_data:
            tasks.append(chunks_call(items))
        result = await asyncio.gather(*tasks)
        return result
    
    results = asyncio.run(run_all(chunks_data))
    
    # Process carousel data
    carousel_prompt = test_carousel_prompt(raw_data, structured_data, data)
    carousel_output = test_carousel_model(carousel_prompt)
    carousel_data = json.loads(improved_output(carousel_output))
    
    return results, data, carousel_data

# Streamlit app
st.title("Monetization Audit Generator")
st.markdown("## Generate Your Monetization Audit Report")

# Password protection
check_password()

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
                # Run the pipeline
                results, data, carousel_data = run_pipeline(name, bio, captions)
                
                # Generate PDF
                output_dir = "output"
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                
                output_file_path = os.path.join(output_dir, f"{name}_audit.pdf")
                create_pdf(results, name, carousel_data=carousel_data, output_file=output_file_path)
                
                st.success("Report generated successfully!")
                st.download_button(
                    label="Download PDF",
                    data=open(output_file_path, 'rb').read(),
                    file_name=f"{name}_audit.pdf",
                    mime="application/pdf"
                )
        except Exception as e:
            st.error(f"Error generating report: {str(e)}")