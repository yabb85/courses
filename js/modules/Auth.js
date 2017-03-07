import { browserHistory } from 'react-router'
import $ from 'jquery'

module.exports = {
  login(login, pass, cb) {
    cb = arguments[arguments.length - 1]
    if (localStorage.token) {
      if (cb) cb(true)
      this.onChange(true)
      return
    }
    pretendRequest(login, pass, (res) => {
      if (res.authenticated) {
        localStorage.token = res.token
        if (cb) cb(true)
        this.onChange(true)
      } else {
        if (cb) cb(false)
        this.onChange(false)
      }
    })
  },

  getToken() {
    return localStorage.token
  },

  logout(cb) {
    delete localStorage.token
    if (cb) cb()
    this.onChange(false)
	browserHistory.push('/login')
  },

  loggedIn() {
    return !!localStorage.token
  },

  onChange() {}
}

function pretendRequest(login, pass, cb) {
	setTimeout(function() {
		let url = '/api/login';
		var data = {
			login: login,
			password: pass
		}
		return $.ajax({
			type: "POST",
			url: url,
			contentType: "application/json; charset=utf-8",
			dataType: "json",
			data: JSON.stringify(data),
			success: function(data) {
				console.log(data);
				cb({
					authenticated: true,
					token: data.access_token
				})
			},
			error: function(data) {
				console.log('fail');
				console.log(data)
				cb({
					authenticated: false
				})
			}
		});
	}, 0)
}
