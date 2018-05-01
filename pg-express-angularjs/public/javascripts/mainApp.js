var mainApp = angular.module("mainApp", ["ngTable", "nvd3"]);

/*
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
*/

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

  $scope.openJS9 = function()
  {
    JS9.LoadWindow(
      url="temp_files/d_e_20180417_4_0_2_1.fits",
      opts={scale:"log"},
      type="light"
    );
  }

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

  $scope.showTheRest = false;

  $scope.send_query = function(queryModel, checkboxModel) {
      $http.post("/query_full", {queryModel, checkboxModel})
      .then(function(response) {
          //First function handles success
          var rows = response.data.rows;
          //console.log('.then triggered')
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

          if (rows.length > 0) {
            $scope.showTheRest = true;
          }
          //console.log($scope.allRows);
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
    //console.log($scope.selectedRows);
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
        //console.log(response.data);
        $scope.downloadLinkAll = response.data;
        $scope.downloadLinkAllReady = true;
        //$window.open(response.data);
      }, function(response)
      {
        console.log("Something went wrong");
      });
    }
  }

  // query the full table and store in the client memory
  $scope.plotSelectedRows = function()
  {
    if ($scope.selectedRows.length == 0) {
      alert('No item is selected')
    } else {
      $http.post("/get_rows", $scope.selectedRows)
      .then(function(response)
      {
        // this is called in the nvd3 tag
        $scope.nvd3Data = [{
          key: "allkeys_table",
          values: response.data.rows
          }]
        $scope.nvd3Header = response.data.fields;
      //console.log($scope.nvd3plotData[0].values);
      //console.log($scope.fullHeader);
      $scope.updatePlot();
      }, function(response)
      {
        console.log("Something went wrong");
      })
    }
  }

  // query the full table and store in the client memory
  $scope.plotAllRows = function()
  {
    $http.post("/get_rows", $scope.allRows)
    .then(function(response)
    {
      // this is called in the nvd3 tag
      $scope.nvd3AllData = [{
        key: "allkeys_table",
        values: response.data.rows
        }]
      $scope.nvd3AllHeader = response.data.fields;
    //console.log($scope.nvd3plotData[0].values);
    //console.log($scope.fullHeader);
    $scope.updateAllPlot();
    }, function(response)
    {
      console.log("Something went wrong");
    })
  }

  $scope.updatePlot = function() {
    var name1 = $scope.xAxisOption.name;
    var name2 = $scope.yAxisOption.name;
    //console.log(name1);
    //console.log(name2);
    // Need to make this nested
    console.log( $scope.nvd3Data[0].values[0][name1] );
    $scope.tempData = [];
    for (var i=$scope.nvd3Data[0].values.length-1; i>=0; i--) {
      //console.log(rows[i]);
      $scope.tempData.push({
        x: $scope.nvd3Data[0].values[i][name1],
        y: $scope.nvd3Data[0].values[i][name2]
      });
    }
    $scope.nvd3PlotData = [{
      key: "allkeys_table",
      values: $scope.tempData
      }]

    console.log($scope.nvd3PlotData);
    $scope.plotApi.updateWithData($scope.nvd3PlotData);
    /*var tempData = $scope.nvd3Data[0].values[name1];
    $scope.nvd3PlotData = [{
      key: "allkeys_table",
      values: tempData
      }]
    console.log($scope.nvd3PlotData);*/
  }


  $scope.updateAllPlot = function() {
    var name1 = $scope.xAxisOptionAll.name;
    var name2 = $scope.yAxisOptionAll.name;
    //console.log(name1);
    //console.log(name2);
    // Need to make this nested
    console.log( $scope.nvd3AllData[0].values[0][name1] );
    $scope.tempAllData = [];
    for (var i=$scope.nvd3AllData[0].values.length-1; i>=0; i--) {
      //console.log(rows[i]);
      $scope.tempAllData.push({
        x: $scope.nvd3AllData[0].values[i][name1],
        y: $scope.nvd3AllData[0].values[i][name2]
      });
    }
    $scope.nvd3PlotAllData = [{
      key: "allkeys_table",
      values: $scope.tempAllData
      }]

    console.log($scope.nvd3AllPlotData);
    $scope.plotAllApi.updateWithData($scope.nvd3AllPlotData);
    /*var tempData = $scope.nvd3Data[0].values[name1];
    $scope.nvd3PlotData = [{
      key: "allkeys_table",
      values: tempData
      }]
    console.log($scope.nvd3PlotData);*/
  }


  $scope.nvd3options = {
    chart: {
      type: "scatterChart",
      height: 600,
      margin : {
        top: 20,
        right: 20,
        bottom: 60,
        left: 80
      },
      x: function(d) { 
        //console.log(d[$scope.xAxisOption.name]);
        //console.log(d.ra_degree);
        //console.log(d);
        return d.x;
      },
      //y: function(d) { return d[$scope.yAxisOption.name]; },
      y: function(d) { return d.y; },
      showValues: true,
      valueFormat: function(d) {
        return d3.format(',.4f')(d);
      },
      transitionDuration: 10,
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
  }


//  $scope.select_data = function(filename) {
//    alert('pretend this is the filepath: ' + filename);
//  }

});

mainApp.directive('ngRightClick', function($parse) {
  return function(scope, element, attrs) {
    var fn = $parse(attrs.ngRightClick);
    element.bind('contextmenu', function(event) {
      scope.$apply(function() {
        event.preventDefault();
        fn(scope, {$event:event});
      });
    });
  };
});

