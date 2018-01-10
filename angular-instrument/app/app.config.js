'use strict';

angular.
  module('instrumentcatApp').
  config(['$locationProvider' ,'$routeProvider',
    function config($locationProvider, $routeProvider) {
      $locationProvider.hashPrefix('!');

      $routeProvider.
        when('/instruments', {
          template: '<instrument-list></instrument-list>'
        }).
        when('/instruments/:instrumentId', {
          template: '<instrument-detail></instrument-detail>'
        }).
        otherwise('/instruments');

      $routeProvider.
        when('/exposure-calculator', {
          template: '<exposure-calculator></exposure-calculator>'
        }).
        otherwise('/instruments');

      $routeProvider.
        when('/heatmap-generator', {
          template: '<heatmap-generator></heatmap-generator>'
        }).
        otherwise('/instruments');

      $routeProvider.
        when('/phase2-rotator', {
          template: '<phase2-rotator></phase2-rotator>'
        }).
        otherwise('/instruments');


    }
  ]);
