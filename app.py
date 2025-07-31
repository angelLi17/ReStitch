import gradio as gr
from huggingface_hub import InferenceClient


#__________________________________________
#STEP 1 FROM SEMANTIC SEARCH
from sentence_transformers import SentenceTransformer
import torch
#__________________________________________


#__________________________________________
#STEP 2 FROM SEMANTIC SEARCH
# Open the restitch.txt file in read mode with UTF-8 encoding
with open("restitch.txt", "r", encoding="utf-8") as file:
  # Read the entire contents of the file and store it in a variable
  restitch_text = file.read()
# jasmine: commenting this out bc it's a lot of text to print 
# print(restitch_text)
#__________________________________________


#__________________________________________
#STEP 3 FROM SEMANTIC SEARCH
def preprocess_text(text):
  # Strip extra whitespace from the beginning and the end of the text
  cleaned_text = text.strip()

  # Split the cleaned_text by every newline character (\n)
  chunks = cleaned_text.split("\n")

  # Create an empty list to store cleaned chunks
  cleaned_chunks = []

  # Write your for-in loop below to clean each chunk and add it to the cleaned_chunks list
  for chunk in chunks:
    cleaned_chunks.append(chunk.strip())

  # Print cleaned_chunks
  print(cleaned_chunks)

  # Print the length of cleaned_chunks
  print(len(cleaned_chunks))

  # Return the cleaned_chunks
  return cleaned_chunks

# Call the preprocess_text function and store the result in a cleaned_chunks variable
cleaned_chunks = preprocess_text(restitch_text) # Complete this line
#__________________________________________


#__________________________________________
#STEP 4 FROM SEMANTIC SEARCH
# Load the pre-trained embedding model that converts text to vectors
model = SentenceTransformer('all-MiniLM-L6-v2')

def create_embeddings(text_chunks):
  # Convert each text chunk into a vector embedding and store as a tensor
  chunk_embeddings = model.encode(text_chunks, convert_to_tensor=True) # Replace ... with the text_chunks list

  # Print the chunk embeddings
  #print(chunk_embeddings)

  # Print the shape of chunk_embeddings
  #print(chunk_embeddings.shape)

  # Return the chunk_embeddings
  return chunk_embeddings

# Call the create_embeddings function and store the result in a new chunk_embeddings variable
chunk_embeddings = create_embeddings(cleaned_chunks) # Complete this line
#print(cleaned_chunks)
#print(chunk_embeddings)
#__________________________________________


#__________________________________________
#STEP 5 FROM SEMANTIC SEARCH
# Define a function to find the most relevant text chunks for a given query, chunk_embeddings, and text_chunks
def get_top_chunks(query, chunk_embeddings, text_chunks):
  # Convert the query text into a vector embedding
  query_embedding = model.encode(query, convert_to_tensor = True) # Complete this line

  # Normalize the query embedding to unit length for accurate similarity comparison
  query_embedding_normalized = query_embedding / query_embedding.norm()

  # Normalize all chunk embeddings to unit length for consistent comparison
  chunk_embeddings_normalized = chunk_embeddings / chunk_embeddings.norm(dim=1, keepdim=True)

  # Calculate cosine similarity between query and all chunks using matrix multiplication
  similarities = torch.matmul(chunk_embeddings_normalized, query_embedding_normalized) # Complete this line

  # Print the similarities
  print(similarities)

  # Find the indices of the 3 chunks with highest similarity scores
  top_indices = torch.topk(similarities, k=3).indices

  # Print the top indices
  print(top_indices)

  # Create an empty list to store the most relevant chunks
  top_chunks = [] #x for i in top_indices

  # Loop through the top indices and retrieve the corresponding text chunks
  for i in top_indices:
    top_chunks.append(text_chunks[i])


  # Return the list of most relevant chunks
  return top_chunks

    
#__________________________________________
#STEP 6 FROM SEMANTIC SEARCH
# Call the get_top_chunks function with the original query
# top_results = get_top_chunks("How does water get into the sky", chunk_embeddings, cleaned_chunks) # Complete this line
# Print the top results
# print(top_results)
#__________________________________________


