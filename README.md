<p align="center">
    <img width="100px" src="api/static/src/logo_voice.ico" align="center" alt="Voice bot assessment" />
    <h1 align="center">Voice Bot Assessment</h1>
    <p align="center"><b>Voice bot app with a tool calling agent.</b>
</p>


## 🔧 Stack

- **Frontend:** HTML, CSS, and JavaScript Vanilla.
- **API:** FastAPI (Python).
- **Agent:** Langchain (Python).
- **Technologies:** Git/Github, Docker.
- **Cloud Deployment:** Microsoft Azure (Container Registry + Web App).

## 🐳 Docker

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

## 🎉 Microsoft Azure Deployment

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