'use strict';

describe('instrumentList', function() {

  // Load the module that contains the `instrumentList` component before each test
  beforeEach(module('instrumentList'));

  // Test the controller
  describe('instrumentListController', function() {
    var $httpBackend, ctrl;

    beforeEach(inject(function($componentController, _$httpBackend_) {
      $httpBackend = _$httpBackend_;
      $httpBackend.expectGET('instruments/instruments.json')
                  .respond([{name: 'Nexus S'}, {name: 'Motorola DROID'}]);

      ctrl = $componentController('instrumentList');
    }));

    it('should create a `instruments` property with 2 instruments fetched with `$http`', function() {
      jasmine.addCustomEqualityTester(angular.equals);

      expect(ctrl.instruments).toEqual([]);

      $httpBackend.flush();
      expect(ctrl.instruments).toEqual([{name: 'Nexus S'}, {name: 'Motorola DROID'}]);
    });

    it('should set a default value for the `orderProp` property', function() {
      expect(ctrl.orderProp).toBe('age');
    });

  });

});
