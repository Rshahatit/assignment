from django.http import HttpResponse
from find_path.scripts.main import main
from find_path.scripts.parse_input import parse_input
import json

def index(request):
    body = json.loads(request.body)
    print(body)
    source = parse_input(body["source"])
    destination = parse_input(body["destination"])
    print(source, destination)
    return HttpResponse(main(source, destination))

