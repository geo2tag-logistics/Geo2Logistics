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

myApp.controller('RemoveFleets',[
    '$scope', '$http', function($scope, $http) {
        $scope.fleet_delete = function(id){
            var index = $scope.fleets.indexOf(id);

            return $http.delete('/api/fleet/'+id).then(function(result) {
                $scope.fleets.splice(index, 1);
                console.log(result);
            }, function(error) {
                console.log(error);

            });
        };
    }
]);

myApp.controller('driversController',[
        '$scope', '$http', 'fleetStorage', function($scope,$http, fleetStorage) {

            $scope.init = function (_fleet_id) {
                $scope.loadFleet(_fleet_id);
            };

            $scope.loadFleet = function (id) {
                return $http.get('/api/fleet/'+id+'/').then(
                    function(result) {
                        fleetStorage.setFleet(result.data);
                        $scope.loadDriversData();
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

            $scope.loadDriversData = function () {
                return $http.get('/api/fleet/'+$scope.getFleetId()+'/drivers/').then(function(result) {
                    return angular.forEach(result.data, function(item) {
                        return fleetStorage.getDrivers().push(item);
                    });
                },function (error){
                    console.log(error);
                });
            };

            $scope.getDrivers = function(){
                return fleetStorage.getDrivers();
            };

            $scope.driver_dismiss = function(fleet_id, driver_id){

                $scope.drivers = fleetStorage.getDrivers();
                var index = $scope.drivers.indexOf(driver_id);

                return $http({
                    url: '/api/fleet/'+fleet_id+'/dismiss',
                    method: 'POST',
                    data: {
                        driver_id: driver_id
                    },
                    headers: {
                        "Content-Type": "application/json;charset=utf-8"
                    }
                }).then(function(res) {
                    $scope.drivers.splice(index, 1);
                    console.log(res + " dismiss "+ driver_id);
                }, function(error) {
                    console.log(error);
                });

// по идее мы не через scope работаем
//             var drivers = fleetStorage.getDrivers();
//             var index = drivers.indexOf(driver_id);
//
//             return  $http({
//                     url: '/api/fleet/'+fleet_id+'/dismiss/',
//                     method: 'DELETE',
//                     data: {
//                         driver_id: driver_id
//                     },
//                     headers: {
//                         "Content-Type": "application/json;charset=utf-8"
//                     }
//                 }).then(function(res) {
//                     $scope.drivers.splice(index, 1);
//                     console.log(res + " dismiss "+ driver_id);
//                 }, function(error) {
//                     console.log(error);
//                 });
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

            $scope.pendDriver = function (fleetId,driverId) {
                return $http.post('/api/fleet/'+fleetId+'/invite/', {driver_id: driverId}).then(function (res) {
                    console.log(res);
                }, function (error) {
                    console.log(error);
                });
            }

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
        },
        setDrivers: function (drivers) {
            _drivers = drivers;
        },
        getDrivers: function () {
            return _drivers;
        }
    }
});


// Контроллер для страницы FleetOwner
myApp.controller('FleetController', function($scope) {

});