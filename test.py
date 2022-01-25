from sanic import Sanic
from devtools import debug
from sanic.response import json

app = Sanic("PepperBot")


@app.post("/hi")
async def hi_my_name_is(request):
    debug(request.json)

    return json({"foo": "bar"})


app.run("0.0.0.0", 8080, debug=True)
