#현재 폴더 내의 pdf 문서를 읽어 csv로 정리하는 파일.
import re
import os
import pdfminer
import pdfminer.high_level
import csv

csv_f = open("poets.csv","w",encoding='utf-8',newline="")
csv_wr = csv.writer(csv_f)

filelist = os.listdir('.')
for path in filelist:
    filename,extension = os.path.splitext(path)
    if extension == '.pdf':
        #파일 이름은 다음과 같이 구성되어 있음
        #시제목#작가#시텍스트#저작권.pdf
        #'#'문자를 구분자로 분리하여 file_info에 정리.
        file_info = filename.split('#')
        poet_name = file_info[0]
        poet_writer = file_info[1]
        poet_cc = file_info[2]
        poet_text = pdfminer.high_level.extract_text(path)
        #\f(폼피드)문자는 절대 쓸일이 없기에 정규식으로 지금 지운다.
        poet_text = re.sub(pattern='[\f]',repl='',string=poet_text)
        #시제목|작가|시텍스트|저작권
        row = [poet_name,poet_writer,poet_text,poet_cc]
        csv_wr.writerow(row)
