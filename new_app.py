import streamlit as st
import os
import pandas as pd
import json
import logging
import openai
import tempfile
from io import BytesIO
from unstract.llmwhisperer import LLMWhispererClientV2
from dotenv import load_dotenv
from config import *
from datetime import datetime





"""Initialize Azure OpenAI settings."""
openai.api_type = "azure"
openai.api_base = "https://dmr-poc-exela.openai.azure.com/"
openai.api_version = "2023-03-15-preview"
openai.api_key = 'c0bbcf067f594c01b588c77d97a2bb33'


def extract_substring_after_first(string, search_substring):
    index = string.find(search_substring)
    if index != -1:
        substring = string[index + len(search_substring):]
        return substring.strip()
    else:
        return string


def convert_to_json(analyzed_text):
    """Convert the analyzed text to JSON format"""
    json_data = {}

    # Split the text into lines and process each line
    for line in analyzed_text.strip().split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            # Clean up the key and value
            key = key.strip()
            value = value.strip()
            json_data[key] = value

    return json.dumps(json_data, indent=4)


def get_prompt35_output(prompt):
    """Get response from Azure OpenAI GPT-3.5."""
    input_messages = [
        {"role": "system",
         "content": "You are a helpful and reliable assistant."},
        {"role": "user",
         "content": prompt}
    ]

    try:
        response = openai.ChatCompletion.create(
            engine="gpt-35-turbo-16k",
            messages=input_messages,
            temperature=0.2,
            max_tokens=2000
        )
        text = response.choices[0].message.content
        return extract_substring_after_first(text, "\n\n")
    except Exception as e:
        logger.error(f"Error in OpenAI API call: {str(e)}")
        raise e


def run_openai_key(read_output):
    """Process extracted text with Azure OpenAI to get key-value pairs."""
    key_pairs_prompt = f"Below is a sample of fields description \n {DEFAULT_FIELD_DESCRIPTIONS}.\n\n\n" \
                       f"Extract key-value pairs {DEFAULT_KEYPAIRS} " \
                       f"from the below text and separate them by line \n\n" \
                       f"Document text: {read_output} \n\n" \
                       f"Entities:"

    try:
        key_pairs_prompt = key_pairs_prompt.encode("utf-8", errors="replace").decode("utf-8")
        extracted_values = get_prompt35_output(key_pairs_prompt)
        print(extracted_values)
        return extracted_values
    except Exception as e:
        logger.error(f"Error in OpenAI key extraction: {str(e)}")
        raise e


def process_file(client, uploaded_file, mode, output_mode):
    """Process the uploaded file using LLM Whisperer."""
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name

        with st.spinner('Processing file...'):
            result = client.whisper(
                file_path=tmp_file_path,
                mode=mode,
                output_mode=output_mode if output_mode != "None" else None,
                wait_for_completion=True,
                wait_timeout=200,
            )

        os.unlink(tmp_file_path)
        return result.get("extraction", {}).get("result_text", "")

    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
        raise e


def parse_key_value_pairs(analyzed_text):
    key_value_pairs = {}

    # Try splitting the analyzed text into key-value pairs manually if it's not a JSON
    for line in analyzed_text.split("\n"):
        if ":" in line:  # Basic check for key-value pairs, separated by ":"
            parts = line.split(":", 1)
            key = parts[0].strip()
            value = parts[1].strip() if len(parts) > 1 else "Not found"
            key_value_pairs[key] = value

    return key_value_pairs


# Convert the DataFrame to an Excel file
def convert_df_to_excel(dataframe):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        dataframe.to_excel(writer, index=False, sheet_name="Key-Value Pairs")
    processed_data = output.getvalue()
    return processed_data



"""Initialize the LLM Whisperer client with environment variables."""
whisperer_base_url = "https://llmwhisperer-api.us-central.unstract.com/api/v2"
whisperer_api_key = "pU9WJLt-JLYcqpHXXY-uzlaudk1MyIiJuVus6W5plKE"

client = LLMWhispererClientV2(base_url=whisperer_base_url, api_key=whisperer_api_key)


