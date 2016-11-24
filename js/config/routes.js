import Auth from '../modules/Auth.js'
import App from '../components/App'
import Login from '../components/Login'
import Inscription from '../components/Inscription'
import Home from '../components/Home'
import Profile from '../components/Profile'
import Basket from '../components/Basket'

const routes = {
	components: App,
	childRoutes: [
		{
			path: '/',
			getComponent: (location, callback) => {
				if (Auth.loggedIn()) {
					callback(null, Home);
				} else {
					callback(null, Inscription);
				}
			}
		},
		{
			path: '/login',
			component: Login
		},
		{
			path: '/logout',
			onEnter: (nextState, callback) => {
				Auth.logout();
				callback(null, '/');
			}
		},
		{
			path: '/profile',
			getComponent: (location, callback) => {
				if (Auth.loggedIn()) {
					callback(null, Profile);
				} else {
					callback(null, Login);
				}
			}
		},
		{
			path: '/basket/:id',
			getComponent: (location, callback) => {
				if (Auth.loggedIn()) {
					callback(null, Basket);
				} else {
					callback(null, Login);
				}
			}
		}
	]
}

export default routes;
