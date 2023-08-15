# OpenCopilot 🕊️

[![Unit tests](https://github.com/nftport/opencopilot/actions/workflows/unit_test.yml/badge.svg)](https://github.com/nftport/opencopilot/actions/workflows/unit_test.yml)
[![E2E Test Linux Native OpenAI](https://github.com/nftport/opencopilot/actions/workflows/e2e_test_linux_native_openai.yml/badge.svg)](https://github.com/nftport/opencopilot/actions/workflows/e2e_test_linux_native_openai.yml)
[![E2E Test Linux CLI](https://github.com/nftport/opencopilot/actions/workflows/e2e_test_cli.yml/badge.svg)](https://github.com/nftport/opencopilot/actions/workflows/e2e_test_cli.yml)
[![E2E Test Linux CLI JWT](https://github.com/nftport/opencopilot/actions/workflows/e2e_test_cli_jwt.yml/badge.svg)](https://github.com/nftport/opencopilot/actions/workflows/e2e_test_cli_jwt.yml)
[![Twitter](https://img.shields.io/twitter/url/https/twitter.com/opencopilot.svg?style=social&label=Follow%20%40OpenCopilot)](https://twitter.com/OpenCopilot)
![Discord](https://img.shields.io/discord/1133675019478782072?logo=discord&label=OpenCopilot)


# Overview

Copilots are becoming the new dominant way users are interacting with LLM-based applications, akin to how websites in the 90's simplified the Internet for consumers. Yet, building a Copilot today is extremely complex as it is time-consuming, expensive and feels like a massive undertaking. Moreover, other solutions such as Microsoft Copilot stack are closed. OpenCopilot solves this problem so developers can now build their own custom Copilot in a single day that actually works, without previous experience. Built by devs, for devs. 

**Example Copilots built with OpenCopilot**

* [Ready Player Me Copilot](https://rpm.opencopilot.dev/) which helps developers integrate RPM avatar SDK into their games
* [Unity Copilot](https://unity.opencopilot.dev/) which helps Unity developers debug, write code and speed up their development flow.

# Quick Start

1. Download the repo

```bash
git clone git@github.com:opencopilotdev/opencopilot.git && cd opencopilot
```

2. Make sure you have the following dependancies:

```md
Python 3.8+
Docker
Docker Compose
Conda (optional for development)
pnpm (optional for front-end development)
```

3. Install Python CLI:

```bash
pip install -e .
```
 
4. Create a new Copilot:

```bash
opencopilot create
```

5. Start the Copilot:

```bash
opencopilot start
```

6. Copilot is running 🎉

To chat from CLI, run `opencopilot chat <message>`.

To chat from the front-end, visit this URL in your browser: [http://0.0.0.0:3001](http://0.0.0.0:3001)

Alright, you now have created a copilot, but you haven't really made it yours. The next section will show you how to customize your copilot.

# Customizing Your Copilot

There are three main ways you can customize your copilot: _Knowledge base_ and _Prompts_ that change the copilot's behaviour, and _Front-end configuration_ that changes how it is presented. To see these in action, you can check out several examples in the `copilots/` directory -- to use one of the provided examples, just copy over the relevant files.

### Knowledge base

The [**knowledge base**] is the set of documents that your copilot relies on when responding to you - you can think of it as the things you've taught it. The copilot has access to everything here when trying to answer your questions. To add things into the knowledge base, just drop files into `copilots/<my-copilot>/data/` directory.

The following file formats are supported:

* `pdf` files
* `csv`, `tsv` and `xls`/`xlsx` (Excel) files
* `txt` files
* `json` files

Thus, to add new knowledge and your own data to the Copilot simply add your own files to `copilots/<my-copilot>/data` folder and run:

```bash
opencopilot restart
```

This will chunk the files, embed them and add them to the vector store so your Copilot can access it. **You need to restart the Copilot in order to ingest new data.**

### Prompt Engineering

In the `copilots/<my-copilot>/prompts/prompt_template.txt` you instruct your copilot about its goals, behaviour, style, etc. There aren't many hard rules to this; you can start from one of our provided [copilots](https://github.com/nftport/opencopilot/tree/master/copilots) and iterate to improve the copilot's behaviour. Prompt engineering is a deep topic; for a more in-depth overview, see [OpenAI's list of prompting guides](https://github.com/openai/openai-cookbook#prompting-guides). But if you only have time for one tip: in addition to describing the desired behaviour, also give examples.

The prompt is not a static piece of text. It is a template that will be filled at runtime, after the user has messaged the copilot but before sending the request to the LLM. For this reason, you should always place three template variables into the prompt template file (ideally at the end), and they will be substituted as follows:

* `{context}`: the most relevant documents retrieved from your [knowledge base](#knowledge-base).
* `{history}`: the conversation history between the user and the copilot.
* `{question}`: the most recent input from the user -- the message they just sent.

**Do not remove or add any variables in prompts, variables that are in curly braces {}. (For example: {context})**

Hot-loading is supported meaning you can change the prompt file any time and during next request, Copilot will use the updated prompt.

### Testing

You can use Debug mode in the front-end which helps you test and iterate your Copilot. 

<img width="1339" alt="Debug mode" src="https://i.imgur.com/MhZaadl.png">

### Evaluating

You can evaluate the performance of your copilot, by adding questions and expected answers to `copilots/<my-copilot>/eval_data/endtoend_human.json`,
and running:
```bash
opencopilot evaluate
```
To see an example of this, check the file in `copilots/rpm/eval_data/endtoend_human.json`.

This is especially helpful in trying to figure out if some data changes or prompt changes actually made the copilot better.

# Integration

### REST API

You can use the REST API to integrate Copilot to your products. See this [gist script](https://gist.github.com/taivop/8c702809f60021c8280101301cc0f402) on how to call the API, or the [full API docs](http://0.0.0.0:3000/docs) after your Copilot is running. Currently, the REST API is unauthenticated (but a measure of privacy is provided by the fact that you can only access a chat's history if you know its uuid).

### Analytics & Monitoring

If you wish to monitor your Copilot usage and have per user analytics, then you can do that with [Helicone](https://www.helicone.ai/). Add your HELICONE_API_KEY to backend/.env and run opencopilot restart.

# Stack

The stack is simple to use, iterate and develop further on for production use:

1. 🧠 LLM: OpenAI GPT-4 by default; any LLM can be used
1. 🤖 OpenCopilot back-end
    1. Python & [FastAPI](https://fastapi.tiangolo.com/) server
    1. 🔗 [Langchain](https://github.com/hwchase17/langchain) for prompting and chaining
    1. 📃 Weaviate for memory and retrieval 
    1. 📚 Simple to use data ingestion
1. 🖼️ Front-end: Next.js and [Vercel AI SDK](https://sdk.vercel.ai/docs)
1. 📊 Analytics: [Helicone](https://www.helicone.ai/) (optional)

At the core of the OpenCopilot stack is the OpenCopilot Server. The server sits on top of the LLM but under your application, and implements the logic of the copilot: ingesting data, retrieving context at runtime, prompting, and parsing the results.

You can use any LLM and embedding model with the OpenCopilot Server, and any front-end. We provide default templates for both for a quicker start.

<img src="https://i.imgur.com/qJuQUj5.png" alt="Stack diagram of OpenCopilot" style="max-width: 50%;" />

# Development guide

OpenCopilot is built modularly so you can customize it further based on your own needs easily. 

## 1. Backend

Create `backend/.env` if it has not been created through `python cli.py create`: 

```shell
cd backend
cp template.env .env
```

Spin up Weaviate for vector storage:

```shell
docker-compose -f docker-compose-weaviate.yml up -d
```

Setup conda environment
```shell
conda env create -f environment.yml
conda activate backend-service
```

Ingest data - ***You will need to repeat this step each time you add new data in the data folder***

***Optional***: To improve document loading experience, use 
[libmagic1](https://github.com/ahupp/python-magic#installation) and 
[tesseract](https://github.com/madmaze/pytesseract#installation) libraries

```shell
python ingest_data.py
```

Run backend REST AP:

```shell
python wsgi.py
```

After some time you should see
```
..........
INFO:     Application startup complete.
```

Visit [0.0.0.0:3000/docs](http://0.0.0.0:3000/docs) to verify.

## 2. Frontend

Create `frontend/.env` if it has not been created through `python cli.py create`: 

```shell
cd frontend
cp .env.example .env
```

Install dependencies
```
pnpm install
```

Run frontend app:
```
pnpm run dev
```

Visit [localhost:3001](localhost:3001) to verify.


You are now ready to change any part of the copilot!

**You need to restart the docker services to deploy the changes.**
  
