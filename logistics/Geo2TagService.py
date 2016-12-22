import hashlib
import json
import socket

import requests

from logistics.models import Fleet

SERVER_URL = "http://demo.geo2tag.org/instance/"
BASE_SERVICE_NAME = "testservice"
SERVICE_NAME = BASE_SERVICE_NAME
SERVICE_URL = SERVER_URL + "service/" + SERVICE_NAME

channel_dict = {}
points_dict = {}

def one_time_startup():
    print("Application startup execution")
    createService()
    clearAllFleetChannels()


def createService():
    m = hashlib.md5()
    m.update(socket.gethostbyname(socket.getfqdn()).encode('utf-8'))
    SERVICE_NAME = BASE_SERVICE_NAME + "_" + str(m.hexdigest())
    print("SERVICE_NAME: "+SERVICE_NAME)
    # curl -b 'cookiefile.cookie' -X POST -d 'name=LOGISTICS&ownerId=new_test_ownerId&logSize=10' http://demo.geo2tag.org/instance/service
    pass

# возвращает url карты (при открытии driver-fleet-id)
def getFleetMap(fleet_id):
    try:
        fleet = Fleet.objects.get(id=fleet_id)
        channel_id = getOrCreateFleetChannel(fleet)
    except:
        channel_id = "none"

    return SERVICE_URL + "/map?zoom=10&latitude=59.8944&longitude=30.2642&channel_ids=[\""+str(channel_id)+"\"]"


# создаёт канал для автопарка, если не существует (при добавлении точки updateDriverPos)
# возвращает oid канала для fleet
def getOrCreateFleetChannel(fleet):
    try:
        channel_oid = channel_dict.get(fleet.id, None)
        if channel_oid is not None:
            return channel_oid

        print("create channel for fleet " + str(fleet))
        url = SERVICE_URL + '/channel'
        full_name = str(fleet.name) + "_" + str(fleet.id)
        data = {'name': full_name, 'json': {'name': str(fleet.name), 'id': str(fleet.id), 'owner': fleet.owner.first_name+' '+fleet.owner.last_name}}
        request = requests.post(url, data=data)
        response = request.text
        channel_exists = response == 'null'
        if channel_exists:
            print(full_name+' already exists : '+str(channel_exists))
            oid = None
        else:
            oid = json.loads(response)["$oid"]
            channel_dict[fleet.id] = oid
        return oid

    except Exception as e:
        print("EXCEPTION WHILE createFleetChannel: " + str(e))


# удаляет канал автопарка (при удалении автопарка)
def deleteFleetChannel(fleet):
    try:
        channel_oid = channel_dict.get(fleet.id)
        headers = {'content-type': 'application/json'}
        url = SERVICE_URL + "/channel/" + channel_oid
        request = requests.delete(url, headers=headers)
        channel_dict.pop(fleet.id)
        print("delete channel of fleet " + str(fleet) +" result: "+request.text)

    except Exception as e:
        print("EXCEPTION WHILE deleteFleetChannel: " + str(e))


# удаляет все каналы (при запуске приложения)
def clearAllFleetChannels():
    print("delete all channels")

    try:
        url = SERVICE_URL + '/channel?number=0'
        request = requests.get(url)
        response = request.text
        print(response)
        parsed_string = json.loads(response)
        for channel in parsed_string:
            channel_oid = channel["_id"]["$oid"]
            headers = {'content-type': 'application/json'}
            url = SERVICE_URL + "/channel/" + channel_oid
            print("DELETE " + url)
            requests.delete(url, headers=headers)
            channel_dict.clear()
            points_dict.clear()

    except Exception as e:
        print("EXCEPTION WHILE clearAllFleetChannels: " + str(e))


# обновляет текущее метоположение водителя ( при api/driver/update_pos/)
def updateDriverPos(fleet, driver, lat, lon):
    try:
        channel_oid = getOrCreateFleetChannel(fleet)
        if channel_oid is not None:
            point_oid = points_dict.get(driver.id, None)

            url = SERVICE_URL + '/point'
            data = [{"lon": float(lat), "lat": float(lon), "alt": 1.1,
                     "json": {"name": driver.first_name + " " + driver.last_name}, "channel_id": channel_oid}]
            if point_oid is None:
                request = requests.post(url, data=json.dumps(data))
                point_oid = json.loads(request.text)[0]
                points_dict[driver.id] = point_oid
                print("added point " + str(lat) + " " + str(lon) + " for driver " + str(driver) + " in fleet " + str(fleet) + " result: "+request.text)

            else:
                # delete old
                del_url = SERVICE_URL + '/point/' + point_oid
                request = requests.delete(del_url)
                success = request.text == '{}'
                if success:
                    points_dict.pop(driver.id)
                    # add new
                    request = requests.post(url, data=json.dumps(data))
                    point_oid = json.loads(request.text)[0]
                    points_dict[driver.id] = point_oid
                    print("updated point " + str(lat) + " " + str(lon) + " for driver " + str(driver) + " in fleet " + str(fleet) + " result: " + request.text)

                else:
                    print("error while delete "+request.text)

    except Exception as e:
        print("EXCEPTION WHILE updateDriverPos: " + str(e))


# удаляет точку, соответствующую водителю в автопарке fleet (при исключении водителя из автопарка и при завершении поездки)
def deleteDriverPos(fleet, driver):
    try:
        point_oid = points_dict.get(driver.id)
        url = SERVICE_URL + '/point/' + point_oid
        request = requests.delete(url)
        points_dict.pop(driver.id)
        print("cleared position for driver " + str(driver) + " from fleet " + str(fleet) + " result: "+request.text)
    except Exception as e:
        print("EXCEPTION WHILE deleteDriverPos: " + str(e))


