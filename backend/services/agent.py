import json
import logging
from typing import List, Dict, Any, Optional

from backend.config import settings
from backend.services.graph_tools import ALL_TOOLS, run_tool

logger = logging.getLogger(__name__)

LOISEKK_SYSTEM_PROMPT = """You are Loisekk AI — an intelligent assistant for the Second Brain knowledge graph.

You have access to the following tools:
{}

When you need to query the graph, respond with a tool call in this format:
<tool>tool_name(param1="value1", param2="value2")</tool>

Available tools:
- get_node(node_id: str) — get full details of a code entity by ID
- search_nodes(query: str, limit: int=10) — search nodes by name/label
- get_neighbors(node_id: str, depth: int=1) — explore relationships
- find_path(source: str, target: str) — find connections between entities
- community(community_id: str, limit: int=50) — list nodes in a community
- project(name: str, limit: int=50) — list nodes in a project
- stats() — get overall knowledge graph statistics

Follow these rules:
1. Always use tools to verify information before answering
2. For project/code questions, search and explore the graph
3. If unsure, be honest and suggest what the user could try
4. Keep answers concise and informative"""


class AgentService:
    def __init__(self):
        tools_desc = "\n".join(
            f"  - {name}: {info['description']}"
            for name, info in ALL_TOOLS.items()
        )
        self.system_prompt = LOISEKK_SYSTEM_PROMPT.format(tools_desc)
        self.llm = None
        self._init_llm()

    def _init_llm(self) -> None:
        provider = settings.llm_provider
        api_key = settings.openai_api_key if provider == "openai" else settings.groq_api_key
        if not api_key:
            logger.warning("No LLM API key configured, agent will use tool-only mode")
            return
        try:
            if provider == "groq":
                from langchain_groq import ChatGroq
                self.llm = ChatGroq(model=settings.llm_model, api_key=api_key, temperature=0.3)
            elif provider == "openai":
                from langchain_openai import ChatOpenAI
                self.llm = ChatOpenAI(model=settings.llm_model or "gpt-4o", api_key=api_key, temperature=0.3)
            logger.info(f"Initialized LLM: {provider}/{settings.llm_model}")
        except Exception as e:
            logger.warning(f"Failed to initialize LLM: {e}")

    def _parse_tool_call(self, text: str) -> Optional[tuple]:
        import re
        match = re.search(r"<tool>(\w+)\(([^)]*)\)</tool>", text)
        if not match:
            return None
        name = match.group(1)
        params_str = match.group(2).strip()
        params = {}
        if params_str:
            for pair in params_str.split(","):
                pair = pair.strip()
                if "=" in pair:
                    key, val = pair.split("=", 1)
                    key = key.strip()
                    val = val.strip().strip('"').strip("'")
                    params[key] = val
        return name, params

    async def chat(self, message: str, history: List[Dict[str, str]]) -> str:
        if not self.llm:
            return self._tool_only_response(message)
        return await self._llm_response(message, history)

    def _tool_only_response(self, message: str) -> str:
        msg = message.lower()
        if "stat" in msg or "how many" in msg or "count" in msg:
            return run_tool("stats")
        if "project" in msg:
            import re
            m = re.search(r"project\s+['\"]?(\w[\w\s-]*)['\"]?", msg)
            if m:
                return run_tool("project", name=m.group(1).strip())
            return run_tool("stats")
        if "community" in msg:
            import re
            m = re.search(r"community\s+['\"]?(\w[\w\s-]*)['\"]?", msg)
            if m:
                return run_tool("community", community_id=m.group(1).strip())
            return run_tool("stats")
        if "neighbor" in msg or "connected" in msg or "related" in msg:
            import re
            m = re.search(r"['\"]?(\w[\w\-\.]+)['\"]?", msg)
            if m:
                return run_tool("get_neighbors", node_id=m.group(1))
        return (
            "I can help you explore the knowledge graph! Try asking:\n"
            "- Show me knowledge graph statistics\n"
            "- Find nodes related to 'config'\n"
            "- What's in project 'backend'?\n"
            "- Search for 'database'"
        )

    async def _llm_response(self, message: str, history: List[Dict[str, str]]) -> str:
        from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

        messages = [SystemMessage(content=self.system_prompt)]
        for h in history[-10:]:
            role = h.get("role", "")
            content = h.get("content", "")
            if role == "user":
                messages.append(HumanMessage(content=content))
            elif role == "assistant":
                messages.append(AIMessage(content=content))
        messages.append(HumanMessage(content=message))

        try:
            result = await self.llm.ainvoke(messages)
            response = result.content

            parsed = self._parse_tool_call(response)
            if parsed:
                tool_name, tool_params = parsed
                tool_result = run_tool(tool_name, **tool_params)
                messages.append(AIMessage(content=response))
                messages.append(HumanMessage(content=f"Tool result: {tool_result}\n\nBased on this, answer the user's question concisely."))
                final = await self.llm.ainvoke(messages)
                return final.content

            return response
        except Exception as e:
            logger.error(f"LLM error: {e}")
            return f"I encountered an error. Please try again or rephrase your question. (Error: {type(e).__name__})"


agent_service = AgentService()
