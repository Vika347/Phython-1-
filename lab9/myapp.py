from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from jinja2 import Environment, FileSystemLoader
import json
import requests


class Currency:
    def __init__(self, num_code, char_code, name, value):
        self.id = f"{char_code}_{num_code}"
        self.num_code = num_code
        self.char_code = char_code
        self.name = name
        self.value = value


class CurrencyHandler(BaseHTTPRequestHandler):
    env = Environment(loader=FileSystemLoader('templates'))

    user = {'id': '504638', 'name': 'Родина Виктория Юрьевна', 'group': 'P3121','email': 'vika.rodina08@mail.ru'}

    currencies = [
        Currency("840", "USD", "Доллар США", 92.50),
        Currency("978", "EUR", "Евро", 101.30),
        Currency("826", "GBP", "Фунт стерлингов", 116.80)
    ]

    subscriptions = ["USD_840", "EUR_978"]

    popular = {
        'USD': {'num': '840', 'name': 'Доллар США'},
        'EUR': {'num': '978', 'name': 'Евро'},
        'GBP': {'num': '826', 'name': 'Фунт стерлингов'},
    }

    def do_GET(self):
        path = urlparse(self.path).path
        query = parse_qs(urlparse(self.path).query)

        if path == '/':
            self.show_index()
        elif path == '/user':
            self.show_user()
        elif path == '/currencies':
            self.show_currencies()
        elif path == '/currency/delete':
            self.handle_delete(query)
        elif path == '/currency/update':
            self.update_rates()
        elif path == '/author':
            self.show_author()
        else:
            self.send_error(404)

    def do_POST(self):
        path = urlparse(self.path).path
        if path == '/currency/add':
            self.handle_add()
        elif path == '/subscribe':
            self.handle_subscribe()
        elif path == '/unsubscribe':
            self.handle_unsubscribe()
        else:
            self.send_error(404)

    def render(self, template, **data):
        data.update({'user': self.user})
        html = self.env.get_template(template).render(**data)
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())

    def show_index(self):
        self.render('index.html')

    def show_user(self):
        sub = [c for c in self.currencies if c.id in self.subscriptions]
        available = [c for c in self.currencies if c.id not in self.subscriptions]
        self.render('user.html', subscriptions=sub, available=available)

    def show_currencies(self):
        rates = self.get_rates()
        self.render('currencies.html', currencies=self.currencies,
                    popular=self.popular, rates=rates)

    def show_author(self):
        self.render('author.html')

    def handle_add(self):
        try:
            length = int(self.headers['Content-Length'])
            data = parse_qs(self.rfile.read(length).decode())

            new = Currency(
                data['num_code'][0],
                data['char_code'][0].upper(),
                data['name'][0],
                float(data['value'][0])
            )
            self.currencies.append(new)
        except:
            pass
        self.redirect('/currencies')

    def handle_delete(self, query):
        cid = query.get('id', [''])[0]
        if cid:
            self.currencies = [c for c in self.currencies if c.id != cid]
            if cid in self.subscriptions:
                self.subscriptions.remove(cid)
        self.redirect('/currencies')

    def update_rates(self):
        rates = self.get_rates()
        for c in self.currencies:
            if c.char_code in rates:
                c.value = rates[c.char_code]
        self.redirect('/currencies')

    def get_rates(self):
        try:
            r = requests.get('https://www.cbr-xml-daily.ru/daily_json.js', timeout=3)
            data = r.json()
            return {code: round(info['Value'] / info['Nominal'], 2)
                    for code, info in data.get('Valute', {}).items()}
        except:
            return {'USD': 95.50, 'EUR': 102.30, 'GBP': 118.80}

    def handle_subscribe(self):
        try:
            data = parse_qs(self.rfile.read(int(self.headers['Content-Length'])).decode())
            cid = data['id'][0]
            if cid not in self.subscriptions:
                self.subscriptions.append(cid)
        except:
            pass
        self.redirect('/user')

    def handle_unsubscribe(self):
        try:
            data = parse_qs(self.rfile.read(int(self.headers['Content-Length'])).decode())
            cid = data['id'][0]
            if cid in self.subscriptions:
                self.subscriptions.remove(cid)
        except:
            pass
        self.redirect('/user')

    def redirect(self, url):
        self.send_response(303)
        self.send_header('Location', url)
        self.end_headers()


def run():
    server = HTTPServer(('localhost', 8080), CurrencyHandler)
    print("Сервер: http://localhost:8080")
    server.serve_forever()


if __name__ == "__main__":
    run()