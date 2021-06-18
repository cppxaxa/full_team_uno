
import uvicorn
from lib.apps.v1.main import mainApp

if __name__ == '__main__':
    uvicorn.run(mainApp)

