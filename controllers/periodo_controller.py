import math
from fastapi import Query, HTTPException
from config.database import get_db


def sanitize_nans(obj):
    if isinstance(obj, float) and math.isnan(obj):
        return None
    elif isinstance(obj, dict):
        return {k: sanitize_nans(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [sanitize_nans(i) for i in obj]
    return obj


async def get_periodos(
    semestreInicio: float | None = Query(None),
    semestreFim: float | None = Query(None),
    curso: str | None = Query(None),
    departamento: str | None = Query(None)
):
    db = get_db()
    collection = db["dados_monitoria"]

    filtro = {}

    menor_doc = await collection.find_one(
        {"semestre": {"$ne": None}},
        sort=[("semestre", 1)],
        projection={"_id": 0, "semestre": 1}
    )

    maior_doc = await collection.find_one(
        {"semestre": {"$ne": None}},
        sort=[("semestre", -1)],
        projection={"_id": 0, "semestre": 1}
    )

    if not menor_doc or not maior_doc:
        raise HTTPException(
            status_code=404,
            detail="Não há semestres cadastrados no banco."
        )

    menor_semestre = menor_doc["semestre"]
    maior_semestre = maior_doc["semestre"]

    
    if semestreInicio is not None and semestreFim is not None:
        
        if semestreInicio > semestreFim:
            raise HTTPException(
                status_code=400,
                detail="semestreInicio não pode ser maior que semestreFim."
            )

        filtro["semestre"] = {
            "$gte": semestreInicio,
            "$lte": semestreFim
        }

    elif semestreInicio is not None and semestreFim is None:
        
        filtro["semestre"] = {
            "$gte": semestreInicio,
            "$lte": maior_semestre
        }

    elif semestreInicio is None and semestreFim is not None:
        
        filtro["semestre"] = {
            "$gte": menor_semestre,
            "$lte": semestreFim
        }

    if curso:
        lista_cursos = [c.strip() for c in curso.split(",") if c.strip()]
        if lista_cursos:
            filtro["Curso"] = {"$in": lista_cursos}

    if departamento:
        lista_departamentos = [d.strip() for d in departamento.split(",") if d.strip()]
        if lista_departamentos:
            filtro["Departamento"] = {"$in": lista_departamentos}

    
    filtro_bolsista = {**filtro, "Modalidade": "Bolsista"}
    filtro_voluntario = {**filtro, "Modalidade": "Voluntario"}

    total_bolsista_periodo = await collection.count_documents(filtro_bolsista)
    total_voluntario_periodo = await collection.count_documents(filtro_voluntario)
    total = total_bolsista_periodo + total_voluntario_periodo


    cursor = collection.find(filtro, {"_id": 0})
    dados = await cursor.to_list(length=None)
    dados_limpos = sanitize_nans(dados)

    return {
        "filtroAplicado": filtro,
        "intervaloUsado": {
            "semestreInicio": filtro.get("semestre", {}).get("$gte"),
            "semestreFim": filtro.get("semestre", {}).get("$lte"),
        },
        "total_por_semestre_selecionado": total,
        "totalBolsistaPeriodo": total_bolsista_periodo,
        "totalVoluntarioPeriodo": total_voluntario_periodo,
        "quantidadeRegistros": len(dados_limpos),
        "data": dados_limpos
    }

# import math
# from fastapi import Query, HTTPException
# from config.database import get_db

# def sanitize_nans(obj):
#     if isinstance(obj, float) and math.isnan(obj):
#         return None
#     elif isinstance(obj, dict):
#         return {k: sanitize_nans(v) for k, v in obj.items()}
#     elif isinstance(obj, list):
#         return [sanitize_nans(i) for i in obj]
#     return obj


# async def get_all_dados():
#     db = get_db()

#     total_bolsista = await db["dados_monitoria"].count_documents({"Modalidade": "Bolsista"})
#     total_voluntario = await db["dados_monitoria"].count_documents({"Modalidade": "Voluntario"})
#     total_geral = total_bolsista + total_voluntario

#     cursor = db["dados_monitoria"].find({}, {"_id": 0})

#     dados = await cursor.to_list(length=None)
#     dados_limpos = sanitize_nans(dados)

#     return {
#         "totalGeral": total_geral,
#         "totalBolsista": total_bolsista,     
#         "totalVoluntario": total_voluntario, 
#         "data": dados_limpos
#     }

# async def get_total():
#     db = get_db()

#     total_bolsista = await db["dados_monitoria"].count_documents(
#         {"Modalidade": "Bolsista"}
#     )

#     total_voluntario = await db["dados_monitoria"].count_documents(
#         {"Modalidade": "Voluntario"}
#     )

#     return {
#         "totalBolsista": total_bolsista,
#         "totalVoluntario": total_voluntario
#     }


# async def get_periodos(
#     # page: int = Query(1),
#     # limit: int = Query(10),
#     semestreInicio: float = Query(...),
#     semestreFim: float = Query(...),
#     curso: str = Query(None),
#     departamento: str = Query(None)
# ):
#     db = get_db()

#     # skip = (page - 1) * limit

#     try:
#         semestreInicio = float(semestreInicio)
#         semestreFim = float(semestreFim)
#     except:
#         raise HTTPException(
#             status_code=400,
#             detail="semestreInicio e semestreFim devem ser números"
#         )

#     filtro = {
#         "semestre": {
#             "$gte": semestreInicio,
#             "$lte": semestreFim
#         }
#     }

#     if curso:
#         lista_cursos = [c.strip() for c in curso.split(",")]
#         filtro["Curso"] = {"$in": lista_cursos}


#     if departamento:
   
#         lista_departamentos = [d.strip() for d in departamento.split(",")]
        
#         # # Limita a 3 departamentos
#         # if len(lista_departamentos) > 3:
#         #     raise HTTPException(
#         #         status_code=400,
#         #         detail="Você pode filtrar por no máximo 3 departamentos simultaneamente."
#         #     )
            

#         filtro["Departamento"] = {"$in": lista_departamentos}

#     filtro_bolsista = {**filtro, "Modalidade": "Bolsista"}
#     filtro_voluntario = {**filtro, "Modalidade": "Voluntario"}
    
#     total_bolsista_periodo = await db["dados_monitoria"].count_documents(filtro_bolsista)
#     total_voluntario_periodo = await db["dados_monitoria"].count_documents(filtro_voluntario)
  
#     total = total_bolsista_periodo + total_voluntario_periodo

#     cursor = (
#         db["dados_monitoria"]
#         .find(filtro, {"_id": 0})
#         # .skip(skip)
#         # .limit(limit)
#     )

#     # dados = await cursor.to_list(length=limit)
#     dados = await cursor.to_list(length=None)
#     dados_limpos = sanitize_nans(dados)

#     return {
#         "total_por_semestre_selecionado": total,
#         # "page": page,
#         # "limit": limit,
#         # "totalPages": math.ceil(total / limit) if limit > 0 else 0,
#         "totalBolsistaPeriodo": total_bolsista_periodo,     
#         "totalVoluntarioPeriodo": total_voluntario_periodo, 
#         "quantidadeRegistros": len(dados_limpos),
#         "data": dados_limpos
#     }