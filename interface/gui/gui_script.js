const form = document.getElementById('form');
form.addEventListener('submit', (event) => {
  event.preventDefault();
  const formData = new FormData(form);
  fetch('/search', {
    method: 'POST',
    body: formData,
  })
    .then((response) => response.text())
    .then((result) => {
      document.getElementById('results').innerHTML = result;
    })
    .catch((error) => {
      console.error(error);
    });
});