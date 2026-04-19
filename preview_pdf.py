from pdf.reportlab_pdf import create_mock_pdf


if __name__ == "__main__":
    output_file = create_mock_pdf()
    print(f"Preview PDF created: {output_file}")
