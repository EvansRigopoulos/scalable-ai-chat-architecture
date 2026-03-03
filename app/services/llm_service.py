import json
import logging
import os
from typing import List

import httpx
from langchain.messages import HumanMessage
from langchain_core.messages import BaseMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI



class LlmService:
    def __init__(self):
        self.api_key = os.environ.get("GROC_API_KEY")
        self.google_api_key = os.environ.get("GOOGLE_API_KEY")
        self.model = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            max_tokens=None,
            timeout=None,
            max_retries=2,
            api_key=self.google_api_key
        )
        self.api_model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
        self.endpoint = "https://api.groq.com/openai/v1/chat/completions"

        if not self.api_key:
            raise ValueError("GROQ_API_KEY not set in .env")


    async def  generate_response(self,messages:List[BaseMessage]) -> str:
        response_text = ""
        formatted_messages = []


        for message in messages:
            if isinstance(message, HumanMessage):
                formatted_messages.append({
                    "role":"user",
                    "content":message.content,
                })
            elif isinstance(message, SystemMessage):
                formatted_messages.append({
                    "role":"system",
                    "content":message.content,
                })
        try:
            raw_response = self.model.invoke(formatted_messages)
            response = raw_response.model_dump_json()
            response_dict = json.loads(response)
            response_text = response_dict['content']
        except httpx.HTTPError as e:
            print("Error", e)
            logging.error(e)

        return response_text
        async with httpx.AsyncClient() as client:
            print("api key", self.api_key)
            response = await client.post(
                self.endpoint,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.api_model,
                    "messages": [{"role":'user',"content":prompt}],
                    "temperature":0.5,
                    "max_tokens":1024
                },
                timeout=60
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]


