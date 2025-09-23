# main.py
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import httpx
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="OpenAI Proxy Service", version="1.0.1")

OPENAI_API_URL = "https://api.openai.com/v1"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("Переменная окружения OPENAI_API_KEY не установлена!")

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def proxy_openai(request: Request, path: str):
    if request.method == "OPTIONS":
        return JSONResponse(content={}, headers={"Access-Control-Allow-Origin": "*", "Access-Control-Allow-Methods": "*", "Access-Control-Allow-Headers": "*"})

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": request.headers.get("Content-Type", "application/json"),
    }
    
    target_url = f"{OPENAI_API_URL}/{path}"
    body = await request.body()
    
    logger.info(f"Проксирую {request.method} запрос на {target_url}")

    async with httpx.AsyncClient(timeout=120.0) as client:
        try:
            response = await client.request(
                method=request.method,
                url=target_url,
                headers=headers,
                content=body,
                params=request.query_params
            )
            response.raise_for_status() # Вызовет исключение для статусов 4xx/5xx
            
            logger.info(f"Ответ от OpenAI: {response.status_code}")
            return JSONResponse(content=response.json(), status_code=response.status_code)

        except httpx.HTTPStatusError as e:
            logger.error(f"Ошибка от OpenAI: {e.response.status_code} - {e.response.text[:500]}")
            return JSONResponse(content={"error": e.response.json()}, status_code=e.response.status_code)
        except httpx.RequestError as e:
            logger.error(f"Ошибка запроса к OpenAI: {e}")
            raise HTTPException(status_code=502, detail="Bad Gateway: не удалось связаться с OpenAI")
        except Exception as e:
            logger.error(f"Неожиданная ошибка: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "OpenAI Proxy"}