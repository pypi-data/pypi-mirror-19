"""
All utils
"""
import xml.etree.cElementTree as ET
import re
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from .styles import get_styles, get_title_style, get_normal_style
from reportlab.lib.units import cm


def get_bare_tag(elem):
    """ Get the tag name without namespace """
    return elem.tag.rsplit('}', 1)[-1]


def get_clean_text(elem):
    """ return value without line breaker chars """
    return re.sub(r"[\f\n\r\t\v]", "", elem.text).strip()


def get_doc(pdf_file):
    """ get the pdf doc """
    return SimpleDocTemplate(pdf_file, pagesize=letter, rightMargin=24,
                             leftMargin=24, topMargin=24, bottomMargin=24)


def get_label(e):
    """ get a label or a title from element """
    return e.attrib.get("name") if e.attrib.get("name") is not None else get_bare_tag(e)


def has_children(e):
    """ true if element has children """
    return True if e.getchildren() else False


def add_logo(Story, logo_file):
    """ add a logo """
    im = Image(logo_file)
    im.hAlign = 'RIGHT'
    Story.append(im)
    Story.append(Spacer(1, 12))


def write_elem(Story, e, level, styles):
    """ write element in the pdf """
    # get label and value
    label = get_label(e)
    value = get_clean_text(e)
    # Gestion des titres: un titre est un élément avec des enfants
    if has_children(e):
        # Si on a un label non vide, on l'affiche
        if label:
            Story.append(Paragraph(label, get_title_style(styles, level)))
        # Si on a forcé le nom du label à vide, on met juste un petit espace
        else:
            Story.append(Spacer(1, 6))
    # C'est un element de type clé-valeur, on l'affiche normalement
    else:
        if label or value:
            Story.append(Paragraph("{}: {}".format(label, value), get_normal_style(styles, level)))
    return Story


def build_pdf(xml_file, pdf_file, logo_file=None):
    """ build the pdf file """
    # Build the doc and the story
    doc = get_doc(pdf_file)
    styles = get_styles()
    Story = []
    # events and level for lxml
    level = 0

    # Add logo
    if logo_file:
        add_logo(Story, logo_file)

    # Parse the full xml
    for action, e in ET.iterparse(xml_file, events=("start", "end")):
        # If a new element is encountered
        if ET.iselement(e) and action == 'start':
            Story = write_elem(Story, e, level, styles)
        # Calcul the level
        if (action == 'start'):
            level += 1
        elif (action == 'end'):
            level -= 1
    doc.build(Story)