def main():


    client = init_llm_client()
    init_azure_openai()



    # Mapping for modes and output modes
    processing_modes_display = ["Form", "Native Text", "Low Cost", "High Quality"]
    processing_modes_internal = ["form", "native_text", "low_cot", "high_quality"]

    output_modes_display = ["Text", "Layout Preserving"]
    output_modes_internal = ["text", "layout_preserving"]

    # Sidebar for recent history
    with st.sidebar:
        st.header("Recent History")
        if recent_extractions:
            for i, record in enumerate(recent_extractions, start=1):
                with st.expander(f"{i}. {record['filename']}"):
                    st.write(f"**Processed At**: {record['timestamp']}")
                    st.markdown("**Extracted Text**")
                    st.text_area(f"Extracted Text - {record['filename']}", record["extracted_text"], height=100, key=f"text_{i}")
                    st.markdown("**Key-Value Pairs**")
                    st.text_area(f"Key-Value Pairs - {record['filename']}", record["analyzed_text"], height=100, key=f"kv_{i}")
        else:
            st.info("No recent history available.")

    # Main interface for file upload and processing
    col1, col2 = st.columns(2)

    # Mode selection
    with col1:
        selected_mode_display = st.selectbox(
            "Select Processing Mode",
            options=processing_modes_display,
            index=0,
            help="High Quality: Better accuracy but slower"
        )
        mode = processing_modes_internal[processing_modes_display.index(selected_mode_display)]

    # Output mode selection
    with col2:
        selected_output_mode_display = st.selectbox(
            "Select Output Mode",
            options=output_modes_display,
            index=0,
            help="Text: Plain text output, Layout Preserving: Text with layout information"
        )
        output_mode = output_modes_internal[output_modes_display.index(selected_output_mode_display)]

    uploaded_file = st.file_uploader("Choose a file", type=['pdf', 'tif', 'tiff', 'png', 'jpg', 'jpeg'])

    if uploaded_file:
        st.write("File uploaded:", uploaded_file.name)

        if st.button("Process File"):
            try:
                extracted_text = process_file(client, uploaded_file, mode, output_mode)

                if extracted_text:
                    st.success("Text extracted successfully!")

                    with st.expander("View Extracted Text"):
                        st.text_area("Original Extracted Text", extracted_text, height=200)

                    with st.spinner('Analyzing text with Azure OpenAI...'):
                        analyzed_text = run_openai_key(extracted_text)

                    try:
                        # Parse the analyzed_text manually if it's not JSON
                        if isinstance(analyzed_text, str):
                            key_value_pairs = parse_key_value_pairs(analyzed_text)
                        else:
                            key_value_pairs = analyzed_text  # In case it's already a dictionary
                    except Exception as e:
                        st.error(f"Error processing key-value pairs: {str(e)}")
                        key_value_pairs = {}

                    # Check if key_value_pairs is a dictionary and render it as a table
                    if isinstance(key_value_pairs, dict):
                        key_value_table = [(key, value) for key, value in key_value_pairs.items()]
                        df = pd.DataFrame(key_value_table, columns=["Field Name", "Extracted Value"])

                        # Display key-value pairs in a tabular format
                        with st.expander("View Extracted Key-Value Pairs", expanded=True):
                            st.table(df)

                        # Button to download the table as an Excel file
                        excel_data = convert_df_to_excel(df)
                        st.download_button(
                            label="Download as Excel",
                            data=excel_data,
                            file_name=f"{uploaded_file.name}.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
                    else:
                        st.error("Extracted data is not in a valid format.")

                    # Save to database
                    save_extraction(
                        filename=uploaded_file.name,
                        extracted_text=extracted_text,
                        analyzed_text=analyzed_text,
                        processing_mode=mode,
                        output_mode=output_mode
                    )

                    col1, col2 = st.columns(2)
                    with col1:
                        st.download_button(
                            label="Download Raw Text",
                            data=extracted_text,
                            file_name=f"{uploaded_file.name}_raw_text.txt",
                            mime="text/plain"
                        )
                    with col2:
                        json_data = convert_to_json(analyzed_text)
                        st.download_button(
                            label="Download Key-Value Pairs",
                            data=json_data,
                            file_name=f"{uploaded_file.name}_key_value_pairs.json",
                            mime="application/json"
                        )
                else:
                    st.warning("No text was extracted from the file.")

            except Exception as e:
                st.error(f"Error processing file: {str(e)}")


if __name__ == "__main__":
    main()
