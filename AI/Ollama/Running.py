import ollama

try:
    
    ollama.list()
    
    print('true')

except ConnectionError:

    print('false')