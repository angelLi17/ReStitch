import gradio as gr

def echo(message, history):
    return message

print("Hello World")

chatbot = gr.ChatInterface(echo, type='messages')
chatbot.launch()
