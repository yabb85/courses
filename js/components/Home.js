import React from 'react';
import $ from 'jquery';
import Auth from '../modules/Auth.js'

var Item = React.createClass({
	displayName: "Item",
	render: function() {
		var createItem = function(item) {
			return(
				<li className="btn btn-default">{item}</li>
			);
		}
		return (
			<li className="list-group-item">
				<a className="btn" href={"/basket/" + this.props.data.id}>{this.props.data.name}</a>
				<div className="btn-group btn-group-sm" role="group">
					<div className="btn-group btn-group-sm" role="group">
						<button className="btn btn-default dropdown-toggle" type="button" data-toggle="dropdown">
							<i className="fa fa-share-alt"></i>
						</button>
						<ul className="dropdown-menu" aria-labelledby="share_list" role="menu">
						</ul>
					</div>
					<button className="btn btn-default" type="button">
						✗
					</button>
				</div>
			</li>
		);
	}
});


var Home = React.createClass({
	displayName: "Home",
	getInitialState: function() {
		return {
			Baskets: []
		}
	},
	componentDidMount: function() {
		let url = "/api/baskets";
		return $.ajax({
			url: url,
			beforeSend: function (xhr) {
				xhr.setRequestHeader('Authorization', "JWT " + localStorage.token);
			},
			success: function(data) {
				this.setState(data);
			}.bind(this),
			error: function(data) {
				if (data.status == 401 || data.status == 403) {
					Auth.logout()
				}
			}.bind(this)
		});

	},
	handleSubmit: function(event) {
		event.preventDefault()

		const name = this.refs.name.value

		let url = '/api/baskets'
		let data = {
			name: name
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
				this.setState(data)
			}.bind(this),
			error: function(data) {
				if (data.status == 401 || data.status == 403) {
					Auth.logout()
				}
			}.bind(this)
		})
	},
	render: function() {
		var createItem = function(item) {
			return(
				<Item key={item.name} data={item}/>
			);
		}
		return (
			<div className="col-md-12">
				<div>
					<form onSubmit={this.handleSubmit} acceptCharset="utf-8">
						Nouvelle Liste:
						<input type="text" name="name" ref="name"/>
						<button type="submit">Créer</button>
					</form>
				</div>

				<h1>All carts</h1>

				<ul className="list-group">
					{this.state.Baskets.map(createItem)}
				</ul>
			</div>
		);
	}
});

export default Home;
