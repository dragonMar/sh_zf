import requests
import re
from bs4 import BeautifulSoup as bs
from conn_sql import conn_sql
import datetime
base_url = 'http://sh.lianjia.com/zufang'
district = ''
targe = ''


def getOneDistrict(url):
    global targe
    try:
        page = requests.get(url)
        soup = bs(page.content, 'lxml')
        div = soup.find('div', {'class': re.compile('sub-option-list')})
        aList = div.findAll('a')
        del aList[0]
        for a in aList:
            targe = a.get_text().strip()
            new_url = 'http://sh.lianjia.com' + a.get('href')
            num = getPageNum(new_url)
            print(targe)
            for i in range(1, int(num) + 1):
                print("%s/%s" % (i, num))
                getOneList(new_url+'d'+str(i))
            break
    except Exception as e:
        print(e)


def getDistrict():
    global base_url,district
    try:
        page = requests.get(base_url)
        soup = bs(page.content, 'lxml')
        div = soup.find('div', {'class': re.compile('option-list')})
        aList = div.findAll('a')
        del aList[0]
        for a in aList:
            district = a.get_text().strip()
            new_url = 'http://sh.lianjia.com' + a.get('href')
            print(district)
            getOneDistrict(new_url)
            break
    except Exception as e:
        print(e)


def getPageNum(url):
    page = requests.get(url)
    soup = bs(page.content, 'lxml')
    div = soup.find('div', {'class': re.compile('house-lst-page-box')})
    aList = div.findAll('a')
    return aList[-2].get_text().strip()


def getOneList(url):
    global district,targe
    page = requests.get(url)
    soup = bs(page.content, 'lxml')
    div = soup.find('div', {'class': 'list-wrap'})
    liList = div.findAll('li')
    # print(len(liList))
    for li in liList:
        data = {}
        _div = li.find('div', {'class': 'info-panel'})
        a = _div.find('a', {'name': 'selectDetail'})
        data['url'] = a.get('href')
        data['title'] = a.get('title').strip()
        div_col_1 = _div.find('div', {'class': 'col-1'})
        span_col_1 = div_col_1.findAll('span')
        data['name'] = span_col_1[0].get('title').strip()
        data['room'] = re.search('(\d)室',span_col_1[1].get_text()).group(1)
        data['toilet'] = re.search('(\d)厅',span_col_1[1].get_text()).group(1)
        data['area'] = re.search('(\d+)平',span_col_1[2].get_text()).group(1)
        div_other = _div.find('div', {'class': 'other'})
        data['district'] = district
        data['height'] = re.search('(\d+)层', div_other.get_text()).group(1)
        try:
            data['direction'] = re.search('朝(.*)',div_other.get_text()).group(1)
        except:
            data['direction'] = ''
        div_chanquan = _div.find('div', {'class':'chanquan'})
        try:
            data['distance'] = re.search('(\d+)米', div_chanquan.get_text()).group(1)
        except:
            data['distance'] = 0
        div_col_3 = _div.find('div', {'class': 'col-3'})
        data['price'] = div_col_3.find('span', {'class': 'num'}).get_text()
        data['updatetime'] = re.search('(\d+\.\d+\.\d+)', div_col_3.find('div', {'price-pre'}).get_text()).group(1)
        data['longitude'], data['latitude'] = getAddress(data['url'])
        data['createtime'] = datetime.datetime.now().strftime('%Y-%m-%d')
        data['status'] = 0
        data['lroom'] = 0
        data['sfzz'] = 0
        data['targe'] = targe
        sql = "insert into lianjia VALUES (%(url)s,%(title)s,%(name)s,%(updatetime)s,%(createtime)s,%(price)s," \
              "%(status)s, %(longitude)s, %(latitude)s, %(area)s, %(room)s, %(lroom)s, %(toilet)s," \
              "%(sfzz)s, %(height)s, %(direction)s, %(distance)s, %(district)s, %(targe)s)"
        conn_sql(sql, data)


def getAddress(url):
    s_url = 'http://sh.lianjia.com'
    new_url = s_url + url
    page = requests.get(new_url)
    soup = bs(page.content, 'lxml')
    div = soup.find('div', {'id': 'zoneMap'})
    return [div.get('longitude'), div.get('latitude')]


def main():
    getDistrict()


if __name__ == '__main__':
    main()