var dApp = angular.module('geo2logistics', []);

dApp.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{[{');
    $interpolateProvider.endSymbol('}]}');
    // $httpProvider.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
});

dApp.controller('getPendings', ['$scope', '$http', function ($scope, $http) {
    $scope.fleets = [];
    return $http.get('/api/driver/pending_fleets').then(function(result) {
        return angular.forEach(result.data, function(item) {
            console.log(item);
            return $scope.fleets.push(item);
        });
    });

}]);

dApp.controller('driverFleets', ['$scope', '$http', function ($scope, $http) {

    $scope.showDriversFleets = function(){
        $scope.dfleets =[];

        $http.get('/api/driver/fleets/').then(function (res) {
            return angular.forEach(res.data, function(item) {
                return $scope.dfleets.push(item);
            });
        }, function (error) {
            console.log(error);
        });
    };

    $scope.check = function (fleet) {
        if(fleet){
            document.getElementById('create-new-trip').style.display = 'block';
        }
        $scope.fleetId = fleet;
    };


    $scope.saveSelection = function (fleetId) {
        if (fleetId) {
            document.getElementById('create-new-trip').style.display = 'block';
        }
        $scope.fleetId = fleetId;
    };

    $scope.getTrips = function () {
        console.log($scope.fleetId);
        $scope.trips = [];
        $http.get('/api/driver/fleet/'+ $scope.fleetId +'/available_trips/').then(function(result) { // можно сделать выборку по конкретному автопарку
            console.log(result.data);
            return angular.forEach(result.data, function(item) {
                $scope.trips.push(item);
            });
        });
        return $scope.trips;
    };

    $scope.getTripsOld = function (fleetId) {

        $scope.fleetId = fleetId;
        console.log($scope.fleetId);
        $scope.trips = [];
        if(fleetId == -1) {
            document.getElementById('create-new-trip').style.display = 'none';

            $http.get('/api/driver/available_trips/').then(function (result) { // можно сделать выборку по конкретному автопарку
                console.log(result.data);
                return angular.forEach(result.data, function (item) {
                    $scope.trips.push(item);
                });
            });
        } else {
            document.getElementById('create-new-trip').style.display = 'block';
            $http.get('/api/driver/fleet/' + $scope.fleetId + '/available_trips/').then(function (result) { // можно сделать выборку по конкретному автопарку
                console.log(result.data);
                return angular.forEach(result.data, function (item) {
                    $scope.trips.push(item);
                });
            });
        }
        return $scope.trips;
    };

    $scope.getPrevTrips = function () {
        console.log($scope.fleetId);
        $scope.trips = [];
        $http.get('/api/driver/fleet/'+ $scope.fleetId +'/available_trips/').then(function(result) { // можно сделать выборку по конкретному автопарку
            console.log(result.data);
            return angular.forEach(result.data, function(item) {
                $scope.trips.push(item);
            });
        });
        return $scope.trips;

    };

    $scope.getFinishedTrips = function(fleet) {
        $scope.finishedTrips = [];

        if(fleet == -1) {
            $http.get('/api/driver/trips/').then(function (result) { // можно сделать выборку по конкретному автопарку
                return angular.forEach(result.data, function (item) {
                    $scope.finishedTrips.push(item);
                });
            });
        }
        else {
            $http.get('/api/driver/fleet/' + fleet + '/trips/').then(function (result) {
                return angular.forEach(result.data, function (item) {
                    $scope.finishedTrips.push(item);
                });
            });
            return $scope.finishedTrips;
        }
    };

    $scope.takeTrip = function (id) {
        console.log(id);
        $http.post('/api/driver/accept_trip/', {trip_id:id}).then(function (res) {
            console.log(res);
            // TODO redirect на "Текущий рейс"
            location.reload();
        }, function (err) {
            console.log(err);
        })

    };

    $scope.haveTrip = function () {
        if ($scope.currentTrip != null){
            console.log($scope.currentTrip);

        }


    };

    $scope.refreshPendings = function () {
        $scope.pendings = [];
        $http.get('/api/driver/pending_fleets/').then(function(result) {
            return angular.forEach(result.data, function(item) {
                $scope.pendings.push(item);
            });
        });
        return $scope.pendings;

    };

    $scope.acceptPending = function (id) {
        $http.post('/api/driver/pending_fleets/accept/', {fleet_id:id}).then(function (res) {
            console.log(res);
            location.reload();
        }, function (err) {
            console.log(err);
        })

    };
    $scope.declinePending = function (id) {
        $http.post('/api/driver/pending_fleets/decline/', {fleet_id:id}).then(function (res) {
            console.log(res);
            location.reload();
        }, function (err) {
            console.log(err);
        })

    };

    $scope.createTripClick = function () {
        console.log($scope.passenger_name);
        $http.post('/api/driver/fleet/'+$scope.fleetId+'/add_trip/', {description: $scope.description, passenger_phone: $scope.passenger_phone, passenger_name: $scope.passenger_name, start_position: $scope.start_position, end_position: $scope.end_position}).then(function (res) {
            console.log(res);
            location.reload()
        }, function (err) {
            console.log(err);
        })

    };

    $scope.getCurrentTrip = function () {
        $scope.currentTrip = null;
        $http.get('/api/driver/current_trip/').then(function(result) {
            document.getElementById('cur-trip-lili').style.display = 'block';
            $scope.currentTrip = result.data;
        }, function (err) {
            document.getElementById('cur-trip-lili').style.display = 'none';
            console.log("No current trip");
        });
        return $scope.currentTrip;
    };

    $scope.finishTrip = function () {
        $http.post('/api/driver/finish_trip/', {}).then(function (res) {
            console.log(res);
            location.reload()
        }, function (err) {
            console.log(err);
        })

    };

    $scope.changeColor = function(param){
        if(param == 1)
            document.getElementById('cur-trip-li').style.borderColor = "darkred";

        else
            document.getElementById('cur-trip-li').style.borderColor = "white";

    };

    $scope.reportTrip = function (id, desc) {
        console.log("report");
        console.log(id);
        $http.post('/api/driver/report_problem/', {problem: id, problem_description:desc}).then(function (res) {
            console.log(res);
            //location.reload()
        }, function (err) {
            console.log(err);
        })

    };

}
]);

