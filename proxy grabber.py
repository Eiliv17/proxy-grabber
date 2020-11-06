from aiohttp import ClientSession
import asyncio
import datetime
import json

class ProxyGrabber():

    headers = {
        "user-agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36"
    }

    def __init__(self):
        self.times = []
        self.urllist = []
        self.responses = []
        self.iplist = []


    def get_time(self):
        # Takes the date of today, yesterday and 2 days before now
        timestamp = []
        ctime = datetime.date.today()
        timestamp.append(ctime)
        timestamp.append(ctime - datetime.timedelta(days=1))
        timestamp.append(ctime - datetime.timedelta(days=2))
        timestamp.append(ctime - datetime.timedelta(days=3))
        timestamp.append(ctime - datetime.timedelta(days=4))
        self.times = timestamp


    def make_url(self):
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


    def save_json(self):
        with open("proxy list.txt", mode="a") as proxyfile:
            for response in self.responses:
                for item in response:
                    proxyfile.write(item["addr"]+"\n")
        

    async def make_request(self):
        # start the process of requesting the url with aiohttp
        tasks = []
        
        # tasks list creation
        for url in self.urllist:
            task = asyncio.create_task(self.request(url))
            tasks.append(task)
        self.responses = await asyncio.gather(*tasks)


    def run(self):
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(self.make_request())
        loop.run_until_complete(future)


def main():
    grabber = ProxyGrabber()
    grabber.get_time()
    grabber.make_url()
    grabber.run()
    grabber.save_json()


if __name__ == "__main__":
    import time
    s = time.perf_counter()
    main()
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")
