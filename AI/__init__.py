from philh_myftp_biz.modules import Module, Service
from philh_myftp_biz.pc import Path, mkdir, cls
from typing import Literal, Iterator

this = Module('E:/AI/')

Ollama = Service(this, '/Ollama/')

# ====================================================
# PARSE INPUT
from philh_myftp_biz import json, ParsedArgs

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
pipeDir = this.dir.child('__pycache__/PipeLines/')
mkdir(pipeDir)

#
cacheDir = this.dir.child('__pycache__/Models/')
mkdir(cacheDir)

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
        from pickle import dumps
        
        # Read the file data
        raw = path.open('rb').read()

        #
        self.__messages += [{
            'kind': 'file',
            'ext': path.ext(),
            'role': role,
            'content': dumps(raw)
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
    from philh_myftp_biz.text import hex
    from philh_myftp_biz.file import PKL
    from diffusers import StableDiffusionPipeline
    import torch
    
    #
    pipeFile = pipeDir.child(f'{hex.encode(model)}.pkl')

    # Wrap the pipeline file
    pipePkl = PKL(pipeFile)

    # If the pipeline is pickled
    if pipeFile.exists():

        # Return the pickled pipeline
        return pipePkl.read()

    # If the pipeline is not pickled
    else:

        # Load the pipeline
        pipeline = StableDiffusionPipeline.from_pretrained(
            pretrained_model_name_or_path = model,
            torch_dtype = torch.float16,
            cache_dir = str(cacheDir),
            safety_checker = None,
            low_cpu_mem_usage = False
        )

        # Move the pipeline to the GPU
        pipeline.to("cuda")

        # Pickle the pipeline
        pipePkl.save(pipeline)

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