from django.http import HttpResponse
from find_path.scripts.async_sol.main import start
from find_path.scripts.parse_input import parse_input
import json
import asyncio

def index(request):
    body = json.loads(request.body)
    print(body)
    source = parse_input(body["source"])
    destination = parse_input(body["destination"])
    print(source, destination)
    return HttpResponse(start(source, destination))

