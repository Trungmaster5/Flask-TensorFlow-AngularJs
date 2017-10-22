(function () {
'use strict';

angular.module('Urban',['ngMaterial'])
.controller('UrbanController', UrbanController);

function UrbanController($scope, $http){
  var $ctrl=this;
  var apiPath='/api/predict'
  $scope.predict=0;
  $scope.confidence=0;
  $scope.get_labels=0;
  $scope.processing=false;

  // $scope.audioUrl='media/'+$scope.selectedObj+'*.wav';

  $ctrl.run=function(){
    $scope.processing=true;
  	$http.post(apiPath, {media:$scope.selectedObj})
                          .then(function(response){
                              console.log({response:response});
                              $scope.predict=response.data.predict;
                              $scope.confidence=response.data.confidence;
                              $scope.get_labels=response.data.true_labels;
                              $scope.processing=false;
                              return response;
                            }, function(error){
                              console.log({error:error});
                              warning(error.statusText);
                              return error;
                            });
    };
  }
 })();
