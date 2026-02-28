from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from gnews_mpc import mcp as news_mcp_server

import contextlib
from email_mcp import mcp as email_mcp_server


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    # ensure both servers have their session managers running
    async with contextlib.AsyncExitStack() as stack:
        await stack.enter_async_context(news_mcp_server.session_manager.run())
        await stack.enter_async_context(email_mcp_server.session_manager.run())
        yield  # run the app until shutdown


app = FastAPI(lifespan=lifespan)

# CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


#  Mount
app.mount("/news", news_mcp_server.streamable_http_app())
app.mount("/email", email_mcp_server.streamable_http_app())


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000, log_level="debug")