# Spectral-response-photometric-sensor

Module to process spectral response from photometric sensor.
Raw data obtained from WebPlotDigitizer software (https://automeris.io/WebPlotDigitizer/) as .csv file

## Instructions

- Copy your .csv file from WebPlotDigitizer software inside the files/raw folder
- Images appear in images folder

## Install Dependencies

- npm install -g electron@1.8.4 orca

In case you find a "ConnectionRefusedError" when you try the fig.write_image() Plotly function, you have to allow configure orca to send requests to remote server with the following command line:

orca serve -p 32909 --plotly

ESTO ES UN TEST
