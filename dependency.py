from fastapi import FastAPI, Request, Form, Depends, Response, Cookie, WebSocket, WebSocketDisconnect
from fastapi.routing import APIRouter
from fastapi.responses import RedirectResponse
from typing import Annotated
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Annotated
from models import User, SessionLocal, engine
from sqlalchemy.orm import Session
import uvicorn
import models, schema
import bcrypt
import jwt
import websockets