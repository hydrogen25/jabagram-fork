from fastapi.responses import JSONResponse
import uvicorn
from fastapi import FastAPI,status
from jabagram.database.chats import ChatStorage
from runner import args
from pydantic import BaseModel
class ConnectResponse(BaseModel):
    chat:str
    muc:str

async def start_server(port:int) -> None:
    global chat_storage
    chat_storage = ChatStorage(args.data)

    global app
    app = FastAPI()
    
    uvicorn.run(app=app,port=port)

@app.post("/chat")
async def connect_chats(ConnectResponse:ConnectResponse) -> JSONResponse:
    if ConnectResponse.chat or ConnectResponse.muc is None:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error":"need to provide proper data"}
        )

    if ConnectResponse.chat in chat_storage.get():
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"error":"The Connection has been created"}
        )
    chat_storage.add(ConnectResponse.chat,ConnectResponse.muc)
    return


