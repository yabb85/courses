var id_list = window.location.pathname.split('/');
var id_list = id_list[id_list.length-1];

var connection = new autobahn.Connection({
	url: "ws://127.0.0.1:8080/ws",
	realm: "realm1"
});

var unfolded = false;


connection.onopen = function (session) {
	console.log("connected");

	session.subscribe('refresh_add_product', function(prod) {
		var li = $('#liste').find('li#'+prod[0])
		if(li.size()) {
			li.find("span").html(prod[4]);
		}else{
			$('#liste').append('<li class="achat" id="'+prod[0]+'" onclick=removeProduct('+prod[0]+','+prod[1]+')><img class="img_achat" src="/static/'+prod[3]+'" alt="'+prod[2]+'"/><span class="count_achat">'+prod[4]+'</span></li>');
		}
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

	newProduct = function(name, price, quantity, unit, img) {
		session.call('me.hory.create_product', [name, price, quantity, unit, img]).then(
			function(res) {
				console.log('product created');
			},
			function(error) {
				console.log('impossible to create product');
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

function unfold() {
	if($('#form_add_product').css('display') == "none") {
		$('#form_add_product').css("display", "block");
	} else {
		$('#form_add_product').css("display", "none");
	}
	unfolded = !unfolded;
};
