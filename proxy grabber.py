from aiohttp import ClientSession
import asyncio
import datetime
import json

class ProxyGrabber():

    def __init__(self):
        self.times = []
        self.urllist = []
        self.responses = []
        self.iplist = []
        self.headers = {
            "user-agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36"
        }


    def get_time(self):
        # Takes the date of today, yesterday and 2 days before now
        timestamp = []
        ctime = datetime.date.today()
        timestamp.append(ctime)
        timestamp.append(ctime - datetime.timedelta(days=1))
        timestamp.append(ctime - datetime.timedelta(days=2))
        self.times = timestamp


    def makeurl(self):
        # Makes the 3 url from the dates in the self.times list
        for date in self.times:
            url = "https://checkerproxy.net/api/archive/{}".format(date)
            self.urllist.append(url)
    

    async def request(self, url):
        # aiohttp coroutine
        print("Making a request to {}".format(url))
        async with ClientSession() as session:
            async with session.get(url, headers=self.headers) as response:
                print("Finished request to {}".format(url))
                return await response.json()


    def savejson(self):
        with open("proxy list.txt", mode="a") as proxyfile:
            for response in self.responses:
                for item in response:
                    proxyfile.write(item["addr"]+"\n")
        

    async def makerequest(self):
        # start the process of requesting the url with aiohttp
        tasks = []
        
        # tasks list creation
        for id,url in enumerate(self.urllist):
            task = asyncio.ensure_future(self.request(url))
            tasks.append(task)
        self.responses = await asyncio.gather(*tasks)


    def run(self):
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(self.makerequest())
        loop.run_until_complete(future)

if __name__ == "__main__":
    import time
    s = time.perf_counter()

    grabber = ProxyGrabber()
    grabber.get_time()
    grabber.makeurl()
    grabber.run()
    grabber.savejson()

    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")
