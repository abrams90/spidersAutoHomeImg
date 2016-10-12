#-*-coding:utf-8-*-
# 声明编码方式 默认编码方式ASCII 参考https://www.python.org/dev/peps/pep-0263/
import urllib
import time
import re
import os
from bs4 import BeautifulSoup
import BeautifulSoup
import sys
from selenium import webdriver        
from selenium.webdriver.common.keys import Keys        
import selenium.webdriver.support.ui as ui        
from selenium.webdriver.common.action_chains import ActionChains




#通过正则式取得连接
def getImg_brand(html):
    #<li id='b14'><h3><a href='/pic/brand-14.html'><i class='icon10 icon10-sjr'></i>本田<em>(72199)</em></a></h3></li>
    #reg = r'(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')'
    reg = r'<a href=\'(.+?)\'>.+?</i>(.+?)<em>'#/w+</i>\w+<em>'
   # result = map(lambda name: re.sub("<a href=.*?>","",name.strip().replace("</a>","")), re.findall("<a href=.*?>.*?</a>",html))
    imgre = re.compile(reg)
    imglist = re.findall(imgre,html)
    return imglist 

def getImg_series(html):
    #<a href="/pic/series/3859.html#pvareaid=2042214"  title="东风本田 哥瑞的图片">哥瑞</a>
    #reg = r'(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')'
    reg = r'<div><span class="fn-left"><a href=\"(.+?)\".+?>(.+?)</a>'#/w+</i>\w+<em>'
    imgre = re.compile(reg)
    imglist = re.findall(imgre,html)
    return imglist 

def getImg_type(html):
    #<a href="/pic/series/3674-1.html#pvareaid=2042222">车身外观</a><span class="uibox-title-font12"> (4张) </span><a href="/pic/series/3674-1.html#pvareaid=2042222" class="more">更多&gt;&gt;
    #reg = r'(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')'
    #<a href="/pic/series/3674-1.html#pvareaid=2042220">车身外观
    #reg = r'车身外观</a>.+?</span><a href=\"(.+?)\" class=\"more\">'#/w+</i>\w+<em>' "choise-cont ma-b-10"
    reg = r'<div class="choise-cont-text"><a href=\"(.+?)\">'
    imgre = re.compile(reg)
    imglist = re.findall(imgre,html)
    return imglist 

def getMiniImg(html):
    #<a href="/photo/series/21066/1/2776856.html" title="ABT ABT S1 2015款 Sportback"
    #reg = r'车身外观</a>.+?</span><a href=\"(.+?)\" class=\"more\">'#/w+</i>\w+<em>' "choise-cont ma-b-10"
    reg = r'<div><a href=\"(\/.+?\.html)\" title=\"(.+?)\" target=.+?>'
    imgre = re.compile(reg)
    imglist = re.findall(imgre,html)
    return imglist 

def getImgUrl(html):
    #<a href="/photo/series/21066/1/2776856.html" title="ABT ABT S1 2015款 Sportback"
    #<img src="http://car1.autoimg.cn/upload/2014/11/22/2014112211215143726411.jpg"
    #<img id="img" src="http://car0.autoimg.cn/upload/spec/10388/u_20110627171714683240.jpg" onside="-1" />
    # <img src="http://car1.autoimg.cn/upload/spec/10388/u_20110627171509261240.jpg" style="display: none" border="0" />
    #reg = r'<img src=\"(.+?\.jpg)\"'
    reg = r'<img id=\"img\" src=\"(.+?.jpg)\"'
    imgre = re.compile(reg)
    imglist = re.findall(imgre,html)
    return imglist 

def getNextPage(html):
    #<a href="/photo/series/21066/1/2776856.html" title="ABT ABT S1 2015款 Sportback"
    #<a class="page-item-next" href="/pic/series/3126-1-p2.html">下一页</a>

    reg = r'<a class="page-item-next" href=\"(.+?\.html)\">.+?</a>'
    imgre = re.compile(reg)
    imglist = re.findall(imgre,html)
    return imglist 

