import tornado.ioloop
import tornado.web
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import base64


class MainHandler(tornado.web.RequestHandler):
    yes_count = 0
    no_count = 0

    def get(self):
        self.write('<html><body><h1>Голосование</h1>')
        self.write('<div><button onclick="vote(\'yes\')">Да</button><span id="yes_count">0</span></div>')
        self.write('<div><button onclick="vote(\'no\')">Нет</button><span id="no_count">0</span></div>')
        self.write('<div><img id="chart" src="/chart"></div>')
        self.write('<script>function vote(choice){fetch("/vote?choice="+choice);}</script>')
        self.write('</body></html>')


class VoteHandler(tornado.web.RequestHandler):
    def get(self):
        choice = self.get_argument('choice')
        if choice == 'yes':
            MainHandler.yes_count += 1
        elif choice == 'no':
            MainHandler.no_count += 1
        self.redirect('/')


class ChartHandler(tornado.web.RequestHandler):
    def get(self):
        data = {'Да': MainHandler.yes_count, 'Нет': MainHandler.no_count}
        labels = list(data.keys())
        values = list(data.values())

        plt.bar(labels, values)
        plt.xlabel('Выбор')
        plt.ylabel('Количество голосов')
        plt.title('Результаты голосования')

        # Сохраняем график в байтовый объект
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        plt.close()

        # Преобразуем байтовый объект в base64 строку для вставки в HTML
        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        self.write('<img src="data:image/png;base64,{}">'.format(image_base64))


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/vote", VoteHandler),
        (r"/chart", ChartHandler),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("Сервер запущен на порте 8888")
    tornado.ioloop.IOLoop.current().start()
