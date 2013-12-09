'use strict'

var weddingApp = angular.module('weddingApp', []);

weddingApp.controller('BrotherListCtrl', function($scope, $http){
	$http.get('data/members.js').success(function(data) {
	var brothers = [];
	for (var i in data) {
		if (1 == data[i]['role'] && true == data[i]['is_come']) {
			brothers.push(data[i]);	
		}
	}
	$scope.brothers = brothers;
	});
});
