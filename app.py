import gradio as gr
import random as rand

def echo(message, history):
    print(message)
    print(history)
    num = rand.randint(0,1)
    if num >= 0.5:
        output = "Yes"
    else :
        output = "No"
    return output

chatbot = gr.ChatInterface(echo, type='messages')
chatbot.launch()
