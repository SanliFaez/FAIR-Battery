"""
Example illustrating some aspects of xarray data.
This file is intended to work with a dataset saved using the Operator of analog_discovery_2_model.py (note that this can
be tun trough the accompanying gui in view)

"""
import xarray as xr

# modify the filename
filename = r'example scan data.nc'

dat = xr.load_dataset(filename)

# To get a feeling for what's possible with xarray dataset, try the following things in an interactive python console:
# (Note that if you only execute one line you don't need the print statement to see the output)

print(dat)
print(dat.measured_voltage)
print(dat.measured_voltage.dims)
print(dat.measured_voltage.coords)
print(dat.measured_voltage.units)
print(dat.measured_voltage.values)
print(dat.scan_voltage)
print(dat.scan_voltage.units)
print(dat.scan_voltage.values)

print(dat.attrs)

print(dat.measured_voltage[10:20])

print(dat.measured_voltage.isel(scan_voltage=2))  # 2nd point
print(dat.measured_voltage[dict(scan_voltage=2)])  # alternative

print(dat.measured_voltage.sel(scan_voltage=2.0))  # where scan_voltage == 2.0
print(dat.measured_voltage.sel(scan_voltage=slice(0, 1.0)))  # for scan_voltage in range 0 to 1.0

# See also http://xarray.pydata.org/en/stable/indexing.html

# Plotting is very easy with xarray:
dat.measured_voltage.plot()