from fastapi import APIRouter
from controllers.periodo_controller import get_periodos, get_total, get_all_dados

router = APIRouter()

router.get("")(get_periodos)
router.get("/total")(get_total)
router.get("/all")(get_all_dados)