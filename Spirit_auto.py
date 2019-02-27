import selenium as selenium
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import configparser
import time
import os
import urllib.request
from datetime import datetime,timedelta
import json
import ast


class WebInterface:

    def __init__(self):

        self.category_index = 0
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.whitelist = config.get('WebInterface', 'Whitelist').split('//')
        self.load_insist_limit = int(config.get('WebInterface', 'Load Insist Limit'))
        self.image_location = config.get('WebInterface', 'Image Location')

        self.user= config.get('Database', 'User')
        self.password = config.get('Database', 'Password')
        self.database = config.get('Database', 'Database')
        self.url='https://KdgAaabOC:fb5508a2-7280-4c77-9175-b40ddf4ae62f@scalr.api.appbase.io/getspiritedaway_ver14/'

    def get_driver(self):

        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        # options.add_argument("--headless")
        options.add_experimental_option("useAutomationExtension",False)
        options.add_experimental_option("prefs", {"profile.default_content_settings.cookies": 2})
        options.add_argument("--test-type")
        options.add_argument("--start-maximized")
        options.add_argument("--no-first-run")
        options.binary_location = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"

        self.driver = webdriver.Chrome(options=options)

    def go_to(self, link):

        if link != self.driver.current_url:
            self.driver.get(link)

    def enter_text(self, x_path, value, submit=False):

        input_element = self.driver.find_element_by_xpath(x_path)
        input_element.send_keys(value)
        if submit:
            input_element.submit()

    def xpath_click(self, x_path):

        input_element = self.driver.find_element_by_xpath(x_path)
        input_element.click()
        return True

    def button_click(self,css):

        input_element = self.driver.find_element_by_css_selector(css)
        input_element.click()

    def text_click(self, text):

        input_element = self.driver.find_elements_by_tag_name(text)
        input_element.click()

    def select_text(self,x_path,text):

        select=Select(self.driver.find_element_by_xpath(x_path))
        pattern = re.compile(text)
        for option in select.options:
            value = option.get_attribute('value')
            if pattern.search(value):
                option.click()
                break

    def load_insist(self, x_path, value=''):

        refresh = False
        refreshed = False
        element_match = False
        start_time = time.time()
        while not element_match:
            refresh = self.should_browser_refresh(start_time, self.load_insist_limit,refreshed)
            if refresh == True and refreshed == False:
                start_time = time.time()
                self.driver.refresh()
                refresh = False
                refreshed = True
            try:
                target_element = self.driver.find_element_by_xpath(x_path)
                if value in target_element.text:
                    element_match = True
            except NoSuchElementException:
                pass
            time.sleep(0.1)

    def should_browser_refresh(self, start, limit, refreshed):

        if time.time()-start>limit:
            if refreshed:
                raise TimeoutException("Timeout Occured")
            return True
        else:
            return False

    def click_view_more_options(self):

        CATEGORY_XPATH = '//*[@id="mainPageContent"]/div[2]/div[1]/div[1]/div/ul[1]'
        VMO = 'View more options...'

        category_text = self.driver.find_element_by_xpath(CATEGORY_XPATH).get_attribute('textContent')

        if VMO in category_text:
            element = self.driver.find_element_by_link_text(VMO)
            element.click()
        else:
            raise NoSuchElementException("\t'"+VMO+"' was not found")

    def on_whitelist(self, branch):

        return any(x in branch[:, 0].tolist() for x in self.whitelist)
    
    def delimiter(self,text,delimiter,value=None):
        text=str(text)
        text=re.split(delimiter,text)
        if value is not None:
            return text[value]
        return text
    
    def hesitate(self,month,idName,className,tag):
        wait=True
        while wait:
            soup=BeautifulSoup(self.driver.page_source,'html.parser') 
            newMonth=soup.find(id=idName)
            newMonth=newMonth.find(tag,class_=className).text
            if newMonth!=month:
                wait=False
                
            
    def beautify(self,element):
        ans= BeautifulSoup(str(element),'lxml').text
        ans=ans[1:-1]
        return ans.split(', ')
    
    
    def createkey(self,depart,dest):
        return str(self.delimiter(depart,',|/',0))+str(self.delimiter(depart,' ',1)) \
                            +str(self.delimiter(dest,',|/',0))+str(self.delimiter(dest,' ',1))
                            
                            
    def isninedollar(self, redmark, price, date):
        if price=='na':
            price=0
        else:
            price=float('{0:.2f}'.format(float(price.replace("$",""))))
        if str(redmark)=='9FC':
            return float('{0:.2f}'.format(price/0.58))
        return price
    
    
    def save_dates(self,oneLocation=" ",twoLocation=" ",timeFrame=range(2)):
        
        pageDay=[None]*90
        pageDate=[0]*90
        pagePrice=[0]*90
        dict_={}
        dict_2={}
        key_dict=1
        ticker=0
        tick=0
        fuse=False
        data = pd.read_csv("D:\GitHub\Web-Scraper\dataframe.csv",index_col=0) 
        latlon=pd.read_csv("D:\GitHub\Web-Scraper\worldcity_py.csv",index_col=1)
        direct=[1,2]
        description="none"
        siteurl="none"
        #looping through different callendar div tags
        for dc in direct:
            ticker=0
            tick=0
            
            for x in timeFrame:
                #using beautiful soup to parse departing dates
                soup=BeautifulSoup(self.driver.page_source,'html.parser')      
                # finding the depart calendar
                depart=soup.find(id="calendarMarket1")
                #finding the depart month
                departMonth=depart.find("div",class_="cal-date h5").text
                #finding the return calendar
                ret=soup.find(id="calendarMarket2")
                #finding the return month
                returnMonth=ret.find("div",class_="cal-date h5").text
                if dc==1:
                    #finding the day, date and price in respective calendar
                    day=self.beautify(depart.find_all("div",{"class":"day-name"}))
                    
                    date=self.beautify(depart.find_all("div",{"class":"day-number"}))
                    price=self.beautify(depart.find_all("div",{"class":"fare_price"}))
                    redmark=self.delimiter(depart.find_all("div",{"class":"redMarker"}),'"')
                        
                    #print(self.delimiter(date,'>|<'), '\n',self.delimiter(price,'>|<'),'\n',)
                else:
                    day=self.beautify(ret.find_all("div",{"class":"day-name"}))
                    date=self.beautify(ret.find_all("div",{"class":"day-number"}))
                    price=self.beautify(ret.find_all("div",{"class":"fare_price"}))
                    redmark=self.delimiter(ret.find_all("div",{"class":"redMarker"}),'"')
                
                count=0
                redmark_hold=redmark
                redmark=['na']*len(price)
                
                
                for mark in redmark_hold:
                
                    if mark == 'redMarker':
                        redmark[count]='9FC'
                        count+=1
                        
                    elif mark == 'redMarker invisible':
                        redmark[count]='na'
                        count+=1
                
                for r in range(len(price)):
                    #is it 9 dollar fare club 
                    price[r]=self.isninedollar(redmark[r],price[r],date[r])
                        
                
                    
                #return(month,day,date,price)
                for y in range(len(day)):
                    #parsing and checking if there is a price 
                    dayHolder=day[y]
                    
                    if dayHolder == 'na':
                      ticker-=1  
                    
                    else:
                        
                        if fuse:
                            ticker=ticker+tick+1
                            fuse= False
                        
                        if price[y] == 'na':
                            pagePrice[y+ticker]=0 
                        else:
                            #removing dollarsign
                            pagePrice[y+ticker]=price[y]

                        #converting and pasring
                        pageDay[y+ticker]=str(day[y])
                        
                        month=departMonth
                        depart=oneLocation
                        dest=twoLocation
                        # creating primary key
                        key=self.createkey(depart,dest)
                        onekey=key
                        
                        
                        if dc==2:
                            depart=twoLocation
                            dest=oneLocation
                            key=self.createkey(depart,dest)
                            twokey=key
                            month=returnMonth
                            
                        
                        #correcting date for elastic search to be in yyyy-mm-dd format
                        if len(date[y])==1:
                            date[y]="0"+date[y]
                            
                            
                        pageDate[y+ticker]="2019-"+self.dateCreate(month)+"-"+date[y]
                                            
                        #finding longitube and latitude
                        if str(self.delimiter(depart,",|/",0))  in latlon.index:
                            res=latlon.loc[str(self.delimiter(depart,",|/",0))]
                            if len(str(self.delimiter(depart,"[ (]| ,",1)))==2:
                                country="United States "
                            elif len(str(self.delimiter(depart,",|/",1)))>3:
                                country=str(self.delimiter(depart,"[(]|, ",1))
                            if res.size>9:
                                lat=res['lat'].loc[res['country']==country[:-1]][0]
                                lon=res['lng'].loc[res['country']==country[:-1]][0]
                            else:
                                lat=res['lat']
                                lon=res['lng']
                        else:
                            continue
                        
                        
                        if dest in data.index:
                            res=data.loc[dest]
                            description=res[0]
                            siteurl=res[1]
                            
                        else:
                            continue
                
                #change months
                if dc==1:
                    self.xpath_click('//*[@id="linkButtonNextMonth1"]')
                    self.hesitate(departMonth,"calendarMarket1","cal-date h5","div")
                
                if dc==2:
                    self.xpath_click('//*[@id="linkButtonNextMonth2"]')
                    self.hesitate(returnMonth,"calendarMarket2","cal-date h5","div")
            
                
                #reset ticker
                tick=y+ticker
                ticker=0
                fuse=True
                
            #finding min price
            arr=np.ma.masked_equal(pagePrice,0,copy=False)
            
            minPrice=arr.min()
            
            try:
                #picking Date
                Date=pageDate[pagePrice.index(minPrice)]
            except ValueError:
                key_dict=key_dict+1
                return
            
            #reset ticker
            tick=y+ticker
            ticker=0
                    
            try:
                dict_[key_dict]=self.save_to_dict(key,depart,dest,description,siteurl,str(departMonth), returnMonth, pageDay, pageDate, pagePrice,minPrice,lat,lon,Date)
            except (UnboundLocalError, KeyError, TypeError):
                return
            key_dict=key_dict+1 
            
            
        dict_2[key_dict-2],dict_2[key_dict-1]=self.returndates(dict_[key_dict-2],dict_[key_dict-1])
        
        val=[onekey,twokey]
        
        for key in dict_.keys():
            try:
                dict_[key]['returnDate']=str(dict_2[key]['returnDate'])
            except (UnboundLocalError, KeyError, TypeError):
                return
            dict_[key]['returnPrice']=str(dict_2[key]['returnPrice'])
            print('\n\n'+str(dict_[key])+'\n\n')
            print('\n'+val[key-1]+'\n')
            self.send_json(dict_[key],val[key-1])
            
         
        #self.print_branch(branch, "Saving Ad image locally...")
        #image_loc = self.save_image(ad_id,branch_str)

        #self.print_branch(branch,"Saving Ad to SQL...")
        #self.save_ad_to_sql(depart,dest, month, day, date, price,departTime,arrivalTime)

    
    def send_json(self,payload,key):
        url=self.url+"_bulk"
        payload="{ \"index\": { \"_type\": \"users\", \"_id\": \""+key+"\" } }\n"\
                "{ \"depart\": \""+str(payload['depart'])+"\","\
                "\"dest\":\""+str(payload['dest'])+"\","\
                "\"url\":\""+str(payload['url'])+"\","\
                "\"description\":\""+str(payload['description'])+"\","\
                "\"Prices\": \""+str(payload['Prices'])+"\","\
                "\"Dates\": \""+str(payload['Dates'])+"\","\
                "\"Date\": \""+str(payload['Date'])+"\","\
                "\"miniPrice\": \""+str(payload['miniPrice'])+"\","\
                "\"returnDate\": \""+str(payload['returnDate'])+"\","\
                "\"returnPrice\": \""+str(payload['returnPrice'])+"\","\
                "\"loc\":{\"lat\":"+json.dumps(payload['loc']['lat'])+",\"lon\":"+json.dumps(payload['loc']['lon'])+"},"\
                "\"departmonth\":\""+str(payload['departmonth'])+"\"}\n"
        response=requests.request('POST',url,data=payload.encode('utf-8'), allow_redirects=False)
        
        try:
            print(response.json())
        except json.decoder.JSONDecodeError:
            return
    
    
    def save_to_dict(self,key, depart, dest,description,siteurl, departmonth, returnmonth, day, pageDate, pagePrice,minPrice,lat,lon,Date):
       
        payload="{ \"depart\": \""+str(depart)+"\","\
                "\"dest\":\""+str(dest)+"\","\
                "\"url\":\""+str(siteurl)+"\","\
                "\"description\":\""+str(description.replace("\n"," "))+"\","\
                "\"Prices\": \""+str(pagePrice)+"\","\
                "\"Dates\": \""+str(pageDate)+"\","\
                "\"Date\": \""+str(Date)+"\","\
                "\"miniPrice\": \""+str(minPrice)+"\","\
                "\"returnDate\": \""+str(Date)+"\","\
                "\"returnPrice\": \""+str(minPrice)+"\","\
                "\"loc\":{\"lat\":"+json.dumps(lat)+",\"lon\":"+json.dumps(lon)+"},"\
                "\"departmonth\":\""+str(departmonth)+"\"}"
        try:
            return(json.loads(payload))
        except json.decoder.JSONDecodeError:
            return

    def returndates(self,codict,ctdict):

        coDates=codict["Dates"]
        coPrices=codict["Prices"]
        coDate=codict["Date"]  
        

        ctDates=ctdict["Dates"]
        ctPrices=ctdict["Prices"]
        ctDate=ctdict["Date"]
        
        coretdate=ast.literal_eval(ctDates)
        ctPrices=ast.literal_eval(ctPrices)
        try:
            coretprice=min(price for price in ctPrices[coretdate.index(coDate)+4:coretdate.index(coDate)+16] if price > 0)
        except ValueError:
            return([0],[0])
        fixed=ctPrices[coretdate.index(coDate)+4:coretdate.index(coDate)+16]
        coretdate=coretdate[coretdate.index(coDate)+4:coretdate.index(coDate)+16]
        coretdate=coretdate[fixed.index(coretprice)]
        print(coDate,coretdate)
        
        ctretdate=ast.literal_eval(coDates)
        coPrices=ast.literal_eval(coPrices)
        
        try:
            ctretprice=min(price for price in coPrices[ctretdate.index(ctDate)+4:ctretdate.index(ctDate)+16] if price > 0)
        except ValueError:
            return([0],[0])
        fixed=coPrices[ctretdate.index(ctDate)+4:ctretdate.index(ctDate)+16]
        ctretdate=ctretdate[ctretdate.index(ctDate)+4:ctretdate.index(ctDate)+16]
        ctretdate=ctretdate[fixed.index(ctretprice)]
        print(ctDate,ctretdate)
        
        return({'returnDate':coretdate,'returnPrice':coretprice}, \
               {'returnDate':ctretdate,'returnPrice':ctretprice})
        
        
    def mapping(self):
        url=self.url+"_mapping/users"
        payload="{\n \"properties\":{\n \"loc\":{\n      \"type\": \"geo_point\"\n    },\n"\
            "\"miniPrice\":{\n      \"type\": \"integer\"\n    },\n"\
            "\"returnPrice\":{\n      \"type\": \"integer\"\n    }\n"\
            "}\n}"
        response=requests.request('PUT',url,data=payload, allow_redirects=False)
        print(response.json())
    
    def dateCreate(self,month):
        monthes={'JANUARY ':'01',
                 'FEBRUARY ':'02',
                 'MARCH ':'03',
                 'APRIL ':'04',
                 'MAY ':'05',
                 'JUNE ':'06',
                 'JULY ':'07',
                 'AUGUST ':'08',
                 'SEPTEMBER ':'09',
                 'OCTOBER ':'10',
                 'NOVEMBER ':'11',
                 'DECEMBER ':'12'}
        
        return monthes[month]
    
