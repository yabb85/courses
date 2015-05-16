'use strict';

var cartServices = angular.module('cartServices', []);


cartServices.service('requestService', function($http) {
	this.list = function(){
		var promise = $http.get('/api/list/').then(function(reponse){
			return reponse.data.lists;
		});
		return promise;
	};

	this.friends = function(){
		var promise = $http.get('/api/friends/').then(function(reponse){
			return reponse.data.friends;
		});
		return promise;
	};

	this.share = function(list_id, friend_id) {
		var promise = $http.post('/api/share/', {'friend': friend_id,'cart': list_id}).then(function(repose){
			return reponse.data
		});
		return promise;
	};

});
