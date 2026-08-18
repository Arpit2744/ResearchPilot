from app.pipeline.paper_search import search_papers


result = search_papers(
    "retrieval augmented generation",
    max_results=5,
)

print(f"\nFound {result['count']} papers\n")

for i, paper in enumerate(result["papers"], 1):
    print(f"{i}. {paper['title']}")
    print(f"   Year: {paper['year']}")
    print(f"   Authors: {', '.join(paper['authors'][:5])}")
    print(f"   DOI: {paper['doi']}")
    print(f"   URL: {paper['url']}")
    print()