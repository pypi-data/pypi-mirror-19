# -*- coding: utf-8 -*-
#coding=utf-8
from selenium import webdriver
import urllib
import re
from bs4 import BeautifulSoup
import sys
import urllib2
import json
import datetime



type = sys.getfilesystemencoding()
#decode('utf-8').encode(type)
#pageobj = bsobj.decode('utf-8').encode(type)
Externalpages = set()
Internalpages = set() 


now = datetime.datetime.now()
bob=str(now.strftime('%Y/%m/%d %H:%M:%S'))
print(bob)  

#a="fdsafdsafds"
#f = open("d:/1.txt", "w+")
#f.write(a)
#f.close()




#################################################################SoupSample
soup = BeautifulSoup('<b class="boldest">Extremely bold</b>')
tag = soup.b
print(tag.name)
print(tag['class'])
print(tag.attrs)
#################################################################


##################################################################html
def getpage(url):
    try:
        html = urllib.urlopen(url)
    except HTTPError as e: 
        print(e)
    else:
        print(html)
    #print('=======================================================html,html')
    #bsobj = BeautifulSoup(html.read(),'html.parser')
    bsobj = BeautifulSoup(html.read(),'lxml')
    print(bsobj.decode('utf-8').encode(type))

    print('=======================================================html,html')
    #print(bsobj.title)
    #print(bsobj.title.name)
    #print(bsobj.title.string)
    #print(bsobj.p)
    #print(bsobj.p['class'])
    #print(bsobj.a)

    print('=======================================================a')
    nameli = bsobj.findAll("a")
    for i,a in enumerate(nameli):
        print(a.get_text())
        print(a['href'])
        element=a.get_text()
        href=str(a['href'])
        i=i+1
        xpathstring ='"' + str(i) + '"' 
        print(xpathstring)
        qinghama_autopage(element,href,"bobsiji@qq.com")
    return bsobj
##############################################################################


