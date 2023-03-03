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
def keywords_from(response:dict) -> list:
    
    response_choices = response.get('choices', None)
    if response_choices == None:
        logging.error(f'keywords_from: response missing choices key-value')
        return None
    
    if len(response_choices) == 0:
        logging.error(f'keywords_from: No choices found in response: {response}')
        return None

    response_text = response_choices[0].get('text', None)
    if response_text is None:
        logging.error(f'keywords_from: response missing choices.text key-value')
        return None

    # response_text will be something like: 
    # "\nanswers: Apache Arrow, Neo4j, Graph Projections, Cloud Object Storage, Cloud Data Warehouses, Neo4j Graph Data Science Python Client, Parallelize in Python"

    # Extract the JSON string by removing the initial text
    answers = response_text.split(": ")[1]
    answers_list = answers.split(", ")
    if isinstance(answers_list, list) is False:
        logging.error(f'keywords_from: {answers_list} was not an instance of a list')
        return None
    return answers_list

# TODO: Test with proper test file
def keywords_from_text_test(text: str) -> list[str]:
    file = open('tests/response_test.json')
    response = json.load(file)
    keywords = keywords_from(response)
    if keywords is not None:
        logging.info(f'keywords_from_text_test: keywords: {keywords}')
    return keywords

def keywords_from_text(text: str) -> list[str]:
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

    # Working test prompt
    # response = openai.Completion.create(
    #   model="text-davinci-003",
    #   prompt="""
    # Extract technology or software keywords from the following text and return a JSON list:

    #   Learn how to leverage Apache Arrow for blazing fast construction of Neo4j graph projections, ludicrously fast exporting of complex graph features, and more. If you're a Data Scientist looking to experiment with your millions of node embeddings or a Data Engineer looking to decrease deployment time, you should check out Neo4j's Apache Arrow support!
    
    #  We'll work through exercises loading data from cloud object storage and cloud data warehouses directly to Neo4j. Since this is about the full lifecycle, we'll also work through pulling the data back out into other cloud storage systems.
    
    #  Along the way, we'll cover some best practices related to:
    
    #  * using the Neo4j Graph Data Science Python client
    #  * how to parallelize in Python without headaches
    #   """
    #   ,
    #   temperature=0.5,
    #   max_tokens=60,
    #   top_p=1.0,
    #   frequency_penalty=0.8,
    #   presence_penalty=0.0
    # )

    # Sample response:
    # {
    #   "choices": [
    #     {
    #       "finish_reason": "stop",
    #       "index": 0,
    #       "logprobs": null,
    #       "text": "\n\nAnswer: `[\"Apache Arrow\", \"Neo4j\", \"Data Scientist\", \"Data Engineer\", \"Cloud Object Storage\", \"Cloud Data Warehouses\", \"Neo4j Graph Data Science Python client\"]`"
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

    logging.info(f'keywords_from_text: response: {response}')

    keywords = keywords_from(response)
    if keywords is not None:
        logging.info(f'keywords_from_text: keywords: {keywords}')

    return keywords


def import_csv(filepath: str)-> list:
    import csv
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        return rows
    
def save_csv(filepath: str, data: list[dict]):
    import csv
    with open(filepath, 'w') as csvfile:
        # TODO: Fix, will crash if the data is empty
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

