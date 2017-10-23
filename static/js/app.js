(function () {
'use strict';

angular.module('Urban',['ngMaterial'])
.controller('UrbanController', UrbanController);

function UrbanController($scope, $http){
  var $ctrl=this;
  var apiPath='/api/predict';
  $scope.predict=0;
  $scope.confidence=0;
  $scope.get_labels=0;
  $scope.isProcessing=false;
  $scope.selectedObj="";
  $scope.error="";
  // $scope.audioUrl='media/'+$scope.selectedObj+'*.wav';

  $ctrl.run=function(){
    $scope.error="";
    $scope.isProcessing=true;
  	$http.post(apiPath, {'media':$scope.selectedObj})
                          .then(function(response){
                              console.log({response:response});
                              $scope.predict=response.data.predict;
                              $scope.confidence=response.data.confidence;
                              $scope.get_labels=response.data.true_labels;
                              $scope.isProcessing=false;
                              return response;
                            }, function(error){
                              console.log({error:error});
                              $scope.error=error.data;
                              $scope.isProcessing=false;
                              return error;
                            });
    };
  }
 })();