############################################################################get element
def searchpage(bsobj,pageurl):
    #pageobj = bsobj.decode('utf-8').encode(type)
    pageobj = bsobj.encode('GB18030')
    f = open("d:/1.txt", "w+")
    print('=======================================================address')
    nameli = bsobj.findAll("address")
    for address in nameli:
        print(address.prettify().encode('GB18030'))
        print('//address')
        element=str(address)
        qinghama_autoobject("address",element,pageurl,"bobsiji@qq.com")

    print('=======================================================area')
    nameli = bsobj.findAll("area")
    for area in nameli:
        print(area.prettify().encode('GB18030'))
        print('//area')
        element=str(area)
        qinghama_autoobject("area",element,pageurl,"bobsiji@qq.com")

    print('=======================================================audio')
    nameli = bsobj.findAll("audio")
    for audio in nameli:
        print(audio.prettify().encode('GB18030'))
        print('//audio')
        element=str(audio)
        qinghama_autoobject("audio",element,pageurl,"bobsiji@qq.com")

    print('=======================================================article')
    nameli = bsobj.findAll("article")
    for article in nameli:
        print(article.prettify().encode('GB18030'))
        print('//article')
        element=str(article)
        qinghama_autoobject("article",element,pageurl,"bobsiji@qq.com")

    print('=======================================================b')
    nameli = bsobj.findAll("b")
    for b in nameli:
        print(b.prettify().encode('GB18030'))
        print('//b')
        element=str(b)
        qinghama_autoobject("b",element,pageurl,"bobsiji@qq.com")

    print('=======================================================br')
    nameli = bsobj.findAll("br")
    for br in nameli:
        print(br.prettify().encode('GB18030'))
        print('//br')
        element=str(br)
        qinghama_autoobject("br",element,pageurl,"bobsiji@qq.com")

    print('=======================================================base')
    nameli = bsobj.findAll("base")
    for base in nameli:
        print(base.prettify().encode('GB18030'))
        print('//base')
        element=str(base)
        qinghama_autoobject("base",element,pageurl,"bobsiji@qq.com")

    print('=======================================================button')
    nameli = bsobj.findAll("button")
    for button in nameli:
        print(button.prettify().encode('GB18030'))
        print('//button')
        element=str(button)
        qinghama_autoobject("button",element,pageurl,"bobsiji@qq.com")

    print('=======================================================body')
    nameli = bsobj.findAll("body")
    for body in nameli:
        print(body.prettify().encode('GB18030'))
        print('//body')
        element=str(body)
        qinghama_autoobject("body",element,pageurl,"bobsiji@qq.com")

    print('=======================================================caption')
    nameli = bsobj.findAll("caption")
    for caption in nameli:
        print(caption.prettify().encode('GB18030'))
        print('//caption')
        element=str(caption)
        qinghama_autoobject("caption",element,pageurl,"bobsiji@qq.com")

    print('=======================================================cite')
    nameli = bsobj.findAll("cite")
    for cite in nameli:
        print(cite.prettify().encode('GB18030'))
        print('//cite')
        element=str(cite)
        qinghama_autoobject("cite",element,pageurl,"bobsiji@qq.com")

    print('=======================================================code')
    nameli = bsobj.findAll("code")
    for code in nameli:
        print(code.prettify().encode('GB18030'))
        print('//code')
        element=str(code)
        qinghama_autoobject("code",element,pageurl,"bobsiji@qq.com")

    print('=======================================================command')
    nameli = bsobj.findAll("command")
    for command in nameli:
        print(command.prettify().encode('GB18030'))
        print('//command')
        element=str(command)
        qinghama_autoobject("command",element,pageurl,"bobsiji@qq.com")

    print('=======================================================datalist')
    nameli = bsobj.findAll("datalist")
    for datalist in nameli:
        print(datalist.prettify().encode('GB18030'))
        print('//datalist')
        element=str(datalist)
        qinghama_autoobject("datalist",element,pageurl,"bobsiji@qq.com")

    print('=======================================================del')
    nameli = bsobj.findAll("del")
    for del1 in nameli:
        print(del1.prettify().encode('GB18030'))
        print('//del')
        element=str(del1)
        qinghama_autoobject("del",element,pageurl,"bobsiji@qq.com")

    print('=======================================================dir')
    nameli = bsobj.findAll("dir")
    for dir in nameli:
        print(dir.prettify().encode('GB18030'))
        print('//dir')
        element=str(dir)
        qinghama_autoobject("dir",element,pageurl,"bobsiji@qq.com")

    print('=======================================================div')
    nameli = bsobj.findAll("div")
    for div in nameli:
        print(div.prettify().encode('GB18030'))
        print('//div')
        element=str(div)
        qinghama_autoobject("div",element,pageurl,"bobsiji@qq.com")

    print('=======================================================footer')
    nameli = bsobj.findAll("footer")
    for footer in nameli:
        print(footer.prettify().encode('GB18030'))
        print('//footer')
        element=str(footer)
        qinghama_autoobject("footer",element,pageurl,"bobsiji@qq.com")

    print('=======================================================form')
    nameli = bsobj.findAll("form")
    for form in nameli:
        print(form.prettify().encode('GB18030'))
        print('//form')
        element=str(form)
        qinghama_autoobject("form",element,pageurl,"bobsiji@qq.com")


    print('=======================================================frame')
    nameli = bsobj.findAll("frame")
    for frame in nameli:
        print(frame.prettify().encode('GB18030'))
        print('//frame')
        element=str(frame)
        qinghama_autoobject("frame",element,pageurl,"bobsiji@qq.com")

    print('=======================================================frameset')
    nameli = bsobj.findAll("frameset")
    for frameset in nameli:
        print(frameset.prettify().encode('GB18030'))
        print('//frameset')
        element=str(frameset)
        qinghama_autoobject("frameset",element,pageurl,"bobsiji@qq.com")


    print('=======================================================iframe')
    nameli = bsobj.findAll("iframe")
    for iframe in nameli:
        print(iframe.prettify().encode('GB18030'))
        print(iframe['href'])
        print('//iframe')
        element=str(iframe)
        qinghama_autoobject("iframe",element,pageurl,"bobsiji@qq.com")

    print('=======================================================h1')
    nameli = bsobj.findAll("h1")
    for h1 in nameli:
        print(h1.prettify().encode('GB18030'))
        print('//h1')
        element=str(h1)
        qinghama_autoobject("h1",element,pageurl,"bobsiji@qq.com")

    print('=======================================================h2')
    nameli = bsobj.findAll("h2")
    for h2 in nameli:
        print(h2.prettify().encode('GB18030'))
        print('//h2')
        element=str(h2)
        qinghama_autoobject("h2",element,pageurl,"bobsiji@qq.com")

    print('=======================================================h3')
    nameli = bsobj.findAll("h3")
    for h3 in nameli:
        print(h3.prettify().encode('GB18030'))
        print('//h3')
        element=str(h3)
        qinghama_autoobject("h3",element,pageurl,"bobsiji@qq.com")

    print('=======================================================h4')
    nameli = bsobj.findAll("h4")
    for h4 in nameli:
        print(h4.prettify().encode('GB18030'))
        print('//h4')
        element=str(h4)
        qinghama_autoobject("h4",element,pageurl,"bobsiji@qq.com")


    print('=======================================================h5')
    nameli = bsobj.findAll("h5")
    for h5 in nameli:
        print(h5.prettify().encode('GB18030'))
        print('//h5')
        element=str(h5)
        qinghama_autoobject("h5",element,pageurl,"bobsiji@qq.com")


    print('=======================================================h6')
    nameli = bsobj.findAll("h6")
    for h6 in nameli:
        print(h6.prettify().encode('GB18030'))
        print('//h6')
        element=str(h6)
        qinghama_autoobject("h6",element,pageurl,"bobsiji@qq.com")

    print('=======================================================img')
    nameli = bsobj.findAll("img")
    for img in nameli:
        print(img.prettify().encode('GB18030'))
        print(img['src'])
        print('//img')
        element=str(img)
        qinghama_autoobject("img",element,pageurl,"bobsiji@qq.com")


    print('=======================================================input')
    nameli = bsobj.findAll("input")
    for input in nameli:
        print(input.prettify().encode('GB18030'))
        print('//input')
        element=str(input)
        qinghama_autoobject("input",element,pageurl,"bobsiji@qq.com")


    print('=======================================================label')
    nameli = bsobj.findAll("label")
    for label in nameli:
        print(label.prettify().encode('GB18030'))
        print('//label')
        element=str(label)
        qinghama_autoobject("label",element,pageurl,"bobsiji@qq.com")

    print('=======================================================lengend')
    nameli = bsobj.findAll("lengend")
    for lengend in nameli:
        print(lengend.prettify().encode('GB18030'))
        print('//lengend')
        element=str(lengend)
        qinghama_autoobject("lengend",element,pageurl,"bobsiji@qq.com")


    print('=======================================================head')
    nameli = bsobj.findAll("head")
    for head in nameli:
        print(head.prettify().encode('GB18030'))
        print('//head')
        element=str(head)
        qinghama_autoobject("head",element,pageurl,"bobsiji@qq.com")

    print('=======================================================header')
    nameli = bsobj.findAll("header")
    for header in nameli:
        print(header.prettify())
        print('//header')
        element=str(header)
        qinghama_autoobject("header",element,pageurl,"bobsiji@qq.com")

    print('=======================================================li')
    nameli = bsobj.findAll("li")
    for li in nameli:
        print(li.prettify().encode('GB18030'))
        print('//li')
        element=str(li)
        qinghama_autoobject("li",element,pageurl,"bobsiji@qq.com")

    print('=======================================================link')
    nameli = bsobj.findAll("link")
    for link in nameli:
        print(link.prettify().encode('GB18030'))
        print(link['href'])
        print('//link')
        element=str(link)
        qinghama_autoobject("link",element,pageurl,"bobsiji@qq.com")

    print('=======================================================map')
    nameli = bsobj.findAll("map")
    for map in nameli:
        print(map.prettify().encode('GB18030'))
        print('//map')
        element=str(map)
        qinghama_autoobject("map",element,pageurl,"bobsiji@qq.com")

    print('=======================================================menu')
    nameli = bsobj.findAll("menu")
    for menu in nameli:
        print(menu.prettify().encode('GB18030'))
        print('//menu')
        element=str(menu)
        qinghama_autoobject("menu",element,pageurl,"bobsiji@qq.com")

    print('=======================================================menuitem')
    nameli = bsobj.findAll("menuitem")
    for menuitem in nameli:
        print(menuitem.prettify().encode('GB18030'))
        print('//menuitem')
        element=str(menuitem)
        qinghama_autoobject("menuitem",element,pageurl,"bobsiji@qq.com")

    print('=======================================================meta')
    nameli = bsobj.findAll("meta")
    for meta in nameli:
        print(meta.prettify().encode('GB18030'))
        print('//meta')
        element=str(meta)
        qinghama_autoobject("meta",element,pageurl,"bobsiji@qq.com")

    print('=======================================================nav')
    nameli = bsobj.findAll("nav")
    for nav in nameli:
        print(nav.prettify().encode('GB18030'))
        print('//nav')
        element=str(nav)
        qinghama_autoobject("nav",element,pageurl,"bobsiji@qq.com")


    print('=======================================================object')
    nameli = bsobj.findAll("object")
    for object in nameli:
        print(object.prettify().encode('GB18030'))
        print('//object')
        element=str(object)
        qinghama_autoobject("object",element,pageurl,"bobsiji@qq.com")

    print('=======================================================ol')
    nameli = bsobj.findAll("ol")
    for ol in nameli:
        print(ol.prettify().encode('GB18030'))
        print('//ol')
        element=str(ol)
        qinghama_autoobject("ol",element,pageurl,"bobsiji@qq.com")


    print('=======================================================option')
    nameli = bsobj.findAll("option")
    for option in nameli:
        print(option.prettify().encode('GB18030'))
        print('//option')
        element=str(option)
        qinghama_autoobject("option",element,pageurl,"bobsiji@qq.com")


    print('=======================================================p')
    nameli = bsobj.findAll("p")
    for p in nameli:
        print(p.prettify().encode('GB18030'))
        print('//p')
        element=str(p)
        qinghama_autoobject("p",element,pageurl,"bobsiji@qq.com")

    print('=======================================================param')
    nameli = bsobj.findAll("param")
    for param in nameli:
        print(param.prettify().encode('GB18030'))
        print('//param')
        element=str(param)
        qinghama_autoobject("param",element,pageurl,"bobsiji@qq.com")


    print('=======================================================samp')
    nameli = bsobj.findAll("samp")
    for samp in nameli:
        print(samp.prettify().encode('GB18030'))
        print('//samp')
        element=str(samp)
        qinghama_autoobject("samp",element,pageurl,"bobsiji@qq.com")


    print('=======================================================script')
    nameli = bsobj.findAll("script")
    for script in nameli:
        print(script.prettify().encode('GB18030'))
        print('//script')
        element=str(script)
        qinghama_autoobject("script",element,pageurl,"bobsiji@qq.com")


    print('=======================================================section')
    nameli = bsobj.findAll("section")
    for section in nameli:
        print(section.prettify().encode('GB18030'))
        print('//section')
        element=str(section)
        qinghama_autoobject("section",element,pageurl,"bobsiji@qq.com")


    print('=======================================================select')
    nameli = bsobj.findAll("select")
    for select in nameli:
        print(select.prettify().encode('GB18030'))
        print('//select')
        element=str(select)
        qinghama_autoobject("select",element,pageurl,"bobsiji@qq.com")


    print('=======================================================span')
    nameli = bsobj.findAll("span")
    for span in nameli:
        print(span.prettify().encode('GB18030'))
        print('//span')
        element=str(span)
        qinghama_autoobject("span",element,pageurl,"bobsiji@qq.com")


    print('=======================================================style')
    nameli = bsobj.findAll("style")
    for style in nameli:
        print(style.prettify().encode('GB18030'))
        print('//style')
        element=str(style)
        qinghama_autoobject("style",element,pageurl,"bobsiji@qq.com")


    print('=======================================================sup')
    nameli = bsobj.findAll("sup")
    for sup in nameli:
        print(sup.prettify().encode('GB18030'))
        print('//sup')
        element=str(sup)
        qinghama_autoobject("sup",element,pageurl,"bobsiji@qq.com")


    print('=======================================================summary')
    nameli = bsobj.findAll("summary")
    for summary in nameli:
        print(summary.prettify().encode('GB18030'))
        print('//summary')
        element=str(summary)
        qinghama_autoobject("summary",element,pageurl,"bobsiji@qq.com")


    print('=======================================================table')
    nameli = bsobj.findAll("table")
    for table in nameli:
        print(table.prettify().encode('GB18030'))
        print('//table')
        element=str(table)
        qinghama_autoobject("table",element,pageurl,"bobsiji@qq.com")


    print('=======================================================td')
    nameli = bsobj.findAll("td")
    for td in nameli:
        print(td.prettify().encode('GB18030'))
        print('//td')
        element=str(td)
        qinghama_autoobject("td",element,pageurl,"bobsiji@qq.com")


    print('=======================================================textarea')
    nameli = bsobj.findAll("textarea")
    for textarea in nameli:
        print(textarea.prettify().encode('GB18030'))
        print('//textarea')
        element=str(textarea)
        qinghama_autoobject("textarea",element,pageurl,"bobsiji@qq.com")


    print('=======================================================th')
    nameli = bsobj.findAll("th")
    for th in nameli:
        print(th.prettify().encode('GB18030'))
        print('//th')
        element=str(th)
        qinghama_autoobject("th",element,pageurl,"bobsiji@qq.com")

    print('=======================================================thead')
    nameli = bsobj.findAll("thead")
    for thead in nameli:
        print(thead.prettify().encode('GB18030'))
        print('//thead')
        element=str(thead)
        qinghama_autoobject("thead",element,pageurl,"bobsiji@qq.com")

    print('=======================================================time')
    nameli = bsobj.findAll("time")
    for time in nameli:
        print(time.prettify().encode('GB18030'))
        print('//time')
        element=str(time)
        qinghama_autoobject("time",element,pageurl,"bobsiji@qq.com")

    print('=======================================================title')
    nameli = bsobj.findAll("title")
    for title in nameli:
        print(title.prettify().encode('GB18030'))
        print('//title')
        element=str(title)
        qinghama_autoobject("title",element,pageurl,"bobsiji@qq.com")

    print('=======================================================tr')
    nameli = bsobj.findAll("tr")
    for tr in nameli:
        print(tr.prettify().encode('GB18030'))
        print('//tr')
        element=str(tr)
        qinghama_autoobject("tr",element,pageurl,"bobsiji@qq.com")

    print('=======================================================ul')
    nameli = bsobj.findAll("ul")
    for ul in nameli:
        print(ul.prettify().encode('GB18030'))
        print('//ul')
        element=str(ul)
        qinghama_autoobject("ul",element,pageurl,"bobsiji@qq.com")

    print('=======================================================var')
    nameli = bsobj.findAll("var")
    for var in nameli:
        print(var.prettify().encode('GB18030'))
        print('//var')
        element=str(var)
        qinghama_autoobject("var",element,pageurl,"bobsiji@qq.com")

    print('=======================================================video')
    nameli = bsobj.findAll("video")
    for video in nameli:
        print(video.prettify().encode('GB18030'))
        print(video['href'])
        print('//video')
        element=str(video)
        qinghama_autoobject("video",element,pageurl,"bobsiji@qq.com")

    print('=======================================================a')
    nameli = bsobj.findAll("a")
    for a in nameli:
        print(a.prettify().encode('GB18030'))
        f.write(a.prettify().encode('GB18030'))
        print(a['href'])
        print('//a')
        element=str(a)
        qinghama_autoobject("a",element,pageurl,"bobsiji@qq.com")
    f.close()

