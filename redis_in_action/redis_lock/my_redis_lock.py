import uuid
import redis
import time

#加锁
def acquire_lock(conn, lockname, acquire_timeout=10):
	identifier = str(uuid.uuid4())
	end = time.time() + acquire_timeout
	while time.time() < end:
		if conn.setnx("lock:" + lockname, identifier):
			return identifier
		time.sleep(.001)
	return False
#释放锁
def release_lock(conn,lockname,identifier):
	pipe = conn.pipeline(True)
	lockname = "lock:" + lockname

	while True:
		try:
			pipe.watch(lockname)
			if pipe.get(lockname) == identifier:
				pipe.multi()
				pipe.delete(lockname)
				pipe.execute()
				return True
			pipe.unwatch()
			break
		except redis.exceptions.WatchError:
			pass
	return False

#带过期时间的锁
def acquire_lock_with_timeout(conn,lockname,acquire_timeout=10,lock_timeout=10):
	identifier = str(uuid.uuid4())
	lockname = "lock:"+lockname
	lock_timeout = int(math.ceil(lock_timeout))
	end = time.time() + acquire_timeout
	while time.time() < end:
		if conn.setnx(lockname,identifier):
			conn.expire(lockname,lock_timeout)
			return identifier
		elif not conn.ttl(lockname):
			conn.expire(lockname,lock_timeout)
		time.sleep(.001)
	return False



conn = redis.Redis(host='127.0.0.1',port=6379)

#print acquire_lock(conn, "mylock")
#print release_lock(conn,"mylock","test")

