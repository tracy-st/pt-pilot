#Calculate Image Features\

Input = /pngs/
Output = *-indico.json, merged_file.json\

## Pre-processing\
mogrify -format png -path png *.jpg\
mogrify -resize 400x400 *.png\
mogrify -type Grayscale *.png\
