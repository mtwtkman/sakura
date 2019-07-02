from sakura import App, Server, resource, get


def handle_get(request):
    data = ','.join(f'{k.upper()}: {v}' for k, v in request.body.items())
    return data or 'no params'


def j(request):
    return request.body or {'sakura': 'kinomoto', 'tomoyo': 'daidouji'}


def handle_post(request):
    return dict(result=True, **request.body)


@get('/decorated')
def decorated(request):
    return 'decorated'


app = App() \
    .service(resource('/').get(handle_get)) \
    .service(resource('/json').get(j)) \
    .service(resource('/post').post(handle_post)) \
    .service(decorated)
Server(app=app).bind('0.0.0.0', 8000).run()
