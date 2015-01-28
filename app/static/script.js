$(function() {

	var unfolded = false;
	var id_list = window.location.pathname.split('/');
	var id_list = id_list[id_list.length-1];
	var connection = new autobahn.Connection({
		url: "ws://127.0.0.1:5000/ws",
		realm: "realm1"
	});


	connection.onopen = function (session) {
		console.log("connected");

		session.subscribe('refresh_add_product', function(prod) {
			var li = $('.list_achat').find('li#'+prod[0]);
			console.log(prod);
			if(li.size()) {
				li.find("span").html(prod[4]);
			}else{
				$('.list_achat').append('<li class="list-group-item achat" id="'+prod[0]+'">'+prod[2]+'<span class="badge">'+prod[4]+'</span></li>');
			}
		});

		session.subscribe('refresh_remove_product', function(prod) {
			$('.list_achat #'+prod).remove();
		});

		session.subscribe('refresh_create_product', function(prod) {
			$('.list_prod').append('<div class="col-xs-4"><div class="thumbnail product" id="'+prod[0]+'"><p class="">'+prod[1]+'</p><p>+</p></div></div>')
		});
	};

	// remove product of cart
	$('.list_achat').on("click", ".achat", function() {
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
	$('.list_prod').on('click', '.product', function() {
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

	//create a new product
	$('#bt_create_product').click(function() {
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

	//add friend
	$('#bt_add_friend').click(function() {
		if(connection.session) {
			var name = $('#name').val();
			connection.session.call('me.hory.add_friend', [name, id]).then(
				function(res) {
				},
				function(error) {
					console.log('impossible to add friend');
				}
			);
		}
	});

	$('.share').click(function() {
		if (connection.session) {
			connection.session.call('me.hory.share_list', [this.tabIndex, this.title]).then(
				function(res) {
					console.log("yeah");
				},
				function(error) {
					console.log("nooooo");
				}
			);
		}
	});

	connection.open();

});
