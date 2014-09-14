var toto = window.location.pathname.split('/');
var toto = toto[toto.length-1];

var connection = new autobahn.Connection({
	url: "ws://127.0.0.1:8080/ws",
	realm: "realm1"
});

connection.onopen = function (session) {
	console.log("connected");

	session.subscribe(toto, function(val) {
		$('#liste').append('<li>'+val+'</li>');
	});

	publication = function(product, liste) {
		session.publish(liste, [product]);
	}	
};

connection.open();


function addProduct(product, liste) {
	alert(toto);
	$('#liste').append('<li>'+product+'</li>');
	if(connection.session) {
		publication(product, liste);
	}
};
