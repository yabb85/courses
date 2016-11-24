import React from 'react';
import { withRouter } from 'react-router';
import Auth from '../modules/Auth.js';

var Login = withRouter(
		React.createClass({
			displayName: "Login",
			getInitialState: function() {
				return {
					error: false
				}
			},
			handleSubmit: function(event) {
				event.preventDefault();

				const login = this.refs.login.value;
				const pass = this.refs.pass.value;

				Auth.login(login, pass, (loggedIn) => {
					if (!loggedIn)
						return this.setState({error: true});

					const { location } = this.props;
					if (location.state && location.state.nextPathname) {
						this.props.router.replace(location.state.nextPathname);
					} else {
						this.props.router.replace('/');
					}
				});
			},
			render: function() {
				return(
						<form onSubmit={this.handleSubmit}>
							<label><input ref='login' placeholder='login'/></label>
							<label><input ref='pass' placeholder='password'/></label>
							<button type='submit'>login</button>
							{this.state.error && (
								<p>Bad login information</p>
							)}
						</form>
					);
			}
	})
);

export default Login;