def mutiPage(nextpage,vtminiPList,fileurl):
    nextpageshow = "http://car.autohome.com.cn"+str(nextpage[0].decode("gb2312").encode("utf-8"))
    fileurl.write("http://car.autohome.com.cn"+str(nextpage[0].decode("gb2312").encode("utf-8"))+'\n')#
    print nextpageshow.decode("utf-8").encode(sys.getfilesystemencoding())
    
    driver.get(nextpageshow)

    content_type = driver.page_source

    nextminiPicList = getMiniImg(content_type)

    nextpage = getNextPage(content_type)

    if not nextpage :
        del nextpage[:]


    vtminiPList.extend(nextminiPicList)

    return nextpage

'''
**************************************************
#第一步 遍历获取每个品牌的URL
#http://car.autohome.com.cn/AsLeftMenu/As_LeftListNew.ashx?typeId=2%20&brandId=0%20&fctId=0%20&seriesId=0
**************************************************
'''

reload(sys)
sys.setdefaultencoding('utf-8')

htmlSource = urllib.urlopen("http://car.autohome.com.cn/AsLeftMenu/As_LeftListNew.ashx?typeId=2%20&brandId=0%20&fctId=0%20&seriesId=0").read()
#soup = BeautifulSoup.BeautifulSoup(htmlSource)
#for item in soup.fetch('a'):#a
#    print item["href"]#href

driver = webdriver.PhantomJS()#executable_path="G:\python\phantomjs-2.1.1-windows\bin\phantomjs.exe"
wait = ui.WebDriverWait(driver,100) 

baseSavePath = 'P:\\frontRearData\\autohome\\'

##日志
logger = open('loger.txt','w')

###设置这个值，接着之前的品牌开始
lastbrand = '宝骏'
lastbrand=lastbrand.decode("utf-8").encode(sys.getfilesystemencoding())
print lastbrand

'''
if os._exists('brandlist.txt'):
   brandtxt = open('brandlist.txt','r')

   while True:
        line = brandtxt.readline()
        if line:
           lastbrand = line.decode("utf-8").encode(sys.getfilesystemencoding())
        else:
           break

   brandtxt.close()
'''
brandtxt = open('brandlist.txt','w')

'''
if not lastbrand == '':
   brandtxt.read()
'''

fileurl=open('autohome_url.txt','w')
fileurl.write('****************获取汽车之家车辆品牌URL*************\n\n') 

temp = 'http://car.autohome.com.cn/AsLeftMenu/As_LeftListNew.ashx?typeId=2%20&brandId=0%20&fctId=0%20&seriesId=0_'
content_main = urllib.urlopen(temp).read()

brandlist = getImg_brand(content_main)

