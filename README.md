# Monoprice Select Mini V2 API Mock

Simulates REST API responses from Monoprice Select Mini V2 printers.

## How to run

```shell 
$ python -m src.FakePrinter
INFO:FakePrinter:Starting fake printer on http://localhost:80
```

Open http://localhost:80

## Supported commands

* Get printer status: `GET /inquiry`
* Print cached model: `GET /set?cmd=%7BP:M%7D`
* Cancel print: `GET /set?cmd=%7BP:X%7D`
* Set hot-end target temperature: `GET /set?cmd=%7BC:T0250%7D`
* Set bed target temperature: `GET /set?cmd=%7BC:P060%7D`
* Send arbitrary gcode command: `GET /set?code=M563%20S5`
* Upload a model. `POST /upload`