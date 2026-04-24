"""
AutoFlow AI - Job Schemas
Esquemas Pydantic para validación de requests/responses
"""

from pydantic import BaseModel, Field, model_validator
from typing import Optional, Any
from datetime import datetime
from enum import Enum
from uuid import UUID


class JobStatus(str, Enum):
    """Estados posibles de un Job"""
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    ERROR = "error"
    CANCELLED = "cancelled"


class JobCreate(BaseModel):
    """Schema para crear un nuevo job (POST /run)"""
    
    instruction: str = Field(
        ...,
        min_length=10,
        max_length=5000,
        description="Instrucción en lenguaje natural del usuario"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "instruction": "Ve a Google, busca 'AutoFlow AI', y extrae los primeros 5 resultados"
            }
        }


class ExecutionStep(BaseModel):
    """Paso individual dentro de un plan de ejecucion"""

    id: int = Field(..., ge=1, description="Numero de paso")
    action: str = Field(..., min_length=2, max_length=100, description="Accion a ejecutar")
    description: str = Field(..., min_length=3, max_length=300, description="Descripcion del paso")
    params: dict[str, Any] = Field(default_factory=dict, description="Parametros del paso")


class ExecutionPlan(BaseModel):
    """Plan estructurado generado por IA"""

    total_steps: int = Field(..., ge=1, le=50, description="Total de pasos")
    steps: list[ExecutionStep] = Field(..., min_length=1, max_length=50)

    @model_validator(mode="after")
    def validate_consistency(self):
        if self.total_steps != len(self.steps):
            raise ValueError("total_steps debe coincidir con la cantidad real de steps")

        ids = [step.id for step in self.steps]
        if len(ids) != len(set(ids)):
            raise ValueError("Los IDs de pasos no deben repetirse")

        return self


class JobResponse(BaseModel):
    """Schema para responder un job (GET /status/{job_id})"""
    
    id: UUID = Field(..., description="ID único del job")
    instruction: str = Field(..., description="Instrucción original")
    status: JobStatus = Field(..., description="Estado actual del job")
    execution_plan: Optional[dict] = Field(None, description="Plan de ejecución generado")
    result: Optional[dict] = Field(None, description="Resultado final")
    logs: Optional[str] = Field(None, description="Logs de ejecución")
    error_message: Optional[str] = Field(None, description="Mensaje de error (si aplica)")
    created_at: datetime = Field(..., description="Fecha de creación")
    started_at: Optional[datetime] = Field(None, description="Fecha de inicio")
    completed_at: Optional[datetime] = Field(None, description="Fecha de finalización")
    
    class Config:
        from_attributes = True


class JobRunResponse(BaseModel):
    """Schema para responder creación de job (POST /run)"""
    
    job_id: UUID = Field(..., description="ID del job creado")
    status: JobStatus = Field(..., description="Estado inicial")
    message: str = Field(..., description="Mensaje de confirmación")
    
    class Config:
        json_schema_extra = {
            "example": {
                "job_id": "123e4567-e89b-12d3-a456-426614174000",
                "status": "pending",
                "message": "Job creado exitosamente. Accede a /status/123e4567-e89b-12d3-a456-426614174000 para ver el progreso"
            }
        }
