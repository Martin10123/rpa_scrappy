"""
AutoFlow AI - Job Model
Modelo de base de datos para tareas de automatización
"""

from sqlalchemy import Column, String, Text, DateTime, Enum as SQLEnum, JSON
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
from enum import Enum
from database import Base


class JobStatus(str, Enum):
    """Estados posibles de un Job"""
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    ERROR = "error"
    CANCELLED = "cancelled"


class Job(Base):
    """Modelo de Job en la base de datos"""
    
    __tablename__ = "jobs"
    
    # ID único
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False
    )
    
    # Instrucción del usuario en lenguaje natural
    instruction = Column(Text, nullable=False)
    
    # Estatus actual del job
    status = Column(
        SQLEnum(JobStatus),
        default=JobStatus.PENDING,
        nullable=False
    )
    
    # Plan de ejecución (JSON generado por Claude)
    execution_plan = Column(JSON, nullable=True)
    
    # Resultado final (JSON)
    result = Column(JSON, nullable=True)
    
    # Logs de ejecución
    logs = Column(Text, nullable=True)
    
    # Mensaje de error (si aplica)
    error_message = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    
    def __repr__(self):
        return f"<Job(id={self.id}, status={self.status}, instruction={self.instruction[:50]}...)>"
