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
docker run -p 80:80 voice_chat_demo:1.0
```

**-p:** publish

## Microsoft Azure Deployment

Using Container Registry + Web App

---

### Tag the Docker image version
```
docker tag voice_chat_demo:1.0 voicebotcontainer.azurecr.io/voice_chat_demo:1.0
```

### Login Azure
```
docker login voicebotcontainer.azurecr.io
```

### Push the image
```
docker push voicebotcontainer.azurecr.io/voice_chat_demo:1.0
```