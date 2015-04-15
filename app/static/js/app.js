'use strict';


var cartApp = angular.module('myCart', [
	'vxWamp',
	'ngRoute',
	'cartControllers'
]);

cartApp.config(['$routeProvider', 
	function($routeProvider){
		$routeProvider.when('/', {
			templateUrl: '../static/partial/index.html',
			controller: 'indexCtrl'
		}).
		when('/list/', {
			templateUrl: '../static/partial/allCarts.html',
			controller: 'allCartsCtrl'
		}).
		when('/list/:listId', {
			templateUrl: '../static/partial/cart.html',
			controller: 'cartCtrl'
		}).
		when('/login/', {
			templateUrl: '../static/partial/login.html',
			controller: 'loginCtrl'
		}).
		when('/profil/', {
			templateUrl: '../static/partial/profil.html',
			controller: 'profilCtrl'
		}).
		otherwise({
			redirectTo: '/test'
		});
	}
]);

cartApp.config(['$wampProvider', 
	function($wampProvider){
		$wampProvider.init({
			url: "ws://127.0.0.1:8080/ws",
			realm: "realm1"
		});
	}
]);

cartApp.run(function($rootScope, $wamp, $http){
	$wamp.open();
	$http({
		url: '/api/connected/',
		method: 'get',
	}).success(function(data) {
		$rootScope.connected = data.connected;
	}).error(function(data){
		console.log(data);
	});
	$rootScope.connected = false;
})
