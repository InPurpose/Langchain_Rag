from fastapi import FastAPI
from pydantic import BaseModel
from mangum import Mangum

import uvicorn
from src.query_data import query_rag


class SubmitQueryRequest(BaseModel):
    query_text: str

app = FastAPI()
handler = Mangum(app)

@app.get('/')
def index():
    return {'Hello': 'World!'}


@app.post('/submit_query')
def submit_query_endpoint(request: SubmitQueryRequest):
    query_response = query_rag(request.query_text)
    return query_response


if __name__ == '__main__':
    port = 8000
    print(f"Running the FastAPI server on port {port}.")
    # uvicorn.run("app_api_handler:app", host="0.0.0.0", port=port)
    uvicorn.run('api:app', port=port,reload=True)