import xml.etree.ElementTree as ET
import sys
import os

def strip_text_from_svg(input_path, output_path):
    """
    Parses an SVG file, removes all <text> and <tspan> elements, 
    and saves the cleaned SVG to a new file.
    """
    if not os.path.exists(input_path):
        print(f"Error: File '{input_path}' not found.")
        return

    # 1. Register common SVG namespaces to prevent ugly 'ns0:' prefixes in the output
    namespaces = {
        'svg': 'http://www.w3.org/2000/svg',
        'xlink': 'http://www.w3.org/1999/xlink',
        'inkscape': 'http://www.inkscape.org/namespaces/inkscape',
        'sodipodi': 'http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd',
        'adobe': 'http://ns.adobe.com/AdobeSVGViewerExtensions/3.0/'
    }
    for prefix, uri in namespaces.items():
        ET.register_namespace(prefix, uri)

    # 2. Parse the SVG
    tree = ET.parse(input_path)
    root = tree.getroot()
    
    # Define the SVG namespace tag format
    ns = '{http://www.w3.org/2000/svg}'

    # 3. Recursive function to find and remove text elements
    def remove_text_elements(parent):
        # We use list(parent) to create a static copy of children, 
        # allowing us to safely remove items while iterating.
        for child in list(parent):
            if child.tag == f'{ns}text' or child.tag == f'{ns}tspan':
                parent.remove(child)
            else:
                # Recurse into groups (<g>), layers, etc.
                remove_text_elements(child)

    remove_text_elements(root)

    # 4. Write the cleaned SVG to the output file
    tree.write(output_path, encoding='utf-8', xml_declaration=True)
    print(f"Success! Text stripped. Cleaned SVG saved to: {output_path}")

if __name__ == "__main__":
    # Default file names for testing
    input_file = "floorplan_input.svg"
    output_file = "floorplan_cleaned.svg"

    # Allow passing custom filenames via command line
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    if len(sys.argv) > 2:
        output_file = sys.argv[2]

    strip_text_from_svg(input_file, output_file)