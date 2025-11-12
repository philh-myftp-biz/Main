from langchain_ollama import OllamaLLM
from philh_myftp_biz.modules import input, output

chat = input()[0]

#llm = OllamaLLM(model="llama3.1:8b")
#insult = llm.invoke("Create a creative, but also stupid insult")# about the following topic: "+about)
#print(insult)

output(chat)