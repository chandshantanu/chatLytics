import asyncio
from datetime import datetime
from telegram_module import TelegramModule
from llm_module import LLMModule
from database_module import DatabaseModule
from web_interface import app
import uvicorn

class MainApplication:
    def __init__(self):
        self.telegram_module = TelegramModule()
        self.llm_module = LLMModule()
        self.db_module = DatabaseModule()

    async def analyze_chat(self, group_id, start_date, query):
        await self.telegram_module.start()
        messages = await self.telegram_module.get_messages(group_id, start_date)
        self.db_module.store_chat(group_id, messages)
        
        # For this example, we'll use OpenAI. You can easily switch to Claude or local LLama.
        result = await self.llm_module.analyze_with_openai(messages, query)
        
        self.db_module.store_analysis(query, result)
        await self.telegram_module.close()
        return result

# Create a global instance of MainApplication
main_app = MainApplication()

# Update the FastAPI route to use MainApplication
@app.post("/analyze", response_model=ChatResponse)
async def analyze_chat(request: ChatRequest, current_user: str = Depends(get_current_user)):
    try:
        start_date = datetime.strptime(request.start_date, "%Y-%m-%d")
        result = await main_app.analyze_chat(request.group_id, start_date, request.query)
        return ChatResponse(result=result)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)