for brand in brandlist:
    fileurl.write("http://car.autohome.com.cn"+str(brand[0].decode("gb2312").encode("utf-8")) + " brand:" +  str(brand[1].decode("gb2312").encode("utf-8")) +'\n')
    show = "http://car.autohome.com.cn"+str(brand[0].decode("gb2312").encode("utf-8"))#+ " " +  str(brand[1].decode("gb2312").encode("utf-8"))
    print show.decode("utf-8").encode(sys.getfilesystemencoding())

    brandname = str(brand[1].decode("gb2312").encode(sys.getfilesystemencoding()))
   
    if not lastbrand == '':
        #print brandname,lastbrand
        if not lastbrand == brandname:
            continue 
        else:
            lastbrand =''

    brandtxt.write(str(brand[1].decode("gb2312").encode("utf-8")) +'\n')

    brandsaveName = brandname.replace('.','')
    brandsaveName = brandsaveName.replace(' ','')
    brandsaveName  = brandsaveName.replace('·','')
    brandsaveName  = brandsaveName.replace('?','')

    brandPath = baseSavePath + brandsaveName

    print brandPath

    if not os.path.exists(brandPath):#.decode(sys.getfilesystemencoding()).encode("utf-8")
           os.makedirs(brandPath)


    #读取品牌URL
    content_brand = urllib.urlopen(show.decode("utf-8").encode(sys.getfilesystemencoding())).read()
    
    seriesList = getImg_series(content_brand)

    for series in seriesList:
        fileurl.write("http://car.autohome.com.cn"+str(series[0].decode("gb2312").encode("utf-8")) + " " +  str(series[1].decode("gb2312").encode("utf-8")) +'\n')
        seriesShow = "http://car.autohome.com.cn"+str(series[0].decode("gb2312").encode("utf-8"))


        seriesName = str(series[1].decode("gb2312").encode(sys.getfilesystemencoding()))
        seriesName=seriesName.replace(brandname+'',brandsaveName+'-')
        seriesName=seriesName.replace(' ','')
        seriesName=seriesName.replace('.','')
        seriesName  = seriesName.replace('?','')
        seriesName  = seriesName.replace(':','')
        #seriesName.replace("","")

        brandtxt.write(seriesName.decode(sys.getfilesystemencoding()).encode("utf-8"))

        seriesPath = brandPath + "\\"+seriesName

        print seriesName

        if not os.path.exists(seriesPath):
            os.makedirs(seriesPath)


        print seriesShow.decode("utf-8").encode(sys.getfilesystemencoding())
        
        #读取车系URL
        #content_series = urllib.urlopen(seriesShow.decode("utf-8").encode(sys.getfilesystemencoding())).read()
        driver.get(seriesShow)

        content_series = driver.page_source

        vechileTypeList = getImg_type(content_series)#车身外观
        
        for vechileType in vechileTypeList:
            fileurl.write("http://car.autohome.com.cn"+str(vechileType.decode("gb2312").encode("utf-8"))+'\n')#
            typeShow = "http://car.autohome.com.cn"+str(vechileType.decode("gb2312").encode("utf-8"))#
            print typeShow.decode("utf-8").encode(sys.getfilesystemencoding())

            driver.get(typeShow)

            content_type = driver.page_source

            vtminiPList = getMiniImg(content_type)

            nextpage = getNextPage(content_type)

            while nextpage:
                nextpage = mutiPage(nextpage,vtminiPList,fileurl)

            for vtminiP in vtminiPList:
                fileurl.write("http://car.autohome.com.cn"+str(vtminiP[0].decode("gb2312").encode("utf-8"))+" "+str(vtminiP[1])+'\n')#
                typeName = str(vtminiP[1])#.decode("gb2312").encode("utf-8"))
                miniPShow = "http://car.autohome.com.cn"+str(vtminiP[0].decode("gb2312").encode("utf-8"))#
                print miniPShow.decode("utf-8").encode(sys.getfilesystemencoding())

                
                imgcontent = urllib.urlopen(miniPShow.decode("utf-8").encode(sys.getfilesystemencoding())).read()
                imgUrl = getImgUrl(imgcontent)

                if imgUrl:
                   fileurl.write(str(imgUrl[0].decode("gb2312").encode("utf-8")) + '\n')#
                   urlShow = str(imgUrl[0].decode("gb2312").encode("utf-8"))
                   print imgUrl[0].decode("utf-8").encode(sys.getfilesystemencoding())

                   filename = os.path.basename(urlShow) #去掉目录路径,返回文件名
                   
                   
                   if os._exists(seriesPath + '\\'+filename):
                       print 'exist \n'
                   else:
                       try:
                          urllib.urlretrieve(urlShow, seriesPath + '\\'+filename)
                       except (urllib.ContentTooShortError, IOError), e:
                         # logger.log("Error downloading NZB: " + str(sys.exc_info()) + " - " + ex(e), logger.ERROR)
                          if os.path.exists(seriesPath + '\\'+filename):
                             os.remove(seriesPath + '\\'+filename)
                             time.sleep(1)

                       time.sleep(0.1)

              

fileurl.close()
brandtxt.close()
logger.close()

print "finish!"

