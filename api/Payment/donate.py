from fastapi import Depends,File, UploadFile, APIRouter,Request
from fastapi.templating import Jinja2Templates
import uuid, datetime
from app.talent.database import SessionLocal, engine, database
from starlette.responses import RedirectResponse
import razorpay
from fastapi.responses import HTMLResponse
#from app.authentication import schemas
from api.user import models
router = APIRouter()

templates = Jinja2Templates(directory="templates")
from random import randint
import pandas as pd

@router.get("/pay/{id}/")#,response_class=HTMLResponse)
async def pay_me(request: Request, id:str):
    #pay = models.Payment.__table__.select(models.Payment.amount).where(models.Payment.id==id)
    
    pay =  "SELECT courses.price FROM courses WHERE courses.id ="+str(id)
    #pay1 =  "SELECT courses.name FROM courses WHERE courses.id ="+str(id)
    pay1 = Course.__table__.select(models.Course.name).where(models.Course.id==id)
    result = await database.execute(pay)
    database.execute(pay1)
    print(pay)
    gid = randint(100000,1000000)
    rec = ("paycd"+str(gid))
    
    print(rec)
    gdate = datetime.datetime.now()
    #print(pay.amount)
    df= pd.read_sql(pay,engine)
    # any = models.Payment.amount
    #print(result)
    print(pay1)
    client = razorpay.Client(auth=("rzp_test_cfbr43uRZAs35w","dcPlBgM8Fv7H2J1cYISFKC81"))
    payment = client.order.create({'amount' : int(df.price.values)*100, 'currency':'INR', 'receipt': "paycd"+str(gid),'payment_capture':'1'})
    print(payment)
    query = Payment.__table__.insert().values(
        id = str(gid),
        pay_id = payment['id'],
        amount = str(payment['amount']),
        currency = payment['currency'],
        receipt = payment['receipt'],
        status = payment['status'],
        pay_createdat = str(payment['created_at']),
        created_date = gdate,)
        # client_id=str('65f8d1e7-82fa-11eb-9a8a-18c04d4a628c)',
        # course_id = id)
    await database.execute(query)
    #return {**payment}
    return templates.TemplateResponse("pay.html", {"request": request, "payment":payment})
@router.get("/payments")
async def get_payment():
    client = razorpay.Client(auth=("rzp_test_cfbr43uRZAs35w", "dcPlBgM8Fv7H2J1cYISFKC81"))
    count = 2
    skip = 1

    resp = client.order.fetch_all()
    return resp
# Get Payment Id client = razorpay.Client(auth=("rzp_test_cfbr43uRZAs35w", "dcPlBgM8Fv7H2J1cYISFKC81")
@router.get("/payments/:id")
async def get_payment_by_id(request: Request, order_id:str):
    
    client = razorpay.Client(auth=("rzp_test_cfbr43uRZAs35w", "dcPlBgM8Fv7H2J1cYISFKC81"))

    order_id = order_id

    resp = client.order.fetch(order_id)
    return resp
@router.get("/payments/:id/payments")
async def get_all_payment_by_id(request: Request, order_id:str):
    
    client = razorpay.Client(auth=("rzp_test_cfbr43uRZAs35w", "dcPlBgM8Fv7H2J1cYISFKC81"))

    order_id = order_id

    resp = client.order.fetch(order_id)
    return resp
@router.get("/success/")
async def success(request: Request):
    return templates.TemplateResponse("success.html", {"request": request})

@router.post("/success/")
async def success(request: Request):
    return templates.TemplateResponse("success.html", {"request": request})