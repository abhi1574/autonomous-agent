import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tools.router import ToolRouter

router = ToolRouter()

print("\n--- Available Tools ---")
for tool in router.list_tools():
    print(f"  {tool['name']}: {tool['description']}")

print("\n--- Testing web_search ---")
result = router.run(
    tool_name  = "web_search",
    input      = {"query": "AI agent frameworks 2025", "max_results": 2},
    agent_name = "research",
    task_id    = "test-task-001"
)
print(result[:400])

print("\n--- Testing llm ---")
result = router.run(
    tool_name  = "llm",
    input      = {"prompt": "What is an AI agent in one sentence?"},
    agent_name = "critic",
    task_id    = "test-task-001"
)
print(result)

print("\n--- Testing code_executor ---")
result = router.run(
    tool_name  = "code_executor",
    input      = {"code": "print('Hello from Tool Router!')"},
    agent_name = "coding",
    task_id    = "test-task-001"
)
print(result)

print("\n--- Testing vector_search ---")
query_vector = router.embed("AI agent frameworks")  # generate real vector first
result = router.run(
    tool_name  = "vector_search",
    input      = {
        "query" : "AI agent frameworks",
        "vector": query_vector,          # pass real vector
        "limit" : 3
    },
    agent_name = "rag",
    task_id    = "test-task-001"
)
print(result[:400])