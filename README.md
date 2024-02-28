# Speech to Text with AWS Transcribe

#Project Description:
The project is a Django web application designed to transcribe video files uploaded by users. It allows users to upload video files, which are then sent to an AWS Transcribe service for transcription. Once the transcription is completed, the text content of the transcription is displayed to the user, and they have the option to download the transcribed text as a file.

#Tech Stack:
Django: Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design. It provides built-in features for authentication, URL routing, template rendering, and more, making it ideal for developing web applications.

Needed Dependencies:
    sudo dnf update -y
    sudo yum update -y
    sudo yum install git -y
    sudo dnf install python3
    sudo dnf install python3-pip
    pip3 install pymysql boto3
    sudo python3 -m pip install boto3
    pip install django

#AWS (Amazon Web Services):

S3 (Simple Storage Service): Used to store the uploaded video files and transcribed text files.
Transcribe: Used for converting speech to text. It transcribes the uploaded video files and provides the text output.
Boto3: Boto3 is the Amazon Web Services (AWS) SDK for Python. It allows Python developers to interact with AWS services, such as S3 and Transcribe, programmatically.

HTML/CSS: Used for creating the user interface of the web application. HTML is used for structuring the content, while CSS is used for styling and layout.

Python: The primary programming language used for backend development. Python is known for its simplicity, readability, and extensive library support, making it well-suited for web development tasks.

Dependencies:
The project likely relies on the following Python packages, managed using pip or another package manager:

Django: The web framework for building the application.
boto3: The AWS SDK for Python, used for interacting with AWS services.
Other dependencies as specified in the requirements.txt file or directly installed using pip.
Workflow:
User uploads a video file through the web interface.
The server receives the uploaded file and stores it in an AWS S3 bucket.
The server triggers an AWS Transcribe job to transcribe the uploaded video file.
The server periodically checks the status of the transcription job until it is completed.
Once the transcription is complete, the server retrieves the transcribed text from AWS Transcribe.
The transcribed text is displayed to the user on the web interface.
The user has the option to download the transcribed text as a file.

