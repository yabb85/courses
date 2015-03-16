



var app = angular.module('myCart', ['vxWamp']);

app.config(function($wampProvider){
	$wampProvider.init({
		url: "ws://127.0.0.1:8080/ws",
		realm: "realm1"
	});
});
	

app.controller('courseCtrl', function($scope, $http, $wamp){

	$scope.id_list = window.location.pathname.split('/');
	$scope.id_list = $scope.id_list[$scope.id_list.length-1];

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

	/* Request to REST api */
	$http.get('/api/extended_list/1').success(function(data){
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
		$wamp.call('me.hory.add_to_list', [id, $scope.id_list]).then(
			function(res){
				console.log('product added to list');
			},
			function(error){
				console.log('impossible to add product in list');
			}
		);
	}

	$scope.removeToCart = function(id){
		$wamp.call('me.hory.remove_to_list', [id, $scope.id_list]).then(
			function(res){
				console.log('product removed to list');
			},
			function(error){
				console.log('impossible to remove product in list');
			}
		);
	}

});

app.run(function($wamp){
	$wamp.open();
})