##############################################################################

def getInternalLinks(domainUrl,pageUrl):
    global Internalpages

    allurl = domainUrl + pageUrl;
    try:
        html = urllib.urlopen(allurl)
    except HTTPError as e: 
        print(e)
    else:
        print(html)
    bsobj = BeautifulSoup(html.read(),'lxml')
    pageobj = bsobj.decode('utf-8').encode(type)
    pageurl = domainUrl + pageUrl
    searchpage(bsobj,pageurl)
    for link1 in bsobj.findAll("a",href = re.compile("^/.*")):
        if 'href' in link1.attrs:
            if link1.attrs['href'] not in Internalpages:
                #我们遇到了新页面
                newPage1 = link1.attrs['href']
                print(newPage1)
                print(link1.get_text())
                element=link1.get_text()
                href=str(link1.attrs['href'])
                qinghama_autopage(element,href,"bobsiji@qq.com")
                Internalpages.add(newPage1)
                getInternalLinks(domainUrl,newPage1)
                for link2 in bsobj.findAll("a",href = re.compile("^/.*")):
                    if 'href' in link2.attrs:
                        if link2.attrs['href'] not in Internalpages:
                            #我们遇到了新页面
                            newPage2 = link2.attrs['href']
                            print(newPage2)
                            print(link2.get_text())
                            element=link2.get_text()
                            href=str(link2.attrs['href'])
                            qinghama_autopage(element,href,"bobsiji@qq.com")
                            Internalpages.add(newPage2)
                            getInternalLinks(domainUrl,newPage2)
                            for link3 in bsobj.findAll("a",href = re.compile("^/.*")):
                                if 'href' in link3.attrs:
                                    if link3.attrs['href'] not in Internalpages:
                                        #我们遇到了新页面
                                        newPage3 = link3.attrs['href']
                                        print(newPage3)
                                        print(link3.get_text())
                                        element=link3.get_text()
                                        href=str(link3.attrs['href'])
                                        qinghama_autopage(element,href,"bobsiji@qq.com")
                                        Internalpages.add(newPage3)
                                        getInternalLinks(domainUrl,newPage3)
                                                      

