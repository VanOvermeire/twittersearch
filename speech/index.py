import boto3

client = boto3.client('polly')

# bucket to put mp3s in
BUCKET = 'result-bucket'


def write_audio_to_file(filename, text):
    response = client.synthesize_speech(OutputFormat='mp3', VoiceId='Joanna', Text=text)


def get_text_from_s3(bucket, filename):
    print("based on the event we receive")
    return ''


