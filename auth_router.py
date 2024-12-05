from dependency import APIRouter, Request, Form, Depends, Response, Annotated, Session, bcrypt, jwt, Jinja2Templates, Cookie, RedirectResponse
from db import get_db
import models

auth_router = APIRouter()
templates = Jinja2Templates(directory="static")

@auth_router.get("/login")
async def login(request: Request, response: Response, token: str = Cookie(None)):
    try:
        jwt.decode(token, "secret", algorithms=["HS256"])["email"]
        return RedirectResponse("/")
    except Exception as e:
        return templates.TemplateResponse("templates/login.html", {"request": request})

@auth_router.get("/register")
async def register(request: Request, response: Response, token: str = Cookie(None)):
    try:
        jwt.decode(token, "secret", algorithms=["HS256"])["email"]
        return RedirectResponse("/")
    except Exception as e:
        return templates.TemplateResponse("templates/register.html", {"request": request})
    

@auth_router.post("/login")
async def login_submit(request: Request, response: Response, email: Annotated[str, Form()], password: Annotated[str, Form()], db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == email).first()
    if db_user is None:
        return templates.TemplateResponse("templates/errors.html", {"request": request, "errors": ["User does not exist"]})
    
    if not bcrypt.checkpw(password.encode('utf-8'), db_user.password.encode('utf-8')):
        return templates.TemplateResponse("templates/errors.html", {"request": request, "errors": ["Incorrect password"]})
    
    token = jwt.encode({"email": email}, "secret", algorithm="HS256")
    
    response.set_cookie(key="token", value=token)
    response.headers['HX-Redirect'] = '/'
    return "Success";
    

@auth_router.post("/register")
async def register_submit(request: Request, response: Response, email: Annotated[str, Form()], password: Annotated[str, Form()], confirmPassword: Annotated[str, Form()], db: Session = Depends(get_db)):
    hashedPassword = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    if password != confirmPassword:
        return templates.TemplateResponse("templates/errors.html", {"request": request, "errors": ["Passwords do not match"]})
    
    db.add(models.User(email=email, password=hashedPassword.decode('utf-8')))
    db.commit()
    response.headers['HX-Redirect'] = '/auth/login'

    return {"email": email, "password": password, "confirmPassword": confirmPassword}

@auth_router.get("/logout")
async def logout(response: Response):
    response.delete_cookie("token")
    response.headers['HX-Redirect'] = '/auth/login'
    return "Success"