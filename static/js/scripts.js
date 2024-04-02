// Example: Form validation
const forms = document.querySelectorAll('form');

forms.forEach(form => {
    form.addEventListener('submit', (event) => {
        event.preventDefault();
        const formData = new FormData(form);
        const formValues = Object.fromEntries(formData);

        // Perform form validation
        let isValid = true;
        for (const field in formValues) {
            if (formValues[field] === '') {
                isValid = false;
                break;
            }
        }

        if (isValid) {
            // Submit the form data to the server
            fetch(form.action, {
                method: 'POST',
                body: formData
            })
            .then(response => response.text())
            .then(data => {
                // Handle the server response
                console.log(data);
            })
            .catch(error => {
                console.error('Error:', error);
            });
        } else {
            // Display an error message
            alert('Please fill in all required fields.');
        }
    });
});