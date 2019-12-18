import glob
from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage

# ADD CREDENTIALS HERE
api_key = 'API_KEY'


# For printing unicode characters to the console
def encode(text):
    if type(text) is list or type(text) is tuple:
        return [x.encode('utf-8') for x in text]
    elif type(text) is not int:
        return text.encode('utf-8')
    else:
        return text


# Counter variables
index = 0
counter = 0
batch_size = 32

# Credentials
app = ClarifaiApp(api_key=api_key)

# Image Directory
path = '/images/*'
files = glob.glob(path)

# Total file amount
total_files = len(files)

while (counter < total_files):

    # Set the range limit
    if total_files > counter + batch_size:
        range_limit = counter + batch_size

    else:
        range_limit = total_files - counter

    # Batch Image List
    imageList = []

    for x in range(counter, range_limit):
        try:
            # ONLY USE ONE OF THESE 3 METHODS
            # Remove the other two

            # Method 1: No custom concepts
            imageList.append(ClImage(filename=files[x]))

            # Method 2: With custom concepts
            #imageList.append(ClImage(filename=files[x], concepts=['cat', 'chunky']))

            # Method 3: With custom concepts AND metadata
            #custom_metadata = {"Breed": "Domestic Shorthair", "Name": "Juliet", "Size": "Chunky"}
            #imageList.append(ClImage(filename=files[x], concepts=['cat', 'chunky'], metadata=custom_metadata))

        except IndexError:
            break

    # Upload Images to your collection
    # Needed for Visual Search and Custom Training
    #app.inputs.bulk_create_images(imageList)

    # And/or get predictions from these images, if desired
    model = app.models.get('general-v1.3')
    model.predict(imageList)

    counter = counter + batch_size
    index = index + 1
