import React from 'react';
import { Link, IndexLink } from 'react-router';
import Auth from '../modules/Auth';


/* Application */
var App = React.createClass({
	displayName: "Application",
	getInitialState() {
		return {
			loggedIn: Auth.loggedIn()
		}
	},
	updateAuth(loggedIn) {
		this.setState({
			loggedIn
		})
	},
	componentWillMount() {
		Auth.onChange = this.updateAuth
		Auth.login()
	},
	render: function() {
		return(
				<div>
					<nav className="navbar navbar-inverse navbar-fixed-top" role="navigation">
						<div className="container">
							<div className="navbar-header">
								<button type="button" className="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
									<span className="sr-only">Toggle navigation</span>
									<span className="icon-bar"></span>
									<span className="icon-bar"></span>
									<span className="icon-bar"></span>
								</button>
								<IndexLink to="/" className="navbar-brand">Course</IndexLink>
							</div>
							<div id="navbar" className="navbar-collapse collapse">
									{this.state.loggedIn ? (
										<ul className="nav navbar-nav navbar-right">
											<li>
												<Link to="/profile">profil</Link>
											</li>
											<li>
												<Link to="/logout">deconnexion</Link>
											</li>
										</ul>
									) : (
										<ul className="nav navbar-nav navbar-right">
											<li>
												<Link to="/login">connexion</Link>
											</li>
										</ul>
									)}
							</div>
						</div>
					</nav>
					<div className="container">
						<div className="starter-template">
							{this.props.children}
						</div>
					</div>
				</div>
			  );
	}
});

export default App
