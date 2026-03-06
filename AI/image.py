from diffusers.pipelines.stable_diffusion.pipeline_stable_diffusion import StableDiffusionPipeline
from philh_myftp_biz.num import nearest_multiple
from __init__ import args, messages, this
from philh_myftp_biz.file import temp, PKL
from philh_myftp_biz.pc import Path
from philh_myftp_biz.text import hex
from torch import float16

# ====================================================
# PARSE INPUT

args.Arg(
    name = 'model',
    default = 'runwayml/stable-diffusion-v1-5'
)

args.Arg(
    name = 'path',
    default = temp('gen_image', 'png'),
    desc = 'Path to save image',
    handler = Path
)

args.Arg(
    name = 'width',
    default = 512,
    handler = lambda x: nearest_multiple(int(x), 8)
)

args.Arg(
    name = 'height',
    default = 512,    
    handler = lambda x: nearest_multiple(int(x), 8)
)

# ====================================================
# PIPELINE

pipePKL = PKL(temp(
    name = hex.encode(args['model']),
    ext = 'pkl',
    id = '0'
))

# If the pipeline is pickled
if pipePKL.path.exists:

    # Return the pickled pipeline
    pipeline: StableDiffusionPipeline = pipePKL.read()

# If the pipeline is not pickled
else:

    # Load the pipeline
    pipeline = StableDiffusionPipeline.from_pretrained(
        pretrained_model_name_or_path = args['model'],
        torch_dtype = float16,
        cache_dir = this.child('/StableDiffusion/data/').path,
        safety_checker = None,
        low_cpu_mem_usage = True
    )

    pipeline.enable_attention_slicing()

    # Pickle the pipeline
    pipePKL.save(pipeline)

# Move the pipeline to the GPU
pipeline.to("cuda")

# ====================================================
# GENERATE IMAGE

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
messages.add_file(
    role = 'assistant', 
    path = imgfile
)

# ====================================================

messages.output()