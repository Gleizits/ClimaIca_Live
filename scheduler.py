"""
Corre el pipeline automáticamente cada 30 minutos
usando APScheduler, sin depender del Task Scheduler de Windows.
"""

from apscheduler.schedulers.blocking import BlockingScheduler
from main import ejecutar_pipeline

scheduler = BlockingScheduler(timezone="America/Lima")

# Ejecuta el pipeline apenas arranca el script (primera corrida inmediata)
ejecutar_pipeline()

# Luego lo repite cada 30 minutos
scheduler.add_job(ejecutar_pipeline, "interval", minutes=30)

if __name__ == "__main__":
    print("Scheduler iniciado. El pipeline correrá cada 30 minutos...")
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("Scheduler detenido.")