def getExternalLinks(domainUrl):
    global Externalpagess
    #domainUrl = ""
    try:
        html = urllib.urlopen(domainUrl )
    except HTTPError as e: 
        print(e)
    else:
        print(html)
    bsobj = BeautifulSoup(html,'lxml') 
    pageobj = bsobj.decode('utf-8').encode(type)
    for link1 in bsobj.findAll("a", href = re.compile("^(http|www).*")):
        if 'href' in link1.attrs:
            if link1.attrs['href'] not in Externalpages:
                #我们遇到了新页面
                newPage1 = link1.attrs['href']
                print(newPage1)
                Externalpages.add(newPage1)
                getExternalLinks(newPage1)
                for link2 in bsobj.findAll("a", href = re.compile("^(http|www).*")):
                    if 'href' in link2.attrs:
                        if link2.attrs['href'] not in Externalpages:
                            #我们遇到了新页面
                            newPage2 = link2.attrs['href']
                            print(newPage2)
                            Externalpages.add(newPage2)
                            getExternalLinks(newPage2)


######################################################################
def qinghama_versions():
    url="http://qinghama.chinacloudsites.cn/api/TestVersionsAPI"
    values = {
      "TestVersionID": "test",
      "TestVersionName": "test",
      "TestVersionDescription": "test",
      "TestVersionOwner": "bobsiji@qq.com",
      "TestVersionAttachment": "",
      "TestVersionTime": bob,
      "TestVersionStatus": "激活",
      "TestVersionMimeType ": "test",
    }
    jdata = json.dumps(values)
    req = urllib2.Request(url, jdata)
    req.add_header('Content-Type', 'text/json')
    req.get_method = lambda:'POST'
    response = urllib2.urlopen(req)
    resp = response.read()
    print resp


