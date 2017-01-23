import redis

def create_chat(conn,sender,recipients,message,chat_id=None):
	chat_id = chat_id or str(conn.incr('ids:chat:'))

	recipients.append(sender)
	recipientsd = dict((r,0) for r in recipients)
	pipeline = conn.pipeline()
	pipeline.zadd('chat:' + chat_id, **recipientsd)
	for rec in recipients:
		pipeline.zadd('seen:' + rec, 0, chat_id)
	pipeline.execute()

	return send_message(conn, chat_id, sender, message)

def send_message(conn, chat_id, sender, message):
	print "waiting..."

#create_chat()

conn = redis.Redis(host='127.0.0.1',port=6379)
sender = "Liup"
recipients = ["Tom","Bryan","Rick"]
message = 'hello everyone!'
chat_id = '1'
create_chat(conn,sender,recipients,message,chat_id)
