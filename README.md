## GPT Func Call for Command

A function call generator for terminal commands, where the user provides the help file for the command and GPT generates the corresponding function call and Json description.

## Usage

Firstly, you need to clone this repo and install the necessary python package:
```
git clone 
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
