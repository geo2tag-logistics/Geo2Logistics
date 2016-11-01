(function() {
  var app;

  app = angular.module('example.app.basic', []);

  app.controller('AppController', [
    '$scope', '$http', function($scope, $http) {
      $scope.posts = [];
      return $http.get('/api/posts').then(function(result) {
        return angular.forEach(result.data, function(item) {
          return $scope.posts.push(item);
        });
      });
    }
  ]);

}).call(this);

(function() {
  var app;

  app = angular.module('geo2logistics', []);

  app.controller('MyFleetsController', [
    '$scope', '$http', function($scope, $http) {
      $scope.posts = [];
      return $http["delete"]('/api/fleet/:fleet_id/delete/').then(function(result) {
        return angular.forEach(result.data, function(item) {
          return $scope.posts.push(item);
        });
      });
    }
  ]);

}).call(this);

(function() {
  var app;

  app = angular.module('geo2logistics', []);

  app.controller('MyFleetsController', [
    '$scope', '$http', function($scope, $http) {
      $scope.posts = [];
      return $http["delete"]('/api/fleet/:fleet_id/delete/').then(function(result) {
        return angular.forEach(result.data, function(item) {
          return $scope.posts.push(item);
        });
      });
    }
  ]);

}).call(this);

(function() {
  var app;

  app = angular.module('geo2logistics', []);

  app.controller('MyFleetsController', [
    '$scope', '$http', function($scope, $http) {
      $scope.posts = [];
      return $http.get('/api/fleet/').then(function(result) {
        return angular.forEach(result.data, function(item) {
          return $scope.fleets.push(item);
        });
      });
    }
  ]);

}).call(this);
