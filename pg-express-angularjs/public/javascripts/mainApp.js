var mainApp = angular.module("mainApp", ["ngTable", "nvd3"]);

mainApp.controller('psqlController', function($scope, $http) {

  $scope.query = function()
  {
      $http.get("/query_fixed")
      .then(function(response) {
          //First function handles success
          $scope.data = response.data;
          //console.log(response.data);
      }, function(response) {
          //Second function handles error
          console.log("Something went wrong");
      });
  };

});


mainApp.controller('psqlController2', function($scope, $http) {

  $scope.query_obsnum = function(minval)
  {
      $http.post("/query_obsnum", {minval})
      .then(function(response) {
          //First function handles success
          $scope.data = response.data;
          //console.log(response.data);
      }, function(response) {
          //Second function handles error
          console.log("Something went wrong");
      });
  };

});


mainApp.controller('queryFormController', function($scope, $http, $window, NgTableParams) {

  $scope.checkboxModel = {
    position: true,
    mjd: false,
    exptime: false,
    azimuth: false,
    altitude: false,
    seeing: false,
    airmass: false,
    tagid: false,
    userid: false,
    propid: false,
    groupid: false,
    obsid: false,
    limit: true
  };

  $scope.queryModel = {
    RA: 101.287,
    DEC: -16.716,
    RADIUS: 60.0,
    MJD_min: 0,
    MJD_max: 58000,
    EXPTIME_min: 0.,
    EXPTIME_max: 3600.,
    AZI_min: 0.0,
    AZI_max: 360.0,
    ALT_min: 0.0,
    ALT_max: 90.0,
    SEEING_min: 0.0,
    SEEING_max: 5.0,
    AIRMASS_min: 0.0,
    AIRMASS_max: 5.0,
    TAGID: 0,
    USERID: 0,
    PROPID: 0,
    GROUPID: 0,
    OBSID: 0,
    LIMIT: 1000
  };

  $scope.send_query = function(queryModel, checkboxModel) {
      $http.post("/query_full", {queryModel, checkboxModel})
      .then(function(response) {
          //First function handles success
          var rows = response.data.rows;

          //console.log(response.data.fields);
          var colNames = Object.values(response.data.fields);
          
          $scope.columnNames = colNames.map(function (field, idx) {
            var filter = {};
            filter[field.name] = 'text';
            return {
              title: field.name,
              sortable: field.name,
              filter: filter,
              show: true,
              field: field.name
            };
          });

          //console.log($scope.columnNames);
          $scope.pgOutput = new NgTableParams({
            page: 1,
            count: 10
          },
            {
            dataset: rows,
            total: rows.length
          });
          
          $scope.allRows = [];
          for (var i=rows.length-1; i>=0; i--) {
            //console.log(rows[i]);
            $scope.allRows.push(rows[i].__obsnum);
          }
          console.log($scope.allRows);
          //$scope.allRows = rows.__obsnum;

      }, function(response) {
          //Second function handles error
          console.log("Something went wrong");
      });
  }

  // Empty array to populate selected items
  $scope.selectedRows = [];

  // Add or remove item to array
  $scope.select_data = function(item) {
    // assume data does not exist
    var exist = false;
    // remove data if it exists
    for (var i=$scope.selectedRows.length-1; i>=0; i--) {
      if ($scope.selectedRows[i] === item) {
        $scope.selectedRows.splice(i, 1);
        // data exists
        exist = true;
      }
    }
    // if data is not in the array, append to the array
    if (exist == false) {
      $scope.selectedRows.push(item);
    }
    console.log($scope.selectedRows);
  }

  // pass the data to here >>
  $scope.getSelectedRows = function()
  {
    if ($scope.selectedRows.length == 0) {
      alert('No item is selected')
    } else {
      $http.post("/get_files", $scope.selectedRows)
      .then(function(response)
      {
        console.log(response.data);
        $scope.downloadLink = response.data;
        $scope.downloadLinkReady = true;
        //$window.open(response.data);
      }, function(response)
      {
        console.log("Something went wrong");
      });
    }
  }

  $scope.getAllRows = function()
  {
    if ($scope.allRows.length == 0) {
      alert('No item is selected')
    } else {
      $http.post("/get_files", $scope.allRows)
      .then(function(response)
      {
        console.log(response.data);
        $scope.downloadLinkAll = response.data;
        $scope.downloadLinkAllReady = true;
        //$window.open(response.data);
      }, function(response)
      {
        console.log("Something went wrong");
      });
    }
  }

  // pass the data to here >>
  $scope.plotSelectedRows = function()
  {
    if ($scope.selectedRows.length == 0) {
      alert('No item is selected')
    } else {
      $http.post("/get_rows", $scope.selectedRows)
      .then(function(response)
      {
        $scope.plotData = [{
          key: "allkeys_table",
          values: response.data.rows
          }]
      console.log($scope.plotData);
      }, function(response)
      {
        console.log("Something went wrong");
      });
    }
  }

  $scope.options = {
    chart: {
      type: "scatterChart",
      height: 600,
      margin : {
        top: 20,
        right: 20,
        bottom: 60,
        left: 80
      },
      x: function(d) { return d.ra_degree; },
      y: function(d) { return d.dec_degree; },
      showValues: true,
      valueFormat: function(d) {
        return d3.format(',.4f')(d);
      },
      transitionDuration: 20,
      xAxis: {
        axisLabel: 'X Axis',
        showMaxMin: false
      },
      yAxis: {
        axisLabel: 'Y Axis',
        showMaxMin: false,
        axisLabelDistance: 5
      },
      showXAis: true,
      showYAis: true,
      zoom: {
        enabled: true,
        scaleExtent: [
          0.5,
          10
        ],
        useFixedDomain: false,
        useNiceScale: true,
        horizontalOff: false,
        verticalOff: false
      }
    }
  };


//  $scope.select_data = function(filename) {
//    alert('pretend this is the filepath: ' + filename);
//  }

});
