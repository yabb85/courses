import React from 'react'
import $ from 'jquery'


var Inscription = React.createClass({
	displayName: "Inscription",
	getInitialState: function() {
		return({
			message: ''
		})
	},
	handleSubmit: function(event) {
		event.preventDefault();

		const name = this.refs.name.value
		const email = this.refs.email.value
		const password = this.refs.password.value

		let url = '/api/users'
		let data = {
			name : name,
			email: email,
			password: password
		}
		$.ajax({
			url: url,
			type: 'POST',
			contentType: 'application/json',
			dataType: 'json',
			data: JSON.stringify(data),
			success: function(data) {
				console.log(data)
				this.setState(data)
			}.bind(this),
			error: function(data) {
				console.log(data)
				this.setState(data)
			}.bind(this)
		})
	},
	render: function() {
		return(
				<form onSubmit={this.handleSubmit}>
					<label htmlFor="name">Nom:</label>
					<input type="text" name="name" ref="name"/>
					<label htmlFor="email">Mail:</label>
					<input type="email" name="email" ref="email"/>
					<label htmlFor="password">Password:</label>
					<input type="password" name="password" ref="password"/>
					<button type="submit">Register</button>
					{ this.state.message && (
						<p>{this.state.message}</p>
					)}
				</form>

			  );
	}
});

export default Inscription;
