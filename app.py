import gradio as gr
from huggingface_hub import InferenceClient

#STEP 1 FROM SEMANTIC SEARCH
from sentence_transformers import SentenceTransformer
import torch

from transformers import pipeline
import torch



#STEP 2 FROM SEMANTIC SEARCH
# Open the restitch.txt file in read mode with UTF-8 encoding
with open("restitch.txt", "r", encoding="utf-8") as file:
  # Read the entire contents of the file and store it in a variable
  restitch_text = file.read()
print(restitch_text)



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



#STEP 4 FROM SEMANTIC SEARCH
# Load the pre-trained embedding model that converts text to vectors
model = SentenceTransformer('all-MiniLM-L6-v2')

def create_embeddings(text_chunks):
  # Convert each text chunk into a vector embedding and store as a tensor
  chunk_embeddings = model.encode(text_chunks, convert_to_tensor=True) # Replace ... with the text_chunks list

  # Print the chunk embeddings
  print(chunk_embeddings)

  # Print the shape of chunk_embeddings
  print(chunk_embeddings.shape)

  # Return the chunk_embeddings
  return chunk_embeddings

# Call the create_embeddings function and store the result in a new chunk_embeddings variable
chunk_embeddings = create_embeddings(cleaned_chunks) # Complete this line



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


#STEP 6 FROM SEMANTIC SEARCH
# Call the get_top_chunks function with the original query
# top_results = get_top_chunks("How does water get into the sky", chunk_embeddings, cleaned_chunks) # Complete this line
# Print the top results
# print(top_results)


# client = InferenceClient("Qwen/Qwen2.5-72B-Instruct")



def respond(message, history):
    messages = [
        {"role": "system", 
            "content": "You are a creative person who tells people how they can upcycle their clothing in concise language. Limit responses to 150 words and always end in a complete sentence. You are very kind! Base your response on the provided context: {str_restitch_text}"
        },
        {
            "role": "user",
            "content": (
                f"Question: {message}"
            )
        }
    ]
    best_restitch_chunks = get_top_chunks(message, chunk_embeddings, cleaned_chunks) # Complete this line
    str_restitch_chunks = "\n".join(best_restitch_chunks)
    
    if history:
        messages.extend(history)

    messages.append({"role": "user", "content": message})

    response = ""
    
    for message in client.chat_completion(
        messages,
        max_tokens=200,
        temperature=0.2,
        stream=True
    ):
        token = message.choices[0].delta.content
        response += token
        yield response

chatbot = gr.ChatInterface(respond, type='messages', examples=["How do I repurpose my shirt?", "Is this good for the environment?", "Can you tell what to do with my old pants?"], title="ReStitch", description="Are you out of closet space? Is your closet filled with clothes you never use? Worry not, our chatbot is designed to give you trendy and creative ideas to make something new out of the old.", theme='kioshi/brightly-colored')
chatbot.launch()
