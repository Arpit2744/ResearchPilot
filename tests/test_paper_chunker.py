from app.pipeline.paper_reader import read_paper
from app.pipeline.paper_chunker import split_into_chunks


PDF_URL = "https://arxiv.org/pdf/2312.10997"


print("\n--- Reading Paper ---")

paper = read_paper(PDF_URL)

print(f"Pages: {paper['page_count']}")
print(f"Characters: {len(paper['text'])}")


print("\n--- Chunking Paper ---")

chunks = split_into_chunks(
    paper["pages"],
    max_chars=12000,
    overlap=1000,
)


print(f"Number of chunks: {len(chunks)}")


print("\n--- Chunk Information ---")

for chunk in chunks:

    print(
        f"{chunk.chunk_id} | "
        f"section={chunk.section} | "
        f"pages={chunk.start_page}-{chunk.end_page} | "
        f"characters={len(chunk.text)}"
    )


print("\n--- First Chunk Preview ---")

print(chunks[0].text[:1500])


print("\n--- Chunker Test Finished ---")