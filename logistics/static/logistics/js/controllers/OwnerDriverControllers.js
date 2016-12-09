/**
 * Created by Denis on 10.12.2016.
 */
var dApp = angular.module('geo2logistics', []);

dApp.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{[{');
    $interpolateProvider.endSymbol('}]}');
    // $httpProvider.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
});

dApp.controller('tripController',[
        '$scope', '$http', 'tripStorage', function($scope, $http, tripStorage) {

        $scope.init = function (_trip_id) {
            $scope.loadTrip(_trip_id);
        };

        $scope.loadTrip = function (id) {
            return $http.get('/api/trip/'+id+'/').then(
                function (result) {
                    tripStorage.setTrip(result.data);
                },
                function (error) {
                    console.log(error);
                }
            );
        };

        $scope.getTrip = function(){
            $scope.currentTrip = tripStorage.getTrip();
            console.log($scope.currentTrip)
            return $scope.currentTrip;
        };

        $scope.getTripId = function () {
            var trip = tripStorage.getTrip();
            return trip != null ? trip.id : -1;
        };

        $scope.getTripName = function () {
            var trip = tripStorage.getTrip();
            return trip != null ? trip.name : "NoName";
        };
}]).service('tripStorage', function () {
    var _trip = null;

    return {
        setTrip: function (trip) {
            _trip = trip;
        },
        getTrip: function () {
            return _trip;
        }
    }
});
