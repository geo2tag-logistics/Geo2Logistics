var myApp = angular.module('geo2logistics', []);

myApp.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{[{');
    $interpolateProvider.endSymbol('}]}');
    // $httpProvider.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
});

// Контроллер для страницы myFleets
myApp.controller('GetOwnersFleetsController',[
    '$scope', '$http', function($scope, $http) {
        $scope.fleets = [];
        return $http.get('/api/fleet/').then(function(result) {
            return angular.forEach(result.data, function(item) {
                return $scope.fleets.push(item);
            });
        });



    }
]);

myApp.controller('addNewFleet',[
    '$scope', '$http', function($scope, $http) {

        $scope.addNewFleetClick = function () {
            console.log($scope.newFleetName);
            console.log($scope.newFleetDescription);
            $http.post('/api/fleet/add-fleet/', {name: $scope.newFleetName, description: $scope.newFleetDescription}).then(function (res) {
                console.log(res);
                location.reload()
            }, function (err) {
                console.log(err);
            })

        };
    }
]);

myApp.controller('RemoveFleets',[
    '$scope', '$http', function($scope, $http) {
        $scope.fleet_delete = function(id){
            var index = $scope.fleets.indexOf(id);

            // TODO add csrftoken cookie
            return $http.delete('/api/fleet/'+id+'/delete/').then(function(result) {
                $scope.fleets.splice(index, 1);
                location.reload();
                console.log(result);
            }, function(error) {
                console.log(error);

            });
        };
    }
]);

myApp.controller('ownerFleetController',[
        '$scope', '$http', 'driversStorage', function($scope, $http, driversStorage) {

            $scope.init = function (_fleet_id) {
                $scope.loadFleet(_fleet_id);
            };

            $scope.loadFleet = function (id) {
                return $http.get('/api/fleet/'+id+'/').then(
                    function(result) {
                        driversStorage.setFleet(result.data);
                        $scope.loadDriversData();
                    },
                    function(error) {
                        console.log(error);
                    }
                );
            };

            $scope.getFleetId = function () {
                var fleet = driversStorage.getFleet();
                return fleet != null ? fleet.id : -1;
            };

            $scope.getFleetName = function () {
                var fleet = driversStorage.getFleet();
                return fleet != null ? fleet.name : "NoName";
            };

            $scope.loadDriversData = function () {
                return $http.get('/api/fleet/'+$scope.getFleetId()+'/drivers/').then(function(result) {
                    return angular.forEach(result.data, function(item) {
                        return driversStorage.getDrivers().push(item);
                    });
                },function (error){
                    console.log(error);
                });
            };

            $scope.getDrivers = function(){
                return driversStorage.getDrivers();
            };

            $scope.driver_dismiss = function(fleet_id, driver_id){

                $scope.drivers = driversStorage.getDrivers();
                var index = $scope.drivers.indexOf(driver_id);

                return $http({
                    url: '/api/fleet/'+fleet_id+'/dismiss/',
                    method: 'POST',
                    data: {
                        driver_id: driver_id
                    },
                    // TODO add csrftoken cookie
                    // headers: {
                    //     "Content-Type": "application/json;charset=utf-8",
                    //     'X-CSRFToken': $cookies['csrftoken']
                    // }
                }).then(function(res) {
                    location.reload();
                    $scope.drivers.splice(index, 1);
                    console.log(res + " dismiss "+ driver_id);
                }, function(error) {
                    console.log(error);
                });
            };

            $scope.showPendingDrivers = function(fleetId){
                $scope.pdrivers =[];

                return $http.get('/api/fleet/'+fleetId+'/pending_drivers/').then(function (res) {
                    return angular.forEach(res.data, function(item) {
                        return $scope.pdrivers.push(item);
                    });
                }, function (error) {
                    console.log(error);
                });
            };

            $scope.pendDriver = function (fleetId, driverIdList) {
                driverId = "";
                driverIdList.forEach(function(item) {
                    driverId += (item + ",");
                });
                return $http({
                    method: 'POST',
                    url: '/api/fleet/'+fleetId+'/invite/',
                    data: {driver_id: driverId}
                    // TODO add csrftoken cookie
                    // headers: {
                    //     "Content-Type": "application/json;charset=utf-8",
                    //     'X-CSRFToken': $cookies['csrftoken']
                    // }
                }).success(function(res) {
                    console.log(res);
                    location.reload()
                }).error(function (err) {
                    console.log(err);
                })
            };
            $scope.getTrips = function (id) {
                $scope.trips = [];
                $http.get('/api/fleet/'+id+'/trips/unaccepted/').then(function (result) { // можно сделать выборку по конкретному автопарку
                    return angular.forEach(result.data, function (item) {
                        $scope.trips.push(item);
                    });
                });
                return $scope.trips;
            };

            $scope.getFinishedTrips = function (id) {
                $scope.finishedTrips = [];
                $http.get('/api/fleet/'+id+'/trips/finished/').then(function (result) { // можно сделать выборку по конкретному автопарку
                    return angular.forEach(result.data, function (item) {
                        $scope.finishedTrips.push(item);
                    });
                });
                return $scope.finishedTrips;
            };

            $scope.createTripClick = function (id) {
                console.log(id);
                $http.post('/api/fleet/'+id+'/add_trip/', {description: $scope.description, passenger_phone: $scope.passenger_phone, passenger_name: $scope.passenger_name, start_position: $scope.start_position, end_position: $scope.end_position}).then(function (res) {
                    console.log(res);
                    location.reload()
                }, function (err) {
                    console.log(err);
                })

            };

        }]
).service('driversStorage', function () {
    var _fleet = null;
    var _drivers = [];

    return {
        setFleet: function (fleet) {
            _fleet = fleet;
        },
        getFleet: function () {
            return _fleet;
        },
        setDrivers: function (drivers) {
            _drivers = drivers;
        },
        getDrivers: function () {
            return _drivers;
        }
    }
});

myApp.controller('mapController',[
        '$scope', '$http', 'fleetStorage', function($scope, $http, fleetStorage) {

            $scope.init = function (_fleet_id) {
                $scope.loadFleet(_fleet_id);
            };

            $scope.loadFleet = function (id) {
                return $http.get('/api/fleet/'+id+'/').then(
                    function(result) {
                        fleetStorage.setFleet(result.data);
                    },
                    function(error) {
                        console.log(error);
                    }
                );
            };

            $scope.getFleetId = function () {
                var fleet = fleetStorage.getFleet();
                return fleet != null ? fleet.id : -1;
            };

            $scope.getFleetName = function () {
                var fleet = fleetStorage.getFleet();
                return fleet != null ? fleet.name : "NoName";
            };
        }]
).service('fleetStorage', function () {
    var _fleet = null;
    var _drivers = [];

    return {
        setFleet: function (fleet) {
            _fleet = fleet;
        },
        getFleet: function () {
            return _fleet;
        }
    }
});

getFakeData = function(){
    return [{id: 10, name: "Vasya", coord:[55.73, 37.75]}, {id: 10, name: "Petya", coord:[55.81, 37.75]}, {id: 10, name: "Stepan", coord:[55.73, 37.65]}];
}