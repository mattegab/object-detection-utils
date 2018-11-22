# Labeled Image Tile

Functions of the script:
1. takes an image and the related XML (with the coordinates of the bounding boxes) as input
2. divide the image in tiles: 
 the number of tiles depends on the specified size of the tiles and the minimum overlapping the tiles might have
3. generate the XML related to each tile,
containing the bounding boxes coordinates derived from the main image

Graphical image annotation tool and label object bounding boxes in images: https://github.com/tzutalin/labelImg

[//]: # (for each tile, 
derive the subset of bounding boxes which have non empty intersection.
un xml ogni tail
)

### Credits
Credits to 
https://github.com/MrPaulBrown/ibmvisualinsights/ 
for the part of the script that deal with cropping an image, 
or set of images in a directory, 
into a set of overlapping tiled regions of the specified size, with a specified minimum overlap between tiles.


## Python version
The scripts were built for Python 3.x and tested on Python 3.6

## Usage

Annotate your imager using *labelImg*, so you have 2 file with same name 
(one with an image extension, second with .xml extension)

`python3 LabeledImageTile.py -i <input> -o <output> -x <xsize> -y <ysize> -m <min overlap>`  

Where:  
`<input>` is the source file or Directory  
`<output>` is the target Directory  
`<xsize>` is the size of the tile horizontally  
`<ysize>` is the size of the tile vertically  
`<min overlap>` is the minimum overlap area between tiles  

Annotations:
- If `<input>` is a file it will process the image, 
if it is a directory it will iterate through the files in the directory, processing each in turn
- *template.xml* is following the [labelImg](https://github.com/tzutalin/labelImg) structure 

## Example
`python3 LabeledImageTile.py -i input/Penguins.jpg -o out/ -x 1000 -y 1000 -m 100`  

## Todos

 - Add compatibility to XML from other "image annotation tool"