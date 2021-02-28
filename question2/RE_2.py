import re

generic_urls = [
    "https://www.genericdomain.com/abc/def/1290aodwb23-ghi.img",
    "https://www.genericdomain.com/abc/31287bdwakj-jkl.img",
    "https://www.genericdomain.com/19unioawd02-jkl.img",
]

for url in generic_urls:
    # use [^/] means does not contain '/'
    # so we are looking for everything between '/' and '-' while not contain '/'
    special_sequence = re.search(r"/([^/]*)-", url).group(1)
