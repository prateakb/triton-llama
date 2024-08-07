import numpy as np
import requests
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import tritonclient.http as httpclient
from tritonclient.utils import *
import psycopg2
from datetime import datetime

# Function to connect to the PostgreSQL database
def connect_db():
    return psycopg2.connect(
        dbname="tritondata",
        user="user",
        password="password",
        host="localhost"  # Change to the service name in Docker if running inside a container
    )

# Function to log inference data
def log_inference(input_text, output_text):
    conn = connect_db()
    with conn:
        with conn.cursor() as curs:
            curs.execute("""
                INSERT INTO inference_logs (input_text, output_text)
                VALUES (%s, %s)
            """, (input_text, output_text))
    conn.close()

# Configuration
model_name = "PY007/TinyLlama-1.1B-Chat-v0.3"
url = "localhost:8000"  # Adjust this URL to your Triton server's location
max_length = 100

# Initialize the tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_name)
model_name="tinyllama"

# Function to generate text using the model hosted on Triton Inference Server
def generate_text_triton(input_text, max_length=5):
    # Tokenize the input text
    input_ids = tokenizer(input_text, return_tensors="pt").input_ids.numpy()
    generated_ids = input_ids.tolist()
    print(f"tokens: {generated_ids}")
    current_length = 0

    # Increase the timeout setting (in seconds)
    client_config = {
        'url': url,
        'verbose': False,
        'network_timeout': 1000.0
    }

    with httpclient.InferenceServerClient(**client_config) as client:
        while current_length < max_length:
            # Prepare the input data for Triton
            inputs = [
                httpclient.InferInput("input_ids", input_ids.shape, "INT64")
            ]
            inputs[0].set_data_from_numpy(input_ids, binary_data=False)

            # Send the inference request to the Triton server
            response = client.infer(model_name, inputs, timeout=1000)

            # Extract logits from the response
            logits = response.as_numpy("output")
            
            # Get the last logits array (last word)
            next_token_logits = logits[:, -1, :]
            # Apply softmax and sample the next token
            probs = torch.nn.functional.softmax(torch.tensor(next_token_logits), dim=-1)
            next_token = torch.multinomial(probs, num_samples=1).numpy()

            # Append the sampled token to the generated sequence and prepare the next input
            generated_ids[0].append(next_token[0][0])
            input_ids = np.array([generated_ids[0][-max_length:]])
            current_length += 1
            
            # Break the loop if the end of sentence token is generated
            if next_token[0][0] == tokenizer.eos_token_id:
                break
            print(tokenizer.decode([next_token[0][0]]))
    # Decode the generated IDs to text
    generated_text = tokenizer.decode(generated_ids[0], skip_special_tokens=True)
    return generated_text

# Example usage
prompt = "Genhealth AI is an awesome company that is currently"
result = generate_text_triton(prompt)
print("Generated text:", result)
log_inference(prompt, result)
