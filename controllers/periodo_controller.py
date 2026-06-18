import math
from fastapi import Query, HTTPException
from config.database import get_db


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
    semestreInicio: float = Query(None),
    semestreFim: float = Query(None),
    curso: str = Query(None),
    departamento: str = Query(None)
):
    if semestreInicio is None or semestreFim is None:
        raise HTTPException(
            status_code=400,
            detail="semestreInicio e semestreFim são obrigatórios"
        )

    db = get_db()
    skip = (page - 1) * limit

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

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "totalPages": math.ceil(total / limit) if limit > 0 else 0,
        "data": dados
    }