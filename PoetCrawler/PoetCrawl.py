#공유마당 사이트에서 시 태그가 달린 파일을 수집하는 코드.
from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import gzip
import csv
import pdfminer
import pdfminer.high_level

max_page = 1740
#max_page = 1

csv_f = open("poets.csv","w",encoding='utf-8',newline="")
csv_wr = csv.writer(csv_f)

for p_n in range(1,max_page + 1):
    url = """https://gongu.copyright.or.kr/gongu/search/search/list.do?menuNo=200070&kwd=%EC%8B%9C&category=TEXT&subCategory=ALL&reSrchFlag=false&pageNum=""" \
        + str(p_n) \
            + """&pageSize=16&detailSearch=false&srchFd=all&sort=regist&date=all&startDate=&endDate=&fileExt=all&writer=&year=all&callLoc=&imageRowNo=0&startYear=&endYear=&usePurps=&copyType=&usageRange=&copyType_1d=&copyType_2d=&licenseCd=&licensePart=&wrtTy=&depth2ClSn=&preKwd=%EC%8B%9C
"""
    res = urllib.request.urlopen(url)
    html = res.read()
    bs = BeautifulSoup(html,'html.parser')
    poet_ul = bs.select("#contents > div.key_container > div.keycontent.type5.clearfix > div.font_list_box > div.bbsList.style2 > ul > li")
    for poet_li in poet_ul:
        is_poet = False
        tags = []
        #시 태그가 붙어있는지 확인하고, 시 태그가 붙어있지 않을 경우 처리하지 않고 다음 링크로 넘어갑니다.
        try:
            tags_ul = poet_li.select("div:nth-child(3) > div.col-md-9 > div > ul > a")
            for tag_a in tags_ul:
                tag = tag_a.getText()
                if tag == "#시":
                    is_poet = True
                else:
                    tags.append(tag)
        except:
            continue
        if is_poet == False:
            continue

        poet_name = poet_li.select_one("div:nth-child(1) > div.col-md-8 > span.tit > a").getText()
        poet_writer = poet_li.select_one("div:nth-child(1) > div.col-md-4.tar > span > span").getText()
        poet_cc = poet_li.select_one("div:nth-child(1) > div.col-md-4.tar > img").attrs.get("alt",None)
        poet_text = ""

        poet_n = str(poet_li.attrs.get("data-value",None))
        poet_f_url = "https://gongu.copyright.or.kr/gongu/wrt/cmmn/wrtFileDownload.do?wrtSn="+ poet_n +"&fileSn=1&wrtFileTy=01"
        try:
            poet_comp = urllib.request.urlopen(poet_f_url).read()
            poet_dcomp = gzip.decompress(poet_comp)
            file_name = poet_name + "#"+ poet_writer + "#" + poet_cc +".pdf"
            with open(file_name,"wb") as f:
                f.write(poet_dcomp)
            poet_text = pdfminer.high_level.extract_text(file_name)
            row = [poet_name,poet_writer,poet_text,poet_cc]
            csv_wr.writerow(row)

        except Exception as e:
            print(poet_n + " download failed.") 
            print(e)