app = angular.module 'geo2logistics', []

app.controller 'MyFleetsController', ['$scope', '$http', ($scope, $http) ->
    $scope.posts = []
    $http.delete('/api/fleet/:fleet_id/delete/').then (result) ->
        angular.forEach result.data, (item) ->
            $scope.posts.push item
]