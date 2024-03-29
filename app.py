from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('message')
def handle_message(message):
    print('Received message:', message)
    # Отправляем обратно тот же текст сообщения
    emit('response', message)

@socketio.on('move')
def handle_move(data):
    # Передаем координаты игрока всем подключенным клиентам, кроме отправителя
    emit('player_moved', data, broadcast=True, include_self=False)


if __name__ == '__main__':
    socketio.run(app, debug=True)
