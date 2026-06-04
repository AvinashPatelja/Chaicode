from redis import Redis
from rq import Queue

queue = Queue(connection = Redis(
    host='localhost', 
    port=6379
    )
)

# from rq import SimpleWorker
# from redis import Redis

# connection = Redis(host="localhost", port=6379)
# worker = SimpleWorker(["default"], connection=connection)
# worker.work()