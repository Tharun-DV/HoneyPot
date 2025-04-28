import http.client
import json

def send_mail(to, subject, content):
    """
    Sends an email using an external mail sending service.

    Args:
        to (str): The recipient's email address.
        subject (str): The email subject.
        content (str): The email body.
    """
    try:
        conn = http.client.HTTPSConnection("mail-sender-endpoint.onrender.com")

        # Construct the payload as a Python dictionary and convert it to JSON
        payload = {
            "to": to,
            "subject": subject,
            "text": content,
        }
        json_payload = json.dumps(payload)

        headers = {'content-type': "application/json"}

        conn.request("POST", "/send-email", json_payload, headers)

        res = conn.getresponse()
        data = res.read()

        print(data.decode("utf-8"))

    except Exception as e:
        print(f"Error sending email: {e}")

# Example usage:
send_mail("tharundv.cs22@bitsathy.ac.in", "test mail", "testing from hiriziam")
