"""
AutoFlow AI - Jobs Router
Endpoints para crear y consultar trabajos de automatización
"""

import asyncio
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from database import get_db
from models.job import Job, JobStatus
from schemas.job import JobCreate, JobResponse, JobRunResponse
from services.job_executor import execute_job

router = APIRouter(
    prefix="/api/jobs",
    tags=["jobs"],
    responses={404: {"description": "Not found"}}
)


@router.post(
    "/run",
    response_model=JobRunResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear y ejecutar un nuevo job",
    description="Crea un nuevo job de automatización. Devuelve el ID para consultar el estado."
)
async def run_job(
    request: JobCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Endpoint para crear un nuevo job de automatización
    
    - **instruction**: Instrucción en lenguaje natural (min 10, max 5000 caracteres)
    
    El job se ejecuta en background. Retorna el ID para consultar su estado con GET /status/{job_id}
    """
    
    # Crear nuevo job
    job = Job(
        instruction=request.instruction,
        status=JobStatus.PENDING
    )
    
    # Guardar en BD
    db.add(job)
    await db.commit()
    await db.refresh(job)
    
    job_id = job.id
    
    # Iniciar ejecución en background
    # Ejecutar sin await (la función inicia un thread internamente)
    asyncio.create_task(execute_job(job_id))
    
    return JobRunResponse(
        job_id=job_id,
        status=JobStatus.PENDING,
        message=f"Job creado exitosamente. Accede a /status/{job_id} para ver el progreso"
    )


@router.get(
    "/status/{job_id}",
    response_model=JobResponse,
    summary="Consultar estado de un job",
    description="Obtiene el estado actual, progreso y resultados de un job."
)
async def get_job_status(
    job_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Endpoint para consultar el estado de un job
    
    - **job_id**: UUID del job a consultar
    
    Retorna toda la información del job incluyendo estado, logs y resultados.
    """
    
    # Buscar el job
    result = await db.execute(select(Job).where(Job.id == job_id))
    job = result.scalar_one_or_none()
    
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job con ID {job_id} no encontrado"
        )
    
    return JobResponse.model_validate(job)


@router.get(
    "/",
    response_model=list[JobResponse],
    summary="Listar todos los jobs",
    description="Obtiene la lista de todos los jobs creados (limitado a 100)."
)
async def list_jobs(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """
    Endpoint para listar todos los jobs
    
    - **skip**: Número de registros a saltar (para paginación)
    - **limit**: Máximo número de registros a retornar (default 100)
    
    Retorna una lista de jobs ordenada por fecha de creación descendente.
    """
    
    # Consultar jobs con paginación
    result = await db.execute(
        select(Job)
        .order_by(Job.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    jobs = result.scalars().all()
    
    return [JobResponse.model_validate(job) for job in jobs]


@router.delete(
    "/{job_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Cancelar un job",
    description="Cancela un job si aún está en estado pendiente o en ejecución."
)
async def cancel_job(
    job_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Endpoint para cancelar un job
    
    - **job_id**: UUID del job a cancelar
    
    Solo se puede cancelar jobs en estado PENDING o RUNNING.
    """
    
    # Buscar el job
    result = await db.execute(select(Job).where(Job.id == job_id))
    job = result.scalar_one_or_none()
    
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job con ID {job_id} no encontrado"
        )
    
    # Validar que el job pueda ser cancelado
    if job.status not in [JobStatus.PENDING, JobStatus.RUNNING]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No se puede cancelar un job en estado {job.status}"
        )
    
    # Cancelar el job
    job.status = JobStatus.CANCELLED
    from datetime import datetime
    job.completed_at = datetime.utcnow()
    
    await db.commit()
