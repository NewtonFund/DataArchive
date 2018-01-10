'use strict';

// Register `instrumentList` component, along with its associated controller and template
angular.
  module('instrumentList').
  component('instrumentList', {
    templateUrl: 'instrument-list/instrument-list.template.html',
    controller: ['instrument',
      function instrumentListController(instrument) {
        this.instruments = instrument.query();
        this.orderProp = 'age';
      }
    ]
  });
