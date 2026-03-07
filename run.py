from ai_engine.rag_core import ask_ai, clear_memory
from ai_engine.chat_history import clear_history
while True:

    q = input("You: ")

    if q.lower() == "exit":
        break
    
    if q.lower()=="new":
        clear_memory()
        clear_history()
        print("Started a new chat.")
        continue

    if q.strip() == "":
        q = "continue the story naturally"
    ans = ask_ai(q)

    print("AI:", ans)