class EndOfBranch(Exception):
    """Basic exception for reaching the end of a branch during recursion"""
    def __init__(self, branch, msg=None):
        if msg is None:
            msg = "End of branch exception caught at " + str(branch)
        super(EndOfBranch, self).__init__(msg)
        self.branch = branch

class AdError(Exception):
    """Basic exception for an error occuring on the ad level"""
    def __init__(self, branch, msg=None):
        if msg is None:
            msg = "Error extracting ad at: " + str(branch)
        super(EndOfBranch, self).__init__(msg)
        self.branch = branch

if __name__ == "__main__":
     
    #restart
    restart ="y"
    
    if restart=="y" or restart=="Y":
        xx=53
        yy=1
    else:
        xx=int(input('x:'))
        yy=int(input('y:'))
    # Instantiate Web Interface
    WI = WebInterface()
    
    WI.mapping()

    print("Instantiating the web driver...")

    # Instantiate the web driver
    WI.get_driver()

    print("Navigating to the first category...")
    # Navigate to Spirit
    WI.go_to('http://www.spirit.com/Default.aspx')
    
    #collecting destination data
    #using beautiful soup to parse departing dates
    soup=BeautifulSoup(WI.driver.page_source,'html.parser')
    # depart locations
    flocations=soup.find("select",{"id":"departCityCodeSelect"})
    flocations=WI.delimiter(flocations,'<option>|</option>')
    fcities=[]
    
    
    for x in range(1,len(flocations)-1):
        fcities.append(WI.delimiter(flocations[x],'>',1))
    
    #looping departure cities 
    for xvalue in range(xx,int(len(fcities))):
        
        
        WI.go_to('https://www.spirit.com/Default.aspx')
        
        # Entering Depature Location
        WI.xpath_click('//*[@id="departCityCodeSelect"]/option['+str(xvalue+2)+']')
        
        #collecting destination data
        #using beautiful soup to parse departing dates        soup=BeautifulSoup(WI.driver.page_source,'html.parser')
        soup=BeautifulSoup(WI.driver.page_source,'html.parser')
        # to locations
        dlocations=soup.find("select",{"id":"destCityCodeSelect"})
        dlocations=WI.delimiter(dlocations,'<option>|</option>')
        dcities=[]
        
        print(xvalue)
        #appending depatrue city locations
        for x in range(1,len(dlocations)-1):
            dcities.append(WI.delimiter(dlocations[x],'>',1))   
        #for value in [x for x in range(2,80) if x != 26]:
        for yvalue in range(yy,len(dcities)):
            try:
                # Navigate to Spirit
                WI.go_to('https://www.spirit.com/Default.aspx')
                
                #Enter Initial Location
                WI.xpath_click('//*[@id="departCityCodeSelect"]/option['+str(xvalue+2)+']')
                                    
                # Entering Destination
                WI.xpath_click('//*[@id="destCityCodeSelect"]/option['+str(yvalue+2)+']')
                
                # Choosing Dates
                current_time = datetime.now()
                weeklater_time=current_time+timedelta(days=7)
                #Depature
                WI.enter_text('//*[@id="departDate"]',current_time.strftime('%m/%d/%Y'))
                #Return
                WI.enter_text('//*[@id="returnDate"]',weeklater_time.strftime('%m/%d/%Y'))
                #Enter
                
                WI.xpath_click('//*[@id="book-travel-form"]/div/p/button')
                        
                #Catch pop up button 
                try:
                    if WI.xpath_click('//*[@id="closeButton_cityPair"]')==True:
                        WI.driver.refresh()
                        yvalue=yvalue-1
                        continue
                except (ElementNotVisibleException, NoSuchElementException):
                    pass
                
                #Collecting Data
                #load results
                #WI.load_insist('//*[@id="content"]/div[2]/div[2]/header/h2','Flight Availability')
                
                try:
                    WI.xpath_click('//*[@id="calendarMarket1"]/div[2]/div[2]/div[1]/div[2]')
                except (NoSuchElementException):
                    yvalue=yvalue-1
                    WI.driver.refresh()
                    continue
                    
                #WI.load_insist('//*[@id="content"]/div[2]/div[2]/header/h2','Flight Availability')
                try:
                    WI.save_dates(fcities[xvalue],dcities[yvalue])
                except:
                    continue
            
            except (ElementNotVisibleException):
                WI.xpath_click('//*[@id="content"]/div[7]/div[1]/div/img')
 
    # Close/kill the driver
    WI.driver.quit()
