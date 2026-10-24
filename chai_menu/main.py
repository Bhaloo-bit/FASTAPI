from fastapi import FastAPI, Query, HTTPException
from models import MenuItem, Menu_response
from data import menu_items  

app = FastAPI(
    title="Chai Point menu API",
    description="Read only menu API for kiosk displays and mobile app" \
    
)

@app.get('/')
def root():
    return {"message": "Welcome to chai point menu API"}

@app.get('/menu', response_model=Menu_response)
def get_menu(category: str |None=Query(None, description="Filter by chai, snacks and combo")):
    if category :
        filtered = [item for item in menu_items if item["category"] ==
                    category.lower()]
        if not filtered:
            raise HTTPException (status_code= 404, deatail= f"No item found in category :{category}")
        return Menu_response(count=len(filtered), items=filtered)
    return Menu_response(count=len(menu_items), items=menu_items)


@app.get('/menu/{item_id}', response_model=MenuItem)
def get_items(item_id: int):
    for items in menu_items :
        if items['id'] == item_id:
            return items
    raise HTTPException(status_code=404, detail=f"Menu item with id {item_id} not found")    
        