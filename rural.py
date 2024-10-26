from bs4 import BeautifulSoup  # html parser
import pandas as pd  # csv parser
import requests as req  # http request


def get_value(s, value):
    return (
        s.find(lambda tag: tag.name == "td" and value in tag.text.strip())
        .find_next_sibling("td")
        .text.strip()
    )


def check_location(latitude, longitude):

    link1 = "https://www.ruralhealthinfo.org/am-i-rural/report?lat={}&lng={}".format(
        longitude, latitude
    )
    print(link1)
    respons1 = req.get(link1)

    s1 = BeautifulSoup(respons1.text, "lxml")

    not_found = s1.find(
        lambda tag: tag.name == "h1" and "The Page Cannot be Found" in tag.text
    )
    if not_found:
        print("not found")
        return
    else:
        print("results found")

    # get information
    cbsa_type = s1.find(lambda tag: tag.name == "li" and "CBSA Type" in tag.text).text
    cbsa_name = s1.find(lambda tag: tag.name == "li" and "CBSA Name" in tag.text).text
    cbsa_id = s1.find(lambda tag: tag.name == "li" and "CBSA ID: " in tag.text).text

    link2 = "https://www.ruralhealthinfo.org/am-i-rural/report/shortage-designations?lat={}&lng={}".format(
        longitude, latitude
    )
    print(link2)
    respons2 = req.get(link2)

    s2 = BeautifulSoup(respons2.text, "lxml")

    table = s2.find("table")
    tds = table.find_all("td")

    primary_care = get_value(s2, "Primary Care")
    dental_care = get_value(s2, "Dental Care")
    mental_health = get_value(s2, "Mental Health")
    mua = get_value(s2, "Medically Underserved Area (MUA)")
    mup = get_value(s2, "Medically Underserved Population (MUP)")
    mua_ge = get_value(s2, "Medically Underserved Area - Governor's Exception (MUA-GE)")
    mup_ge = get_value(
        s2, "Medically Underserved Population - Governor's Exception (MUP-GE)"
    )
    print(
        (
            cbsa_type,
            cbsa_name,
            cbsa_id,
            primary_care,
            dental_care,
            mental_health,
            mua,
            mup,
            mua_ge,
            mup_ge,
        )
    )
    csv_file = open("results.csv", "a")
    csv_file.write(
        "{},{},{},{},{},{},{},{},{},{}\n".format(
            cbsa_type,
            cbsa_name,
            cbsa_id,
            primary_care,
            dental_care,
            mental_health,
            mua,
            mup,
            mua_ge,
            mup_ge,
        )
    )
    csv_file.close()


if __name__ == "__main__":
    df = pd.read_csv("uscities.csv", header=0)
    cities = df["city"]
    longitudes = df["lat"]
    latitudes = df["lng"]

    # csv_file = open("results.csv", "w")
    # csv_file.write(
    #     "cbsa_type,cbsa_name,cbsa_id,primary_care,dental_care,mental_health,mua,mup,mua_ge,mup_ge\n"
    # )
    # csv_file.close()
    for i in range(0, len(latitudes)):
        city = cities[i]
        latitude = latitudes[i]
        longitude = longitudes[i]
        print(
            "checking  (city={},latitude={},longitude={})".format(
                city, latitude, longitude
            )
        )
        check_location(latitude, longitude)
