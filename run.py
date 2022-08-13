from tapneat.app import app, socketio
from tapneat.model import model
import netifaces

server_ip=''

for iface in netifaces.interfaces():
	try:
		for addr in netifaces.ifaddresses(iface)[netifaces.AF_INET]:
			server_ip=addr["addr"]
	except KeyError:
	# No address for this interface
		pass



if __name__ == '__main__':
	print("Server now Online @" + server_ip)
	with app.app_context():
		model.db.init_app(app)
		model.db.create_all()
	socketio.run(app, host=server_ip)