# TODO: Create a generic function that takes a filepath and header rows to use in the prompt
# TODO: Create another function for mapping information of interest to pass along withe keywords returned
def nodes_records_from_csv(
        filepath: str,
        headers_to_use: list[str],
        keep: list[str]) -> list[dict]:
    
    rows = import_csv(filepath)

    # Sample csv record from 2022 Nodes
    # {'Session Id': '369057', 'Title': 'Blazing Fast Graphs 🔥: Hands-On With Apache Arrow and Neo4j', 'Description': "Learn how to leverage Apache Arrow for blazing fast construction of Neo4j graph projections, ludicrously fast exporting of complex graph features, and more. If you're a Data Scientist looking to experiment with your millions of node embeddings or a Data Engineer looking to decrease deployment time, you should check out Neo4j's Apache Arrow support!\n \n\n We'll work through exercises loading data from cloud object storage and cloud data warehouses directly to Neo4j. Since this is about the full lifecycle, we'll also work through pulling the data back out into other cloud storage systems.\n \n\n Along the way, we'll cover some best practices related to:\n \n\n * using the Neo4j Graph Data Science Python client\n * how to parallelize in Python without headaches", 'Owner': 'Dave Voutila', 'Owner Email': 'dave.voutila@neotechnology.com', 'Session format': 'Workshop >2 hours', 'Level': 'Advanced', 'Pre-requisites for attendees?': 'Python knowledge (can import modules, write a function, and use core primatives like Dictionaries), familiarity with a Jupyter notebook', 'Topic of your presentation': 'Performance, Graph Data Science', 'Neo4j Use-Case': 'General', 'Internet/AV setup': 'Checked', 'Graph your story': '', 'Your Timezone': 'US Eastern', 'Status': 'Accepted', 'Date Submitted': '25 Jul 2022 8:49 PM', 'Owner Notes': 'I would love for this to use AuraDS if the Apache Arrow support is available by then 😉', 'Speaker Id': '1072622f-3c07-4256-8a51-0ecbb22044f0', 'FirstName': 'Dave', 'LastName': 'Voutila', 'Email': 'dave.voutila@neotechnology.com', 'TagLine': 'Sales Engineering Manager at Neo4j', 'Bio': 'Dave Voutila is a Sales Engineering Manager at Neo4j. A flatlander now living in Vermont (USA), Dave\'s been a part of Neo4j\'s field team since 2019. He\'s proudly never seen "Jerry Maguire" and intends to keep it that way.', 'timezone': '', 'T-Shirt Size': '', 'Address / Street': '', 'Company': '', 'ZIP': '', 'City': '', 'Country': '', 'Phone Number': '', 'Ninja': 'Not checked', 'Twitter': 'https://twitter.com/voutilad', 'LinkedIn': 'https://www.linkedin.com/in/davevoutila/', 'Blog': 'https://sisu.io', 'Company Website': 'https://neo4j.com', 'Profile Picture': 'https://sessionize.com/image/44e6-400o400o2-ENcDGKksb9xhajqF2PzPcn.jpg'}

    records = []

    for row in rows:
        combined_text = ""
        for header in headers_to_use:
            if header not in row:
                raise Exception(f'nodes_records_from_csv: header not found in row: {header}')
            combined_text += row[header] + ' '
        keywords = keywords_from_text(combined_text)
        # keywords = ["test"]
        logging.info(f'nodes_records_from_csv: keywords: {keywords}')
        if keywords is None:
            return records
        for keyword in keywords:
            record = {}
            # record['session_id'] = session_id
            record["keyword"] = keyword
            # record["speaker_email"] = email
            for key in keep:
                record[key] = row[key]
            records.append(record)
    return records

def export_csv_for_nodes(
        filepath: str,
        headers: list[str],
        keep: list[str],
        output: str) -> None:
    records = nodes_records_from_csv(filepath, headers, keep)
    logging.info(f'export_csv_for_nodes: records: {records}')
    save_csv(f'exports/{output}', records)

if __name__ == "__main__":
    # Logging setup
    logging.basicConfig(filename='logs.log', encoding='utf-8', level=logging.DEBUG)

    # Argument setup
    argParser = argparse.ArgumentParser()
    argParser.add_argument("-f", "--file", help="Path to .csv file to process")
    argParser.add_argument("-hl", "--headers-list", nargs='+', default=[], help="List of .csv headers to search for keywords")
    argParser.add_argument("-kl", "--keep-list", nargs='+', default=[], help="List of .csv header values to pass into output")
    argParser.add_argument("-o", "--output", default="keywords.csv", help="Output file name")
    args = argParser.parse_args()

    # Extract arguments
    file = args.file
    headers = args.headers_list
    keep = args.keep_list
    output = args.output
    # print(f'file: {file}, headers: {headers}, keep: {keep}')

    # Run keyword extraction
    export_csv_for_nodes(file, headers, keep, output)
