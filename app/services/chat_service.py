import datetime
import json

from pydantic import BaseModel
from sqlalchemy import insert, select

from app.db.database import database
from app.db.redis_setup import redis_client
from app.models.message import Message, ChatSession
from app.services.graph_service import GraphService



class ChatService:
    def __init__(self,graphService:GraphService):
        self.graphService = graphService


    async def add_message(self, user_id: int, message: str, response: str, role: str='user'):
        get_session_query = select(ChatSession).where(ChatSession.user_id == user_id).limit(1)
        session_row = await database.fetch_one(get_session_query)

        if session_row:
            session_id = session_row["id"]
        else:
            create_session_query = insert(ChatSession).values(user_id=user_id).returning(ChatSession.id)
            session_id = await database.execute(create_session_query)

        user_query = insert(Message).values(
            user_id=user_id,
            session_id=session_id,
            message=message,
            role="user",
            created_at=datetime.datetime.now()
        )

        ai_query = insert(Message).values(
            user_id=user_id,
            session_id=session_id,
            message=response, 
            role="assistant",
            created_at = datetime.datetime.now()
        )
        await database.execute(user_query)
        await database.execute(ai_query)

    async def generate_response(self, user_id: int, message: str,session_id:str) -> str:
        response_text = ""
        try:
            raw_response = await self.graphService.run(user_id, message,session_id)
            print(f"DEBUG: Response was not JSON: {raw_response}")
            if not raw_response:
                raise ValueError("Received empty response from graph service")

            try:
                response = json.loads(raw_response)
                response_text = response["response"]
            except json.JSONDecodeError:
                print(f"DEBUG: Response was not JSON: {raw_response}")
                response_text = raw_response

            await self.add_message(user_id=user_id, message=message, response=response_text)
        except Exception as e:
            print(f"DEBUG: Chat API error: {e}")
            response_text = "Error generating response"

        key = f"user:{user_id}:recent_messages"
        try:
            await redis_client.rpush(key, message)
            await redis_client.rpush(key, response_text)
            print(f"DEBUG: Successfully pushed to {key}")
        except Exception as e:
            print(f"DEBUG: Redis Cloud Error: {e}")

        return response_text
