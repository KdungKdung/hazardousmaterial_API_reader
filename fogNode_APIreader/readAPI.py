import urllib.request
from bs4 import BeautifulSoup

#CASNO를 먼저 조회하고, 그 CAS NO를 이용해 방재법을 조회해야한다.

#API접속 KEY
url = 'http://hazmat.mpss.kfi.or.kr/openapi-data/service/MaterialInfoSvc/getMaterialList?'
key = '&ServiceKey=jpYEvRS91GbTo4z5QJzQ1PZNzWR4yOLhs3sIk6YLtFTYasIVcInx1D784oB7zj%2F9a25TgLsrCS6wGBgPtogTqA%3D%3D&jpYEvRS91GbTo4z5QJzQ1PZNzWR4yOLhs3sIk6YLtFTYasIVcInx1D784oB7zj%2F9a25TgLsrCS6wGBgPtogTqA%3D%3D'

casno_dic = {}

def make_casno_dic():

    request = urllib.request.Request('http://hazmat.mpss.kfi.or.kr/openapi-data/service/MaterialInfoSvc/getMaterialList?pageNo=1&numOfRows=99999'+key)
    request.get_method = lambda: 'GET'
    response_body = urllib.request.urlopen(request).read()

    u = str(response_body, "utf-8")
    soup = BeautifulSoup(u, 'html.parser')

    #print(soup.prettify()) # soup를 정렬해서 출력해준다!
    casno_list = soup.find_all('casno')
    chemicalname_list = soup.find_all('chemicalname')

    for i in range(len(casno_list)):
        casno_dic[chemicalname_list[i].text] = casno_list[i].text

    print(casno_dic)

def read_emergencyaction(materialkorname):

    tempdata={}

    make_casno_dic()
    material_casno = casno_dic[materialkorname]

    request = urllib.request.Request(' http://hazmat.mpss.kfi.or.kr/openapi-data/service/MaterialInfoSvc/getMaterialInfo?casNo='+material_casno+'&ServiceKey=jpYEvRS91GbTo4z5QJzQ1PZNzWR4yOLhs3sIk6YLtFTYasIVcInx1D784oB7zj%2F9a25TgLsrCS6wGBgPtogTqA%3D%3D&&pageNo=1&numOfRows=1')
    request.get_method = lambda: 'GET'
    response_body = urllib.request.urlopen(request).read()
    u = str(response_body, "utf-8")

    soup=BeautifulSoup(u,'html.parser')

   # print(soup.prettify())

    tempdata['METERIALKORNAME'] = materialkorname
    tempdata['emergencymeasures'] = soup.find('emergencymeasures').text
    tempdata['permeatedmouse'] = soup.find('permeatedmouse').text
    tempdata['permeatedskin'] = soup.find('permeatedskin').text

   # print(tempdata)
    return tempdata

#read_emergencyaction('질산')