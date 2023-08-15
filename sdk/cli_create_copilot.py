import json
import os
import string
import time
from typing import List, Optional

from sdk import settings, messages
from sdk.utils import openai_utils
from sdk.utils import print_utils

BACKEND_ENV_TEMPLATE = """COPILOT_NAME="{copilot_name}"
API_PORT=3000
HOSTNAME=backend
MODEL="gpt-4"
OPENAI_API_KEY="{openai_api_key}"
# RAG
WEAVIATE_URL="http://weaviate:8080/"

JWT_CLIENT_ID = "CLIENT_ID"
JWT_CLIENT_SECRET = "CLIENT_SECRET"
JWT_TOKEN_EXPIRATION_SECONDS = "86400"
"""

FRONTEND_ENV_TEMPLATE = """VERCEL_ENV=preview
BACKEND_HOST="http://0.0.0.0:3000"

KV_URL=XXXXXXXX
KV_REST_API_URL=XXXXXXXX
KV_REST_API_TOKEN=XXXXXXXX
KV_REST_API_READ_ONLY_TOKEN=XXXXXXXX

AUTH0_SECRET="random-secret"
AUTH0_BASE_URL="http://localhost:3000"
AUTH0_ISSUER_BASE_URL="https://sidekik.ai"
AUTH0_CLIENT_ID="client-id"
AUTH0_CLIENT_SECRET="secret"

API_KEY="SECRET-API-KEY"

NEXT_PUBLIC_COPILOT_NAME="{copilot_canonized_name}"
NEXT_PUBLIC_COPILOT_DISPLAY_NAME="{copilot_name}"
DEBUG_ENABLED="{debug_enabled}"
NEXT_PUBLIC_LOGIN_REQUIRED=false
NEXT_PUBLIC_DEBUG_ENABLED="{debug_enabled}"

JWT_CLIENT_ID = "CLIENT_ID"
JWT_CLIENT_SECRET = "CLIENT_SECRET"
"""

SYSTEM_PROMPT_TEMPLATE = """You are a {copilot_name}.

As context to reply to the user you are given the following extracted parts of a long document, previous chat history, and a question from the user.

Only use hyperlinks that are explicitly listed as a source in the relevant context metadata. For example with ("metadata", "source": "https://docs.opencopilot.com/quickstart", "title": "Quickstart") the source would be "https://docs.opencopilot.com/quickstart".
DO NOT use hyperlinks inside the text and DO NOT make up a hyperlink that is not listed in the metadata as a source.

If the user question includes a request for code, provide a code block directly from the documentation.
If you don"t know the answer, please ask the user to be more precise with their question in a polite manner. Don"t try to make up an answer if you do not know it or have no information about it in the context.
If the question is not related to the goals, politely inform the user that you are tuned to only answer questions related to the goals.
REMEMBER to always provide 3 example follow up questions that would be helpful for the user to continue the conversation.

=========
{{context}}
=========

{{history}}
User: {{question}}
{copilot_name} answer in Markdown:
"""


def _get_copilot_canonized_name(copilot_name: str) -> str:
    # TODO: add strip and etc... to make it more safe?
    return copilot_name.lower().replace(" ", "_")


def _save_env_file(copilot_name: str, openai_api_key: str, debug_enabled: str):
    canonized_name = _get_copilot_canonized_name(copilot_name)
    with open("backend/.env", "w", encoding="utf-8") as file:
        file.write(
            BACKEND_ENV_TEMPLATE.format(
                copilot_name=canonized_name,
                openai_api_key=openai_api_key,
            )
        )
    with open("frontend/.env", "w", encoding="utf-8") as file:
        file.write(
            FRONTEND_ENV_TEMPLATE.format(
                copilot_name=copilot_name,
                copilot_canonized_name=canonized_name,
                debug_enabled=debug_enabled,
            )
        )


def _create_data_folder(copilot_name: str):
    copilot_folder = _get_copilot_path(copilot_name)
    copilot_data_folder = os.path.join(copilot_folder, "data")
    os.makedirs(copilot_data_folder, exist_ok=True)
    with open(os.path.join(copilot_data_folder, "placeholder.txt"), "w") as file:
        file.write("Dummy document file")


def _create_eval_folder(copilot_name: str):
    copilot_folder = _get_copilot_path(copilot_name)
    copilot_data_folder = os.path.join(copilot_folder, "eval_data")
    os.makedirs(copilot_data_folder, exist_ok=True)
    with open(os.path.join(copilot_data_folder, "endtoend_human.json"), "w") as file:
        json.dump(
            {
                "examples": [
                    {
                        "query": "The question to be evaluated",
                        "answer": "A correct answer to the question to be compared with a prediction."
                    }
                ]},
            file,
            indent=4
        )


