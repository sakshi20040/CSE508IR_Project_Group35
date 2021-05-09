# QueRe

QueRe is an effective end-to-end Question-Answer retrieval system capable of retrieving a ranked list of relevant Question-Answer pairs against a user query.

## Requirements

Download and install Elasticsearch using the [guide documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/install-elasticsearch.html)

Download [USE](https://tfhub.dev/google/universal-sentence-encoder/4)(universal-sentence-encoder) version 4.

Download and install the ngrok using the [documentation](https://ngrok.com/download).


## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the following commands.

```bash
pip install pywebio
pip install contractions
pip install scipy
pip install bs4
pip install joblib
pip install tensorflow
```

## Usage
Run Elasticsearch using the [guide documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/starting-elasticsearch.html)

Fire up ngrok.

```bash
ngrok http 3000
```

Run the searching.py
```bash
python searching.py
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

