from memory.vector_store import VectorStore

class VectorSearchTool:
    name        = "vector_search"
    description = "Search Qdrant vector store for relevant past memories"

    def __init__(self):
        self.store = VectorStore()

    def run(self, input: dict) -> str:
        query     = input.get("query", "")
        limit     = input.get("limit", 5)
        filter_by = input.get("filter_by", None)
        vector    = input.get("vector")  # caller must pass real vector

        if not vector:
            return "❌ No vector provided — use router.embed() before calling vector_search"

        results = self.store.search(
            vector   = vector,
            limit    = limit,
            filter_by= filter_by
        )

        if not results:
            return "No relevant memories found in knowledge base"

        output = f"Found {len(results)} relevant memories:\n\n"
        for i, r in enumerate(results, 1):
            output += f"{i}. Score: {r['score']:.3f}\n"
            output += f"   Agent: {r['metadata'].get('agent', 'unknown')}\n"
            output += f"   {r.get('text', '')[:300]}\n\n"

        return output