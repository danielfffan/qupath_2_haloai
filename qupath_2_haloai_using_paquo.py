import argparse
from paquo.projects import QuPathProject
import os
from xml.dom import minidom

def generate_annotation(image):
    fileID = image.image_name
    root = minidom.Document()
    annotations = root.createElement('Annotations')
    root.appendChild(annotations)
    objs = image.hierarchy.annotations
    if not any(obj.path_class.id == args.category for obj in objs):
        raise ValueError(f"Error: there is no annotation named {args.category} in the QuPath project")
    for obj in objs:
        if (obj.path_class.id == args.category):
            annotation = root.createElement('Annotation')
            annotation.setAttribute('Linecolor', args.color)
            annotation.setAttribute('Name', args.category)
            annotation.setAttribute('Visible', 'True')
            annotations.appendChild(annotation)
            regions = root.createElement('Regions')
            roi = obj.roi
            if (roi.type == 'Polygon'):
                boundary = roi.boundary
                print(boundary)
                coordinates = list(boundary.coords)
                region = root.createElement('Region')
                region.setAttribute('Type', 'Polygon')
                region.setAttribute('HasEndcaps', '0')
                region.setAttribute('NegativeROA', '0')
                regions.appendChild(region)
                annotation.appendChild(regions)
                vertices = root.createElement('Vertices')
                region.appendChild(vertices)
                for c in coordinates:
                    v = root.createElement('V')
                    x = c[0]
                    y = c[1]
                    v.setAttribute('X', f'{x}')
                    v.setAttribute('Y', f'{y}')
                    vertices.appendChild(v)
                comments = root.createElement('Comments')
                # comments.setAttribute()
                region.appendChild(comments)

            elif (roi.type == 'MultiPolygon'):
                boundaries = roi.boundary
                for boundary in boundaries:
                    coordinates = list(boundary.coords)
                    region = root.createElement('Region')
                    region.setAttribute('Type', 'Polygon')
                    region.setAttribute('HasEndcaps', '0')
                    region.setAttribute('NegativeROA', '0')
                    regions.appendChild(region)
                    annotation.appendChild(regions)
                    region = root.createElement('Region')
                    region.setAttribute('Type', 'Polygon')
                    region.setAttribute('HasEndcaps', '0')
                    region.setAttribute('NegativeROA', '0')
                    regions.appendChild(region)
                    annotation.appendChild(regions)

                    vertices = root.createElement('Vertices')
                    region.appendChild(vertices)
                    for c in coordinates:
                        v = root.createElement('V')
                        x = c[0]
                        y = c[1]
                        v.setAttribute('X', f'{x}')
                        v.setAttribute('Y', f'{y}')
                        vertices.appendChild(v)
                    comments = root.createElement('Comments')
                    # comments.setAttribute()
                    region.appendChild(comments)
    annotations.appendChild(annotation)
    with open(f"{args.outputdir}/{fileID}_{args.category}.annotations", "w") as file:
        file.write(root.toprettyxml(indent=" "))
    return

def qupath_2_haloai_direct(args):
    if (os.path.exists(f'{args.inputdir}/project.qpproj')==False or os.path.exists(args.outputdir)==False):
        raise ValueError(f"Please check if the {args.inputdir}/project.qpproj and/or {args.outputdir} exist(s)!")
    with QuPathProject(f'{args.inputdir}/project.qpproj', mode='r') as qp:
        for image in qp.images:
            generate_annotation(image)
    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Transfer the data from geojson to haloai annotation (.annotation)')
    parser.add_argument('inputdir', help="The directory containing the qupath project files.", type=str)
    parser.add_argument('outputdir', help="The directory for the output annotation files.",type=str)
    parser.add_argument('category', help="The category for the primitive (e.g. tubule/cortex).", type=str, default=None)
    parser.add_argument('-c','--color', help="The color for the primitive shown in the HALOAI.", type=str, default='65535')
    args = parser.parse_args()
    print(args)
    qupath_2_haloai_direct(args)