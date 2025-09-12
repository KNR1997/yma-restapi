import uvicorn
from uvicorn.config import LOGGING_CONFIG

if __name__ == "__main__":
    uvicorn.run("yma.main:app", host="0.0.0.0", port=8080, reload=True, log_config=LOGGING_CONFIG)
