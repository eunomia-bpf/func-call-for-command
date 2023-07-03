# GPT Func Call generator for Command-line

** Your one-click solution to transform traditional command-line tools into natural language-driven powerhouses! **

Ever wondered if your command-line tools could understand plain English? We did too, so we built **Naturaliser**. Built on the bedrock of OpenAI's GPT technology, **Naturaliser** turns your dense, jargon-filled help files into sleek, interactive commands that anyone can understand and execute.

## Features ✨

- 🧠 Smart Function Call Generation: Provide your tool's help file, and GPT Func Call generator will do the rest. We'll generate the corresponding OpenAI GPT function calls and JSON descriptions in a flash, and the driven library in any language as well.
- 🛠 Python and Web App Support: Whether you're dealing with Python scripts or web apps, Naturaliser has got you covered.
- 🔄 Single-Click Operation: Simplify your workflow with our user-friendly interface. One click, and you're good to go!

Let's make command-line tools more accessible, user-friendly, and less intimidating.

## Web tool

See https://ai-func-call-gen.vercel.app/ for details.

![image](https://github.com/eunomia-bpf/func-call-for-command/assets/34985212/aa65b5b3-4dd1-4f74-9186-a6f573792db9)

A function call generator for terminal commands, where the user provides the help file for the command and GPT generates the corresponding function call and Json description. Support python scripts or web apps.

Repo: https://github.com/eunomia-bpf/ai-func-call-gen

## Python Script Usage

Firstly, you need to clone this repo and install the necessary python package:
```
git clone https://github.com/eunomia-bpf/func-call-for-command.git
pip install -r requirements.txt
```
Then, use command line interaction to generate function calls and JSON descriptions. You can provide command name such as `python ./main.py -k you_openai_api_key -c uname`. When using this method, make sure you have the relevant commands installed.

There is an example about this tools:

```console
$python ./main.py -k you_openai_api_key -c ugc

The response from ChatGPT:

Here is a Python function to execute the "ugc" command according to the provided help docs:

import subprocess

def execute_ugc_command(pid, language=None, verbose=False, milliseconds=False, minimum=None, filter=None):
    command = ['./ugc', str(pid)]
    if language:
        command.extend(['-l', language])
    if verbose:
        command.append('-v')
    if milliseconds:
        command.append('-m')
    if minimum:
        command.extend(['-M', str(minimum)])
    if filter:
        command.extend(['-F', filter])
    
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout


And here is the JSON code to describe this command function:


[{
    "name": "execute_ugc_command",
    "description": "Execute the ugc command",
    "parameters": {
        "type": "object",
        "properties": {
            "pid": {
                "type": "integer",
                "description": "The process id to attach to"
            },
            "language": {
                "type": "string",
                "enum": ["java", "node", "python", "ruby"],
                "description": "The language to trace"
            },
            "verbose": {
                "type": "boolean",
                "description": "Verbose mode: print the BPF program (for debugging purposes)"
            },
            "milliseconds": {
                "type": "boolean",
                "description": "Report times in milliseconds (default is microseconds)"
            },
            "minimum": {
                "type": "integer",
                "description": "Display only GCs longer than this many milliseconds"
            },
            "filter": {
                "type": "string",
                "description": "Display only GCs whose description contains this text"
            }
        },
        "required": ["pid"]
    }
}]
```
