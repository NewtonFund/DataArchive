'use strict';

angular.
  module('core.instrument').
  factory('instrument', ['$resource',
    function($resource) {
      return $resource('instruments/:instrumentId.json', {}, {
        query: {
          method: 'GET',
          params: {instrumentId: 'instruments'},
          isArray: true
        }
      });
    }
  ]);
