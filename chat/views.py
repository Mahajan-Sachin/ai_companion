from django.http import HttpResponse, JsonResponse, StreamingHttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from ai_engine.rag_core import ask_ai, ask_ai_stream
from ai_engine.memory import clear_all_memory
from ai_engine.chat_history import clear_history
import json


def chat_page(request):
    return render(request, "chat/chat.html")


@csrf_exempt
def chat_api(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_message = data.get("message", "")
        if user_message.lower() == "new":
            clear_all_memory()
            clear_history()
            return JsonResponse({"reply": "Started a new chat"})
        if user_message.strip() == "":
            user_message = "Continue the story naturally"
        ai_reply = ask_ai(user_message)
        return JsonResponse({"reply": ai_reply})
    return JsonResponse({"error": "Invalid request"})


@csrf_exempt
def chat_stream_api(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_message = data.get("message", "")

        # handle "new" command — clear memory and signal done
        if user_message.lower() == "new":
            clear_all_memory()
            clear_history()
            def new_chat_gen():
                yield f"data: {json.dumps('Started a new chat')}\n\n"
                yield "data: [DONE]\n\n"
            return StreamingHttpResponse(new_chat_gen(), content_type="text/event-stream")

        if user_message.strip() == "":
            user_message = "Continue the story naturally"

        # SSE generator — each token is JSON-encoded so special chars are safe
        def event_stream():
            for token in ask_ai_stream(user_message):
                yield f"data: {json.dumps(token)}\n\n"
            yield "data: [DONE]\n\n"

        response = StreamingHttpResponse(event_stream(), content_type="text/event-stream")
        response["Cache-Control"] = "no-cache"
        response["X-Accel-Buffering"] = "no"  # disable nginx buffering if behind proxy
        return response

    return JsonResponse({"error": "Invalid request"})