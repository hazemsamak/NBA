// MODULE
var weatherApp = angular.module('weatherApp', ['ngRoute', 'ngResource']);

weatherApp.config(['$locationProvider','$compileProvider', function($locationProvider,$compileProvider) {
  $locationProvider.hashPrefix('');
$compileProvider.aHrefSanitizationWhitelist(/^\s*(https?|ftp|mailto|chrome-extension|magnet):/);
}]);
