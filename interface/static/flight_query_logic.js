const departureAirportSelect = document.querySelector('#departure-airport');
departureAirportSelect.addEventListener('change', (event) => {
  console.log('departure airport change event triggered!');
  const selectedOption = event.target.value;
  if (selectedOption === 'other') {
    // create a text input element
    const textInput = document.createElement('input');
    textInput.type = 'text';
    textInput.name = 'departure-airport';
    textInput.id = 'departure-airport';

    // replace the select element with the text input element
    departureAirportSelect.parentNode.replaceChild(textInput, departureAirportSelect);
  }
});

const arrivalAirportSelect = document.querySelector('#arrival-airport');
arrivalAirportSelect.addEventListener('change', (event) => {
  console.log('arrival airport change event triggered!');
  const selectedOption = event.target.value;
  if (selectedOption === 'other') {
    // create a text input element
    const textInput = document.createElement('input');
    textInput.type = 'text';
    textInput.name = 'arrival-airport';
    textInput.id = 'arrival-airport';

    // replace the select element with the text input element
    arrivalAirportSelect.parentNode.replaceChild(textInput, arrivalAirportSelect);
  }
});