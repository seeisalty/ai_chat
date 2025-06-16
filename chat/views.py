from django.shortcuts import render
from django.http import StreamingHttpResponse
import requests
import json

# Simple chat UI
def chat_ui(request):
    return render(request, 'chat/chat.html')

# Streaming endpoint for real LocalAI responses
def chat_stream(request):
    user_message = request.GET.get('message', '')
    def event_stream():
        url = "http://localhost:5000/v1/chat/completions"
        headers = {"Content-Type": "application/json"}
        payload = {
            # Use the model name from the YAML config, not the GGUF filename
            "model": "mistral-7b-v0.1.Q4_K_M",  
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}
            ],
            "stream": True
        }
        try:
            with requests.post(url, headers=headers, data=json.dumps(payload), stream=True, timeout=120) as resp:
                for line in resp.iter_lines():
                    if line:
                        if line.startswith(b"data:"):
                            chunk = line[5:].strip()
                            if chunk and chunk != b"[DONE]":
                                try:
                                    data = json.loads(chunk)
                                    # LocalAI may use either 'delta' or 'message' for streaming content
                                    choice = data.get("choices", [{}])[0]
                                    delta = ""
                                    if "delta" in choice and "content" in choice["delta"]:
                                        delta = choice["delta"]["content"]
                                    elif "message" in choice and "content" in choice["message"]:
                                        delta = choice["message"]["content"]
                                    if delta:
                                        yield f"data: {delta}\n"
                                except Exception:
                                    pass
        except Exception as e:
            yield f"data: [Error: {str(e)}]\n"
    return StreamingHttpResponse(event_stream(), content_type='text/event-stream')
