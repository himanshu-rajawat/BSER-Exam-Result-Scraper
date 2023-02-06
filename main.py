import os
import requests
import pandas as pd
from bs4 import BeautifulSoup

def scrape_data(roll_no: int, last_roll_no: int):
    roll_no_list = []
    name = []
    Hindi = []
    English = []
    Science = []
    soc_science = []
    Math = []
    Sanskrit = []
    Total = []
    Percentage = []
    Result = []

    while roll_no < last_roll_no:
        url = f"https://rajeduboard.rajasthan.gov.in/RESULT2022/SEV/Roll_Output.asp?roll_no={roll_no}&B1=Submit"

        result = requests.get(url)
        soup = BeautifulSoup(result.content, "html.parser")

        try:
            name_tag = soup.find("td", width="63%", align="left")
            marks_tag = soup.find_all("td", width="13%", align="center")
            tot_marks_tag = soup.find_all("td", align="right", width="99%")
            result_tag = soup.find_all("td", align="center", width="99%")
            Result.append(result_tag[0].text[8:])
            if result_tag[0].text[8:] == "Absent":
                Total.append("0")
                Percentage.append("0%")
                Hindi.append("0")
                English.append("0")
                Science.append("0")
                soc_science.append("0")
                Math.append("0")
                Sanskrit.append("0")
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
        except:
            pass

        roll_no += 1

    result_df = pd.DataFrame(
        {
            "Name": name,
            "Roll No": roll_no_list,
            "Hindi": Hindi,
            "English": English,
            "Science": Science,
            "Social Science": soc_science,
            "Mathematics": Math,
            "Sanskrit": Sanskrit,
            "Total": Total,
            "Percentage": Percentage,
            "Result": Result,
        }
    )
    return result_df
roll_no_start = 2415249
roll_no_end = 2415318
result_df = scrape_data(roll_no_start, roll_no_end)
result_df.to_excel("Result_voc.xlsx", index=False)
