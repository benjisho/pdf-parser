document.getElementById("uploadForm").addEventListener("submit", async function (event) {
    event.preventDefault();
    
    const fileInput = document.getElementById("pdfFile");
    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append("pdfFile", file);

    try {
        // Assuming you have an API endpoint that handles the uploaded file
        const response = await fetch('YOUR_API_ENDPOINT', {
            method: 'POST',
            body: formData,
        });

        if (response.ok) {
            const data = await response.json();
            document.getElementById("output").classList.remove("hidden");
            document.getElementById("downloadLink").href = data.downloadUrl; // Adjust according to your API response
        } else {
            alert("Error parsing PDF. Please try again.");
        }
    } catch (error) {
        console.error("Error:", error);
        alert("An error occurred while parsing the PDF.");
    }
});
