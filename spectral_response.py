# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 21:08:00 2020

@author: Carlos Rodero García

Module to process spectral response from photometric sensor

"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import interpolate
import plotly.graph_objs as go
from plotly.subplots import make_subplots

# allow configure orca to send requests to remote server
import plotly.io as pio

pio._orca.ensure_server = lambda: None
pio._orca.orca_state["port"] = 32909

if __name__ == "__main__":
    print("test")