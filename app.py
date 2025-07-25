import gradio as gr
from huggingface_hub import InferenceClient

client = InferenceClient("HuggingFaceH4/zephr-7b-beta")

def respond(message, history):
    messages = [{"role": "system", "content": "You are a friendly chatbot"}]
    
    if history:
        messages.extend(history)

    messages.append({"role": "user", "content": message})

    response = client.chat_completion(
        messages,
        max_tokens=100,
        temperature=0.2
    ) 
    
    return response['choices'][0]['message']['content'].strip()

chatbot = gr.ChatInterface(respond, type='messages', examples=["Will it rain tomorrow?", "Will I enjoy my dinner?", "Will I be successful?"], title="8Oracle", description="I see your future...", theme=gr.themes.Glass())
chatbot.launch()
