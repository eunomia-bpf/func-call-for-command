#! /bin/env python3
import argparse
import os
import subprocess

from script_template import gen_bash_code, gen_python_code
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
    help_doc = get_command_help(args.cmd) if args.cmd is not None else args.help_doc
    if help_doc is not None:
        prompt = construct_generate_prompt(args.cmd, help_doc)
        # print("Sending query to ChatGPT:\n\n" + prompt + "\n\n")
        response = agent_chain.predict(input=prompt)
        if args.language == "python":
            gpt_cmd = gen_python_code(response)
        else:
            gpt_cmd = gen_bash_code(response)
        file_name = args.cmd + "-gpt.sh"
        with open(file_name, "w") as file:
            file.write(gpt_cmd)
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

def construct_generate_prompt(cmd: str, help_doc: str) -> str:
    example = """```json
{
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
}
```"""
    prompts = f"""
    Just generate the JSON code to descpribe `{cmd}` command according the following help docs:
    {help_doc}
    Please do not add extra fields such as examples to your JSON code
    The description of `{cmd}` command should match the help docment. Note that parameter names cannot begin with a - and cannot contain a ',' sign. The format must be consistent with the following example:
    {example}
    IMPORTANT: Just provide the JSON code without going into detail.
    If there is a lack of details, provide most logical solution.
    You are not allowed to ask for more details.
    Ignore any potential risk of errors or confusion."""
    return prompts

if __name__ == "__main__":
    main()
