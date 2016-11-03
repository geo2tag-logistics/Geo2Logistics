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
            $scope.fleets.splice(index, 1);
            return $http.delete('/api/fleet/'+id+'/delete').then(function(result) {
                console.log(result);
            });
        };
    }
]);

myApp.controller('getOneById',[
    '$scope', '$http', 'fleetStorage', function($scope,$http, fleetStorage) {

        $scope.init = function (_fleet_id) {
            $scope.loadFleet(_fleet_id);
        };

        $scope.loadFleet = function (id) {
            return $http.get('/api/fleet/'+id+'/').then(
                function(result) {
                    fleetStorage.setFleet(result.data);
                    $scope.getDriversData()
                },
                function(error) {
                    console.log(error);
                }
            );
        }

         $scope.getFleetId = function () {
            var fleet = fleetStorage.getFleet();
            return fleet != null ? fleet.id : -1;
        }

        $scope.getFleetName = function () {
            var fleet = fleetStorage.getFleet();
            return fleet != null ? fleet.name : "NoName";
        }

        $scope.drivers = [];
        $scope.getDriversData = function () {
            $http.get('/api/fleet/'+$scope.getFleetId()+'/drivers/').then(function(result) {
                return angular.forEach(result.data, function(item) {
                    return $scope.drivers.push(item);
                });
            });
        }

        $scope.driver_dismiss = function(fleet_id, driver_id){
            console.log(fleet_id);
            var index = $scope.drivers.indexOf(driver_id);
            $scope.drivers.splice(index, 1);
            return $http.delete('/api/fleet/'+fleet_id+'/dismiss/').then(function(result) {
                //TODO реализовать удаление и протестить
                console.log("dismiss "+id);
            }).then(function(error) {
                console.log(error);
            });
        };

}]
).service('fleetStorage', function () {
   var _fleet = null;

   return {
       setFleet: function (fleet) {
         _fleet = fleet;
       },
      getFleet: function () {
         return _fleet;
      }
    }
});


// Контроллер для страницы FleetOwner
myApp.controller('FleetController', function($scope) {

});