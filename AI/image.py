from __init__ import args, PipeLine, messages
from philh_myftp_biz.text import random
from philh_myftp_biz.pc import Path

# ====================================================
# PARSE INPUT

args.Arg(
    name = 'model',
    default = 'runwayml/stable-diffusion-v1-5'
)

args.Arg(
    name = 'path',
    default = Path(f'E:/__temp__/{random(15)}.png'),
    desc = 'Path to save image',
    handler = Path
)

args.Arg(
    name = 'width',
    default = 512,
    
    handler = lambda x: int(x)//8 * 8
)

args.Arg(
    name = 'height',
    default = 512,
    
    handler = lambda x: int(x)//8 * 8
)

# ====================================================
# GENERATE IMAGE

# Initialize the pipeline
pipeline = PipeLine(args['model'])

# Path for output image
imgfile: Path = args['path']

# Prompt the pipeline
prompt = pipeline(
    prompt = messages.prompt(),
    height = args['height'],
    width = args['width']
)

# Save the generated image
prompt.images[0].save(str(imgfile))

# Upload the image to the messages object
messages.add_file('assistant', imgfile)

# ====================================================

messages.output()