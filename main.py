from dependency import FastAPI, Request, Cookie, StaticFiles, Jinja2Templates, jwt, websockets, WebSocket, WebSocketDisconnect
from datetime import datetime 
from auth_router import auth_router

templates = Jinja2Templates(directory="static")

app = FastAPI()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()



app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(auth_router, prefix="/auth", tags=["auth"])

@app.get("/")
async def root(request: Request, token: str = Cookie(None)):
    try:
        email = jwt.decode(token, "secret", algorithms=["HS256"])["email"]
        if email is None:
            return templates.TemplateResponse("index.html", {"request": request})
        
        return templates.TemplateResponse("templates/auth.html", {"request": request, "email": email})
    
    except Exception as e:
        return templates.TemplateResponse("index.html", {"request": request})
    
@app.get("/about") 
async def about(request: Request):
    return templates.TemplateResponse("templates/about.html", {"request": request})

@app.get("/home")
async def home(request: Request):
    return templates.TemplateResponse("templates/home.html", {"request": request})

@app.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket, token: str = Cookie(None)):
    email = jwt.decode(token, "secret", algorithms=["HS256"])["email"]
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            message = templates.get_template("templates/message.html").render({"message": data.get("message"), "email": email, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")});
            await manager.broadcast(message)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8080)