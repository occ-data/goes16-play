GOES-16 Plotting Script
===

This script uses bands 1, 2, and 3 to generate a true color image. Band 13 is used for the areas not currently lit by the sun. Band 13 is converted to grey scale and then blended with the true color image using a "lighten" blend mode which takes the brightest RGB value for each pixel.

These scripts power the GOES-16 display on [https://play.opensciencedatacloud.org](https://play.opensciencedatacloud.org)

# plot.py
This script plots the netcdf file.

Usage:
```
Usage: ./plot.py <MCMIP netcdf file> <output.png>
```

# run.csh
This script pulls down the last hours worth of full disk multi-band netcdf files and then plots them. Suggested usage is with crontab for automatically producing new figures.
