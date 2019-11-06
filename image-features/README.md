# Calculate Image Features

Input = /pngs<br>
Output = *-indico.json, merged_file.json

## Pre-processing
mogrify -format png -path png *.jpg<br>
mogrify -resize 400x400 *.png<br>
mogrify -type Grayscale *.png
