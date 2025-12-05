from __init__ import args, PipeLine, Messages
from philh_myftp_biz.file import temp

# ====================================================
# PARSE INPUT

args.Arg(
    name = 'model',
    default = 'runwayml/stable-diffusion-v1-5',
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
# GENERATE IMAGE

# Initialize the pipeline
pipeline = PipeLine(args['model'])

# Temporary path for output image
imgfile = temp('ai_image', 'png')

# Prompt the pipeline
prompt = pipeline(messages.prompt())

# Save the generated image
prompt.images[0].save(str(imgfile))

# Upload the image to the messages object
messages.add_file(imgfile)

# ====================================================

messages.output()