import math
from fastapi import Query, HTTPException
from config.database import get_db
import math



def sanitize_nans(obj):
    if isinstance(obj, float) and math.isnan(obj):
        return None
    elif isinstance(obj, dict):
        return {k: sanitize_nans(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [sanitize_nans(i) for i in obj]
    return obj

async def get_total():
    db = get_db()

    total_bolsista = await db["dados_monitoria"].count_documents(
        {"Modalidade": "Bolsista"}
    )

    total_voluntario = await db["dados_monitoria"].count_documents(
        {"Modalidade": "Voluntario"}
    )

    return {
        "totalBolsista": total_bolsista,
        "totalVoluntario": total_voluntario
    }


async def get_periodos(
    page: int = Query(1),
    limit: int = Query(10),
    semestreInicio: float = Query(...),
    semestreFim: float = Query(...),
    curso: str = Query(None),
    departamento: str = Query(None)
):
    db = get_db()

    skip = (page - 1) * limit

    try:
        semestreInicio = float(semestreInicio)
        semestreFim = float(semestreFim)
    except:
        raise HTTPException(
            status_code=400,
            detail="semestreInicio e semestreFim devem ser números"
        )

    filtro = {
        "semestre": {
            "$gte": semestreInicio,
            "$lte": semestreFim
        }
    }

    if curso:
        filtro["Curso"] = curso

    if departamento:
        filtro["Departamento"] = departamento

    total = await db["dados_monitoria"].count_documents(filtro)

    cursor = (
        db["dados_monitoria"]
        .find(filtro, {"_id": 0})
        .skip(skip)
        .limit(limit)
    )

    dados = await cursor.to_list(length=limit)
    dados_limpos = sanitize_nans(dados)

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "totalPages": math.ceil(total / limit) if limit > 0 else 0,
        "data": dados_limpos
    }