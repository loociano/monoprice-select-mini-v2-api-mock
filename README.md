# Fake Monoprice Select Mini V2 Printer

This program simulates a Monoprice Select Mini V2 printer. 

It is used to develop the [Monoprice Select Mini Wi-Fi plugin for Cura](https://github.com/loociano/MPSM2NetworkPrinting) without a real printer.

## How to run

```shell 
$ python -m src.FakePrinter

INFO:FakePrinter:Starting fake printer on http://localhost/
```

Then open http://localhost:80.

## Supported commands

* Get printer status: http://localhost/inquiry
* Print cached model: http://localhost/set?cmd=%7BP:M%7D
* Cancel print: http://localhost/set?cmd=%7BP:X%7D
* Set hot-end target temperature: http://localhost/set?cmd=%7BC:T0250%7D
* Set bed target temperature: http://localhost/set?cmd=%7BC:P060%7D
* Send arbitrary gcode command: http://localhost/set?code=M563%20S5
* Upload a model. `POST http://localhost/upload

## Troubleshooting

### Program exits on Windows

Try disabling World Wide Web Publishing Service to use port 80:

1. Go to Start > All Programs > Administrative Tools > Services. 
1. In the services list, right-click on **World Wide Web Publishing Service**, and then click Stop.