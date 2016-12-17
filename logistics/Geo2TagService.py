SERVER_URL = "http://demo.geo2tag.org/instance/"
SERVICE_NAME = "testservice"


# возвращает url карты (при открытии driver-fleet-id)
def getFleetMap(fleet_id):
    return SERVER_URL + "service/" + SERVICE_NAME + "/map?fleet_id=" + fleet_id


# создаёт канал для автопарка, если не существует (при добавлении точки updateDriverPos)
def createFleetChannel(fleet):
    print("create channel for fleet "+fleet)
    # TODO реализовать
    # curl -b 'cookiefile.cookie' -H "Content-Type: application/json" -X POST -d '{"name":"test_channel","json":"{1: 2, 2: 4}"}' http://demo.geo2tag.org/instance/service/testservice/channel
    pass


# удаляет канал автопарка (при удалении автопарка)
def deleteFleetChannel(fleet):
    print("delete channel of fleet " + fleet)
    # TODO реализовать
    pass


# удаляет все каналы (при запуске приложения)
def clearAllFleets():
    print("delete all channels")
    # TODO реализовать
    # http://demo.geo2tag.org/instance/service/testservice/channel?number=1000 - получить все
    # удалить их
    pass


# обновляет текущее метоположение водителя ( при api/driver/update_pos/)
def updateDriverPos(driver, lat, lon, alt):
    print("added point " + str(lat) + " " + str(lon) + " "+ str(alt) + " for driver " + str(driver))
    # TODO реализовать
    # для всех автопарков водителя driver (for fleet in fleets)
    # 1) Если канала для f1eet не существует, то createFleetChannel(fleet)
    # 2) создаёт точку, если её не существует
    # curl -b 'cookiefile.cookie' -H "Content-Type: application/json" -X POST -d '[{"lat":1.1,"lon":1.1,"alt":1.1,"json":{"a":"b"},"channel_id":"5852791edaf98572b31e7ecf", "bc":true}]' http://demo.geo2tag.org/instance/service/testservice/point
    # 2) обновляет точку, если существует
    pass


# удаляет точку, соответствующую водителю в автопарке fleet (при исключении водителя из автопарка)
def deleteDriver(fleet, driver):
    print("dismiss driver " + str(driver) + " from fleet " + fleet)
    # TODO реализовать
    pass


