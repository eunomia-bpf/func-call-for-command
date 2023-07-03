
#!/bin/bash
user_input="$@"
response=$(curl -s https://api.openai.com/v1/chat/completions -u :$OPENAI_API_KEY -H 'Content-Type: application/json' -d '{
  "model": "gpt-3.5-turbo-0613",
  "messages": [
    {"role": "user", "content": "'"$user_input"'"}
  ],
  "functions": [
{
    "name": "uname",
    "description": "Print certain system information",
    "parameters": {
        "type": "object",
        "properties": {
            "all": {
                "type": "boolean",
                "description": "Print all information"
            },
            "kernel-name": {
                "type": "boolean",
                "description": "Print the kernel name"
            },
            "nodename": {
                "type": "boolean",
                "description": "Print the network node hostname"
            },
            "kernel-release": {
                "type": "boolean",
                "description": "Print the kernel release"
            },
            "kernel-version": {
                "type": "boolean",
                "description": "Print the kernel version"
            },
            "machine": {
                "type": "boolean",
                "description": "Print the machine hardware name"
            },
            "processor": {
                "type": "boolean",
                "description": "Print the processor type (non-portable)"
            },
            "hardware-platform": {
                "type": "boolean",
                "description": "Print the hardware platform (non-portable)"
            },
            "operating-system": {
                "type": "boolean",
                "description": "Print the operating system"
            }
        },
        "required": []
    }
}
]}')

# Parsing JSON data
full_command=$(echo "$response" | jq -r '.choices[0].message.function_call.name')
args=$(echo "$response" | jq '.choices[0].message.function_call.arguments')

args=$(echo -e $args | tr -d '\\')
args=$(echo $args | sed 's/^"//;s/"$//')

for key in $(echo "$args" | jq -r 'keys[]'); do
    value=$(echo $args | jq -r --arg key $key '.[$key]')
    if [ "$value" != "true" ] && [ "$value" != "false" ]; then
        full_command+=" --$key "$value" "
    else
        full_command+=" --$key "
    fi
done

echo "Run: $full_command"
eval "$full_command"
