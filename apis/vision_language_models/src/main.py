from config import settings
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from vqa import router as vqa_router

app = FastAPI(title='Vision Language Models API')

origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_headers=settings.CORS_HEADERS,
    allow_credentials=True,
    allow_methods=["*"],
)


@app.on_event("startup")
def startup_event():
    vqa_router.init(settings)


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Get the original 'detail' list of errors
    details = exc.errors()
    error_details = []

    for error in details:
        error_details.append({'error': error['msg'] + " " + str(error['loc'])})
    return JSONResponse(content={"message": error_details})


@app.get('/', include_in_schema=False)
def root() -> None:
    return RedirectResponse('/docs')


@app.get('/health', status_code=status.HTTP_200_OK, tags=['health'])
def perform_healthcheck() -> None:
    return JSONResponse(content={'message': 'success'})


app.include_router(vqa_router.router, prefix='/vqa')


if __name__ == '__main__':
    import uvicorn

    print("Settings:")
    for attr_name in dir(settings):
        if not attr_name.startswith("_"):
            attr_value = getattr(settings, attr_name)
            if attr_name.isupper():
                print(f"    {attr_name}: {attr_value}")

    uvicorn.run('main:app', host=settings.HOST, port=settings.PORT)
