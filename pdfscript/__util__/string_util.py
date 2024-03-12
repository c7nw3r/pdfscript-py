import math

from pdfscript.__spi__.protocols import PDFOpset
from pdfscript.__spi__.styles import TextStyle
from pdfscript.__spi__.types import PDFPosition, TextChunk


def chunk_text(text: str, num_chunks: int):
    tokens = text.split(" ")
    token_range = math.ceil(len(tokens) / num_chunks)

    chunks = []
    for i in range(num_chunks):
        idx1 = token_range * i
        idx2 = token_range * (i + 1)
        chunk = " ".join(tokens[idx1:idx2])
        chunks.append(chunk)

    return chunks


def split_text_by_height(ops: PDFOpset, style: TextStyle, pos: PDFPosition, text: str, num_cols: int = 1):
    chunk_width = (pos.max_x - pos.x) / num_cols - style.gap
    chunks = chunk_text(text, num_cols)

    available_height = pos.y - pos.min_y
    necessary_height = max([ops.get_height_of_text(e, style, chunk_width) for e in chunks])

    if available_height > necessary_height:
        return [TextChunk(text, necessary_height)]
    if available_height <= 0:
        return [TextChunk(text, necessary_height)]

    chunk_height = necessary_height
    all_tokens = text.split(" ")
    tokens = text.split(" ")

    split_pos = None
    while chunk_height > available_height:
        # TODO: make more performant
        split_pos = len(tokens) - 1
        tokens = tokens[:split_pos]
        chunk = " ".join(tokens)

        chunks = chunk_text(chunk, num_cols)
        chunk_height = max([ops.get_height_of_text(e, style, chunk_width) for e in chunks])

    if split_pos is None:
        return [TextChunk(text, necessary_height)]
    elif split_pos <= 0:
        return [TextChunk(text, chunk_height)]
    return [
        TextChunk(" ".join(all_tokens[:split_pos]), chunk_height),
        *split_text_by_height(ops, style, pos, " ".join(all_tokens[split_pos:]), num_cols)
    ]
