var toto = window.location.pathname.split('/');
var toto = toto[toto.length-1];

var connection = new autobahn.Connection({
	url: "ws://127.0.0.1:8080/ws",
	realm: "realm1"
});

connection.onopen = function (session) {
	console.log("connected");

	session.subscribe('refresh_add_product', function(prod, liste) {
		$('#liste').append('<li class="produit" id="'+prod[0]+'" onclick=removeProduct('+prod[0]+','+prod[1]+')>'+prod[2]+'</li>');
	});

	session.subscribe('refresh_remove_product', function(prod) {
		$('#liste #'+prod).remove();
	});

	addToList = function(product, liste, name) {
		session.call('me.hory.add_to_list', [product, liste, name]).then(
			function(res){
				console.log('product added to list');
			},
			function(error){
				console.log('impossible to add product in list');
			}		
		);
	}	
	
	removeToList = function(product, liste) {
		session.call('me.hory.remove_to_list', [product, liste]).then(
			function(res){
				console.log('product removed to list');
			},
			function(error){
				console.log('impossible to remove product in list');
			}		
		);
	}	
};

connection.open();


function addProduct(product, list_id, name) {
	//$('#liste').append('<li>'+product+'</li>');
	if(connection.session) {
		addToList(product, list_id, name);
	}
};

function removeProduct(product, list_id) {
	//$('#liste').append('<li>'+product+'</li>');
	if(connection.session) {
		removeToList(product, list_id);
	}
};
