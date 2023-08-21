import uvicorn

import settings

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=settings.get().API_PORT,
                reload=True,
                timeout_keep_alive=120)
