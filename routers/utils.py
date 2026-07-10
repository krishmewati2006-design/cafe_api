from fastapi import APIRouter, HTTPException
import httpx

router = APIRouter()

@router.get("/exchange-rate/{base_currency}")
async def get_exchange_rate(base_currency: str):
    url = f"https://api.exchangerate.fun/latest?base={base_currency.upper()}"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status() # Raise exception for http error
            return response.json()
    except httpx.RequestError as exc:
            raise HTTPException(status_code=503, detail=f"An error occurred while requesting.{str(exc)}")
    except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=503, detail=f"Error response {exc.response.status_code} while requesting {exc.request.url}.")


