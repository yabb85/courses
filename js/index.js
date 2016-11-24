import React from 'react';
import { Router, browserHistory } from 'react-router';
import routes from './config/routes.js'

var Index = React.createClass({
	displayName: "Index",
	render: function() {
		return(
				<Router history={browserHistory} routes={routes}>
				</Router>
			  );
	}
});

export default Index;
