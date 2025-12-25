from philh_myftp_biz.pc import Path, mkdir, cls
from philh_myftp_biz import json, ParsedArgs
from philh_myftp_biz.modules import Module
from typing import Literal, Iterator

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
# DIRECTORIES

#
class d:

    pipelines = this.dir.child('/__pycache__/Pipelines/')
    mkdir(pipelines)

    #
    models = this.dir.child('/StableDiffusion/data/')
    mkdir(models)

# ====================================================
# CLASSES + FUNCTIONS

class Messages:

    def __init__(self,
        messages: list[dict[str, str]] = []
    ):
        self.__messages = messages

    def add_text(self,
        role: Literal['user', 'assistant'],
        content: str
    ) -> None:
        self.__messages += [{
            'kind': 'text',
            'role': role,
            'content': content
        }]

    def add_file(self,
        role: Literal['user', 'assistant'],
        path: Path
    ):

        #
        self.__messages += [{
            'kind': 'file',
            'role': role,
            'content': str(path)
        }]

    def __iter__(self) -> Iterator[dict[str, str]]:
        return iter(self.__messages)
    
    def output(self):
        
        # Clear the Terminal Window
        cls()

        # Print the messagees
        print(self.__messages)

        # Stop the execution
        exit()

    def prompt(self) -> None | str:

        lmessage = self.__messages[-1]

        if lmessage['role'] == 'user':
            return lmessage['content']

def PipeLine(model: str):
    from diffusers import StableDiffusionPipeline
    from philh_myftp_biz.file import PKL
    import torch
    
    #
    pipeFile = d.pipelines.child(model.replace('/', '__') + '.pkl')

    # Wrap the pipeline file
    pipePkl = PKL(pipeFile)

    # If the pipeline is pickled
    if pipeFile.exists():

        # Return the pickled pipeline
        pipeline = pipePkl.read()

    # If the pipeline is not pickled
    else:

        # Load the pipeline
        pipeline = StableDiffusionPipeline.from_pretrained(
            pretrained_model_name_or_path = model,
            torch_dtype = torch.float16,
            cache_dir = str(d.models),
            safety_checker = None,
            low_cpu_mem_usage = True
        )

        # Pickle the pipeline
        pipePkl.save(pipeline)

    # Move the pipeline to the GPU
    pipeline.to("cuda")

    # Return the pipeline
    return pipeline

# ====================================================
# PARSE MESSAGES

if args['messages']:
    messages = Messages(args['messages'])

elif args['prompt']:
    messages = Messages()
    messages.add_text('user', args['prompt'])

else:

    raise Exception('No prompt or messages given')

# ====================================================