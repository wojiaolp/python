import redis
import time
import uuid

def acquire_semaphore(conn, semname, limit, timeout=10):
	identifier = str(uuid.uuid4())
	now = time.time()

	pipeline = conn.pipeline(True)
	pipeline.zremrangebyscore(semname, '-inf', now - timeout)
	pipeline.zadd(semname, identifier, now)
	pipeline.zrank(semname,identifier)
	if pipeline.execute()[-1] < limit:
		return identifier
	
	conn.zrem(semname,identifier)
	return None

def release_semaphore(conn, semname, identifier):
	return conn.zrem(semname,identifier)

conn = redis.Redis(host='127.0.0.1',port=6379)
semname = "my_semname"
limit = 4
timeout = 3

acquire_semaphore(conn, semname, limit, timeout)

print(conn.zrange(semname,0,-1,withscores=True)) 
