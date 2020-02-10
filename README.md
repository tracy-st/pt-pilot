## PhotoTech Pilot

### Files


### Stages

CV experiments in the pilot were conducted in three phases:

#### 1. 100-image sample set

#### 2. 1000-image sample set

#### 3. Full image set
        a. Recto (_001)
        b. Verso (_002)


### Pre-Processing

Artworks were cropped from full-page derivatives using Photoshop Batch Processing (Automate > Crop and Straighten Photos).

### Tools

#### Google Cloud Vision API

Uses: OCR, Label annotation (secondary)

#### Clarifai API
Uses: Label Annotation


### Scripts

#### get_images_from_open_Excel_column_A.wflow
Apple Automator workflow
To use: Paste list of filenames in Column A of an open Excel file. When prompted, select source floder and output folder

