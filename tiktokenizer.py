import torch
from transformers import GPT2Model, GPT2Tokenizer

model_name = 'gpt2'
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2Model.from_pretrained(model_name)

# Your text
text = "ChatGPT is amazing"

# Token IDs (simulate what TikToken gives you)
tokens = tokenizer.encode(text, add_special_tokens=False)
token_strings = tokenizer.convert_ids_to_tokens(tokens)

print("Token IDs:", tokens)
print("Token Strings:", token_strings)

# Get embeddings
input_ids = torch.tensor([tokens])
with torch.no_grad():
    outputs = model(input_ids)
    embeddings = outputs.last_hidden_state  # shape: (1, sequence_len, hidden_size)

#print("Embeddings shape:", embeddings.shape)  # e.g., (1, 4, 768)

embeddings = embeddings.squeeze(0)  # shape: (seq_len, hidden_size)

# Print token + first few values of its embedding
for token_str, emb in zip(token_strings, embeddings):
    print(f"Token: {token_str:<10} → Embedding: {emb[:5].tolist()}...")  # show first 5 dims
