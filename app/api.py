import pandas as pd
import plotly.express as px
from datetime import datetime
from fastapi import APIRouter, Request, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse

from app.model import Data
from app.database import session
from app.schema import DataCreate

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def read_data(request: Request, framework: str = None, type: str = None, date: str = None, operation: str = None, specification: str = None):
    with session() as db:
        query = db.query(Data)
        if type:
            query = query.filter(Data.type == type)
        if date:
            query = query.filter(Data.created_at >= datetime.strptime(date, "%Y-%m-%d"))
        if framework:
            query = query.filter(Data.framework.in_(framework.split(",")))
        if specification:
            query = query.filter(Data.specification == specification)

        data_entries = query.all()
        records = [{
            "framework": entry.framework,
            "operation": res['name'],
            "value": float(res['value'])
        } for entry in data_entries for res in entry.result if not operation or res['name'] == operation]

        df = pd.DataFrame(records if records else [{"framework_name": "", "operation": "", "value": 0.0}])
        fig = px.bar(df, x="framework_name", y="value", color="operation", title=f"Performance Metrics: {type} Type", orientation='v', barmode='group')
        graph_html = fig.to_html(full_html=False)
        context = {"request": request, "graph_html": graph_html}
    return templates.TemplateResponse("index.html", context)

@router.get("/frameworks", response_class=JSONResponse)
async def get_frameworks():
    with session() as db:
        frameworks = db.query(Data.framework_name).distinct().all()
        return [framework[0] for framework in frameworks]

@router.get("/types", response_class=JSONResponse)
async def get_types():
    with session() as db:
        types = db.query(Data.type).distinct().all()
        return [data_type[0] for data_type in types]

@router.post("/", response_class=JSONResponse, status_code=status.HTTP_201_CREATED)
async def create_data(data: DataCreate):
    with session() as db:
        new_data = Data(
            type=data.type,
            framework_name=data.framework_name,
            specification=data.specification,
            result=[{'name': item.name, 'value': item.value} for item in data.result],
            created_at=data.created_at or datetime.utcnow()
        )
        db.add(new_data)
        db.commit()
        db.refresh(new_data)
        return {"message": "Data created successfully", "data_id": new_data.id}
