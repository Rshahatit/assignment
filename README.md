Wikiracer Write up 

High Level Architecture 
Diagram

What the code does:
The wikiracer code takes in a source or destination, can be a wiki url or a title for a wiki page. It starts at the source page and calls the media wiki api to find the wiki pages that have links on that page. It continues calling the media wiki api - searching for the destination page -  among the links on the upcoming pages. While it is requesting links on pages from the media wiki api it is asynchronously checking if any of the links it already has retrieved has the destination page among them. I use two asynchronous queues to give each kind of worker their jobs. One queue (titles to visit) is giving our search worker a title and a set of links on the page --- that worker checks if the destination page is in that set then adds all the links into a queue for the fetcher worker to fetch all the links for those pages. When the fetcher worker gets the links for the title it puts them in the queue (titles to visit) for the search worker to keep checking.
The code optimizes for the wall clock time of jumping from page to page like the instructions specifies. I chose to do this asynchronously because of the nature of how many IO operations occur and the time that is wasted waiting for that request. Doing it asynchronously allows me to only worry about one thread, the event loop will take care of running the workers whenever there is free time from a request. 
I also have a Dockerfile included with my application. You can utilize it through the make file, I give instructions below. 
Instructions for how to run your Wikiracer:
Testing:
make test
	This command installs the requirements from the requirements.txt file and runs the automated tests end to end tests in django.
Spin up docker container with application running:
 make serve-application
Your docker container will be listening on localhost:8000
You can send a post request with a (filling in source and dest with a wiki url or page title)
curl -X POST http://127.0.0.1:8000/findpath/  -H 'Content-Type: application/json' -d '{"source" : "Mickey Mouse","destination" : "Albert Einstein"}’

Strategies I tried:
(Links, pages, and titles are all referring to the same thing in a way throughout my description)
Initial thoughts:
At first I thought I could have a database to store everything. That would take care of the async issues and before any methods make any calls they would make sure the destination page hasn't been found by checking the db if any other process found it. I thought making those db calls would be unnecessary and time consuming so I pushed forward without pursuing that approach.

node js:
I have been going through this book called Building Enterprise Javascript applications so thought to start attempting this with node. The asynchronous nature of nodejs made it attractive for decreasing wall clock time between pages. I had a boilerplate app ready to go from the book so I started thinking about how to solve the problem of wikiracing. 
So I started with the Media wiki api. I read through some of the documentation to find how we can get all the links from a wikipedia page given its title. After finding what I was looking for I poked around more to see if anything else could be useful, I found an api call that can give you all the pages that link to a given page. 
A big concept in the book was test driven development, I find it really hard to do it without fully understanding how to solve the problem, but I did know what the problem had to do so I wrote an end to end test using cucumber and gherkin to find a path between Rami Malek and 12 Strong (The pages could be easily changed) I chose 12 strong because it just one page away from Rami Malek after 2018 in Film. 
I wrote the test to make a request to /findpath with a payload of a source and destination. Then the response should be json with the path. (I wasn’t too focused on returning the time just yet). I started with a findpath handler function to accept the request. This handler would start the process to begin searching for the destination.
Now for the algorithm,  I thought of three different algorithms to attempt to implement: Breadth first search, depth first search, and some sort of A* search.
Before choosing one, I started writing the way that I would retrieve links from the media wiki api. I had to check for a field that was returned to ensure I got all the links for a page since the limit for a response was 500. I made sure to put them in a set to make quick look ups and take care of any duplicates. 
So now the process would be: get links -> parse them -> check if the destination is in the set of links -> if not start the process again with a recursive call to get the links of the links on the page you just checked. This led to an eternal depth first approach on the first page of every first page. So I implemented a way to keep track of the depth and reset to search the next page breadth wise. This was the start of my journey to callback hell. 
I spent a lot of time trying to make node synchronous which is an easy way to find yourself losing your mind. So after attempting to do async mutual recursion, I got to the point of finding the destination page, but I had to slow down my api calls because I was getting blocked by media wiki. So I decided to write a simple web scraper script to pull the links myself, while also putting some measures to slow down the concurrent requests.
There was still the problem of stopping. It would find the destination page but my wikiracer was not satisfied, it just kept searching. Some suggested just process.exit()however this isn’t just a script running. I need to get the response to the server.
Python

I started reading more about asynchronous coding. In the end, I decided to pivot to python. I thought implementing this synchronously with a language I have more experience with would make the implementation of the async solution easier. I found asyncio, a python library for making python asynchronous, which made me hopeful of my approach.
The python solution I decided on was a variation of A* search. I would use a priority queue to store the next pages to search. The priority (heuristic) would be the amount of links a page had similar to the destination page. This has its immediate drawbacks being you have to get the links for all the pages you retrieved before you can give a priority, but it does give you an idea to start searching in a direction with some context. For short paths this worked well, but the amount of time to get the links was a major speed bump in performance and finding distant pages was taking too long.
I started doing more reading on the benefits of asynchronous code. I read a great example of a chess player that I will link below in the resources section. Basically while my wikiracer is waiting for the links to come from the api (an IO operation) it could be doing some other operation like checking the links it already has received. 
Async io has good documentation and there are a lot of great resources for learning about async io implementations in python. I had to decouple the process of getting links(titles) from the process of checking if the destination page was among them. While async io has an awaitable priority queue, I did not want to wait to have the getting links process hindered by determining the priority of the next page to get links for… I wanted them to just keep chugging on the pages to get links from. I am keeping track of a couple states of my graph: the page titles with the links on that page, the previous page from which a page linked from, all the pages we have seen/checked, and a queue keeping track of all the pages we have yet to get links for and check.
The queue is important because our get links function is popping jobs from it to get links for and sending those results to our search function which checks the set of links for our dest page and adds any unseen pages back to the queue from the resulting pages links. 
Now I can see the wikiracer getting links and checking those links. Still I am not fully taking advantage of the full power of running concurrent requests as I came to find out. I was only ever waiting on one request at a time. I need to spin up multiple instances of my get links function to be able to process the queue faster. 
Now I am making 7 workers who get links and 1 worker who checks them and refills the queue to get more links. This solution runs very quickly and takes advantage of the IO operations of requesting the links to check links it already has.  
 The search is faster but going back to the media wiki api call from earlier (that gets the pages that link to a page), it would allow me to search backwards from the destination for the source as well as forwards and see if they ever cross. That would allow me to search even faster. That would be the future implementation for this wikiracer. 

How long you spent on each part:
	Nodejs version - 					                a day and a half
    Python synchronous version - 			            one day
    Python asynchronous version - 			            two days
    Optimizing async, error checking, dockerizing -	    one day 
