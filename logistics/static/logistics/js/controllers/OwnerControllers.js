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
    '$scope', '$http', function($scope,$http) {
        // var myVar = document.getElementById("myVar").value;
        // $scope.intrew = myVar;
        $scope.getFleet = function (id) {
            // $scope.fleetName={};
            return $http.get('/api/fleet/' + id).then(function(result) {
                return result;
            });
            // return id;
            };
        }]);


        // $scope.getFleet = function(id) {
        //     // return id;
        //     return $http.get('/api/fleet/' + id ).then(function (result) {
        //         console.log(result);
        //         return result.data;
        //     }).then(function (error) {
        //         console.log(error);
        //     });
        // };

myApp.controller('RemoveDriver',[
    '$scope', '$http', function($scope, $http) {
        $scope.driver_delete = function(id){
            var index = $scope.drivers.indexOf(id);
            $scope.drivers.splice(index, 1);
            return $http.delete('/api/fleet/'+id+'/dismiss').then(function(result) {
                console.log(result);
            });
        };
    }
]);




//         $scope.fleet_delete = function(id){
//             var index = $scope.fleets.indexOf(id);
//             $scope.fleets.splice(index, 1);
//             return $http.delete('/api/fleet/'+id+'/delete').then(function(result) {
//                 console.log(result);
//             });
//         };
//     }
// ]);



// Контроллер для страницы FleetOwner
myApp.controller('FleetController', function($scope) {

});