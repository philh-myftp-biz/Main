from __init__ import args, messages, this
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
# OLLAMA SERVICE

running: bool = this.run('Ollama/Running', hide=True).output('json')

if not running:

    this.run('Ollama/Start')

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