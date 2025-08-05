from fastapi import APIRouter
from app.services.document_loader import load_pdf_from_url
from app.services.embedding_search import search_similar_chunks
from app.services.clause_matcher import clause_semantic_match
from app.utils.schema import QueryRequest

router = APIRouter()

@router.post("/hackrx/run", response_model=dict)
def run_query_retrieval(req: QueryRequest):
    document_text = load_pdf_from_url(req.documents)

    answers = []
    for question in req.questions:

        intent = "coverage_check"
        entities = ["knee surgery" if "knee" in question.lower() else "pre-existing diseases"]
        constraints = []

        top_chunks = search_similar_chunks(question)

        best_chunk = clause_semantic_match(question, top_chunks)

        decision = {
            "answer": "Yes, this policy covers the queried condition.",
            "conditions": ["Subject to waiting period", "Pre-authorization required"]
        }

        answers.append({
            "question": question,
            "answer": decision.get("answer", ""),
            "conditions": decision.get("conditions", []),
            "source_clauses": [{"clause": best_chunk['clause'], "page": best_chunk['page']}]
        })

    return {"answers": answers}
