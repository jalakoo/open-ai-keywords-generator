# Keyword Generator
This app generates a list of technology keywords associated with values from specified parts of an imported .csv file. The original intent of this app is to produce a table of keywords associated with data from a source .csv file to then import through Neo4j's Data-Importer tool. This app requires a valid OpenAI API key to work.

# Config
Create a .env file with the entry: 
```
OPENAI_API_KEY="<your_open_api_key>"
```

# Using
Running example: `pipenv run python3 app.py -f imports/2020_nodes.csv -hl Title Bio -kl Speakers -o 2020.csv`

# Options
| Flag  | Description | Sample Value |
| ---- | ----- | -----|
| -f | Filepath of .csv file to process | "imports/2020_nodes.csv" |
| -o | Output filepath of new .csv | "2020.csv" (All exports will automatically placed into the exports/ folder) |
| -hl | List of header row values to use for generating keywords from | Title Description Bio |
| -kl | List of header row values to pass onto the output .csv file | SpeakerId |

# Output
A row will be created for each keyword and kept (-kl arg) header values, for example:
```
SpeakerId, Keyword
abc123, neo4j
abc123, cypher
```

# PIPENV NOTES
Using pipenv to manage virtaul env

To start: `pipenv shell`
To add new lib: `pipenv install <package_name>`
To run: `pipenv run python3 app.py`