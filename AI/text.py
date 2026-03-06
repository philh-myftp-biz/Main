from philh_myftp_biz.modules import Service
from philh_myftp_biz.terminal import Log
from __init__ import args, messages
import ollama

OllamaServ = Service('E:/AI/Ollama/')

# ====================================================
# MODEL

args.Arg(
    name = 'model',
    default = 'llama3'
)

if not OllamaServ.running:

    OllamaServ.start()

Log.VERB(f'Pulling Model: {args['model']}')

# Download & install the model
ollama.pull(args['model'])

# ====================================================
# HANDLE RESPONSE

Log.VERB(f'Sending Messages to Model')

stream = ollama.chat(
    model = args['model'],
    messages = messages,
    stream = True
)

content = ''

for chunk in stream:

    content += chunk['message']['content']
    
    Log.VERB(f'Response: {content}')

messages.add_text(
    role = 'assistant', 
    content = content
)

# ====================================================

messages.output()
