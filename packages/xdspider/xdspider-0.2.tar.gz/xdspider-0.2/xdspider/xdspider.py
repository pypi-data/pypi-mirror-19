import threading
import urllib2
import sys
import re
from bs4 import BeautifulSoup
import json
from xml.sax.saxutils import escape
configs_ = dict({
            "force2https": 0,          # forces application to parse all links with only https
            "follow_redirects" : 1,  # application accepts and follows all redirects
            "multi_threaded": 1 ,     # use for multi threading
            "format":"xml",                # default output format (xml, csv, json)
            "spider_depth" : 4,            # default of 4 links deep per link from base link. from page x to page a->b->c->d
            "exclusion_list": [         # default is None, Set to a list of strings in the form of a regex "file.extension"
                
            ],
            "websites": [
                
            ],
            "save2file": 0,
            "output_file":"sitemap",
            "user_container_link" : 1,
            "headers": {
                "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0",
                "Accept-Language":"en-US,en;q=0.5",
                "Upgrade-Insecure-Requests":1,
                "Connection":"keep-alive",
                "Referer":""
            }
    }) #bnecause static doent exist :/

class XDSpider(threading.Thread):
    prop_re = None
    debug = False          # used for debugging purposes only
    spidering = False     # used for tread (only allow spider to be called once)
    configs = dict()  # empty list for configs
    links    =     list() # empty list for storage

    url = ""
    lvl = 0

    def config(self,args_x):
        # default configs - read only
        global configs_
        self.configs =  configs_
        if "--urls" in args_x:
            #find urls command, parse till next command
            #set website
            pass
        elif "--file" in args_x:
            #find filename, parse till next command
            #load websites from a file
            pass
        return self

    #threaded - single (one class instance per site)
    #url = url to spider
    #lvl = depth
    def StartSpider(self, url,lvl=4):
        self.url = url
        self.lvl = lvl

    def run(self):
        print("STARTED SPIDER FOR: "+ self.url)
        print("HAS MAX DEPTH SET TO: "+ str(self.lvl))
        self.Spider(self.url,self.lvl)
        if self.configs['save2file']:
            f = open(self.configs['output_file']+"."+self.configs['format'],"w")
            f.write(self.Output())
            f.close()
        else:
            print self.Output()
        print("SPIDER COMPLETED FOR: "+ self.url)
        return

    def Output(self):
        if self.configs['format'] == "xml":
            return self.OutputXML()
        if self.configs['format'] == "json":
            return self.OutputJSON()
        if self.configs['format'] == "csv":
            return self.OutputCSV()
        return "Output Error - No Format Specified"

    def Spider(self, url, lvl=4, scheme="", domain="", port=""):
        if lvl == None or int(lvl) <= 0:
            return
        if scheme == "" or domain == "" and url != "":
            self.prop_re = re.compile("^(https?:\/\/)([^\/]+):(\d+)/?(.+)")
            url = "".join(url).encode('ascii','ignore')
            rex = self.prop_re.search(url)
            if rex != None:
                scheme = rex.group(1)
                domain = rex.group(2) 
                port = rex.group(3)
            else:
                self.prop_re = re.compile("^(https?:\/\/)([^\/]+)/?(.+)")
                rex = self.prop_re.search(url)
                if rex != None:
                    scheme = rex.group(1)
                    domain = rex.group(2) 
                    port = ""
             
        if url[0] == "#":
            return

        _links = self.getPageLinks(self.getHTML(self.fixURL(url,scheme, domain,port)),scheme, domain,port)

        
        if _links != None:
            for __link in _links:
                self.links.append(__link)
                __link = self.fixURL(__link,scheme, domain,port)
                self.Spider(__link, lvl-1,"")
        self.links = self.unique(self.links)
        return

    def fixURL(self, url, scheme, domain,port):
        if url!=None:
            return  ((scheme + domain + (":"+port if port!="" else "") + url) if url[0] == "/" else url)
        return url
    # Bounce if depth reached
    # GetLinksFromLinks
    # BounceLinks till no more found
    # downloader + retries of 3
    def getHTML(self, link, retries=3):
        #downloads page and returns html data
        while retries>=0:
            try:
                global debug
                if debug:
                    print("> Scanning "+str(link))
                response = urllib2.urlopen(link)
                html = response.read()
                return html
            except Exception as e:
                global debug
                if debug:
                    print(e)
            retries = retries-1
        return ""

    #parser            
    def getPageLinks(self, html_page_data, scheme, domain, port):
        soup = BeautifulSoup(html_page_data, 'html.parser')
        links = list()
        for link in soup.find_all('a'):
            if link != None:
                url = None
                try:
                    url = link['href'] if link['href'] else None
                except:
                    pass
                if url != None:
                    if url[0] == "#":
                        continue
                    if "javascript" in url:
                        continue
                    if "mailto" in url:
                        continue
                    if "tel" in url:
                        continue
                    url = self.fixURL(url,scheme, domain,port)
                links.append(url)
        return self.unique(links)

    def unique(self, y):
        # order preserving
        noDupes = []
        [noDupes.append(i) for i in y if not noDupes.count(i)]
        return noDupes

    def Help():
        print("> python xdspider.py [--urls http://ww.example.com/] [--file <siteurls.csv> ] [--get-defaults] [--get-defaults-save <config.ini>] [--configs <config.ini>] [--format <XML|CSV|JSON>]")
        return None

    def Version(self):
        return "1.0.0.0"

    def OutputXML(self):
        data=""
        data+='<?xml version="1.0" encoding="UTF-8"?>'+"\r\n"
        data+='<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">'+"\r\n"
        links = list()
        for link in self.links:
            if link != None:
                data+="    <url>"+"\r\n"
                data+="        <loc>"+escape(str("".join(link)))+"</loc>"+"\r\n"
                data+="        <changefreq>"+["daily","weekly","monthly","yearly"][2]+"</changefreq>"+"\r\n"
                data+="        <priority>"+str(1)+"</priority>"+"\r\n"
                data+="    </url>"+"\r\n"
        data+='</urlset>'+"\r\n"
        return data

    def OutputJSON(self):
        data=""
        data+=('[')+"\r\n"
        data+=('    urls: [')+"\r\n"
        for link in self.links:
            data+='{'+"\r\n"
            data+='"loc":"'+link+'"'+"\r\n,"
            data+='"changefreq":"'+["daily","weekly","monthly","yearly"][3]+'"'+"\r\n,"
            data+='"priority":"1.00"'+"\r\n"
            data+='}'+"\r\n"
        data+=']'+"\r\n"
        return data

    def OutputCSV(self):
        data=""
        for link in self.links:
            data+=link+"\r\n"
        return data

