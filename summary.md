# Summary of Changes

## Changes Made

1. **Output Directory Creation**:
   - Created an `/output/` directory to store all generated PDFs
   - All existing PDF files were moved to this directory

2. **Modified Files**:
   - `main.py`: Updated to generate PDFs in the output directory
   - `preview_pdf.py`: Updated to generate preview PDFs in the output directory
   - `pdf/reportlab_pdf.py`: No changes needed, but it now receives the output path from the calling functions

3. **New Files**:
   - `output/README.md`: Documentation for the output directory
   - `TESTING.md`: Instructions for testing the PDF generation

4. **Updated Documentation**:
   - `README.md`: Updated to reflect the new version (v1.1) and mention the output directory

## Directory Structure

The project now organizes all PDFs in the `/output/` directory:
```
/output/
  - Mariia_audit.pdf
  - mock_preview_audit.pdf
  - Sarah Li_audit.pdf
  - Skye_audit.pdf
  - Zosia_audit.pdf
  - {name}_audit.pdf (new generated files)
```

## Benefits

1. **Organized Output**: All PDFs are now in one dedicated directory
2. **Easier Management**: Simple to find and manage all generated reports
3. **Cleaner Root Directory**: The main project directory is less cluttered
4. **Backward Compatibility**: Existing functionality is preserved

## Usage

1. Run `python preview_pdf.py` to generate a preview PDF in the output directory
2. Run `python main.py` to generate a personalized PDF in the output directory (requires user input)

All generated PDFs will be saved in the `/output/` directory.