from celery import Celery
from celery.utils.log import get_task_logger
import time
from ai import return_x


logger = get_task_logger(__name__)

app = Celery('tasks',
             broker='amqp://admin:mypass@rabbitmq:5672',
             backend='mongodb://db:27017/silicon')

@app.task()
def test_celery(x):
    logger.info('Got Request - Starting work ')
    b = return_x(x)
    time.sleep(10)
    logger.info('Work Finished ')
    
    # 다른 함수에서 동영상을 저장하는 과정 진행 후 url return 시켜주면
    # 그 url을 받아서 celery return 값으로 넣어주는 과정 진행해보기
    return b
    # return 값을 db에 저장
