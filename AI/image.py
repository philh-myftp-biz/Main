from __init__ import args, PipeLine, messages
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