from app.pipeline.paper_reader import read_paper
from app.pipeline.paper_chunker import split_into_chunks
from app.pipeline.chunk_analyzer import analyze_chunk


PDF_URL = "https://arxiv.org/pdf/2312.10997"


print("\n--- Reading Paper ---")

paper = read_paper(PDF_URL)

print(
    f"Pages: {paper['page_count']}"
)


print("\n--- Chunking Paper ---")

chunks = split_into_chunks(
    paper["pages"],
    max_chars=12000,
    overlap=1000,
)

print(
    f"Chunks: {len(chunks)}"
)


print("\n--- Analyzing First Chunk ---")

chunk = chunks[0]

print(
    f"Chunk: {chunk.chunk_id}"
)

print(
    f"Pages: {chunk.start_page}-{chunk.end_page}"
)

print(
    f"Characters: {len(chunk.text)}"
)


result = analyze_chunk(chunk)


print("\n--- GEMINI RESULT ---")

print(result)


print("\n--- Chunk Analyzer Test Finished ---")