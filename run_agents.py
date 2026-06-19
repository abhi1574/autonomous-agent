import threading
import sys
import os
import time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents.research_agent import ResearchAgent
from agents.rag_agent      import RAGAgent
from agents.critic_agent   import CriticAgent
from agents.coding_agent   import CodingAgent
from agents.browser_agent  import BrowserAgent
from backend.logger        import get_logger

logger = get_logger("agent.runner")

def run_agent(agent):
    while True:
        try:
            agent.run()
        except Exception as e:
            logger.error(f"Agent {agent.agent_name} crashed: {e}")
            time.sleep(5)  # wait before restart

if __name__ == "__main__":
    agents = [
        ResearchAgent(),
        RAGAgent(),
        CriticAgent(),
        CodingAgent(),
        BrowserAgent(),
    ]

    logger.info("🚀 Starting all agents...")
    threads = []
    for agent in agents:
        t = threading.Thread(target=run_agent, args=(agent,), daemon=True)
        t.start()
        threads.append(t)
        logger.info(f"✅ {agent.agent_name} agent started")

    logger.info("✅ All agents running — waiting for jobs")

    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        logger.info("🛑 Shutting down agents")