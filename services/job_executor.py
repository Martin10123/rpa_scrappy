"""
AutoFlow AI - Job Executor Service
Servicio para ejecutar jobs de automatización en background
"""

import threading
from datetime import datetime
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import select

from database import SyncSessionLocal
from models.job import Job, JobStatus
from services.gemini_parser import parse_instruction_with_gemini, GeminiParserError


class JobExecutor:
    """Ejecutor de jobs usando sesiones síncronas (para threads separados)"""

    def __init__(self, job_id: UUID):
        self.job_id = job_id
        self.logs = []

    def add_log(self, message: str, level: str = "INFO"):
        timestamp = datetime.utcnow().isoformat()
        log_entry = f"[{timestamp}] {level}: {message}"
        self.logs.append(log_entry)
        print(log_entry)

    def _get_job(self, session: Session) -> Job:
        return session.execute(select(Job).where(Job.id == self.job_id)).scalar_one()

    def update_job_status(self, session: Session, status: JobStatus):
        job = self._get_job(session)
        job.status = status
        job.logs = "\n".join(self.logs)
        if status == JobStatus.RUNNING and not job.started_at:
            job.started_at = datetime.utcnow()
        elif status in [JobStatus.SUCCESS, JobStatus.ERROR, JobStatus.CANCELLED]:
            job.completed_at = datetime.utcnow()
        session.commit()

    def simulate_execution_plan(self) -> dict:
        return {
            "total_steps": 3,
            "steps": [
                {"id": 1, "action": "analyze_instruction", "description": "Analizar la instrucción del usuario"},
                {"id": 2, "action": "process_data",        "description": "Procesar y validar datos"},
                {"id": 3, "action": "generate_result",     "description": "Generar resultado final"},
            ]
        }

    def build_execution_plan(self, instruction: str) -> dict:
        """Construye el plan con Gemini y fallback local si falla."""
        try:
            self.add_log("Generando plan de ejecucion con Gemini...")
            plan = parse_instruction_with_gemini(instruction)
            self.add_log("Plan generado por Gemini y validado")
            return plan.model_dump()
        except GeminiParserError as e:
            self.add_log(f"Gemini fallo, usando fallback local: {e}", level="WARNING")
            return self.simulate_execution_plan()

    def execute_step(self, step: dict) -> bool:
        self.add_log(f"Ejecutando paso {step['id']}: {step['action']}")
        try:
            import time; time.sleep(2)   # reemplaza asyncio.sleep
            self.add_log(f"✓ Paso {step['id']} completado", level="SUCCESS")
            return True
        except Exception as e:
            self.add_log(f"✗ Error en paso {step['id']}: {e}", level="ERROR")
            return False

    def execute(self):
        """Ejecutar el job completo de forma síncrona."""
        self.add_log(f"Iniciando ejecución del job {self.job_id}")

        with SyncSessionLocal() as session:
            try:
                self.update_job_status(session, JobStatus.RUNNING)

                job = self._get_job(session)
                instruction = job.instruction
                self.add_log(f"Instrucción: {instruction}")

                execution_plan = self.build_execution_plan(instruction)

                job = self._get_job(session)
                job.execution_plan = execution_plan
                session.commit()
                self.add_log(f"Plan generado con {execution_plan['total_steps']} pasos")

                all_success = all(self.execute_step(s) for s in execution_plan["steps"])

                if all_success:
                    self.add_log("✓ Ejecución completada exitosamente")
                    job = self._get_job(session)
                    job.result = {
                        "status": "success",
                        "instruction": instruction,
                        "execution_plan": execution_plan,
                        "steps_completed": execution_plan["total_steps"],
                        "completed_at": datetime.utcnow().isoformat(),
                    }
                    session.commit()
                    self.update_job_status(session, JobStatus.SUCCESS)
                else:
                    self.add_log("✗ Ejecución fallida")
                    job = self._get_job(session)
                    job.error_message = "Error durante la ejecución de los pasos"
                    session.commit()
                    self.update_job_status(session, JobStatus.ERROR)

            except Exception as e:
                self.add_log(f"Error fatal: {e}", level="ERROR")
                try:
                    job = self._get_job(session)
                    job.error_message = str(e)
                    session.commit()
                    self.update_job_status(session, JobStatus.ERROR)
                except Exception:
                    pass
            finally:
                self.add_log("Ejecución finalizada")


_background_tasks: dict = {}


def _run_in_thread(job_id: UUID):
    print(f"\n{'='*80}\n🚀 EJECUTANDO JOB EN THREAD: {job_id}\n{'='*80}\n")
    try:
        JobExecutor(job_id).execute()
    finally:
        _background_tasks.pop(job_id, None)


async def execute_job(job_id: UUID):
    """Lanza el job en un thread daemon (no bloquea el event loop de Uvicorn)."""
    print(f"\n{'='*80}\n🚀 INICIANDO EJECUCIÓN DE JOB: {job_id}\n{'='*80}\n")
    thread = threading.Thread(target=_run_in_thread, args=(job_id,), daemon=True)
    _background_tasks[job_id] = thread
    thread.start()