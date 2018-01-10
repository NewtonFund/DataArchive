'use strict';

// Register `instrumentDetail` component, along with its associated controller and template
angular.
  module('instrumentDetail').
  component('instrumentDetail', {
    templateUrl: 'instrument-detail/instrument-detail.template.html',
    controller: ['$routeParams', 'instrument',
      function instrumentDetailController($routeParams, instrument) {
        var self = this;
        self.instrument = instrument.get({instrumentId: $routeParams.instrumentId}, function(instrument) {
          self.setImage(instrument.images[0]);
        });

        self.setImage = function setImage(imageUrl) {
          self.mainImageUrl = imageUrl;
        };
      }
    ]
  });
