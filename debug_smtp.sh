#!/bin/bash

# Test SMTP connectivity from backend to MailCatcher
echo "=== Testing backend to MailCatcher SMTP connectivity ==="
docker compose exec backend python -c "
import socket
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    result = sock.connect_ex(('mailcatcher', 1025))
    sock.close()
    if result == 0:
        print('SMTP connection to mailcatcher:1025 SUCCESS')
    else:
        print(f'SMTP connection to mailcatcher:1025 FAILED: {result}')
except Exception as e:
    print(f'SMTP connection test ERROR: {e}')
"

echo ""
echo "=== MailCatcher SMTP logs (last 20 lines) ==="
docker compose logs --no-color mailcatcher | tail -20

echo ""
echo "=== MailCatcher HTTP API test ==="
curl -s http://localhost:1080/messages | jq '. | length' || echo "API test failed"

echo ""
echo "=== Test sending email directly via Python SMTP ==="
docker compose exec backend python -c "
import smtplib
from email.mime.text import MIMEText

try:
    # Create a simple test email
    msg = MIMEText('Test email from backend')
    msg['Subject'] = 'Test Email'
    msg['From'] = 'test@example.com'
    msg['To'] = 'test_manual@example.com'
    
    # Connect to MailCatcher SMTP
    server = smtplib.SMTP('mailcatcher', 1025)
    server.set_debuglevel(1)  # Enable debug output
    
    # Send the email
    server.send_message(msg)
    server.quit()
    
    print('Manual SMTP test: SUCCESS')
except Exception as e:
    print(f'Manual SMTP test: FAILED - {e}')
"
