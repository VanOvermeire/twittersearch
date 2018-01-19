import os


def send_email(client, mail, tag, url):
    source = os.environ['SOURCE']

    print('Sending mail to %s for tag %s' % (mail, tag))

    client.send_email(
        Source=source,
        Destination={
            'ToAddresses': [
                mail,
            ]
        },
        Message={
            'Subject': {
                'Data': 'Your tweets with hastag #' + tag,
                'Charset': 'utf-8'
            },
            'Body': {
                'Text': {
                    'Data': 'Hi,\nClick the url to download your mp3 file:\n\n' + url,
                    'Charset': 'utf-8'
                }
            }
        }
    )
