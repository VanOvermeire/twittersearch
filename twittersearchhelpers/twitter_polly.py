import boto3

AUDIO_BUCKET_PREFIX = 'audio/'
CHUNK_SIZE = 1024
TMP_FILE = '/tmp/temp.mp3'


def write_audio_to_file(client, bucket, filename, text):
    # for now just taking an english voice
    response = client.synthesize_speech(OutputFormat='mp3', VoiceId='Joanna', Text=text)
    stream = response.get('AudioStream')

    with open(TMP_FILE, 'wb') as filewriter:
        while True:
            data = stream.read(CHUNK_SIZE)
            filewriter.write(b"%X\r\n%s\r\n" % (len(data), data))

            if not data:
                break
        # Ensure any buffered output has been transmitted and close the stream
        filewriter.flush()

    s3 = boto3.resource('s3')
    s3.meta.client.upload_file(TMP_FILE, bucket, AUDIO_BUCKET_PREFIX + filename)
