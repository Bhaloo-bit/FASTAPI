from fastapi.responses import JSONResponse
from fastapi import Request


# custom Exceptoin 
class PinCodeNotFoundError(Exception):
    def __init__(self, pincode: str):
        self.pincode = pincode

class InvalidPinCodeError(Exception):
    def __init__(self, pincode: str, reason : str ="Invalid Format"):
        self.pincode = pincode
        self.reason = reason


async def pincode_not_found_handler(request: Request, exc: PinCodeNotFoundError):
    return JSONResponse(
        status_code=404,
        content= {
            "error": "pincode not found",
            "message": f"No location for pincode: {exc.pincode}"
        }
    )
async def invalid_pincode_handler(request: Request, exc: InvalidPinCodeError):
    return JSONResponse(
        status_code=400,
        content= {
            "error": "invalid pincode",
            "message": F"Pincode '{exc.pincode}' is valid: {exc.reason}" ,
            "pincode": exc.pincode
        }
    )