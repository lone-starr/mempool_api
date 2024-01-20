from fastapi import FastAPI

app = FastAPI()


@app.get("/blocktip")
async def root():
    return {"height": "826590"}
