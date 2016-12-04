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
    }

}]);



dApp.controller('createTrip',[
    '$scope', '$http', function($scope, $http) {
        console.log(123);
        $scope.createTripClick = function () {
            console.log(321);

            console.log($scope.passenger_name);
            $http.post('/api/driver/fleet/add_trip/', {description: $scope.description, passenger_phone: $scope.passenger_phone, passenger_name: $scope.passenger_name, start_position: $scope.start_position, end_position: $scope.end_position}).then(function (res) {
                console.log(res);
                location.reload()
            }, function (err) {
                console.log(err);
            })

        };
    }
]);
