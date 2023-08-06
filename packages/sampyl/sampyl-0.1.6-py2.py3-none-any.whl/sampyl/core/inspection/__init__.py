import os
from sampyl.core.element import Element
from selenium.webdriver.remote.webdriver import WebDriver

INSPECTION_PATH = os.path.dirname(os.path.abspath(__file__))
STYLE_PATH = os.path.join(INSPECTION_PATH, 'style.css')
SCRIPT_PATH = os.path.join(INSPECTION_PATH, 'script.js')
TEMPLATE_PATH = os.path.join(INSPECTION_PATH, 'template.html')
ELEMENT_PATH = os.path.join(INSPECTION_PATH, 'element.js')

__all__ = ['save_inspection']


def save_inspection(web_driver, image, elements, name_attr='data-qa-id'):

    wd = web_driver if isinstance(web_driver, WebDriver) else None

    if wd:

        screen_size = wd.get_window_size()
        s_elements = [ele.element() for ele in elements if isinstance(ele, Element)]

        # Compile style
        with open(STYLE_PATH, 'r') as f:
            css = f.read().format(image.replace('\n', ''), screen_size[u'height'])

        # Retrieve highlight-able elements
        with open(ELEMENT_PATH, 'r') as f:
            element_template = f.read()
            elementjs = '\n\t\t'.join([element_template.format(e.get_attribute(name_attr).replace('.', '_').replace('[', '_').replace(']', '_'),
                                                               int(e.location['x']), int(e.location['y']),
                                                               int(e.size['width']), int(e.size['height'])) for e in s_elements])

        # Compile script
        with open(SCRIPT_PATH, 'r') as f:
            js = f.read().format(screen_size[u'width'], screen_size[u'height'], elementjs)

        # Compile document
        with open(TEMPLATE_PATH, 'r') as f:
            html = f.read().format(css, js)

        return html
