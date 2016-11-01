app = angular.module 'geo2logistics', []

app.controller 'GetOwnersFleetsController', ['$scope', '$http', ($scope, $http) ->
    $scope.fleets = []
    $http.get('/api/fleet/').then (result) ->
        angular.forEach result.data, (item) ->
            $scope.fleets.push item
]