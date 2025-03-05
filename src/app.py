import numpy as np
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from sensor import Visitors

app = FastAPI()

@app.get("/")
def visit(date: str) -> JSONResponse:
    """
    Api send a number of visitors for one day
    :param date: str
    :return: JSONResponse with the value
    """
    visitors = Visitors()
    try:
        nb_visit = 0
        for i_day in range(8, 20):
            nb_visitors_hours = visitors.get_number_visitors(date, hour=i_day)

            if not np.isnan(nb_visitors_hours):
                nb_visit += int(nb_visitors_hours)

        return JSONResponse(status_code=200, content=nb_visit)

    except IndexError:
        return JSONResponse(
            status_code=400, content=f"La valeur {date} n'est pas valide !"
        )
