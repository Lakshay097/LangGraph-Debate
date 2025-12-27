import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI 

load_dotenv()

def build_llm(seed=None):
    return ChatOpenAI(
        model= "openai/gpt-oss-120b",
        api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1",
        temperature=0.3,
        seed=seed,
    )
