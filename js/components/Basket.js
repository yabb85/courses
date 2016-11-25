import React from 'react'
import { Dropdown, DropdownButton, MenuItem, Button } from 'react-bootstrap'
import EventEmitter from 'events'
import $ from 'jquery'
import io from 'socket.io-client'


var socket = io('http://localhost:5000')

/* Define local store */
var CHANGE_EVENT = 'change'

var _basket = {
	id: '',
	name: '',
	products: [],
	inBasket: []
}

var Actions = {
	loadProductList: function() {
		/*
		 * Retrieve a list of products
		 */
		let url_products = "/api/products";
		$.ajax({
			url: url_products,
			type: 'GET',
			contentType: 'application/json',
			beforeSend: function (xhr) {
				xhr.setRequestHeader('Authorization', "JWT " + localStorage.token);
			},
			success: function(data) {
				_basket.products = data.products
				Store.emitChange()
			},
			error: function(data) {
				console.error(data)
			}
		});
	},
	loadBasketList: function() {
		/*
		 * Retrieve a list of products in basket
		 */
		let url_basket = "/api/baskets/" + _basket.id;
		$.ajax({
			url: url_basket,
			beforeSend: function (xhr) {
				xhr.setRequestHeader('Authorization', "JWT " + localStorage.token);
			},
			success: function(data) {
				_basket.id = data.id
				_basket.name = data.name
				_basket.inBasket = data.inBasket
				Store.emitChange()
			},
			error: function(data) {
				console.error(data)
			}
		});
	},
	createProduct: function(data) {
		/*
		 * create a new product
		 */
		let url = '/api/products'
		$.ajax({
			url: url,
			type: 'POST',
			contentType: 'application/json',
			dataType: 'json',
			data: JSON.stringify(data),
			beforeSend: function (xhr) {
				xhr.setRequestHeader('Authorization', "JWT " + localStorage.token);
			},
			success: function(data) {
				_basket.products = data.products
				Store.emitChange()
			},
			error: function(data) {
				console.error(data)
			}
		})
	},
	addProduct: function(item) {
		/*
		 * Add a new product in basket
		 */
		let url = "/api/baskets/" + _basket.id
		let data = {
			id: item.id
		}
		$.ajax({
			url: url,
			type: 'POST',
			contentType: 'application/json',
			dataType: 'json',
			data: JSON.stringify(data),
			beforeSend: function (xhr) {
				xhr.setRequestHeader('Authorization', "JWT " + localStorage.token);
			},
			success: function(data) {
				//_basket.inBasket = data.inBasket
				//Store.emitChange()
			},
			error: function(data) {
				console.error(data)
			}

		})
	},
	removeProduct: function(item) {
		/*
		 * Remove product in basket
		 */
		let url = "/api/baskets/" + _basket.id
		let data = {
			id: item.id
		}
		$.ajax({
			url: url,
			type: 'DELETE',
			contentType: 'application/json',
			dataType: 'json',
			data: JSON.stringify(data),
			beforeSend: function (xhr) {
				xhr.setRequestHeader('Authorization', "JWT " + localStorage.token);
			},
			success: function(data) {
				//_basket.inBasket = data.inBasket
				//Store.emitChange()
			},
			error: function(data) {
				console.error(data)
			}

		})
	},
	updateBasket: function(data) {
		_basket = data
		Store.emitChange()
	}
}

var Store = Object.assign({}, EventEmitter.prototype, {

	getBasket: function() {
		return _basket;
	},

    emitChange: function() {
        this.emit(CHANGE_EVENT);
    },

    addChangeListener: function(callback) {
        this.on(CHANGE_EVENT, callback);
    },

    removeChangeListener: function(callback) {
        this.removeListener(CHANGE_EVENT, callback);
    }
});


