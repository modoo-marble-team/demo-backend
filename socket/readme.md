- python socketio 설치
```
pip install python-socketio "python-socketio[asyncio_client]" uvicorn
```

- 서버 실행
```
uvicorn server_asgi:app --host 0.0.0.0 --port 8000
```