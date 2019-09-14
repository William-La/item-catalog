// code adapted from:
// https://developers.google.com/identity/sign-in/web/sign-in
function onSignIn(googleUser) {
  var id_token = googleUser.getAuthResponse().id_token;
  var xhr = new XMLHttpRequest();
  xhr.open('POST', 'http://localhost:8000/googleoauth');
  xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
  xhr.onload = function() {
    if (localStorage.getItem('token')) {
      localStorage.setItem('token', xhr.responseText);
    } else {
      localStorage.setItem('token', xhr.responseText);
      window.location.href = 'http://localhost:8000/';
    }
  };
  xhr.send('idtoken='+id_token);
}

function signOut() {
  localStorage.removeItem('token');
  if (gapi.auth2) {
    var auth2 = gapi.auth2.getAuthInstance();
    auth2.signOut().then(function() {
      console.log('User signed out.');
    });
  }
  var xhr = new XMLHttpRequest();
  xhr.open('POST', 'http://localhost:8000/googleoauth');
  xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
  xhr.onload = function() {
    window.location.href = 'http://localhost:8000/';
  };
  xhr.send('signout');
}
