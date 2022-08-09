import datetime
import requests
import pymysql.cursors
import xml.etree.ElementTree as ET

from dotenv import dotenv_values

config_env = dotenv_values(".env")

connection = pymysql.connect(host=config_env["HOST"],
                             user=config_env["USER"],
                             password=config_env["PASSWORD"],
                             db=config_env["DB"],
                             charset=config_env["CHARSET"],
                             cursorclass=pymysql.cursors.DictCursor)

with connection.cursor() as cursor:
    sql = config_env["SQL"]
    cursor.execute(sql)
    result = cursor.fetchall()

url = config_env["NHSO_URL"]

for i in result:
    cid = i['cid']
    token = config_env["TOKEN"]
    user_id = config_env["USER_ID"]
    now = datetime.datetime.now()

    payload = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<S:Envelope\nxmlns:S=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:SOAPENV=\"http://schemas.xmlsoap.org/soap/envelope/\">\n    <S:Body>\n        <ns2:searchCurrentByPID xmlns:ns2=\"http://tokenws.ucws.nhso.go.th/\">\n            <user_person_id>" + user_id + "</user_person_id>\n            <smctoken>" + token + "</smctoken>\n            <person_id>" + cid + "</person_id>\n        </ns2:searchCurrentByPID>\n    </S:Body>\n</S:Envelope>"
    headers = {
        'Content-Type': 'text/xml'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    root = ET.fromstring(response.text)

    child = root[0][0][0]
    if child.find('status_desc') is not None:
        status_desc = child.find('status_desc').text
        print('death => ', cid)

        with connection.cursor() as cursor:
            sql = "UPDATE check_death SET status_desc = %s, check_death_date = %s, is_death = 'Y' WHERE cid = %s"
            cursor.execute(sql, (status_desc, now, cid))
            connection.commit()

    else:
        print('not death')
        with connection.cursor() as cursor:
            sql = "UPDATE check_death SET check_death_date = %s, is_death = 'N' WHERE cid = %s"
            cursor.execute(sql, (now, cid))
            connection.commit()
