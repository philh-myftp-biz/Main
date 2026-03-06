from philh_myftp_biz.terminal import ParsedArgs, cls
from philh_myftp_biz.modules import Module
from philh_myftp_biz import json, HELP
from typing import Literal, NoReturn
from philh_myftp_biz.pc import Path

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