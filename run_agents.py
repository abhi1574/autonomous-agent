import threading
import sys
import os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents.research_agent import ResearchAgent
from agents.rag_agent      import RAGAgent
from agents.critic_agent   import CriticAgent
from agents.coding_agent   import CodingAgent
from agents.browser_agent  import BrowserAgent

def run_agent(agent):
    try:
        agent.run()
    except Exception as e:
        print(f"Agent {agent.agent_name} crashed: {e}")
        time.sleep(1)

if __name__ == "__main__":
    agents = [
        ResearchAgent(),
        RAGAgent(),
        CriticAgent(),
        CodingAgent(),
        BrowserAgent(),
    ]

    print("🚀 Starting all agents...")
    threads = []
    for agent in agents:
        t = threading.Thread(target=run_agent, args=(agent,), daemon=True)
        t.start()
        threads.append(t)
        print(f"✅ {agent.agent_name} agent started")

    print("✅ All agents running — waiting for jobs from Redis queue")
    print("Press Ctrl+C to stop")

    try:
        for t in threads:
            t.join()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down agents")