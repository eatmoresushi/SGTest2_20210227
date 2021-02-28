import re

generic_urls = [
    "https://www.genericdomain.com/abc/def/1290aodwb23-ghi.img",
    "https://www.genericdomain.com/abc/31287bdwakj-jkl.img",
    "https://www.genericdomain.com/19unioawd02-jkl.img",
]

for url in generic_urls:
    # if we are sure what we want does not contains '/'
    # we can use [^/] which means does not contain '/'
    # so we are looking for everything between '/' and '-' while not contain '/'
    special_sequence = re.search(r"/([^/]*)-", url).group(1)
    # Otherwise, if we are sure what we want has a fixed length of 11
    # special_sequence = re.search(r"/(.{11})-", url).group(1)
