import os
from dotenv import load_dotenv
import openai
import logging
import json
import argparse

# Setup
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Extract
def keywords_from_openai_response(response:dict) -> list:
    
    # Extracting keywords from an open ai response like the following:
    # {
    #   "choices": [
    #     {
    #       "finish_reason": "stop",
    #       "index": 0,
    #       "logprobs": null,
    #       "text": "\nanswers: Apache Arrow, Neo4j, Graph Projections, Cloud Object Storage, Cloud Data Warehouses, Neo4j Graph Data Science Python Client, Parallelize in Python"
    #     }
    #   ],
    #   "created": 1677274110,
    #   "id": "cmpl-6nZuAgu4xaX324HJTuf1A2StIvD00",
    #   "model": "text-davinci-003",
    #   "object": "text_completion",
    #   "usage": {
    #     "completion_tokens": 47,
    #     "prompt_tokens": 178,
    #     "total_tokens": 225
    #   }
    # }

    response_choices = response.get('choices', None)
    if response_choices == None:
        logging.error(f'keywords_from_openai_response: response missing choices key-value')
        return None
    
    if len(response_choices) == 0:
        logging.error(f'keywords_from_openai_response: No choices found in response: {response}')
        return None

    response_text = response_choices[0].get('text', None)
    if response_text is None:
        logging.error(f'keywords_from_openai_response: response missing choices.text key-value')
        return None
    
    # Extract the JSON string by removing the initial text
    answers = response_text.split(": ")[1]
    answers_list = answers.split(", ")
    if isinstance(answers_list, list) is False:
        logging.error(f'keywords_from_openai_response: {answers_list} was not an instance of a list')
        return None
    return answers_list


def openai_keywords_from_text(text: str) -> list[str]:
    # Promptsmithing to get a consistent response from openai
    prompt = f'''
    Given a prompt, extract software technology keywords and their related programming languages (like python, javascript, java, go, c++) from it and provide a list of answers.

    Example:
    prompt: Learn how to leverage Apache Arrow for blazing fast construction of Neo4j graph projections
    answers: Apache Arrow, Neo4j, Graph Projections
    
    prompt: {text}
    '''

    #  Q&A example
    # response = openai.Completion.create(
    #     model="text-davinci-003",
    #     prompt=prompt,
    #     temperature=0,
    #     max_tokens=100,
    #     top_p=1,
    #     frequency_penalty=0.0,
    #     presence_penalty=0.0,
    #     stop=["\n"]
    #     )
    
    # Keyword example
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.5,
        max_tokens=60,
        top_p=1.0,
        frequency_penalty=0.8,
        presence_penalty=0.0
        )

    logging.debug(f'openai_keywords_from_text: response: {response}')
    keywords = keywords_from_openai_response(response)
    if keywords is not None:
        logging.debug(f'openai_keywords_from_text: keywords: {keywords}')

    return keywords


def import_csv(
        filepath: str)-> list:
    import csv
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        return rows
    
def save_csv(filepath: str, data: list[dict]):
    import csv
    logging.info(f'save_csv: Saving {len(data)} records to {filepath}')
    with open(filepath, 'w') as csvfile:
        if data is None:
            raise Exception(f'save_csv.py: save_csv: No data to save to {filepath}')
        if len(data) == 0:
            raise Exception(f'save_csv.py: save_csv: Empty data list to save to {filepath}')
        if data[0] is None:
            raise Exception(f'save_csv.py: save_csv: No data found in data list: {data}')
        fieldnames = data[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            if isinstance(row, dict) is False:
                logging.error(f'save_csv: row item is not a dict: {row}')
                continue
            writer.writerow(row)

def records_from_csv(
        filepath: str,
        headers_to_use: list[str],
        keep: list[str]) -> list[dict]:
    # Extract keywords from a csv file and return a list of records.
    # There will be one record for each keyword found in the targeted text columns.

    if filepath is None:
        raise Exception(f'records_from_csv: filepath is None')
    if headers_to_use is None:
        raise Exception(f'records_from_csv: headers_to_use is None')

    # Import the source .csv file
    rows = import_csv(filepath)
    if rows is None or len(rows)==0:
        logging.error(f'records_from_csv: No rows found in {filepath}')
        return None

    logging.info(f'Processing {len(rows)} rows from {filepath}')

    # Create a list of records for export
    records = []
    for row in rows:
        combined_text = ""
        for header in headers_to_use:
            if header not in row:
                # Check to see if the desired header is actually in the imported data
                raise Exception(f'records_from_csv: target header {header} not found in row: {row}')
            combined_text += row[header] + ' '
        
        # Get list of keywords from open ai
        keywords = openai_keywords_from_text(combined_text)
        logging.debug(f'records_from_csv: keywords: {keywords}')

        if keywords is None:
            logging.warning(f'records_from_csv: No keywords found for row: {row}')
            return records
        for keyword in keywords:
            record = {}
            record["keyword"] = keyword
            for key in keep:
                record[key] = row[key]
            records.append(record)

    if records is None or len(records) == 0:
        logging.error(f'records_from_csv: No records found for {filepath}, headers_to_use: {headers_to_use}, keep: {keep}')
        return None
    
    logging.info(f'Created {len(records)} records from {filepath}')

    return records

def extract_keywords_from_csv_string_columns(
        filepath: str,
        headers: list[str],
        keep: list[str],
        output: str) -> None:
    records = records_from_csv(filepath, headers, keep)
    logging.debug(f'extract_keywords_from_csv_string_columns: records: {records}')
    save_csv(f'exports/{output}', records)

if __name__ == "__main__":
    # Logging setup
    logging.basicConfig(
        filename='logs.log', 
        encoding='utf-8', 
        level=logging.DEBUG,
        format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
        )

    # Argument setup
    argParser = argparse.ArgumentParser()
    argParser.add_argument("-i", "--input", help="Input path to .csv file to process")
    argParser.add_argument("-sh", "--source-headers", nargs='+', default=[], help="Space separated list of .csv headers to search for keywords")
    argParser.add_argument("-kh", "--keep-headers", nargs='+', default=[], help="Space separated list of .csv header values to pass into output")
    argParser.add_argument("-o", "--output", default="keywords.csv", help="Output file name")
    args = argParser.parse_args()

    # Extract arguments
    file = args.input
    headers = args.source_headers
    keep = args.keep_headers
    output = args.output

    # Run keyword extraction
    logging.info(f'extract_keywords_from_csv_string_columns: starting extraction for file: {file}, headers: {headers}, keep: {keep}, output: {output}')
    extract_keywords_from_csv_string_columns(file, headers, keep, output)
