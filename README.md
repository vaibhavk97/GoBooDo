# GoBooDo
### A google books downloader with proxy support.


     .88888.            888888ba                    888888ba           
    d8'   `88           88    `8b                   88    `8b          
    88        .d8888b. a88aaaa8P' .d8888b. .d8888b. 88     88 .d8888b. 
    88   YP88 88'  `88  88   `8b. 88'  `88 88'  `88 88     88 88'  `88 
    Y8.   .88 88.  .88  88    .88 88.  .88 88.  .88 88    .8P 88.  .88 
     `88888'  `88888P'  88888888P `88888P' `88888P' 8888888P  `88888P' 
    ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
                                                                   


GoBooDo is a **python3** program for downloading **previewable** books on Google books. It downloads high resolution images of pages and combines them to save the file as a PDF. 
# Usage
For downloading a book GoBooDo requires the book id which can be fetched from the url of the book. For instance consider the example below:
~~~
https://books.google.co.in/books?id=XUwOtdcIWdkC&printsec=frontcover#v=onepage&q&f=false
~~~
in this url the id=XXX is the part we are interested in.

To start downloading:
~~~
python GoBooDo.py --id=XUwOtdcIWdkC
~~~

The configuration can be done in the settings.json and the description is as follows:
~~~
{
  "country":"co.in", // The TLD for the service that is being used for example books.google.co.in or books.google.de
  "page_resolution": 1500, // The resoution of page in dpi.
  "empty_image_size": 98670, // The size of empty image, it refers to the size of "Image not available pages".
  "proxy_links":0,   // 0 for disabling proxy when fetching page links upon reaching the limit.
  "proxy_images":0,  // 0 for disabling proxy when fetching  page images upon reaching the limit.
  "max_retry_links":1, // Max retries for fetching a link using proxies.
  "max_retry_images":1 // Max retries for a fetching a image using proxies.
  "global_retry_time": // 0 for not running GoBooDo indefinitely, the number of seconds in each iteration otherwise.
}
~~~

The output will be saved as a folder named the 'id' of the book which was given as input. The final PDF will be in the output folder inside it along with a folder containing the images.
Proxies may be added in proxies.txt (a sample proxy has been added already).

For changing "empty_image_size" according to the resolution of the page set in page_resolution, run setEmptyImageSize.py. The resolution is set with respect to books scanned in **potrait** manner
which is the case for most of them. However, it can still be the case that this page is present in the final PDF.

The breakup of the files downloaded is as follows:
~~~
    "data/obstinatePages.pkl": Pages which are to be fetched in the subsequent iterations.
    "data/pageLinkDict.pkl": A dictionary of pages and their links.
    "data/pagesFetched.pkl": Pages which have been fetched already.
    "Images/": All the images which have been downloaded for the current book.
    "Output/": The PDF of the current book.
~~~
 
# Dependencies
Use pip install requirements.txt for installing all the packages at once.
~~~
requests
bs4
Pillow
fpdf
html5lib
~~~

# Features 
1. Stateful : GoBooDo keeps a track of the books which are downloaded. In each subsequent iterations of operation only those those links and images are fetched which were not downloaded earlier.
2. Proxy support : Since Google limits the amount of pages accessible to each individual majorly on the basis of IP address, GoBooDo uses proxies for circumventing that limit and maximizing the number of pages that can be accessed in the preview.

# Todo
1. Add proxy integration with a checker.
2. Make the system more robust from being detected by google.