/* define component for custom menu to add product */
var CustomMenu = React.createClass({
	displayName: 'CustomMenu',
	getInitialState: function() {
		return({
			name: '',
			img: ''
		})
	},
	updateName: function(event) {
		let state = this.state
		state.name = event.target.value
		this.setState(state)
	},
	updateQuantity: function(event) {
		let state = this.state
		this.setState(state)
	},
	updateImg: function(event) {
		let state = this.state
		state.img = event.target.value
		this.setState(state)
	},
	handleSubmit: function(event) {
		event.preventDefault()
		Actions.createProduct(this.state)
		this.props.onClose(event)
	},
	render: function() {
		return (
			<div className="dropdown-menu">
				<form id="form_create_product" className="form-group" onSubmit={this.handleSubmit}>
					<label htmlFor="name">Nom:</label>
					<input type="text" name="name" className="form-control" ref="name" value={this.state.name} onChange={this.updateName}/>
					<label htmlFor="img">Image:</label>
					<input type="text" name="img" className="form-control" ref="img" value={this.state.img} onChange={this.updateImg}/>
					<button type="submit">Creer</button>
				</form>
			</div>
		);
	}
})

/* define component to create a product tile */
var ProductItem = React.createClass({
	dispalyName: 'ProductItem',
	handleClick: function(event) {
		event.preventDefault()
		Actions.addProduct(this.props.data)
	},
	render: function() {
		return(
			<div className="col-xs-4 col-sm-3 col-lg-2" onClick={this.handleClick}>
				<div className="thumbnail product">
					<p className="">{this.props.data.name}</p>
				</div>
			</div>
		)
	}
})

/* define component to create a product tile in basket list */
var BasketItem = React.createClass({
	dispalyName: 'BasketItem',
	handleClick: function(event) {
		event.preventDefault()
		Actions.removeProduct(this.props.data)
	},
	render: function() {
		return(
			<li className="list-group-item" onClick={this.handleClick}>
				{this.props.data.name}
				<span className="badge">{this.props.data.quantity}</span>
			</li>
		)
	}
})

/* basket component */
var Basket = React.createClass({
	displayName: 'Basket',
	getInitialState: function() {
		return Store.getBasket();
	},
	componentWillMount: function() {
		Store.removeChangeListener(this._onChange);
	},
	componentDidMount: function() {
		Store.addChangeListener(this._onChange)
		_basket.id = this.props.params.id
		Actions.loadProductList()
		Actions.loadBasketList()
		Store.emitChange()
		socket.on('connect', function() {
			socket.emit('join', {room: _basket.id})
		})
		socket.on('update', function(data) {
			console.log('received')
			Actions.updateBasket(data)
		})
	},
	componentWillUnmount: function() {
		Store.removeChangeListener(this._onChange);
		socket.emit('leave', {room: this.state.id})
	},
	render: function() {
		var createProductItem = function(item) {
			return(
				<ProductItem key={item.id} data={item}/>
			)
		}
		var createBasketItem = function(item) {
			return(
				<BasketItem key={item.id} data={item}/>
			)
		}
		var countProduct = function(array) {
			let cpt = 0
			array.map(x => cpt += x.quantity)
			return cpt
		}
		return(
			<div className="col-md-12 left">
				<div className="row">
					<Dropdown id="test">
						<Dropdown.Toggle bsStyle='primary'>
							Ajouter un nouveau produit
						</Dropdown.Toggle>
						<CustomMenu bsRole="menu">
						</CustomMenu>
					</Dropdown>
				</div>
				<div className="col-md-6" role="tabpanel">
					<h3>Panier</h3>
					<ul className="list-group list_achat">
						{this.state.inBasket.map(createBasketItem)}
					</ul>
					<strong>{countProduct(this.state.inBasket)}</strong> produit(s) dans le panier.
				</div>
				<div className="col-md-6" role="tabpanel">
					<h3>Produits</h3>
					<div className="row list_prod">
						{this.state.products.map(createProductItem)}
					</div>
				</div>
			</div>
		);
	},
	_onChange: function() {
		this.setState(Store.getBasket())
	}
});

export default Basket;
