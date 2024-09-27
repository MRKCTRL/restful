from celery import Celery 


app=Celery('tasks', broker='pya,qp://guest@localhost//')


@app.task
def async_task(data):
    return "Tasl Completed!pi"