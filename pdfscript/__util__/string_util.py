import math


def chunk_text(text: str, num_chunks: int = 2):
    tokens = text.split(" ")
    token_range = math.ceil(len(tokens) / num_chunks)

    chunks = []
    for i in range(num_chunks):
        idx1 = token_range * i
        idx2 = token_range * (i + 1)
        chunk = " ".join(tokens[idx1:idx2])
        chunks.append(chunk)

    return chunks
