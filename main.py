from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn

from routs import auth, base
from dependencies import Base, engin


Base.metadata.create_all(bind=engin)

app = FastAPI()
app.include_router(router=auth.router, prefix='/auth')
app.include_router(router=base.router, prefix='/reg')

@app.get('/')
def root_page():
    html_content = """
        <html>
            <head>
                <title>Title</title>
            </head>
            <body>
                <h1>Главная страница социальной сети</h1>
            </body>
        </html>
        """
    return HTMLResponse(content=html_content, status_code=200)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)