from philh_myftp_biz import json, ParsedArgs
from philh_myftp_biz.pc import cls
import ollama

# ====================================================
# PARSE INPUT

args = ParsedArgs()

args.Arg(
    name = 'messages',
    default = 'null',
    desc = '',
    handler = json.loads
)

args.Arg(
    name = 'message',
    default = 'null',
    desc = '',
    handler = str
)

args.Arg(
    name = 'model',
    default = 'llama3',
    desc = '',
    handler = str
)

# ====================================================
# PARSE MESSAGES

messages: list[dict[str, str]]

if args['messages']:
    messages = args['messages']

elif args['message']:
    messages = [{
        'role': 'user',
        'content': args['message']
    }]

# ====================================================
# INSTALL MODEL

# Iter through installed modules
for model in ollama.list()['models']:
    
    # If module is selected
    if model['name'] == args['model']:
        
        break

# If the model is not installed
else:

    # Download & Install the model
    ollama.pull(args['model'])

# ====================================================
# HANDLE RESPONSE

#
response = ollama.chat(
    model = 'llama3',
    messages = messages,
    stream = True
)

rcontent = ""

for chunk in response:

    if chunk.get('message'):

        rcontent += chunk['message']['content']

messages += [{
    'role': 'assistant',
    'content': rcontent
}]

# ====================================================
# HANDLE OUTPUT

#
cls()
print(messages)