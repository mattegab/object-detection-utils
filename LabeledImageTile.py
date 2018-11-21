import math
import sys
import os
import getopt
import cv2
import xml.etree.ElementTree
from jinja2 import Environment, FileSystemLoader

PATH = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_ENVIRONMENT = Environment(
    autoescape=False,
    loader=FileSystemLoader(os.path.join(PATH, 'templates')),
    trim_blocks=False
)


def render_template(template_filename, context):
    return TEMPLATE_ENVIRONMENT.get_template(template_filename).render(context)

def getNumberOfTiles(size, tile_size, min_overlap):
    return math.ceil(size/(tile_size-min_overlap))

def getOverlap(size, num_tiles, tile_size):
    return abs(((size-tile_size)/(num_tiles-1))-tile_size)


def getBoundingBoxesCoords(input):
    # XML PARSING
    input_xml = "{}.xml".format(os.path.splitext(input)[0])
    print('XML file is {}'.format(input_xml))

    BB_coords = []

    e = xml.etree.ElementTree.parse(input_xml).getroot()
    for obj in e.findall('object'):
        name = obj.find('name').text
        for obj_el in obj:
            dict = {}
            dict['name'] = name
            if obj_el.tag == 'bndbox':
                for el3 in obj_el:
                    dict[el3.tag] = float(el3.text)
                    # print(el3.tag, el3.text)
                BB_coords.append(dict)
    print("Bounding Boxes Coords: {}".format(BB_coords))
    return BB_coords


def area(a_xmin, a_xmax, a_ymin, a_ymax, b_xmin, b_xmax, b_ymin, b_ymax):
    dx = min(a_xmax, b_xmax) - max(a_xmin, b_xmin)
    dy = min(a_ymax, b_ymax) - max(a_ymin, b_ymin)
    if (dx>=0) and (dy>=0):
        return dx*dy
    else:
        # if rectangles don't intersect
        return None


def tileImage(filename, outputdir, xsize, ysize, min_overlap):
    list_coords = getBoundingBoxesCoords(filename)

    # print("Tiling: {}".format(filename))
    # print("Output dir: {}".format(outputdir))

    img = cv2.imread(filename)

    if img is None:
        # Problem reading file
        print("Failed to read file: {}".format(filename))
        return

    # get image height, width
    (h, w) = img.shape[:2]

    # print("h: {}, w: {}".format(h, w))

    xtiles = getNumberOfTiles(w, xsize, min_overlap)
    ytiles = getNumberOfTiles(h, ysize, min_overlap)

    xoverlap = getOverlap(w, xtiles, xsize)
    yoverlap = getOverlap(h, ytiles, ysize)

    # print("xtiles: {}, xoverlap: {}".format(xtiles, xoverlap))
    # print("ytiles: {}, yoverlap: {}".format(ytiles, yoverlap))

    basename, fname = os.path.split(filename)
    rootname, file_extension = os.path.splitext(fname)

    yoffset = 0

    for ytile in range(ytiles):
        xoffset = 0
        for xtile in range(xtiles):

            xmin = xoffset
            xmax = xoffset + xsize
            ymin = yoffset
            ymax = yoffset + ysize
            crop = img[int(ymin):int(ymax), int(xmin):int(xmax)]

            cropfn = "{}_{}_{}{}".format(rootname, ytile, xtile, file_extension)
            crop_filename = os.path.join(outputdir, cropfn)
            print("creating...  {} \t\t X: {}-{} \t Y: {}-{}".format(crop_filename, xmin, xmax, ymin, ymax))

            objects = []

            # iteration for each detection on the MAIN image
            for coords in list_coords:
                # check if is contained in the current tile
                # print(coords['name'], coords['xmin'], coords['xmax'], coords['ymin'], coords['ymax'])
                area_inter = area(xmin, xmax, ymin, ymax, coords['xmin'], coords['xmax'], coords['ymin'], coords['ymax'])
                if area_inter:
                    print("---- There's an IntersectionArea:{} with Tag:{} in Img:{}".format(int(area_inter), coords['name'], crop_filename))
                    obj = [coords['name'],
                           int(max(xmin, coords['xmin']) - xoffset),
                           int(max(ymin, coords['ymin']) - yoffset),
                           int(min(xmax, coords['xmax']) - xoffset),
                           int(min(ymax, coords['ymax']) - yoffset)
                    ]
                    objects.append(obj)

            output_xml = "{}.xml".format(os.path.splitext(crop_filename)[0])
            context = {
                'filename': cropfn,
                'width': int(xmax-xmin),
                'height': int(ymax-ymin),
                'objects': objects,
            }
            with open(output_xml, 'w') as f:
                html = render_template('template.xml', context)
                f.write(html)

            # print("{}, ({}, {}) ({}, {})".format(crop_filename, xmin, ymin, xmax, ymax))

            cv2.imwrite(crop_filename, crop)

            xoffset = xmax - xoverlap
            # print(xoffset)

        yoffset = ymax - yoverlap



def main(argv):
    input = ''
    output = ''
    xsize = 0
    ysize = 0
    min_overlap = 0
    try:
        opts, args = getopt.getopt(argv,"hi:o:x:y:m:",["input=","output=","xsize=","ysize=","minoverlap="])
    except getopt.GetoptError:
        print('LabeledImageTile.py -i <input> -o <output> -x <x size> -y <y size> -m <min overlap>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('LabeledImageTile.py -i <input> -o <output> -x <x size> -y <y size> -m <min overlap>')
            sys.exit()
        elif opt in ("-i", "--input"):
            input = arg
            if not os.path.exists(input):
                print('-i <input> path does not exist')
                sys.exit(2)
        elif opt in ("-o", "--output"):
            output = arg
        elif opt in ("-x", "--xsize"):
            try:
                xsize = int(arg)
            except ValueError:
                print('-x <x size> option requires an integer value')
                sys.exit(2)
        elif opt in ("-y", "--ysize"):
            try:
                ysize = int(arg)
            except ValueError:
                print('-y <y size> option requires an integer value')
                sys.exit(2)
        elif opt in ("-m", "--maxoverlap"):
            try:
                min_overlap = int(arg)
            except ValueError:
                print('-m <min overlap> option requires an integer value')
                sys.exit(2)

    print('Input is {}'.format(input))
    print('Output is {}'.format(output))
    print('x, y is {}, {}'.format(xsize, ysize))
    print('Min overlap is {}'.format(min_overlap))


    if xsize < 100 or ysize < 100:
        print('Image size too small')
        sys.exit(2)

    if min_overlap > (xsize / 2) or min_overlap > (ysize / 2):
        print('Min overlap too big')
        sys.exit(2)

    if not os.path.exists(output):
        try:
            os.makedirs(output)
        except OSError:
            print('Error creating output directory')
            sys.exit(2)
    elif not os.path.isdir(output):
        print('-o <output> path is not a directory')
        sys.exit(2)

    if os.path.isdir(input):
        for f in os.listdir(input):
            filename = os.path.join(input, f)
            tileImage(filename, output, xsize, ysize, min_overlap)
    else:
        tileImage(input, output, xsize, ysize, min_overlap)


if __name__ == '__main__':
    # main(['-i', 'input/test.BMP', '-o', 'out/', '-x', '1000', '-y', '1000', '-m', '450'])
    main(['-i', 'input/Penguins.jpg', '-o', 'out/', '-x', '300', '-y', '300', '-m', '30'])
