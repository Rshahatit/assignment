from django.http import HttpResponse
from find_path.scripts.main import main
from parse_input import parse_input

def index(request, source, destination):
    source = parse_input(source)
    destination = parse_input(destination)
    return HttpResponse(main(source, destination))

