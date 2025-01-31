# Document Field Extraction Tool

A Streamlit web application for extracting and analyzing text fields from documents using LLM Whisperer and Azure OpenAI.

## Features

- Document text extraction with multiple processing modes
- Key-value pair extraction using Azure OpenAI
- Export options: Excel, JSON, raw text
- Processing history tracking
- Support for PDF, TIFF, PNG, JPG formats

## Setup

### Prerequisites
```bash
pip install streamlit openai python-dotenv pandas xlsxwriter unstract-llmwhisperer
```

### API Configuration
1. Azure OpenAI credentials:
```python
openai.api_type = "azure"
openai.api_base = "your-azure-endpoint"
openai.api_version = "2023-03-15-preview"
openai.api_key = "your-api-key"
```

2. LLM Whisperer credentials:
```python
whisperer_base_url = "https://llmwhisperer-api.us-central.unstract.com/api/v2"
whisperer_api_key = "your-api-key"
```

## Usage

1. Start the application:
```bash
streamlit run app.py
```

2. Select processing options:
   - Processing Mode: Form, Native Text, Low Cost, High Quality
   - Output Mode: Text, Layout Preserving

3. Upload document and click "Process File"

4. View and download results:
   - Extracted raw text
   - Key-value pairs in table format
   - Excel/JSON exports

## Processing Modes

- Form: Optimized for structured documents
- Native Text: Basic text extraction
- Low Cost: Faster, economical processing
- High Quality: Better accuracy, slower processing

## Output Formats

- Excel (.xlsx): Tabulated key-value pairs
- JSON: Structured data format
- Raw Text: Extracted document text
- Layout Preserving: Maintains document formatting

## Error Handling

The application includes:
- File processing validation
- API error catching
- Data format verification
- User feedback messages

## Functions

- `process_file()`: Document processing using LLM Whisperer
- `run_openai_key()`: Key-value extraction using Azure OpenAI
- `parse_key_value_pairs()`: Data structure conversion
- `convert_df_to_excel()`: Excel export functionality

## License

[Specify your license]

## Support

[Add contact information]
