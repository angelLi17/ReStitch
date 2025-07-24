import gradio as gr

def echo(message, history):
    return message

chatbot = gr.ChatInterface(echo)
chatbot.launch()
