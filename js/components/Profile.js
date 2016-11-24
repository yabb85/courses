import React from 'react';


var Inscription = React.createClass({
	displayName: "Inscription",
	render: function() {
		return(
				<div>
					<h1>Profil</h1>
					<div className="col-md-12">
						<div className="btn-group">
							<div className="dropdown">
								<button type="button" className="btn btn-primary dropdown-toggle" data-toggle="dropdown">
									Ajouter un amis <span className="caret"></span>
								</button>
								<div className="dropdown-menu">
									<form id="form_add_friend">
										<label htmlFor="name">Nom:</label>
										<input type="text" name="name"/>
										<p>ou</p>
										<label htmlFor="name">Email:</label>
										<input type="email" name="mail"/>
										<input type="button" value="Creer"/>
									</form>
								</div>
							</div>
						</div>
						<div className="col-md-12">
							Amis
							<ul className="list-group">
								<li className="list-group-item">
								<div className="btn-group btn-group-sm" role="group">
									<div className="btn-group btn-group-sm" role="group">
										<button className="btn btn-default dropdown-toggle" type="button" data-toggle="dropdown">
											<i className="fa fa-share-alt"></i>
										</button>
										<ul className="dropdown-menu" role="menu">
										</ul>
									</div>
									<button className="btn btn-default" type="button">
										✗
									</button>
								</div>
								</li>
							</ul>
						</div>
					</div>
				</div>
			  );
	}
});

export default Inscription;
