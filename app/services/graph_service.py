from typing import TypedDict, List

from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.constants import END

from app.db.redis_setup import get_redis, redis_client
from app.services.llm_service import LlmService
from langgraph.graph import StateGraph, state
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, \
    HumanMessagePromptTemplate
from app.prompts.prompt_assistant import ASSISTANT_PROMPT
from app.db.database import database

llm_service = LlmService()
class GraphState(TypedDict):
    user_id:int
    input:str
    messages:list
    context:str
    response:str

class GraphService:
    def __init__(self):
        self.llm = llm_service
        self.system_prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(ASSISTANT_PROMPT),
        ])
        self.graph = self._build_graph()

    async def load_memory(self, state: GraphState):

        key = f"user:{state['user_id']}:recent_messages"

        messages = []
        redis = await get_redis()

        try:
            recent = await redis
            recent_messages = await recent.lrange(key, 0, -1)
            print(recent_messages)

            for msg in recent_messages:
                messages.append(HumanMessage(content=msg))

        except Exception as e:
            print("Redis error:", e)

        return GraphState(
            user_id=state["user_id"],
            input=state["input"],
            messages=messages,
            context=state["context"],
            response=state["response"]
        )

    async def retrieve_context(self, state: GraphState):

        query = """
           SELECT message
           FROM messages
           WHERE user_id = :user_id
           ORDER BY created_at DESC
           LIMIT 5
           """

        rows = await database.fetch_all(query=query, values={"user_id": state["user_id"]})

        context = "\n".join([row["message"] for row in rows])

        return {**state, "context": context}

    async def call_llm(self, state: GraphState):

        messages = self.system_prompt.format_messages(input=state['context'])


        messages.extend(state["messages"])


        messages.append(HumanMessage(content=state["input"]))

        response = await self.llm.generate_response(messages)

        return {**state, "response": response}

    async def save_memory(self, state: GraphState):

        key = f"user:{state['user_id']}:recent_messages"

        await redis_client.rpush(key, state["input"])
        await redis_client.rpush(key, state["response"])

        await redis_client.ltrim(key, -20, -1)

        return state


    def _build_graph(self):

        builder = StateGraph(GraphState)

        builder.add_node("load_memory", self.load_memory)
        builder.add_node("retrieve_context", self.retrieve_context)
        builder.add_node("call_llm", self.call_llm)
        builder.add_node("save_memory", self.save_memory)

        builder.set_entry_point("load_memory")

        builder.add_edge("load_memory", "retrieve_context")
        builder.add_edge("retrieve_context", "call_llm")
        builder.add_edge("call_llm", "save_memory")
        builder.add_edge("save_memory", END)

        checkpointer = MemorySaver()
        graph = builder.compile(
            checkpointer=checkpointer,
        )
        return graph

    async def run(self, user_id: int, message: str,session_id: str):
        # Evidentrace: one handler per request captures the whole LangGraph
        # run (nodes -> spans, Gemini call -> llm span) and posts the trace
        # for evaluation when the root chain finishes.
        from evidentrace_sdk import get_tracer
        from evidentrace_sdk.integrations.langchain import EvidentCallbackHandler

        handler = EvidentCallbackHandler(
            tracer=get_tracer(),
            user_input=message,
            session_id=session_id,
            user_id=str(user_id),
        )
        config = {
            "configurable": {"thread_id": session_id},
            "callbacks": [handler],
        }
        result = await self.graph.ainvoke({
            "user_id": user_id,
            "input": message,
            "messages": [],
            "context": "",
            "response":"",
            },
            config=config
        )
        print(result)
        return result["response"]




