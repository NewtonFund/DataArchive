'use strict';

describe('Instrument', function() {
  var $httpBackend;
  var Instrument;
  var instrumentsData = [
    {name: 'Instrument X'},
    {name: 'Instrument Y'},
    {name: 'Instrument Z'}
  ];

  // Add a custom equality tester before each test
  beforeEach(function() {
    jasmine.addCustomEqualityTester(angular.equals);
  });

  // Load the module that contains the `Instrument` service before each test
  beforeEach(module('core.instrument'));

  // Instantiate the service and "train" `$httpBackend` before each test
  beforeEach(inject(function(_$httpBackend_, _Instrument_) {
    $httpBackend = _$httpBackend_;
    $httpBackend.expectGET('instruments/instruments.json').respond(instrumentsData);

    Instrument = _Instrument_;
  }));

  // Verify that there are no outstanding expectations or requests after each test
  afterEach(function () {
    $httpBackend.verifyNoOutstandingExpectation();
    $httpBackend.verifyNoOutstandingRequest();
  });

  it('should fetch the instruments data from `/instruments/instruments.json`', function() {
    var instruments = Instrument.query();

    expect(instruments).toEqual([]);

    $httpBackend.flush();
    expect(instruments).toEqual(instrumentsData);
  });

});
