def clause_semantic_match(query: str, chunks: list) -> dict:
    best_chunk = chunks[0]
    return {
        "clause": best_chunk['metadata']['text'],
        "page": best_chunk['metadata'].get('page', 'Unknown')
    }
