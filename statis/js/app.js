"use strict";

var myApp = angular.module('myApp', [
    'ngResource',
    'ngFileUpload',
    'toaster',
]);



// asd
/**
 * Configure our angular app
 */
myApp.config(function($resourceProvider) {
    $resourceProvider.defaults.stripTrailingSlashes = false;
});

/**
 * Main Controller of our App
 * Handles the image upload within the frontend
 */
myApp.controller('MainCtrl', function($http,$scope, Images, toaster)
{
    $scope.showImage = false;
    console.log('In main Control');

    $scope.images = [];

    $scope.newImage = {};


    $scope.imagesLoading = false;

    $scope.loadImages = function() {
        $scope.imagesLoading = true;

        return Images.query().$promise.then(
            // on success
            function success(response) {
                // store response
                $scope.images = response;
                // loading has finished
                $scope.imagesLoading = false;

                return response;
            },
            // on error
            function error(rejection) {
                // log the error to console
                console.log(rejection);
                // loading has finished (although with an error)
                $scope.imagesLoading = false;
                return rejection;
            }
        );
    };

    /**
     * Upload an Image on Button Press
     */
    $scope.uploadImage = function()
    {

        Images.save($scope.newImage).$promise.then(
            function(response) {
              console.log('Saving images');
              console.log('URL');
              var url = 'http://185.22.67.87:8000/openalpr/check?nameOf='
              console.log(url);
                $scope.images.unshift(response);
                toaster.pop('success', "Image uploaded!");
                $http({
                    method: 'GET',
                    url: url+$scope.newImage['image']['name'],
                }).then(function(data, status, headers, config){
                    if(data['data']['found']==true){
                      console.log(data['data']);
                      $scope.imagesLoading = data['data']['found'];
                      $scope.imagePath = data['data']['filename']
                      $scope.plate = data['data']['plate'];
                      $scope.newImage = {};
                      $scope.imagePath = $scope.imagePath.split('/plateReg')[1];
                      console.log($scope.imagePath);
                    }else{
                      console.log(data['data']);
                      $scope.imagesLoading = true;
                      $scope.imagePath = data['data']['filename']
                      $scope.plate = data['data']['plate'];
                      $scope.newImage = {};
                      $scope.imagePath = $scope.imagePath.split('/plateReg')[1];
                      console.log($scope.imagePath);
                    }

                });
            },
            function(rejection) {
                console.log('Failed to upload image');
                console.log(rejection);
                toaster.pop('error', "Failed to upload image");
            }
        );
    };

    /**
     * Delete an image on Button Press
     */
    $scope.deleteImage = function(image)
    {
        // call REST API endpoint
        image.$delete(
            // process response of delete
            function(response)
            {
                // success delete
                console.log('Deleted it');

                // update $scope.images
                var idx = $scope.images.indexOf(image);
                if (idx < 0) {
                    console.log('Error: Could not find image');
                } else {
                    $scope.images.splice(idx, 1);
                }

                toaster.pop('success', "Image deleted");

                // alternatively, update $scope.images from REST API
                // $scope.loadImages();
            },
            function(rejection)
            {
                // failed to delete it
                console.log('Failed to delete image');
                console.log(rejection);
                toaster.pop('error', "Failed to delete image");
            }
        );
    };


    // load images from API
    $scope.loadImages();
});
