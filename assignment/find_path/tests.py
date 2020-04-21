import unittest
from .scripts.sync_sol.get_links import get_all_links
from django.test import Client


class e2eTest(unittest.TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        self.easy_payload = {"source": "https://en.wikipedia.org/wiki/Rami_Malek", "destination" : "https://en.wikipedia.org/wiki/Iran"}
        self.medium_payload = {"source": "https://en.wikipedia.org/wiki/Mickey_Mouse", "destination" : "Albert Einstein"}
        self.hard_payload = {"source": "Super Mario", "destination" : "https://en.wikipedia.org/wiki/Aleut"}  
        self.goal_payload =  {"source": "Tennessee", "destination" : "Printer (computing)"}
        self.bad_payload =  {"source": "https://google.com", "destination" : "Printer (computing)"}
        self.same_src_dest_payload =  {"source": "Printer (computing)", "destination" : "Printer (computing)"}
        self.exist =  {"source": "Tennessee", "destination" : "Printer"}

    def test_bad_payload(self):
        # Issue a POST request.
        response = self.client.post('/findpath/', content_type="application/json", data=self.bad_payload)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 400)

        # verify the path
        res = response.json()
        if res["error"]:
            message = res["message"]
            self.assertEqual(message, "You must enter a valid wikipedia link")

    def test_goal(self):
        source = "Tennessee"
        destination = "Printer (computing)"
        # Issue a POST request.
        response = self.client.post('/findpath/', content_type="application/json", data=self.goal_payload)

        # verify the path
        res = response.json()
        path = res['path']
        duration = res['duration']
        if res["error"]:
            message = res["message"]
            self.assertEqual(response.status_code, 400)
            self.assertEqual(message, "path does not exist with a depth of 15 from the source page")
        else:
            self.assertEqual(response.status_code, 200)
            self.assertEqual(path[0], source, f'Path must start with {source}') # starts with source
            self.assertEqual(path[len(path)-1], destination, f'Path must end with {destination}') # ends with destination
            verified, message = self.verify_path(path)
            self.assertTrue(verified, message)
            print(f'Path from {source} to {destination}: {path} completed in {duration:0.2f} seconds')

    def test_easy(self):
        source = "Rami Malek"
        destination = "Iran"
        # Issue a POST request.
        response = self.client.post('/findpath/', content_type="application/json", data=self.easy_payload)

        # verify the path
        res = response.json()
        path = res['path']
        duration = res['duration']
        if res["error"]:
            self.assertEqual(response.status_code, 400)
            message = res["message"]
            self.assertEqual(message, "path does not exist with a depth of 15 from the source page")
        else:
            # Check that the response is 200 OK.
            self.assertEqual(response.status_code, 200)
            self.assertEqual(path[0], source, f'Path must start with {source}') # starts with source
            self.assertEqual(path[len(path)-1], destination, f'Path must end with {destination}') # ends with destination
            verified, message = self.verify_path(path)
            self.assertTrue(verified, message)
            print(f'Path from {source} to {destination}: {path} completed in {duration:0.2f} seconds')

    def test_medium(self):
        source = "Mickey Mouse"
        destination = "Albert Einstein"
        # Issue a POST request.
        response = self.client.post('/findpath/', content_type="application/json", data=self.medium_payload)

        # verify the path
        res = response.json()
        path = res['path']
        duration = res['duration']
        if res["error"]:
            self.assertEqual(response.status_code, 400)
            message = res["message"]
            self.assertEqual(message, "path does not exist with a depth of 15 from the source page")
        else:
            self.assertEqual(response.status_code, 200)
            self.assertEqual(path[0], source, f'Path must start with {source}') # starts with source
            self.assertEqual(path[len(path)-1], destination, f'Path must end with {destination}') # ends with destination
            verified, message = self.verify_path(path)
            self.assertTrue(verified, message)
            print(f'Path from {source} to {destination}: {path} completed in {duration:0.2f} seconds')
    
    # verifies that each next element in the path is on the previous page.
    def verify_path(self, path):
        for i in range(len(path) - 1):
            prev = path[i]
            cur = path[i+1]
            if cur not in get_all_links(prev):
                return (False, f'Path was invalid {cur} is not found on {prev}\'s wiki page')
        return (True, 'Path was valid')


    #this is also a longer test if you want to run it.
    #aleut is an native alaskan people
    # def test_hard(self):
    #     source = "Super Mario"
    #     destination = "Aleut"
    #     # Issue a POST request.
    #     response = self.client.post('/findpath/', content_type="application/json", data=self.hard_payload)

    #     # verify the path
    #     res = response.json()
    #     path = res['path']
    #     duration = res['duration']
    #     if res["error"]:
    #         self.assertEqual(response.status_code, 400)
    #         message = res["message"]
    #         self.assertEqual(message, "path does not exist with a depth of 15 from the source page")
    #     else:
    #         # Check that the response is 200 OK.
    #         self.assertEqual(response.status_code, 200)
    #         self.assertEqual(path[0], source, f'Path must start with {source}') # starts with source
    #         self.assertEqual(path[len(path)-1], destination, f'Path must end with {destination}') # ends with destination
    #         verified, message = self.verify_path(path)
    #         self.assertTrue(verified, message)
    #         print(f'Path from {source} to {destination}: {path} completed in {duration:0.2f} seconds')

    # I commented out this test because it takes a while to get to a depth of 15
    # def test_depth(self):
    #     # Issue a POST request.
    #     response = self.client.post('/findpath/', content_type="application/json", data=self.exist)

    #     # Check that the response is 200 OK.
    #     self.assertEqual(response.status_code, 200)

    #     # verify the path
    #     res = response.json()
    #     if res["error"]:
    #         message = res["message"]
    #         self.assertEqual(message, "path does not exist with a depth of 15 from the source page")

