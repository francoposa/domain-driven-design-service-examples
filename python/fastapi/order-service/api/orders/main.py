import sys

import uvicorn
from fastapi import FastAPI

app = FastAPI()


def main():
    uvicorn.run("api.orders.main:app", host="0.0.0.0", port=8000)


if __name__ == "__main__":
    sys.exit(main())
