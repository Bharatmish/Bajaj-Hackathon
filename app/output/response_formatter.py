# app/output/response_formatter.py
def format_final_output(llm_response: dict, query: str):
    return {
        "query": query,
        "decision": llm_response.get("decision", "Unknown"),
        "justification": llm_response.get("justification", ""),
        "clauses_used": llm_response.get("clauses_used", [])
    }
