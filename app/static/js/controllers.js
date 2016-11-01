

var cartControllers = angular.module('cartControllers', ['cartServices']);

cartControllers.controller('cartCtrl', function($scope, $http, $wamp, $routeParams){

	$scope.id_list = window.location.pathname.split('/');
	$scope.id_list = $scope.id_list[$scope.id_list.length-1];
	$scope.product = {};

	/* Wamp */
	//Executed at connection to wamp server
	$scope.$on("$wamp.open", function (event, session) {
		console.log('We are connected to the WAMP Router!');
	});

	//Executed after loose or close connection with wamp server
	$scope.$on("$wamp.close", function (event, data) {
        $scope.reason = data.reason;
        $scope.details = data.details;
    });

	function refreshListAdded(args) {
		var finded = 0;
		for (var i = 0; i < $scope.bought.length; i++) {
			if ($scope.bought[i].id != args[0])
				continue;
			$scope.bought[i].list.quantity = args[3];
			finded = 1
			break;
		};
		if (!finded) {
			$scope.bought.push({
				"id": args[0],
				"list": {
					"id": args[1],
					"product_id": args[0],
					"quantity": args[3]
				},
				"product": {
					"id": args[0],
					"img": args[5],
					"name": args[2],
					"price": 0,
					"quantity": 1,
					"unit": args[4]
				}
			});
		}
	}
	$wamp.subscribe('refresh_add_product', refreshListAdded);

	function refreshListRemoved(args) {
		for (var i = 0; i < $scope.bought.length; i++) {
			if ($scope.bought[i].id != args[0])
				continue;
			$scope.bought.splice(i, 1);
			break;
		};
	}
	$wamp.subscribe('refresh_remove_product', refreshListRemoved);

	function refreshListProduct(args) {
		$scope.items.push({
			"id": args[0],
			"img": args[1],
			"name": args[2],
			"price": 1,
			"quantity": args[4],
			"unit": args[5]
		});
	}
	$wamp.subscribe('refresh_create_product', refreshListProduct);

	/* Request to REST api */
	$http.get('/api/extended_list/' + $routeParams.listId).success(function(data){
		$scope.bought = data.achats;
	}).
	error(function(data){
		console.log(data);
	});

	$http.get('/api/products/').success(function(data){
		$scope.items = data.products;
	}).
	error(function(data){
		console.log(data);
	});

	/* Action */
	$scope.addToCart = function(id){
		$wamp.call('me.hory.add_to_list', [id, $routeParams.listId]).then(
			function(res){
				console.log('product added to list');
			},
			function(error){
				console.log('impossible to add product in list');
			}
		);
	}

	$scope.removeToCart = function(id){
		$wamp.call('me.hory.remove_to_list', [id, $routeParams.listId]).then(
			function(res){
				console.log('product removed to list');
			},
			function(error){
				console.log('impossible to remove product in list');
			}
		);
	}

	$scope.createProduct = function(product) {
		console.log(product.name);
		$wamp.call('me.hory.create_product', [product.name, product.price, product.quantity, product.unit, product.img]).then(
			function(res){
				console.log('product created');
				$scope.product = {};
			},
			function(error){
				console.log('impossible to create product');
			}
		);
	}

});


cartControllers.controller('loginCtrl', function($scope, $rootScope, $http, $location){
	$scope.user_to_login= {};

	$scope.loginUser = function(user) {
		$scope.user_to_login = angular.copy(user);
		$scope.user = {};

		$http({
			url: '/api/login/',
			method: 'post',
			data: $scope.user_to_login
		}).success(function(data) {
			$rootScope.connected = true;
			$location.path('/list');
		}).error(function(data){
			console.log(data);
		});
	};
});

cartControllers.controller('logoutCtrl', function($scope, $rootScope, $http, $location){
	$scope.logoutUser = function() {
		$http({
			url: '/api/logout/',
			method: 'post',
			data: $scope.user_to_login
		}).success(function(data) {
			$rootScope.connected = false;
			$location.path('/');
		}).error(function(data){
			console.log(data);
		});
	};
});

cartControllers.controller('allCartsCtrl', function($scope, $http, requestService) {
	$scope.cart_to_create = {}

	/* Request to REST api */
	requestService.list().then(function(d){
		$scope.allCarts = d
	});

	requestService.friends().then(function(d){
		$scope.friends = d;
	});

	$scope.shareList = requestService.share;

	$scope.createCart = function(cart) {
		$scope.cart_to_create = angular.copy(cart);
		$scope.cart = {};

		$http({
			url: '/api/list/',
			method: 'post',
			data: $scope.cart_to_create
		}).success(function(data) {
			console.log(data);
			$http.get('/api/list/').success(function(data){
				$scope.allCarts = data.lists;
			}).
			error(function(data){
				console.log(data);
			});
		}).error(function(data){
			console.log(data);
		});
	};

	$scope.removeCart = function(cart) {
		$http({
			url: '/api/list/' + Number(cart),
			method: 'delete',
		}).success(function(data) {
			console.log(data);
			$http.get('/api/list/').success(function(data){
				$scope.allCarts = data.lists;
			}).
			error(function(data){
				console.log(data);
			});
		}).error(function(data){
			console.log(data);
		});

	};
});

cartControllers.controller('profilCtrl', function($scope, $http, requestService) {

	requestService.friends().then(function(d){
		$scope.friends = d;
	});

	requestService.list().then(function(d){
		$scope.lists = d;
	});


	$scope.addFriends = function(new_friend) {
		$scope.friends_to_create = angular.copy(new_friend);
		$scope.new_friend = {};
		console.log($scope.friends_to_create);

		$http({
			url: '/api/friend/',
			method: 'post',
			data: $scope.friends_to_create
		}).success(function(data) {
			console.log(data);
			//$scope.friends = data.friends;
		}).error(function(data){
			console.log(data);
		});
	};

	$scope.shareList = requestService.share;
});

cartControllers.controller('indexCtrl', function($scope, $http){
	$scope.createUser = function(register) {
		$scope.register_to_create = angular.copy(register);
		$scope.register = {};

		console.log(register);
		$http({
			url: '/api/register/',
			method: 'post',
			data: $scope.register_to_create
		}).success(function(data) {
			console.log(data);
		}).error(function(data) {
			console.log(data);
		});
	};
});
