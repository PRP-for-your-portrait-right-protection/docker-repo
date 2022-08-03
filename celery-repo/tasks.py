from celery import Celery
from celery.utils.log import get_task_logger
from module.ai_module import mosaic, character

logger = get_task_logger(__name__)

# app = Celery('tasks',
#     broker='amqp://localhost:5672',
#     result_backend='mongodb://localhost:27017/',
#     mongodb_backend_settings = {
#         'database': 'silicon',
#         'taskmeta_collection': 'celery'
#     }
# )
app = Celery('tasks',
    broker='amqp://admin:mypass@rabbitmq:5672',
    result_backend='mongodb://db:27017/',
    mongodb_backend_settings = {
        'database': 'silicon',
        'taskmeta_collection': 'celery'
    }
)

# 모자이크
@app.task()
def run_mosaic(whitelistFaceImgList, videoUrl, user):
    taskId = run_mosaic.request.id
    location = mosaic(taskId, logger, whitelistFaceImgList, videoUrl, user)
    return location

# 캐릭터
@app.task()
def run_character(whitelistFaceImgList, blockCharacterImgUrl, videoUrl, user):
    taskId = run_character.request.id
    location = character(taskId, logger, whitelistFaceImgList, blockCharacterImgUrl, videoUrl, user)
    return location