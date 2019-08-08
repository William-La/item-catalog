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
  xhr.send('idtoken=' + id_token);
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

function getRequestHandler(url) {
  var xhr = new XMLHttpRequest();
  xhr.open('GET', 'http://localhost:8000' + url);
  xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
  if (localStorage.getItem('token')) {
    xhr.setRequestHeader(
      'Authorization',
      'Token ' + localStorage.getItem('token')
    );
  }
  xhr.onload = function() {
    if (xhr.responseText == 'Unauthorized Access') {
      window.location.href = 'http://localhost:8000/';
    } else {
      document.querySelector('#response').innerHTML = xhr.responseText;
      window.history.pushState('object or string', 'Title', url);

      if (localStorage.getItem('token')) {
        refreshToken();
      }
    }
  };
  xhr.send();
}


function refreshToken() {
  var xhr = new XMLHttpRequest();
  xhr.open('GET', 'http://localhost:8000/token');
  xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
  xhr.setRequestHeader(
    'Authorization',
    'Token ' + localStorage.getItem('token')
  );

  xhr.onload = function() {
    localStorage.setItem('token', xhr.responseText);
  };
  xhr.send();
}