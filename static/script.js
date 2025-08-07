async function generateEmail() {
    const prompt = document.getElementById('prompt').value;
    document.getElementById('status').innerText = 'Generating email...';

    const res = await fetch('/generate-email', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt })
    });

    const data = await res.json();
    if (data.email) {
        document.getElementById('output').value = data.email;
        document.getElementById('status').innerText = 'Email generated successfully!';
    } else {
        document.getElementById('output').value = '';
        document.getElementById('status').innerText = data.error || 'Failed to generate email.';
    }
}

async function sendEmail() {
    const to = document.getElementById('to').value;
    const subject = document.getElementById('subject').value;
    const body = document.getElementById('output').value;

    document.getElementById('status').innerText = 'Sending email...';

    const res = await fetch('/send-email', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ to, subject, body })
    });

    const data = await res.json();
    if (data.success) {
        document.getElementById('status').innerText = 'Email sent successfully!';
    } else {
        document.getElementById('status').innerText = `Failed to send email: ${data.error}`;
    }
}
