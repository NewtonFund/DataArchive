'use strict';

// Register `phase2rotator` component, along with its associated controller and template
angular.
module('phase2Rotator').
component('phase2Rotator', {
    templateUrl: 'phase2-rotator/phase2-rotator.template.html',
    controller: [ '$http',
        function($http) {

            var self = this;

            self.loadHelloWorld = function () {
                $http.get("server-side/generate_hello_world.py")
                .success( function (data) {
                    $http.get("server-side/helloworld.txt")
                    .success( function (data) {
                        alert(data);
                        console.log(data);
                    })
                    .error(function() {
                        alert("File not found.");
                    })
                })
                .error(function() {
                    alert("Script not found.");
                })



//                $http.head("server-side/generate_hello_world.py")
//                .then( function success(data) {
//                    alert(data);
//                    console.log(data);
//                } , function error(data) {
//                    alert("Python script not found.");
//                })

//                $http.get("server-side/generate_hello_world.py").success(function (data) {
//                    alert(data);
                    //console.log(data);
                    //fs.createWriteStream().write(data);
//                }).error(function() {
//                    alert("Python script not found.");
//                })
            }

        }
    ]
});