#__________________________________________
client = InferenceClient("Qwen/Qwen2.5-72B-Instruct")

desc = "ReStitch is a tool that aids in upcycling old clothes that have been sitting in your closet, untouched, for years." # update this
tagline = "One Stitch At A Time"
logo = "logo.png"
icon = "icon.png"

custom_theme = gr.themes.Ocean(
    primary_hue="yellow",
    secondary_hue="rose", 
    neutral_hue="rose",
    spacing_size="lg",
    radius_size="lg",
    text_size="lg",
    font=[gr.themes.GoogleFont("Intel One Mono"), "serif"],
    font_mono=[gr.themes.GoogleFont("Playwrite Magyarország"), "cursive"]
)
#__________________________________________


#__________________________________________
def respond(message, history, level):
    response = ""
    best_restitch_chunks = get_top_chunks(message, chunk_embeddings, cleaned_chunks) # Complete this line
    str_restitch_chunks = "\n".join(best_restitch_chunks)
    
    messages = [
        {"role": "system", 
        "content": f"You are a creative person who tells people how they can upcycle their clothing in concise language suitable for someone who is at the {level} level for sewing. Make sure that you always end your message with a complete sentence and under 100 words but if it is a step-by-step instruction then 150 words is the limit. You are very kind! Base your response on the provided context: {str_restitch_chunks}"
        },
        {"role": "user", "content": f"Question: {message}"
        }
    ]
    
    
    if history:
        messages.extend(history)


    messages.append({"role": "user", "content": message})

    stream = client.chat_completion(
        messages,
        max_tokens=200,
        temperature=0.2,
        stream=True
    )
    for message in stream:
        token = message.choices[0].delta.content
        if token is not None: 
            response += token
            yield response

# chatbot = gr.ChatInterface(
#     fn=respond, type='messages', examples=["How do I repurpose my shirt?", "Is this good for the environment?", "Can you tell what to do with my old pants?"], title="ReStitch", description="Are you out of closet space? Is your closet filled with clothes you never use? Worry not, our chatbot is designed to give you trendy and creative ideas to make something new out of the old.", theme='kioshi/brightly-colored')
# chatbot.launch()
#__________________________________________


#__________________________________________

with gr.Blocks(theme=custom_theme) as ReStitch:
    with gr.Row(scale=1):
        gr.Image(
	    value="ReStitch.png",
        show_label=False, 
        show_share_button = False,  
        show_download_button = False)
        # with gr.Column(scale=1):
        #     gr.Image(
        # 	    value="icon.png", 
        # 	    show_label=False, 
        # 	    show_share_button = False, 
        # 	    show_download_button = False)
        # with gr.Column(scale=4):
        #     with gr.Row():
        #         gr.Markdown("ReStitch")
        #     with gr.Row():
        #         gr.Markdown(tagline)
level = "Beginner"
    with gr.Row(scale=3):
        with gr.Column(scale=1):
            with gr.Row():
                level = gr.Dropdown(["Beginner", "Intermediate", "Advanced"], label="Sewing Skill Level", info="What is your crafting skill level? Skills that you might need for upcycling like sewing, tailoring, and pattern constructing.")
            #with gr.Row():
                #spotify playlist here
            #with gr.Row():
                #example image here
        with gr.Column(scale=4):
            gr.ChatInterface(
                fn=respond, 
                type='messages', 
                examples=[["How do I repurpose my shirt?", level], ["Teach me how to make a tote from my jeans.", level], ["Can you tell what to do with my old pants?", level]], 
                title="ReStitch", 
                additional_inputs = [level],
                description="Are you out of closet space? Is your closet filled with clothes you never use? Worry not, our chatbot is designed to give you trendy and creative ideas to make something new out of the old.", 
            )
    
#__________________________________________
#ADD SONG PLAYLIST HERE, EXAMPLE IMAGES, AND LINKS TO RESOURCES
    # with gr.Row(scale=1):
        # header
    # with gr.Row(scale=1):
        # with gr.Column():
        # resources links here
#__________________________________________        
    
ReStitch.launch()