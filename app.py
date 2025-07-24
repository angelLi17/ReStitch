import gradio as gr
import random as rand

def echo(message, history):
    list = ["Yes", "Yes, definitely", "Most likely", "No", "My sources say no", "Ask again later", "Don't count on it", "Very doubtful", "Outlook not so good"]
    return rand.choice(list)

chatbot = gr.ChatInterface(echo, type='messages', examples=["Will it rain tomorrow?", "Will I enjoy my dinner?", "Will I be successful?"], title="8Oracle")
chatbot.launch()
