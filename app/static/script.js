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

		session.subscribe('refresh_create_product', function(prod) {
			$('#list_prod').append('<li class="list-group-item achat" id="'+prod[0]+'">'+prod[1]+'<img class="unfold" src="" alt="&#x271A" /></li>')
		});
	};

	// remove product of cart
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


	// add an article to cart
	$('#list_prod').on('click', '.achat', function() {
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

	//unfold form to create product
	$('#button_add').click(function() {
		if($('#form_add_product').css('display') == "none") {
			$('#form_add_product').css("display", "block");
		} else {
			$('#form_add_product').css("display", "none");
		}
		unfolded = !unfolded;
	});

	//create a new product
	$('#create').click(function() {
		if(connection.session) {
			var name = $('#name').val();
			var price = $('#price').val();
			var quantity = $('#quantity').val();
			var unit = $('#unit').val();
			var img = $('#img').val();
			connection.session.call('me.hory.create_product', [name, price, quantity, unit, img]).then(
				function(res) {
					console.log('product created');
				},
				function(error) {
					console.log('impossible to create product');
				}
			);
		}
	});

	connection.open();
});
