# Labeled Image Tile

Credits to: https://github.com/MrPaulBrown/ibmvisualinsights/

Graphical image annotation tool and label object bounding boxes in images: https://github.com/tzutalin/labelImg

## Python version
The scripts were built for Python 3.x and tested on Python 3.6

## Usage

Annotate your imager using *labelImg*, so you have 2 file with same name (one with an image extension, second with .xml extension)

`python LabeledImageTile.py -i <input> -o <output> -x <xsize> -y <ysize> -m <min overlap>`  

Where:  
`<input>` is the source file or Directory  
`<output>` is the target Directory  
`<xsize>` is the size of the tile horizontally  
`<ysize>` is the size of the tile vertically  
`<min overlap>` is the minimum overlap area between tiles  

Annotations:
- If `<input>` is a file it will process the image, if it is a directory it will iterate through the files in the directory, processing each in turn  
- *template.xml* is following the labelImg structure 

## Example
`python LabeledImageTile.py -i input/Penguins.jpg -o out/ -x 1000 -y 1000 -m 100`  

## Todos

 - Add compatibility to XML from other "image annotation tool"