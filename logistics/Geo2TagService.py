from logistics.models import Fleet

SERVER_URL = "http://demo.geo2tag.org/instance/"
SERVICE_NAME = "testservice"


def one_time_startup():
    print("Application startup execution")
    clearAllFleetChannels()

# возвращает url карты (при открытии driver-fleet-id)
def getFleetMap(fleet_id):
    try:
        fleet = Fleet.objects.get(id=fleet_id)
        channel_name = createFleetChannel(fleet)
    except:
        channel_name = "none"

    return SERVER_URL + "service/" + SERVICE_NAME + "/map?latitude=59.8944&longitude=30.2642&channel=" + str(channel_name)


# создаёт канал для автопарка, если не существует (при добавлении точки updateDriverPos)
def createFleetChannel(fleet):
    print("create channel for fleet " + str(fleet))
    # TODO реализовать
    # curl -b 'cookiefile.cookie' -H "Content-Type: application/json" -X POST -d '{"name":"test_channel","json":"{1: 2, 2: 4}"}' http://demo.geo2tag.org/instance/service/testservice/channel
    # возвращает имя канала
    pass


# удаляет канал автопарка (при удалении автопарка)
def deleteFleetChannel(fleet):
    print("delete channel of fleet " + str(fleet))
    # TODO реализовать
    pass


# удаляет все каналы (при запуске приложения)
def clearAllFleetChannels():
    print("delete all channels")
    # TODO реализовать
    # http://demo.geo2tag.org/instance/service/testservice/channel?number=1000 - получить все
    # удалить их
    pass


# обновляет текущее метоположение водителя ( при api/driver/update_pos/)
def updateDriverPos(fleet, driver, lat, lon):
    print("added point " + str(lat) + " " + str(lon) + " for driver " + str(driver) + " in fleet "+ str(fleet))
    # TODO реализовать
    # для автопарка fleet
    # 1) Если канала для f1eet не существует, то createFleetChannel(fleet)
    # 2) обновляет точку, если она уже существует
    # 3) создаёт точку, если её не существует
    # curl -b 'cookiefile.cookie' -H "Content-Type: application/json" -X POST -d '[{"lat":1.1,"lon":1.1,"alt":1.1,"json":{"a":"b"},"channel_id":"5852791edaf98572b31e7ecf", "bc":true}]' http://demo.geo2tag.org/instance/service/testservice/point
    pass


# удаляет точку, соответствующую водителю в автопарке fleet (при исключении водителя из автопарка и при завершении поездки)
def deleteDriverPos(fleet, driver):
    print("dismiss driver " + str(driver) + " from fleet " + str(fleet))
    # TODO реализовать
    pass