def main():
    global configs_
    print("Welcome To XDSpider - Version "+ XDSpider().Version())    
    args_x = sys.argv + list({"--configs configs.json --debug --out sitemap --format xml"})
    args_x = " ".join(args_x).split(" ")
    
    
    if "--debug" in args_x:
        global debug
        debug = True
        print(args_x)
    else:
        debug = False

    #"--get-defaults-save filename"
    if "--get-defaults-save" in args_x:
        f = open(args_x[args_x.index("--get-defaults-save")+1],"w")
        json.dump(configs_,f)
        f.close()
        return
    #"--get-defaults"
    elif "--get-defaults" in args_x:
        configs = str(XDSpider().configs()).replace("'",'"').replace("/", "\\/")
        print json.dumps(configs)
        return

    #--configs
    if "--configs" in args_x:
        f = open(args_x[args_x.index("--configs")+1],"r")
        configs_ = json.loads("".join(f.readlines()).replace("'", "\"").replace("/", "\\/"))
        f.close()

    #--format <XML | JSON | CSV>
    if "--format" in args_x:
        configs_["format"] = args_x[args_x.index("--format")+1]

    #--out filename
    if "--out" in args_x:
        configs_["output_file"] = args_x[args_x.index("--out")+1]
        configs_["save2file"] = 1

    #if "--urls" in args_x:
    #    i = 1
    #    while i:
    #        data = args_x[args_x.index("--out")+1
    #        configs_["website"].append()
    #        i=i+1
    #--file
    if "--file" in args_x:
        f = open(args_x[args_x.index("--file")+1],"w")
        lines = f.readlines()
        f.close()
        for line in lines:
            configs_["websites"].append(line)
    threads = []
    for i in range(len(configs_["websites"])):
        threads.append(XDSpider())
        threads[i].config(args_x)
        threads[i].StartSpider(configs_["websites"][i], threads[i].configs["spider_depth"])
        threads[i].start()
    return

#calls main
main()