var myApp = angular.module('geo2logistics', []);

myApp.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{[{');
    $interpolateProvider.endSymbol('}]}');
    // $httpProvider.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
});

// Контроллер для страницы myFleets
myApp.controller('MyFleetsController', function($scope) {

    $scope.fleets = [
        {
            id: 1,
            name: "Yandex",
            description: "very good work at Russia",
            creation_date: "2016-10-22T14:01:23Z",
            cars_count:1,
            trips_count:1
        },
        {
            id: 2,
            name: 'Uber',
            description: "good at EU",
            creation_date: "2016-10-22T14:01:23Z",
            cars_count:21,
            trips_count:31
        },
        {
            id: 3,
            name: 'Get',
            description: "rather good",
            creation_date: "2016-10-22T14:01:23Z",
            cars_count:11,
            trips_count:13
        }];

    $scope.fleet_delete = function (id) {
        alert("Delete "+id);
    }
});

// Контроллер для страницы FleetOwner
myApp.controller('FleetController', function($scope) {

});