var addDataApp=angular.module('addDataApp');
addDataApp.controller('dataController', function($scope) {

    $scope.taxiServices = [
        {
            name: "Yandex",
            description: "very good work at Russia",
            creation_date: "2016-10-22T14:01:23Z",
            cars_count:1,
            trips_count:1
        },
        {
            name: 'Uber',
            description: "good at EU",
            creation_date: "2016-10-22T14:01:23Z",
            cars_count:21,
            trips_count:31
        },
        {
            name: 'Get',
            description: "rather good",
            creation_date: "2016-10-22T14:01:23Z",
            cars_count:11,
            trips_count:13
        }]
});