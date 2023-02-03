import os
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd

roll_no = 2415249
roll_no_list=[]
name = []
Hindi = []
English = []
Science = []
soc_science = []
Math = []
Sanskrit = []
Total = []
Percentage = []
Result =[]

while roll_no < 2415318:
    roll_no_str = str(roll_no)
    url = "https://rajeduboard.rajasthan.gov.in/RESULT2022/SEV/Roll_Output.asp?roll_no="+roll_no_str+"&B1=Submit"

    result = requests.get(url)

    #converting into a beautiful soup object
    soup = bs(result.content,features="html.parser")
    # content = soup.prettify()
    # print(content)

    try:

        name_tag = soup.find(["td"],width="63%",align="left")
        marks_tag = soup.find_all(["td"],width="13%",align="center")
        tot_marks_tag = soup.find_all(["td"],align="right",width="99%")
        result_tag =  soup.find_all(["td"],align="center",width="99%")
        Result.append(result_tag[0].text[8:])
        if result_tag[0].text[8:] == "Absent":
            Total.append('0')
            Percentage.append('0%')
            Hindi.append('0')
            English.append('0')
            Science.append('0')
            soc_science.append('0')
            Math.append('0')
            Sanskrit.append('0')
        else:
            Total.append(tot_marks_tag[0].text[-3:])
            Percentage.append(tot_marks_tag[1].text[11:])
            Hindi.append(marks_tag[9].text)
            English.append(marks_tag[14].text)
            Science.append(marks_tag[19].text)
            soc_science.append(marks_tag[24].text)
            Math.append(marks_tag[29].text)
            Sanskrit.append(marks_tag[34].text)
        roll_no_list.append(roll_no)
        name.append(name_tag.text[3:])
        print(name_tag.text[3:]+" "+result_tag[0].text[8:])

    except:
        pass


    roll_no +=1


# print(len(name))
# print(len(roll_no_list))
# print(len(Hindi))
# print(len(Result))
result_df = pd.DataFrame({"Name":name,"Roll No":roll_no_list,"Hindi":Hindi,"English":English,"Science":Science,"Social Science":soc_science,"Mathematics":Math,"SansKrit":Sanskrit,"Total":Total,"Percentage":Percentage,"Result":Result})
print(result_df)
writer = pd.ExcelWriter('Result_voc.xlsx')
result_df.to_excel(writer)
writer.save()
