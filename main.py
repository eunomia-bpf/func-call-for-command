#! /bin/env python3
import argparse
import os
import subprocess
import web
import flask

from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain

OPENAI_API_KEY = "OPENAI_API_KEY"

def main():
    parser = argparse.ArgumentParser(
        prog="gen_function_call",
        description="Use ChatGPT to generate function call according help docs."
    )
    parser.add_argument("-v", "--verbose", help="Show more details", action="store_true")
    parser.add_argument("-c", "--cmd", help="Command name")
    parser.add_argument("-l", "--language", default="python", help="The language of function call")
    parser.add_argument("-w", "--web", help="The language of function call")
    parser.add_argument("-d", "--help_doc", help="Help documentation for the command")
    parser.add_argument(
        "-k", "--key",
        help=f"Openai api key, see `https://platform.openai.com/docs/quickstart/add-your-api-key` or passed through `{OPENAI_API_KEY}`")

    args = parser.parse_args()
    if args.key is not None:
        os.environ['OPENAI_API_KEY'] = args.key
    if os.environ.get(OPENAI_API_KEY, None) is None:
        print(f"Either provide your openai api key through `-k` or through environment variable {OPENAI_API_KEY}")
        return
    agent_chain = init(args.verbose)
    if args.web is not None:
        run(args, agent_chain)
    help_doc = get_command_help(args.cmd) if args.cmd is not None else args.help_doc
    if help_doc is not None:
        prompt = construct_generate_prompt(help_doc, args.language)
        # print("Sending query to ChatGPT:\n\n" + prompt + "\n\n")
        response = agent_chain.predict(input=prompt)
        print("The response from ChatGPT:\n\n" + response)
    else:
        parser.print_help()

def init(verbose):
    llm = ChatOpenAI(model_name="gpt-3.5-turbo",temperature=0)
    agent_chain = ConversationChain(llm=llm, verbose=verbose,
                    memory=ConversationBufferMemory())
    return agent_chain


def get_command_help(command):
    try:
        output = subprocess.check_output([command, '--help'], universal_newlines=True)
        return output
    except subprocess.CalledProcessError as e:
        return f"Error executing help command: {e.output}"

def construct_generate_prompt(help_doc: str, language: str="python") -> str:
    example = """```json
[{
    "name": "get_current_weather",
    "description": "Get the current weather",
    "parameters": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "The city and state, e.g. San Francisco, CA",
            },
            "format": {
                "type": "string",
                "enum": ["celsius", "fahrenheit"],
                "description": "The temperature unit to use. Infer this from the users location.",
            },
        },
        "required": ["location", "format"],
    },
}]
```"""

    prompts = f"""Provide a {language} function to execute the below command according the following help docs:
```text
{help_doc}
```
Then provide the json code to descpribe this command function. The description of this function should be consistent with the command, and the format is the same as in the following example:
{example}
IMPORTANT: Just provide the code without going into detail.
If there is a lack of details, provide most logical solution.
You are not allowed to ask for more details.
Ignore any potential risk of errors or confusion."""
    return prompts

def run(args, agent_chain):

    flask_app = flask.Flask(__name__)

    def homepage():
        return flask.render_template("index.html")

    def query_api():
        query_str: str = flask.request.json["search"]  # type: ignore
        if not query_str.strip():
            return "Empty strings are not accepted", 400
        prompt = construct_generate_prompt(query_str, args.language)
        result = agent_chain.predict(input=prompt)
        print(result)
        return flask.jsonify(response=result)
    flask_app.route("/", methods=["GET"])(homepage)
    flask_app.route("/query", methods=["POST", "GET"])(query_api)
    flask_app.run(host="0.0.0.0", port="4100")
if __name__ == "__main__":
    main()
