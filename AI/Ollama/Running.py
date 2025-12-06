from philh_myftp_biz.pc import cls
import ollama

cls()

try:
    
    ollama.list()
    
    print('true')

except ConnectionError:

    print('false')