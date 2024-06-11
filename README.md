# Voice_Bot_Ultrix
A sample voice bot using LLM.

## Docker

### Build the Docker image, version 1.0
```
docker build -t voice_chat_demo:1.0 .
```

**-t:** tags

### Build the Docker container
```
docker run -p 8000:8000 voice_chat_demo:1.0
```

**-p:** publish
