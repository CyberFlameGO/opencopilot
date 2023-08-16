# OpenCopilot 🕊️

[![Unit tests](https://github.com/opencopilotdev/opencopilot/actions/workflows/unit_test.yml/badge.svg)](https://github.com/opencopilotdev/opencopilot/actions/workflows/unit_test.yml)
[![E2E Test Linux Native](https://github.com/opencopilotdev/opencopilot/actions/workflows/e2e_test_linux_native_openai.yml/badge.svg)](https://github.com/opencopilotdev/opencopilot/actions/workflows/e2e_test_linux_native_openai.yml)
[![E2E Test Linux CLI](https://github.com/opencopilotdev/opencopilot/actions/workflows/e2e_test_cli.yml/badge.svg)](https://github.com/opencopilotdev/opencopilot/actions/workflows/e2e_test_cli.yml)
[![Twitter](https://img.shields.io/twitter/url/https/twitter.com/opencopilot.svg?style=social&label=Follow%20%40OpenCopilot)](https://twitter.com/OpenCopilot)
![Discord](https://img.shields.io/discord/1133675019478782072?logo=discord&label=OpenCopilot)


## Overview

Copilots are becoming the new dominant way users are interacting with LLM-based applications, akin to how websites in the 90's simplified the Internet for consumers. Yet, building a Copilot today is extremely complex as it is time-consuming, expensive and feels like a massive undertaking. Moreover, other solutions such as Microsoft Copilot stack are closed. OpenCopilot solves this problem so developers can now build their own custom Copilot in a single day that actually works, without previous experience. Built by devs, for devs.

**Example Copilots built with OpenCopilot**

- [Ready Player Me Copilot](https://rpm.opencopilot.dev/) which helps developers integrate RPM avatar SDK into their games
- [Unity Copilot](https://unity.opencopilot.dev/) which helps Unity developers debug, write code and speed up their development flow.

## Quickstart

Install the OpenCopilot framework:

```bash
pip install opencopilot-ai
```

Create your copilot file (for example app.py):

```python
from opencopilot import OpenCopilot

copilot = OpenCopilot()
copilot()
```

Run the script:

```bash
python app.py
```

Copilot is running and can be interacted through OpenAPI docs in your browser: [http://0.0.0.0:3000/docs](https://www.notion.so/f32591ea322d40db83ca5844c97f22bf?pvs=21)

## Customizing your Copilot

There are three main ways you can customize your copilot: *Static Knowledge base, Dynamic Knowledge base* and *Prompts* that change the copilot's behaviour.

### **Static knowledge base**

This is the set of documents that your copilot relies on when responding to you - you can think of it as the things you've taught it. The copilot has access to everything here when trying to answer your questions. To add things into the knowledge base, just drop files into a local folder.

The following file formats are supported:

- `pdf` files
- `csv`, `tsv` and `xls`/`xlsx` (Excel) files
- `txt` files
- `json` files

Thus, to add new knowledge and your own data to the Copilot simply let the copilot know which files to load:

```python
# Loads the entire folder and subfolders
copilot.add_local_files("mycopilot/data")
# Loads just one file
copilot.add_local_file("mycopilot/extra.json")
```

It is also possible to support any files and any connections by letting the copilot call your own data loading function:

```python
@copilot.data_loader
def custom_dataloader() -> List[Document]:
    # this is pseudo code showing that you can do anything
    document1 = my_sql_db.query()
    document2 = my_s3_bucket.query()
    document3 = requests.get("mysecret.website/super_secret.txt")
    return [document1, document2, document3]
```

You need to restart the Copilot in order to ingest new data.

### Dynamic knowledge base

It is possible to also skip the vector store completely or return additional documents for LLM to answer queries. The following function is called every time user chats with the Copilot and the documents can be user specific.

```python
@copilot.search
def custom_search(query: str, user_id: str) -> List[Document]:
    # For example you can do a SQL query to get relevant information based 
    # on the user query and user_id. 
    return my_sql_db.search(query, user_id)
```

### Prompt engineering

You can instruct your copilot about its goals, behaviour, style, etc. There aren't many hard rules to this; you can start from one of our provided [copilots](https://github.com/nftport/opencopilot/tree/master/copilots) and iterate to improve the copilot's behaviour. Prompt engineering is a deep topic; for a more in-depth overview, see [OpenAI's list of prompting guides](https://github.com/openai/openai-cookbook#prompting-guides). But if you only have time for one tip: in addition to describing the desired behaviour, also give examples.

The prompt is not a static piece of text. It is a template that will be filled at runtime, after the user has messaged the copilot but before sending the request to the LLM. For this reason, you should always place three template variables into the prompt template file (ideally at the end), and they will be substituted as follows:

- `{context}`: the most relevant documents retrieved from your [knowledge base](https://github.com/nftport/opencopilot#knowledge-base).
- `{history}`: the conversation history between the user and the copilot.
- `{question}`: the most recent input from the user -- the message they just sent.

Create a file `my_prompt_template.txt`

```
Your are a Basketball Copilot. You are an expert on basketball.

=========
{context}
=========

{history}
User: {question}
Copilot answer in Markdown:
```

Let the Copilot know about your prompt template:

```python
copilot.add_prompt_template("my_prompt_template.txt")
```

### Evaluation

You can evaluate the performance of your copilot, by adding questions and expected answers to a json file, for example: `eval.json`

```python
{
  "examples": [
    {
      "query": "Who is the president of US?",
      "answer": "Joe Biden"
    }
  ]
}
```

Run the validation:

```bash
opencopilot validate eval.json
```

This is especially helpful in trying to figure out if some data changes or prompt changes actually made the copilot better.

### Testing

The Copilot stack comes with an example frontend that you can run by following examples in this repository: https://github.com/opencopilotdev/opencopilot-frontend

You can use Debug mode in the front-end which helps you test and iterate your Copilot.