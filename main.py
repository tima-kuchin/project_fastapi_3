from fastapi import FastAPI
from datetime import datetime

from public.car_router import car_router
from public.region_router import region_router

app = FastAPI()

# Подключение роутера car_router
app.include_router(car_router)
app.include_router(region_router)

# Путь к файлу лога
log_file_path = 'log.txt'

# Функция для записи в файл
def write_to_log(message):
    with open(log_file_path, mode='a') as log_file:
        log_file.write(f'{datetime.utcnow()}: {message}\n')

@app.on_event('startup')
async def startup_event():
    write_to_log('Begin')

@app.on_event('shutdown')
async def shutdown_event():
    write_to_log('Shutdown')