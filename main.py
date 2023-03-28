import datetime
import requests
import pymysql.cursors
import xml.etree.ElementTree as ET

import line_noti as line

from dotenv import dotenv_values

config_env = dotenv_values(".env")

connection = pymysql.connect(host=config_env["HOST"],
                             user=config_env["USER"],
                             password=config_env["PASSWORD"],
                             db=config_env["DB"],
                             charset=config_env["CHARSET"],
                             cursorclass=pymysql.cursors.DictCursor)

with connection.cursor() as cursor:
    # start sent line notify
    # line.sent_notify_message('NHSO_check API: Start')
    # YOUR CODE HERE # SUCH AS: sql = "SELECT cid FROM check_death"
    sql = "SELECT cid FROM check_death WHERE is_death <> 'Y'"
    cursor.execute(sql)
    result = cursor.fetchall()

url = config_env["NHSO_URL"]

j = 1

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
        print(j, cid, ' =X death ')

        with connection.cursor() as cursor:
            sql = "UPDATE check_death SET status_desc = %s, check_death_date = %s, is_death = 'Y' WHERE cid = %s"
            cursor.execute(sql, (status_desc, now, cid))
            connection.commit()

    else:
        maininscl = child.find('maininscl').text if child.find('maininscl') is not None else ''
        hmain = child.find('hmain').text if child.find('hmain') is not None else ''
        hsub = child.find('hsub').text if child.find('hsub') is not None else ''
        cardid = child.find('cardid').text if child.find('cardid') is not None else ''
        startdate = child.find('startdate').text if child.find('startdate') is not None else ''
        expdate = child.find('expdate').text if child.find('expdate') is not None else ''
        ws_status_desc = child.find('ws_status_desc').text if child.find('ws_status_desc') is not None else ''
        birthdate = child.find('birthdate').text if child.find('birthdate') is not None else ''
        fname = child.find('fname').text if child.find('fname') is not None else ''
        lname = child.find('lname').text if child.find('lname') is not None else ''

        print(j, cid, ' => not death => ', maininscl, hmain, hsub, cardid, startdate, expdate, birthdate, fname, lname,
              ws_status_desc)

        with connection.cursor() as cursor:
            sql = "UPDATE check_death SET check_death_date = %s, is_death = 'N', TYPE = %s, HOSPMAIN = %s" \
                  ", HOSPSUB = %s, CARDID = %s, REGISTER = %s, DATEEXP = %s, birthdate = %s, fname = %s, lname = %s  " \
                  "WHERE cid = %s"
            cursor.execute(sql, (now, maininscl, hmain, hsub, cardid, startdate, expdate, birthdate, fname, lname, cid))
            connection.commit()

    j += 1

connection.close()

# line.sent_notify_message('NHSO_check API: finish for ' + str(j - 1) + ' records')


