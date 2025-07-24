import gradio as gr
import random as rand

def echo(message, history):
    list = ["Yes", "Yes, definitely", "Most likely", "No", "My sources say no", "Ask again later", "Don't count on it", "Very doubtful", "Outlook not so good"]
    return rand.choice(list)

chatbot = gr.ChatInterface(echo, type='messages')
chatbot.launch()
