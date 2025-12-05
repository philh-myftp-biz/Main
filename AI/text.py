from __init__ import args, Messages
import ollama

# ====================================================
# PARSE INPUT

args.Arg(
    name = 'model',
    default = 'llama3',
    desc = '',
    handler = str
)

# ====================================================
# PARSE MESSAGES

if args['messages']:
    messages = Messages(args['messages'])

elif args['message']:
    messages = Messages()
    messages.add_text('user', args['message'])

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

messages.add_text('assistant', rcontent)

# ====================================================
# HANDLE OUTPUT

messages.output()