function queryPDF() {
    const prompt = document.getElementById('prompt').value;
    const responseContainer = document.getElementById('response-container');

    fetch('/query', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ prompt: prompt })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            responseContainer.textContent = data.error;
        } else {
            responseContainer.textContent = `Response: ${data.result}\n\nSource Documents:\n${data.source_docs.join('\n\n')}`;
        }
    })
    .catch(error => {
        responseContainer.textContent = 'Error querying the PDF: ' + error.message;
    });
}
