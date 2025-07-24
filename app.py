import gradio as gr

def echo(message, history):
    print(message)
    print(history)
    return message

chatbot = gr.ChatInterface(echo, type='messages')
chatbot.launch()
