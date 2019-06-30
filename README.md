# What
This is wsgi based toy webframework.


# Example

```python
def handle_get(request):
    data = ','.join(f'{k.upper()}: {v}' for k, v in request.body.items())
    return data or 'no params'

def j(request):
    return request.body or {'sakura': 'kinomoto', 'tomoyo': 'daidouji'}

def handle_post(request):
    return dict(result=True, **request.body)

app = App() \
    .service(resource('/').get(handle_get)) \
    .service(resource('/json').get(j)) \
    .service(resource('/post').post(handle_post))
Server(app=app).bind('0.0.0.0', 8000).run()
```
