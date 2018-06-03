import requests
import argparse
from queue import Queue
import threading
import os
import errno
import random

header = """
                              ,      \    /      ,
                             / \     )\__/(     / \\
                            /   \   (_\  /_)   /   \\
    _______________________/_____\___\@  @/___/_____\\____________________
   |                                 |\../|                              |
   |                                  \VV/                               |
   |   _______ _______  ______ _______  _____  _  _  _ _______ __   _    |
   |   |  |  | |_____| |_____/ |       |     | |  |  | |______ | \  |    |
   |   |  |  | |     | |    \_ |_____  |_____| |__|__| |______ |  \_|    |
   |_____________________________________________________________________|
     || ||               |    /\ /     \\\\     \ /\    |
     || ||               |  /   V       ))     V   \  |
     || ||               |/     `      //      '     \|
     || ||               `             V              '
    _||_||________________
   |                      |
   | FlipHTML5 Downloader |
   |______________________|
   """
print(header)

parser = argparse.ArgumentParser()
parser.add_argument(
    "bookID", help="The ID of the book. Example: \'ousx/stby\' for http://fliphtml5.com/ousx/stby")
parser.add_argument("start", help="Starting page to download", type=int)
parser.add_argument("end", help="Last page to download", type=int)
parser.add_argument("-n", "--folderName",
                    help="The folder name to save the pages. Defaults to bookID")
parser.add_argument("threadNum",
                    help="Number of threads to run. Defaults to 20", type=int)
parser.add_argument("-s", "--skipExisting", action="store_true",
                    help="Skip downloading existing file")

args = parser.parse_args()

start = args.start
end = args.end
bookID = args.bookID
skipExisting = args.skipExisting
threadNum = args.threadNum

if args.folderName is not None:
    folderName = args.folderName
else:
    folderName = bookID.replace("/", "-")

printLock = threading.Lock()


def downloadImage(taskID):
    filepath = "{0}/{1}.jpg".format(folderName, taskID)
    with printLock:
        print("[ ] {0} downloading page {1}".format(
            threading.current_thread().name, taskID))

    # Create directory if does not exist
    os.makedirs(folderName, exist_ok=True)

    URL = "http://online.fliphtml5.com/{0}/files/large/{1}.jpg".format(
        bookID, taskID)
         
    with open("useragents.txt", "r") as f:
        useragents = [line.rstrip("\n") for line in f]

    useragent = useragents[random.randrange(0, len(useragents))]
    headers = {
        'User-Agent':  useragent}

    try:
        r = requests.get(URL, headers=headers, timeout=1.000)
        with open(filepath, "wb") as f:
            f.write(r.content)
        with printLock:
            print("[+] {0} downloaded page {1}".format(
                threading.current_thread().name, taskID))

    #Pass task to others so the downloading won't stop
    except requests.exceptions.HTTPError as errh:
        print("[-] {0} encountered HTTP error on page {1}. Skipped Task.".format(threading.current_thread().name, taskID))
        q.put(taskID)
    except requests.exceptions.ConnectionError as errc:
        print("[-] {0} encountered Connection error on page {1}. Skipped Task.".format(threading.current_thread().name, taskID))
        q.put(taskID)
    except requests.exceptions.Timeout as errt:
        print("[-] {0} encountered Timeout error on page {1}. Skipped Task.".format(threading.current_thread().name, taskID))
        q.put(taskID)

def threader():
    while True:
        taskID = q.get()
        filepath = "{0}/{1}.jpg".format(folderName, taskID)

        if skipExisting:
            if not os.path.isfile(filepath):
                downloadImage(taskID)
            else:
                with printLock:
                    print("[ ] {0} skipped page {1}".format(threading.current_thread().name, taskID))
        else:
            downloadImage(taskID)
        q.task_done()


q = Queue()

# Create threads
for x in range(threadNum):
    t = threading.Thread(target=threader)
    t.daemon = True
    t.start()

# Put taskID to queue
for taskID in range(start, end + 1):
    q.put(taskID)

q.join()
print("[+] Finished. Press any key to exit")
input()
