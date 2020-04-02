# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 21:08:00 2020

@author: Carlos Rodero García

Module to process spectral response from photometric sensor

"""
import os
import glob
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

np.warnings.filterwarnings('ignore')


class SpectralResponse:
    """
    Process spectral response from photometric sensor
    
    """

    def __init__(self):
        # class variables
        self.path_Licor = r"files\raw\Licor"
        self.all_files_Licor = glob.glob(os.path.join(self.path_Licor, "*.csv"))
        self.path_TCS34725 = r"files\raw\TCS34725"
        self.all_files__TCS34725 = glob.glob(os.path.join(self.path_TCS34725, "*.csv"))
        self.df_licor = pd.DataFrame()
        self.df_tcs34725 = pd.DataFrame()
        self.path_images_plotly = r"images\plotly"

    def create_dataframe_from_csv_data(self, path_file=None):
        """
        Create dataframe from .csv file
        
        Parameters
        ----------
            path_file: str
                Path of the file (Default=None)

        """
        if path_file is not None:
            self.path = path_file

        # LiCOR
        
        # Create dataframe from .csv files
        try:
            df_from_each_file = (pd.read_csv(f) for f in self.all_files_Licor)
            self.df_licor = pd.concat(df_from_each_file, ignore_index=True)
        except (FileNotFoundError, ValueError):
            print(f"File .csv not found")
            exit()

        # TCS34725
        
        # Create dataframe from .csv files
        try:
            df_from_each_file = (pd.read_csv(f) for f in self.all_files__TCS34725)
            self.df_tcs34725 = pd.concat(df_from_each_file, ignore_index=True)
        except (FileNotFoundError, ValueError):
            print(f"File .csv not found")
            exit()
        
    def plot_data(self):
        """
        Interpolate and plot data
        """
        df_licor = self.df_licor
        df_tcs34725 = self.df_tcs34725

        # LiCOR
        x_lic = df_licor["wavelength"]
        y_lic = df_licor["relative_responsivity_LiCOR"]

        step = (x_lic.max()-x_lic.min())/len(x_lic)
        wl_lic = np.arange(x_lic.min(), x_lic.max(), step)

        intfunc_lic = interpolate.interp1d(
            x_lic, y_lic, kind='slinear')
        # use interpolation function returned by `interp1d`
        y_interp_lic=intfunc_lic(wl_lic)
        
        # convert x to numpy array
        x_lic = np.array(x_lic)

        # TCS34725
        # Red
        x_r = df_tcs34725["wavelength_Red"]
        y_r = df_tcs34725["relative_responsivity_Red"]

        step = (x_r.max()-x_r.min())/len(x_r)
        wl_r = np.arange(x_r.min(), x_r.max(), step)

        intfunc_r = interpolate.interp1d(
            x_r, y_r, kind='slinear')
        # use interpolation function returned by `interp1d`
        y_interp_r=intfunc_r(wl_r)
        
        # convert x to numpy array
        x_r = np.array(x_r)

        # Green
        x_g = df_tcs34725["wavelength_Green"]
        y_g = df_tcs34725["relative_responsivity_Green"]
        step = (x_g.max()-x_g.min())/len(x_g)
        wl_g = np.arange(x_g.min(), x_g.max(), step)

        intfunc_g = interpolate.interp1d(
            x_g, y_g, kind='slinear')
        # use interpolation function returned by `interp1d`
        y_interp_g=intfunc_g(wl_g)
        
        # convert x to numpy array
        x_g = np.array(x_g)
        
        # Blue
        x_b = df_tcs34725["wavelength_Blue"]
        y_b = df_tcs34725["relative_responsivity_Blue"]
        step = (x_b.max()-x_b.min())/len(x_b)
        wl_b = np.arange(x_b.min(), x_b.max(), step)

        intfunc_b = interpolate.interp1d(
            x_b, y_b, kind='slinear')
        # use interpolation function returned by `interp1d`
        y_interp_b=intfunc_b(wl_b)
        
        # convert x to numpy array
        x_b = np.array(x_b)
        
        # Clear
        x_c = df_tcs34725["wavelength_Clear"]
        y_c = df_tcs34725["relative_responsivity_Clear"]
        step = (x_c.max()-x_c.min())/len(x_c)
        wl_c = np.arange(x_c.min(), x_c.max(), step)

        intfunc_c = interpolate.interp1d(
            x_c, y_c, kind='slinear')
        # use interpolation function returned by `interp1d`
        y_interp_c=intfunc_c(wl_c)
        
        # convert x to numpy array
        x_c = np.array(x_c)

        if not os.path.exists("images/plotly"):
            os.mkdir("images/plotly")

        fname = "sensor"
        f = os.path.join(self.path_images_plotly, fname)

        fig = go.Figure()

        # Normalized spectra
        fig.add_trace(go.Scatter(
            x=wl_lic,
            y=y_interp_lic/max(y_interp_lic)*100,
            line = dict(color='orange'),
            name="LiCOR 192 quantum sensor normalized"
            ))

        fig.add_trace(go.Scatter(
            x=wl_lic,
            y=y_interp_lic,
            line = dict(color='orange', width=3, dash='dot'),
            name="LiCOR 192 quantum sensor"
            ))

        fig.add_trace(go.Scatter(
            x=wl_r,
            y=y_interp_r/max(y_interp_r)*100,
            line = dict(color='red'),
            name="TCS 34725 RED normalized"
            ))

        fig.add_trace(go.Scatter(
            x=wl_r,
            y=y_interp_r*100,
            line = dict(color='red', width=3, dash='dot'),
            name="TCS 34725 RED"
            ))

        fig.add_trace(go.Scatter(
            x=wl_g,
            y=y_interp_g/max(y_interp_g)*100,
            line = dict(color='green'),
            name="TCS 34725 GREEN normalized"
            ))

        fig.add_trace(go.Scatter(
            x=wl_g,
            y=y_interp_g*100,
            line = dict(color='green', width=3, dash='dot'),
            name="TCS 34725 GREEN"
            ))

        fig.add_trace(go.Scatter(
            x=wl_b,
            y=y_interp_b/max(y_interp_b)*100,
            line = dict(color='blue'),
            name="TCS 34725 BLUE normalized"
            ))

        fig.add_trace(go.Scatter(
            x=wl_b,
            y=y_interp_b*100,
            line = dict(color='blue', width=3, dash='dot'),
            name="TCS 34725 BLUE"
            ))

        fig.add_trace(go.Scatter(
            x=wl_c,
            y=y_interp_c/max(y_interp_c)*100,
            line = dict(color='black'),
            name="TCS 34725 CLEAR normalized"
            ))

        fig.add_trace(go.Scatter(
            x=wl_c,
            y=y_interp_c*100,
            line = dict(color='black', width=3, dash='dot'),
            name="TCS 34725 CLEAR"
            ))


        fig.update_layout(legend_title='<b> Sensors </b>',showlegend=True)

        fig.update_xaxes(
            title_text="Wavelength (nm)",
            title_font=dict(size=12),
            ticklen=5,
            zeroline=False)
        
        fig.update_yaxes(
            title_text='Relative Responsivity',
            title_font=dict(size=12),
            ticklen=5,
            zeroline=False)

        try:
            fig.write_image(f"{f}.svg",
                            width=1920, height=1080, scale=2)
        except Exception as e:
            print(
                "allow configure orca to send requests to remote "
                "server with the following command line:"
                "\norca serve -p 32909 --plotly")

        fig.write_html(f"{f}.html")
        




if __name__ == "__main__":

    sr = SpectralResponse()
    sr.create_dataframe_from_csv_data()
    sr.plot_data()

    