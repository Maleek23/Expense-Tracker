// Home page specific JavaScript
document.addEventListener('DOMContentLoaded', function() {
    const downloadLink = document.getElementById('download-link');
    if (downloadLink) {
        downloadLink.addEventListener('click', function(e) {
            e.preventDefault();
            const projectZipUrl = '/download-project';
            window.location.href = projectZipUrl;
        });
    }
});