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
| Flag  | Verbose Flag |Description | Sample Value |
| ---- | ----- | -----| ---- |
| -i | --input | Input filepath of .csv file to process | "imports/2020_nodes.csv" |
| -o | --output | Output filepath of new .csv | "2020.csv" (All exports will automatically placed into the exports/ folder) |
| -sh | --source_headers | Space separated list of header row values to use for generating keywords from | Title Description "Header with spaces" |
| -kh | --keep-headers | Space separated list of header and row values to pass onto the output .csv file | SpeakerId "Session Title" |

# Output
A row will be created for each keyword and kept (-kl arg) header values, for example:
```
SpeakerId, Session Title, Keyword
abc123, Session Alpha, neo4j
abc123, Session Alpha, cypher
```

# Testing
`pipenv run pytest`

# PIPENV NOTES
Using pipenv to manage virtaul env

To start: `pipenv shell`
To add new lib: `pipenv install <package_name>`
Example run commands: 

`pipenv run python3 app.py -i imports/2019_nodes.csv -o 2019.csv -sh Industries "Your Professional Title" "Social Links" Title Description Technologies Bio  -kh Event Name Email`
`pipenv run python3 app.py -i imports/2020_nodes.csv -o 2020.csv -sh Title Bio -kh Event Speakers "Title / Company"`
`pipenv run python3 app.py -i imports/2022_nodes.csv -o 2022.csv -sh Title Description "Topic of your presentation" "Pre-requisites for attendees?" "LinkedIn" "Blog" "Owner Notes" Bio -kh Event Owner "Owner Email"`
`pipenv run python3 app.py -i imports/meetups.csv -o meetups.csv -sh eventUrl name topic -kh source meetup_event_id name state city`
