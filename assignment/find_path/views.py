from django.http import JsonResponse
from find_path.scripts.async_sol.main import start
from find_path.scripts.parse_input import parse_input
import json
import asyncio

def index(request):
    body = json.loads(request.body)
    source = parse_input(body["source"])
    destination = parse_input(body["destination"])
    print(source, destination)
    if source == destination:
        payload = {"error":True, "message" : "Source and destination should not be the same"}
        return JsonResponse(payload, status=400) 
    elif source == 0 or destination == 0:
        payload = {"error": True, "message" : "You must enter a valid wikipedia link"}
        return JsonResponse(payload, status=400)
    else:
        payload = start(source, destination)
        if payload["error"]:
            return JsonResponse(payload,status=400)
        else:
            return JsonResponse(payload, status=200)

