from fastapi import APIRouter
from controllers.periodo_controller import get_periodos, get_total

router = APIRouter()

router.get("")(get_periodos)
router.get("/total")(get_total)