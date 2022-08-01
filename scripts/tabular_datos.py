import csv
import json
from dateutil import tz
from datetime import datetime
from google.cloud import firestore
from google.cloud import storage

db = firestore.Client()

def get_data_with_day(date):
    data = []
    ref = db.collection("prod_v2").get()
    for cosecha in ref:
        datum = cosecha.to_dict()
        datum_date = datum.get("timestamp")
        # if type(datum_date) == str:
        #     tw_datetime = datetime.strptime(tw_date, "%Y-%m-%d %H:%M:%S")
        if datum_date.date() == date.date():
            data.append(datum)
    return data

def get_data():
    data = []
    ref = db.collection("prod_v2").get()
    for cosecha in ref:
        data.append(cosecha.to_dict())
    return data

def get_columns(data):
    columns = []
    columns.append("form_id")
    for row in data:
        payload = row.get("payload")
        for field in payload:
            if not(field.get("id") in columns):
                columns.append(field.get("id"))
    return columns


def flatten_data(data):
    flattened = {}
    flattened.update({"form_id": data.get("form_id")})
    payload = data.get("payload")
    for field in payload:
        field_id = field.get("id")
        field_value = field.get("type")
        if (field_value == "date" or field_value == "text"):
            value = field.get("value")
        elif(field_value == "geo_point"):
            lat = field.get("value").latitude
            lon = field.get("value").longitude
            value = [lat, lon]
        elif (field_value == "single_choice"):
            value = field.get("value").get("label")
        elif(field_value == "multi_choice"):
            value = []
            for m_value in field.get("value"):
                value.append(m_value.get("label"))
        else:
            value = field.get("value")
        flattened.update({field_id : value}) 
    return flattened


print("Inserte una fecha con el formato dd-mm-AAAA")
date_format = "%d-%m-%Y"
fecha = input()
datetime_obj = datetime.strptime(fecha, date_format)
date_str = datetime_obj.strftime(date_format)
  
with open("data.csv", mode="w") as file:
    data = get_data_with_day(datetime_obj)
    fieldnames = get_columns(data)
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    for row in data:
        print(type(row))
        flattened_data = flatten_data(data=row)
        for field in fieldnames:
            if not field in flattened_data:
                flattened_data.update({field : "-"})
        writer.writerow(flattened_data)