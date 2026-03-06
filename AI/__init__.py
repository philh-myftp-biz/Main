from diffusers.pipelines.stable_diffusion.pipeline_stable_diffusion import StableDiffusionPipeline
from philh_myftp_biz.terminal import ParsedArgs, cls
from philh_myftp_biz.file import PKL, temp
from philh_myftp_biz.modules import Module
from philh_myftp_biz import json, HELP
from typing import Literal, NoReturn
from philh_myftp_biz.text import hex
from philh_myftp_biz.pc import Path
from torch import float16

# ====================================================

this = Module('E:/AI/')

# ====================================================
# PARSE INPUT

args = ParsedArgs()

args.Arg(
    name = 'messages',
    handler = json.loads
)

args.Arg(
    name = 'prompt'
)

# ====================================================

class Messages(list[dict[Literal['kind', 'role', 'content'], str]]):

    def __init__(self,
        messages: list[dict[str, str]] = []
    ) -> None:
        
        super().__init__()

        self += messages

    def add_text(self,
        role: Literal['user', 'assistant'],
        content: str
    ) -> None:
        self += [{
            'kind': 'text',
            'role': role,
            'content': content
        }]

    def add_file(self,
        role: Literal['user', 'assistant'],
        path: Path
    ) -> None:
        self += [{
            'kind': 'file',
            'role': role,
            'content': str(path)
        }]
    
    def output(self) -> NoReturn:
        
        # Clear the Terminal Window
        cls()

        data = json.dumps(self)

        # Print the messagees
        print(data)

        # Stop the execution
        exit()

    def prompt(self) -> None | str:

        lmessage = self[-1]

        if lmessage['role'] == 'user':
            
            return lmessage['content']

# ====================================================

def PipeLine(model: str) -> StableDiffusionPipeline:
    
    pipeFile = temp(
        name = hex.encode(model),
        ext = 'pkl',
        id = '0'
    )

    # Wrap the pipeline file
    pipePkl = PKL(pipeFile)

    # If the pipeline is pickled
    if pipeFile.exists:

        # Return the pickled pipeline
        pipeline = pipePkl.read()

    # If the pipeline is not pickled
    else:

        # Load the pipeline
        pipeline = StableDiffusionPipeline.from_pretrained(
            pretrained_model_name_or_path = model,
            torch_dtype = float16,
            cache_dir = this.child('/StableDiffusion/data/').path,
            safety_checker = None,
            low_cpu_mem_usage = True
        )

        pipeline.enable_attention_slicing()

        # Pickle the pipeline
        pipePkl.save(pipeline)

    # Move the pipeline to the GPU
    pipeline.to("cuda")

    # Return the pipeline
    return pipeline # pyright: ignore[reportReturnType]

# ====================================================
# PARSE MESSAGES

# Do nothing if '-h' is passed
if HELP:
    messages = None

elif args['messages']:
    messages = Messages(args['messages'])

elif args['prompt']:
    messages = Messages()
    messages.add_text('user', args['prompt'])

else:
    raise Exception('No prompt or messages given')

# ====================================================