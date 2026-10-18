# this is design model view pydantic that will validator data 

from pydantic import BaseModel, field_validator

'''as data file stru is pincode_db = {"pincode":"{pincode, state,city, disctrict}"}'''

class PincodeRequest(BaseModel):
    pincode: str #key 

    #pincode must be exactly 6 digit
    @field_validator("pincode")
    @classmethod
    def validate_pincode(cls, value):
        if len(value) != 6 or not value.isdigit():
            raise ValueError("Pincode must be exactly 6 digit")
        return value

class LocationResponse(BaseModel):
    pincode : str
    cit: str
    state: str
    district: str

class BullkRequest(BaseModel):
    pincode : list[str]

    @field_validator("pincode")
    @classmethod
    def validate_pincode(cls, values):
        if len(values) == 0:
            raise ValueError("At least one pincode is required")
        if len(values) > 20 :
            raise ValueError("Maximum 20 pincode allowed per request")

        for code in values:
            if len(code) != 6 or not code.digit():
                raise ValueError("Each Pincodee must be exactly 6 digit")
        return values
                

class BulkResponse(BaseModel):
    status : str = "success"
    found : int
    not_found: int 
    results: list[LocationResponse]
    missing: list[str] 