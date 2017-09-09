import urllib2
import sys
import zipfile
import time


def make_url(date):
    month_dict = {
        1: "JAN", 2: "FEB", 3: "MAR", 4: "APR",
        5: "MAY", 6: "JUN", 7: "JUL", 8: "AUG",
        9: "SEP", 10: "OCT", 11: "NOV", 12: "DEC"}
    date_list = date.split('-')
    day = date_list[2]
    month = date_list[1]
    year = date_list[0]
    month_str = month_dict.get(int(month))
    if len(day) != 2:
        day = '0' + day
    url = "http://www.nseindia.com/content/historical/EQUITIES/{0}/{1}/cm{2}{1}{0}bhav.csv.zip".format(
        year, month_str, day)
    return url


def unzip(filename):
    fh = open(filename, 'rb')
    z = zipfile.ZipFile(fh)
    for name in z.namelist():
        z.extract(name)
        with open(name) as f:
            print "no of line in {0} is {1}".format(name, sum(1 for _ in f))
    fh.close()


def download_zip(url):
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Encoding': 'gzip,deflate,sdch',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}

    req = urllib2.Request(url, headers=hdr)
    try:
        page = urllib2.urlopen(req)
        content = page.read()
        zipfile_name = url.split('/')[-1]
        localFile = open(zipfile_name, 'w')
        localFile.write(content)
        localFile.close()
        page.close()
        unzip(zipfile_name)

    except urllib2.HTTPError, e:
        print e.fp.read()



def main():
    date = sys.argv[1]
    url = make_url(date)
    download_zip(url)

if __name__ == '__main__':
    main()
