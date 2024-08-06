from fasthtml.common import *
import requests
# Set up the app, including daisyui and tailwind for the chat component
tlink = Script(src="https://cdn.tailwindcss.com"),
dlink = Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/daisyui@4.11.1/dist/full.min.css")
app = FastHTML(hdrs=(tlink, dlink, picolink))

import google.generativeai as genai
import os

# Gemini configuration
genai.configure(api_key=os.environ["API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')
system_command = "You are a helpful and concise assistant"
chat = model.start_chat(history=[])
messages = []

# Chat message component, polling if message is still being generated
def ChatMessage(msg_idx):
    msg = messages[msg_idx]
    text = "..." if msg['content'] == "" else msg['content']
    bubble_class = f"chat-bubble-{'primary' if msg['role'] == 'user' else 'secondary'}"
    chat_class = f"chat-{'end' if msg['role'] == 'user' else 'start'}"
    generating = 'generating' in messages[msg_idx] and messages[msg_idx]['generating']
    stream_args = {"hx_trigger":"every 0.1s", "hx_swap":"outerHTML", "hx_get":f"/chat_message/{msg_idx}"}
    return Div(Div(msg['role'], cls="chat-header"),
               Div(text, cls=f"chat-bubble {bubble_class}"),
               cls=f"chat {chat_class}", id=f"chat-message-{msg_idx}", 
               **stream_args if generating else {})

# The input field for the user message. Also used to clear the 
# input field after sending a message via an OOB swap
def ChatInput():
    return Input(type="text", name='msg', id='msg-input', 
                 placeholder="Type a message", 
                 cls="input input-bordered w-full", hx_swap_oob='true')

# The main screen
@app.route("/")
def get():
    messages = []
    page = Body(H1('Chatbot Demo'),
                Div(*[ChatMessage(idx) for idx in range(len(messages))],
                    id="chatlist", cls="chat-box h-[73vh] overflow-y-auto"),
                Form(Group(ChatInput(), Button("Send", cls="btn btn-primary")),
                    hx_post="/", hx_target="#chatlist", hx_swap="beforeend",
                    cls="flex space-x-2 mt-2",
                ), cls="p-4 max-w-lg mx-auto")
    return Title('Chatbot Demo'), page 

# Run the chat model in a separate thread
@threaded
def get_response(r, idx):
    for chunk in r: messages[idx]["content"] += chunk
    messages[idx]["generating"] = False

def query_gemini(message):
    response = chat.send_message(message)
    return response.text

# Handle the form submission
@app.post("/")
def post(msg:str):
    idx = len(messages)
    messages.append({"role": "user", "content": msg})  
    # Call Gemini API using the query_gemini function
    prompt = f"{system_command}\n\n{msg}"
    gemini_response = query_gemini(prompt)
    messages.append({"role": "assistant", "generating": True, "content": gemini_response})
    get_response(gemini_response, idx+1) # Start a new thread to fill in content

    return (ChatMessage(idx),  # The user's message
            ChatMessage(idx + 1),  # The chatbot's response
            ChatInput())  # Clear the input field

if __name__ == '__main__': uvicorn.run("app:app", host='0.0.0.0', port=8080, reload=True)