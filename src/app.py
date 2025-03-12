from fastapi import FastAPI
from fastapi.responses import JSONResponse
from src.sensor import Visitors

app = FastAPI()

@app.get("/")
def visit(date: str, store: str) -> JSONResponse:
    """
    Api send a number of visitors for one day
    :param date: str
    :param store: str
    :return: JSONResponse with the value
    """
    visitors = Visitors()
    try:
        nb_visit = 0
        for i_day in range(8, 20):
            nb_visitors_hours = visitors.get_number_visitors(
                date, hour=i_day, store=store
            )
            if nb_visitors_hours != "null":
                nb_visit += int(nb_visitors_hours)

        return JSONResponse(status_code=200, content=nb_visit)

    except IndexError:
        return JSONResponse(
            status_code=400, content=f"La valeur {date} n'est pas valide !"
        )

@app.get("/all_data_day_hour")
def visit(date: str) -> JSONResponse:
    """
    Api send all the data for a specific day and hour
    :param date: str
    :return: JSONResponse with the value
    """
    visitors = Visitors()
    try:
        return JSONResponse(status_code=200, content=visitors.get_all_data_day(date))

    except IndexError:
        return JSONResponse(
            status_code=400, content=f"La valeur {date} n'est pas valide !"
        )
