from django_socketio.events import on_subscribe

sockets = dict()


# useless
@on_subscribe(channel='room-42')
def client_subscribe(request, socket, context, channel):
    room = request.session['room']
    if "room" not in sockets:
        sockets[room] = list()
    sockets[room].append(socket)
