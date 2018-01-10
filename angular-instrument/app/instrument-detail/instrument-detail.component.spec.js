'use strict';

describe('instrumentDetail', function() {

  // Load the module that contains the `instrumentDetail` component before each test
  beforeEach(module('instrumentDetail'));

  // Test the controller
  describe('instrumentDetailController', function() {
    var $httpBackend, ctrl;
    var xyzinstrumentData = {
      name: 'instrument xyz',
      images: ['image/url1.png', 'image/url2.png']
    };

    beforeEach(inject(function($componentController, _$httpBackend_, $routeParams) {
      $httpBackend = _$httpBackend_;
      $httpBackend.expectGET('instruments/xyz.json').respond(xyzinstrumentData);

      $routeParams.instrumentId = 'xyz';

      ctrl = $componentController('instrumentDetail');
    }));

    it('should fetch the instrument details', function() {
      jasmine.addCustomEqualityTester(angular.equals);

      expect(ctrl.instrument).toEqual({});

      $httpBackend.flush();
      expect(ctrl.instrument).toEqual(xyzinstrumentData);
    });

  });

});
