# Adapted from: https://www.thepythoncode.com/article/using-threads-in-python

import requests
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from time import time


buffer_size = 1024 # read 1024 bytes every time 

def download(url):
    response = requests.get(url, stream=True) # download the body of response by chunk, not immediately
    filename = url.split("/")[-1] # get the file name
    with open(filename, "wb") as f:
        for data in response.iter_content(buffer_size): # write data read to the file
            f.write(data)

if __name__ == "__main__":
    urls = [
        "https://cdn.pixabay.com/photo/2018/01/14/23/12/nature-3082832__340.jpg",
        "https://cdn.pixabay.com/photo/2013/10/02/23/03/dawn-190055__340.jpg",
        "https://cdn.pixabay.com/photo/2016/10/21/14/50/plouzane-1758197__340.jpg",
        "https://cdn.pixabay.com/photo/2016/11/29/05/45/astronomy-1867616__340.jpg",
        "https://cdn.pixabay.com/photo/2014/07/28/20/39/landscape-404072__340.jpg",
    ] * 5
    
    for workers in [1, 2, 4, 8, 16, 32]:
        t = time()
        with ProcessPoolExecutor(max_workers=workers) as pool:
            pool.map(download, urls)
        print(f"Time took with {workers} process(es): {time() - t:.2f} sec.")

        t = time()    
        with ThreadPoolExecutor(max_workers=workers) as pool:
            pool.map(download, urls)
        print(f"Time took with {workers} thread(s): {time() - t:.2f} sec.")