######################################################################
def qinghama_autopage(element,href,user):
    url="http://qinghama.chinacloudsites.cn/api/AutoPagesAPI"
    values = {
      "AutoPageID": "test",
      "AutoPageName": element,
      "AutoPageDescription": href,
      "AutoPageOwner": user ,
      "AutoPageAttachment": "",
      "AutoPageTime": bob,
      "AutoPageStatus": "激活",
      "AutoPageMimeType ": ""
    }

    jdata = json.dumps(values)
    req = urllib2.Request(url, jdata)
    req.add_header('Content-Type', 'text/json')
    req.get_method = lambda:'POST'
    response = urllib2.urlopen(req)
    resp = response.read()
    print resp


######################################################################
def qinghama_autoobject(leixing,element,autopage,user):
    url='http://qinghama.chinacloudsites.cn/api/AutoObjectsAPI'
    values = {
      "AutoObjectID": "test",
      "AutoObjectName": element,
      "AutoObjectDescription": autopage,
      "AutoObjectOwner": user,
      "AutoObjectTime": bob,
      "AutoObjectAttachment": "",
      "AutoObjectStatus": "激活",
      "TestObjectFather ": "test",
      "TestObjectChild ": "test",
      "TestObjectClass ": leixing,
      "ObjectPropertyName1": "",
      "ObjectPropertyValue1": "",
      "ObjectPropertyName2": "",
      "ObjectPropertyValue2": "",
      "ObjectPropertyName3": "",
      "ObjectPropertyValue3": "",
      "ObjectPropertyName4": "",
      "ObjectPropertyValue4": "",
      "ObjectPropertyName5": "",
      "ObjectPropertyValue5": "",
      "ObjectPropertyName6": "",
      "ObjectPropertyValue6": "",
      "ObjectPropertyName7": "",
      "ObjectPropertyValue7": "",
      "ObjectPropertyName8": "",
      "ObjectPropertyValue8": "",
      "ObjectPropertyName9": "",
      "ObjectPropertyValue9": "",
      "ObjectPropertyName0": "",
      "ObjectPropertyValue0": ""
    }
    jdata = json.dumps(values)
    req = urllib2.Request(url, jdata)
    req.add_header('Content-Type', 'text/json')
    req.get_method = lambda:'POST'
    response = urllib2.urlopen(req)
    resp = response.read()
    print resp

                                                  
#qinghama.getpage("http://hama.chinacloudsites.cn")

#qinghama.getInternalLinks("http://qinghama.chinacloudsites.cn","")

#qinghama.getExternalLinks("http://www.jd.com")
