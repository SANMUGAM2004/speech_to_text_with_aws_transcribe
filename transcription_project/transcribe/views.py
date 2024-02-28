# views.py

from django.shortcuts import render
from .forms import VideoUploadForm
from django.conf import settings
from django.http import HttpResponse 
import boto3
import json


def transcribe_view(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Get the uploaded video file
            video_file = request.FILES['video_file']
            # Generate a unique filename for the video file
            video_file_name_in_s3 = f"video-{request.user.id}-{video_file.name}"
            # Upload the file to S3
            s3 = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                              aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                              region_name=settings.AWS_REGION)
            try:
                s3.upload_fileobj(video_file, settings.AWS_STORAGE_BUCKET_NAME, video_file_name_in_s3)
                print("Video uploaded to S3 successfully.")
            except Exception as e:
                return f"Error uploading video to S3: {str(e)}"
            
            # Start the transcription job
            transcribe_client = boto3.client('transcribe', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                             aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                                             region_name=settings.AWS_REGION)
            transcription_job_name = f'transcription_job_{request.user.id}'
            try:
                response = transcribe_client.start_transcription_job(
                    TranscriptionJobName=transcription_job_name,
                    Media={'MediaFileUri': f's3://{settings.AWS_STORAGE_BUCKET_NAME}/{video_file_name_in_s3}'},
                    MediaFormat='mp4',
                    LanguageCode='en-US',
                    OutputBucketName=settings.AWS_STORAGE_BUCKET_NAME,
                    OutputKey='transcribed.txt'  
                )
                print("Transcription job started successfully.")
                while True:
                    job = transcribe_client.get_transcription_job(TranscriptionJobName=transcription_job_name)
                    if job['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
                        break
                print("Transcription job completed.")
                transcribed_file_key = 'transcribed.txt'

                transcribed_file_obj = s3.get_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=transcribed_file_key)
                transcribed_data = json.load(transcribed_file_obj['Body'])
                transcribed_text = transcribed_data['results']['transcripts'][0]['transcript']


                return render(request, 'transcribe/transcribe.html', {'transcribed_text': transcribed_text})
            except Exception as e:
                return HttpResponse(f"Error: {str(e)}", status=500)

    else:
        form = VideoUploadForm()
    return render(request, 'transcribe/upload.html', {'form': form})


def download_transcribed_file(request):
    # Retrieve the transcribed text from the request
    transcribed_text = request.POST.get('transcribed_text', '')
    
    # Serve the transcribed text as a downloadable file
    response = HttpResponse(transcribed_text, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="transcribed.txt"'
    return response