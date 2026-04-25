import os
from pdf.reportlab_pdf import create_mock_pdf


if __name__ == "__main__":
    # Create the output directory if it doesn't exist
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    output_file = create_mock_pdf(output_file=os.path.join("output", "mock_preview_audit.pdf"))
    print(f"Preview PDF created: {output_file}")