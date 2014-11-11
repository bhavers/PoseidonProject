'use strict';

var sensorsApp = angular.module('sensorsApp', ['ngResource']);

/*sensorsApp.config(['$sceDelegateProvider', function($sceDelegateProvider) {
         $sceDelegateProvider.resourceUrlWhitelist(['self', 'http://poseidon.mybluemix.net/**']);
}]);
*/
sensorsApp.factory('SensorList', ['$resource',
  function($resource){
    return $resource('http://poseidon.mybluemix.net/sensors', {}, {
      query: {method:'GET', isArray:true}
    });
  }]);

var sensorsController = sensorsApp.controller('sensorsController', ['$scope', 'SensorList', function ($scope, SensorList) {
  $scope.sensors = SensorList.query();  
}]);