def _save_config_yaml(copilot_name: str):
    copilot_config_folder = _get_copilot_path(copilot_name)
    os.makedirs(copilot_config_folder, exist_ok=True)
    with open(os.path.join(copilot_config_folder, "config.yaml"), "w") as file:
        file.write("data:\n  loaders:\n")


def _get_copilot_path(copilot_name: str) -> str:
    canonized_name = _get_copilot_canonized_name(copilot_name)
    return os.path.join(settings.COPILOTS_ROOT_DIR, canonized_name)


def _save_prompt_configuration(copilot_name: str):
    copilot_path = _get_copilot_path(copilot_name)
    copilot_prompts_folder = os.path.join(copilot_path, "prompts")
    os.makedirs(copilot_prompts_folder, exist_ok=True)
    with open(os.path.join(copilot_prompts_folder, "prompt_template.txt"), "w") as file:
        file.write(
            SYSTEM_PROMPT_TEMPLATE.format(
                copilot_name=copilot_name
            )
        )
    prompt_configuration = {
        "question_key": "User",
        "response_key": copilot_name
    }
    with open(os.path.join(copilot_prompts_folder, "prompt_configuration.json"), "w") as file:
        json.dump(prompt_configuration, file, indent=4)


def _input_list(prompt: str) -> List[str]:
    print(messages.EMPTY_LINE_TO_FINISH)
    i = 1
    user_inputs = []
    while True:
        user_input = input(f"{prompt} {i}: ")
        if user_input == "":
            break
        else:
            user_inputs.append(user_input)
        i += 1
    return user_inputs


def _get_copilot_name() -> str:
    allowed_chars = string.ascii_letters + ' -_'
    while True:
        copilot_name = input(messages.COPILOT_NAME_PROMPT)
        if len(copilot_name) >= 3 and all(c in allowed_chars for c in copilot_name):
            return copilot_name
        else:
            print(messages.COPILOT_NAME_VALIDATION_ERROR)


def _get_openai_api_key() -> str:
    while True:
        openai_api_key = input(messages.OPENAI_KEY_PROMPT)
        if openai_utils.validate_api_key(openai_api_key):
            print_utils.print_green(messages.OPENAI_KEY_VALIDATION_SUCCESS)
            return openai_api_key
        else:
            print_utils.print_red(messages.OPENAI_KEY_VALIDATION_ERROR)


def _get_debug_mode() -> str:
    while True:
        is_enable = input(messages.ENABLE_DEV_MODE_PROMPT)
        is_enable = is_enable.lower().strip()
        if is_enable == "y":
            print_utils.print_green(messages.ENABLE_DEV_MODE_ENABLED)
            return "true"
        elif is_enable == "n":
            print_utils.print_green(messages.ENABLE_DEV_MODE_DISABLED)
            return ""
        else:
            print_utils.print_red(messages.Y_OR_N_INVALID)


def _create_copilot() -> Optional[str]:
    try:
        copilot_name = _get_copilot_name()
        _save_prompt_configuration(copilot_name)
        return copilot_name
    except:
        return None


def main():
    print_utils.print_green(messages.GREETING)
    time.sleep(1)
    print_utils.print_yellow(messages.INTRODUCTION)
    time.sleep(1)
    print_utils.print_yellow(messages.FIRST_QUESTION)
    time.sleep(1)
    selection = print_utils.select(messages.INITIAL_OPTIONS)
    if selection is None:
        return
    openai_api_key = _get_openai_api_key()
    debug_enabled = _get_debug_mode()
    data_path = None
    if selection == 0:
        if copilot_name := _create_copilot():
            _save_env_file(copilot_name, openai_api_key, debug_enabled)
            _save_config_yaml(copilot_name)
            _create_data_folder(copilot_name)
            _create_eval_folder(copilot_name)
            data_path = copilot_name
        else:
            print_utils.print_red(messages.INTERRUPTED)
            return
    elif selection == 1:
        _save_env_file("rpm", openai_api_key, debug_enabled)
        data_path = "rpm"
    elif selection == 2:
        _save_env_file("unity", openai_api_key, debug_enabled)
        data_path = "unity"
    data_path = _get_copilot_path(data_path) + "/data"
    print_utils.print_green(f"You're all set!\nAdd your custom files to:\n -> {data_path}\n")


if __name__ == "__main__":
    main()
