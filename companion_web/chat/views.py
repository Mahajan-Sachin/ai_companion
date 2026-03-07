from django.http import HttpResponse
from django.http import JsonResponse
from ai_engine.rag_core import ask_ai, clear_memory
from django.shortcuts import render
import json
from django.views.decorators.csrf import csrf_exempt
from ai_engine.chat_history import clear_history

def chat_page(request):
    return render(request,"chat/chat.html")


@csrf_exempt
def chat_api(request):
    if request.method=="POST":
        data=json.loads(request.body) # req.body means {json format} but we are converting json to dict, which has actually {"message":"text"}
        user_message=data.get("message","")
        if user_message.lower()=="new":
            clear_memory()
            clear_history()
            return JsonResponse({
                "reply":"Started a new chat"
                })
        if user_message.strip()=="":
            user_message="Continue the Storynaturally"
        ai_reply=ask_ai(user_message)
        return JsonResponse({
            "reply":ai_reply
        })
    return JsonResponse({"error":"Invalid request"})