def gen_gpt_cmd(func_descript):
    pre_content = """
#!/bin/bash
user_input="$@"
response=$(curl -s https://api.openai.com/v1/chat/completions -u :$OPENAI_API_KEY -H 'Content-Type: application/json' -d '{
  "model": "gpt-3.5-turbo-0613",
  "messages": [
    {"role": "user", "content": "'"$user_input"'"}
  ],
  "functions": [
"""
    post_content="""
]}')

# Parsing JSON data
full_command=$(echo "$response" | jq -r '.choices[0].message.function_call.name')
args=$(echo "$response" | jq '.choices[0].message.function_call.arguments')

args=$(echo -e $args | tr -d '\\\\')
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
"""
    return pre_content + func_descript + post_content

if __name__ == "__main__":
    print(gen_gpt_cmd("[{}]"))
