from ninja import NinjaAPI

from backend.crm.api import router as crm_router
from backend.financial.api import router as financial_router
from backend.project.api import router as project_router
from backend.task.api.issue_api import router as issue_router
from backend.task.api.milestone_api import router as milestone_router
from backend.task.api.task_api import router as task_router

api = NinjaAPI(csrf=True)

api.add_router('/crm/', crm_router)
api.add_router('/financial/', financial_router)
api.add_router('/project/', project_router)
api.add_router('/task/', milestone_router)
api.add_router('/task/', issue_router)
api.add_router('/task/', task_router)
