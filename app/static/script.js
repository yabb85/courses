$(function() {

	var unfolded = false;
	var id_list = window.location.pathname.split('/');
	var id_list = id_list[id_list.length-1];
	var connection = new autobahn.Connection({
		url: "ws://127.0.0.1:8080/ws",
		realm: "realm1"
	});


	connection.onopen = function (session) {
		console.log("connected");

		session.subscribe('refresh_add_product', function(prod) {
			var li = $('#liste').find('li#'+prod[0]);
			console.log(prod);
			if(li.size()) {
				li.find("span").html(prod[4]);
			}else{
				$('#liste').append('<li class="list-group-item panier" id="'+prod[0]+'">'+prod[2]+'<span class="badge">'+prod[4]+'</span></li>');
			}
		});

		session.subscribe('refresh_remove_product', function(prod) {
			$('#liste #'+prod).remove();
		});

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


	$('#liste').on("click", ".panier", function() {
		if (connection.session) {
			connection.session.call('me.hory.remove_to_list', [this.id, id_list]).then(
				function(res){
					console.log('product removed to list');
				},
				function(error){
					console.log('impossible to remove product in list');
				}		
			);
		}
	});


	$('.achat').click(function() {
		if (connection.session) {
			connection.session.call('me.hory.add_to_list', [this.id, id_list]).then(
				function(res){
					console.log('product added to list');
				},
				function(error){
					console.log('impossible to add product in list');
				}		
			);
		}
	});


	$('#button_add').click(function() {
		if($('#form_add_product').css('display') == "none") {
			$('#form_add_product').css("display", "block");
		} else {
			$('#form_add_product').css("display", "none");
		}
		unfolded = !unfolded;
	});


	connection.open();
});
