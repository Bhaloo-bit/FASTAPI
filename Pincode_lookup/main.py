from fastapi import FastAPI
from exception import ( 
    PinCodeNotFoundError,
    InvalidPinCodeError,
    pincode_not_found_handler,
    invalid_pincode_handler
    )

from models import LocationResponse, BulkResponse
from data import pincode_db

app = FastAPI(
    title="Pincode lookup API",
    description="Auto fill city and state from India during checkout"
)

# register you custom exception handleer
app.add_exception_handler(PinCodeNotFoundError, pincode_not_found_handler)
app.add_exception_handler(InvalidPinCodeError, invalid_pincode_handler)

@app.get('/')
def home():
    return {"message": "hello world"}

@app.get('/pincode/{code}' , response_model=LocationResponse)
def lookup_pincode(code:str):
    if len(code) != 6 or not code.isdigit():
        raise InvalidPinCodeError(code, "Must be exactly 6 digit")
    if code not in pincode_db:
        raise PinCodeNotFoundError(code)
    return pincode_db[code]


@app.post("/pincode/bulk", response_model=BulkResponse)
def bulk_response(request: BulkResponse ):
    results = []
    missing = []

    for code in request.pincodes:
        if code in pincode_db:
            results.append(pincode_db[code])
        else:
            missing.append(code)

    return BulkResponse(
        found= len(results),
        not_found= len(missing),
        results= results,
        missing= missing
        )        


    