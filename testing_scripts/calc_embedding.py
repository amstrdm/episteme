from sentence_transformers import SentenceTransformer
import numpy as np

text = "shelf life is longer"
model = "all-MiniLM-L6-v2"

st = SentenceTransformer(model)

emb = np.array(st.encode(text)).tolist()


print(emb)