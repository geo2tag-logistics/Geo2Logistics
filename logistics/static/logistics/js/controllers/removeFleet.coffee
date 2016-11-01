app = angular.module 'geo2logistics', []

app.controller 'DeleteFleetController', ['$scope', 'fleets', ($scope, fleets) ->
    $scope.canDelete = (post) ->
        return post.fleets.id == fleets.id

    $scope.delete = (post) ->
        post.$delete()
        .then ->
            # Remove it from the list on success
            idx = $scope.fleets.indexOf(post)
            $scope.fleets.splice(idx, 1)
]