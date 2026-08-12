/* =========================================================
   ACT — login & signup form logic
   ========================================================= */

function showFieldError(fieldEl, message){
  fieldEl.classList.add('invalid');
  const err = fieldEl.querySelector('.error');
  if(err) err.textContent = message;
}

function clearFieldError(fieldEl){
  fieldEl.classList.remove('invalid');
}

function setStatus(el, message, ok){
  el.textContent = message;
  el.classList.remove('ok', 'err');
  el.classList.add('show', ok ? 'ok' : 'err');
}

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

function initLoginForm(){
  const form = document.getElementById('login-form');
  if(!form) return;

  // If already signed in, skip straight to the dashboard.
  if(Store.currentUser()) window.location.href = 'dashboard.html';

  const status = document.getElementById('login-status');

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const emailField = document.getElementById('field-email');
    const passField = document.getElementById('field-password');
    const email = form.email.value.trim();
    const password = form.password.value;

    [emailField, passField].forEach(clearFieldError);
    status.classList.remove('show');

    let valid = true;
    if(!EMAIL_RE.test(email)){
      showFieldError(emailField, 'Enter a valid email address.');
      valid = false;
    }
    if(!password){
      showFieldError(passField, 'Enter your password.');
      valid = false;
    }
    if(!valid) return;

    const user = Store.findUser(email);
    if(!user || user.password !== password){
      setStatus(status, 'Email or password is incorrect.', false);
      return;
    }

    Store.setSession(user.email);
    setStatus(status, 'Welcome back — redirecting…', true);
    setTimeout(() => { window.location.href = 'dashboard.html'; }, 400);
  });
}

function initSignupForm(){
  const form = document.getElementById('signup-form');
  if(!form) return;

  if(Store.currentUser()) window.location.href = 'dashboard.html';

  const status = document.getElementById('signup-status');

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const nameField = document.getElementById('field-name');
    const emailField = document.getElementById('field-email');
    const passField = document.getElementById('field-password');

    const name = form.name.value.trim();
    const email = form.email.value.trim();
    const password = form.password.value;

    [nameField, emailField, passField].forEach(clearFieldError);
    status.classList.remove('show');

    let valid = true;
    if(name.length < 2){
      showFieldError(nameField, 'Enter your full name.');
      valid = false;
    }
    if(!EMAIL_RE.test(email)){
      showFieldError(emailField, 'Enter a valid email address.');
      valid = false;
    }
    if(password.length < 6){
      showFieldError(passField, 'Use at least 6 characters.');
      valid = false;
    }
    if(!valid) return;

    if(Store.findUser(email)){
      setStatus(status, 'An account with that email already exists.', false);
      return;
    }

    Store.createUser({name, email, password});
    Store.setSession(email);
    setStatus(status, 'Account created — redirecting…', true);
    setTimeout(() => { window.location.href = 'dashboard.html'; }, 400);
  });
}

document.addEventListener('DOMContentLoaded', () => {
  initLoginForm();
  initSignupForm();
});
