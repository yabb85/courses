
function createProduct() {
	if(connection.session) {
		var name = $('#name').val();
		var price = $('#price').val();
		var quantity = $('#quantity').val();
		var unit = $('#unit').val();
		var img = $('#img').val();
		newProduct(name, price, quantity, unit, img);
	}
};
