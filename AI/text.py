from __init__ import args, messages
import ollama

# ====================================================
# INSTALL MODEL

args.Arg(
    name = 'model',
    default = 'llama3'
)

# Iter through installed models
for model in ollama.list()['models']:
    
    # If model is selected
    if model['model'] == args['model']:
        break

# If the model is not installed
else:

    # Download & install the model
    ollama.pull(args['model'])

# ====================================================
# HANDLE RESPONSE

response = ollama.chat(
    model = 'llama3',
    messages = list(messages),
    stream = True
)

rcontent = ""

for chunk in response:

    if chunk.get('message'):

        rcontent += chunk['message']['content']

messages.add_text('assistant', rcontent)

# ====================================================
# HANDLE OUTPUT

messages.output()