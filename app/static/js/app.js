'use strict';


var cartApp = angular.module('myCart', [
	'vxWamp',
	'ngRoute',
	'cartControllers'
]);

cartApp.config(['$routeProvider', 
	function($routeProvider){
		$routeProvider.when('/', {
			templateUrl: '../static/partial/home.html'
		}).
		when('/test/:listId', {
			templateUrl: '../static/partial/test.html',
			controller: 'courseCtrl'
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
	
cartApp.run(function($wamp){
	$wamp.open();
})
