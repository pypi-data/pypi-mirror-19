from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle


def get_styles():
    """
    get styles for the pdf, default are :
    Title: <ParagraphStyle ‘Title’>
    Heading1: <ParagraphStyle ‘Heading1’>
    Heading2: <ParagraphStyle ‘Heading2’>
    Heading3: <ParagraphStyle ‘Heading3’>
    Heading4: <ParagraphStyle ‘Heading4’>
    Heading5: <ParagraphStyle ‘Heading5’>
    Heading6: <ParagraphStyle ‘Heading6’>
    Bullet: <ParagraphStyle ‘Bullet’>
    Definition: <ParagraphStyle ‘Definition’>
    Normal: <ParagraphStyle ‘Normal’>
    Italic: <ParagraphStyle ‘Italic’>
    BodyText: <ParagraphStyle ‘BodyText’>
    Code: <ParagraphStyle ‘Code’>
    """
    styles = getSampleStyleSheet()
    # Titles
    styles.add(ParagraphStyle(name='cTitle', parent=styles['Title'], spaceAfter=24))
    styles.add(ParagraphStyle(name='cHeading1', parent=styles['Heading1'], spaceBefore=10,
        borderRadius=5, borderWidth=1, borderPadding=4, borderColor=colors.HexColor("#668cff"), backColor=colors.HexColor("#668cff")))
    styles.add(ParagraphStyle(name='cHeading2', parent=styles['Heading2'], spaceBefore=10, leftIndent=12,
        borderRadius=5, borderWidth=1, borderPadding=4, borderColor=colors.HexColor("#809fff"), backColor=colors.HexColor("#809fff")))
    styles.add(ParagraphStyle(name='cHeading3', parent=styles['Heading3'], spaceBefore=10, leftIndent=24,
        borderRadius=5, borderWidth=1, borderPadding=4, borderColor=colors.HexColor("#99b3ff"), backColor=colors.HexColor("#99b3ff")))
    styles.add(ParagraphStyle(name='cHeading4', parent=styles['Heading4'], spaceBefore=10, leftIndent=36,
        borderRadius=5, borderWidth=1, borderPadding=4, borderColor=colors.HexColor("#b3c6ff"), backColor=colors.HexColor("#b3c6ff")))
    styles.add(ParagraphStyle(name='cHeading5', parent=styles['Heading5'], spaceBefore=10, leftIndent=48,
        borderRadius=5, borderWidth=1, borderPadding=4, borderColor=colors.HexColor("#ccd9ff"), backColor=colors.HexColor("#ccd9ff")))
    styles.add(ParagraphStyle(name='cHeading6', parent=styles['Heading6'], spaceBefore=10, leftIndent=60,
        borderRadius=5, borderWidth=1, borderPadding=4, borderColor=colors.HexColor("#e6ecff"), backColor=colors.HexColor("#e6ecff")))
    # Normals
    styles.add(ParagraphStyle(name='cNormal', parent=styles['Normal']))
    styles.add(ParagraphStyle(name='cNormal1', leftIndent=12, parent=styles['Normal']))
    styles.add(ParagraphStyle(name='cNormal2', leftIndent=24, parent=styles['Normal'])),
    styles.add(ParagraphStyle(name='cNormal3', leftIndent=36, parent=styles['Normal'])),
    styles.add(ParagraphStyle(name='cNormal4', leftIndent=48, parent=styles['Normal'])),
    styles.add(ParagraphStyle(name='cNormal5', leftIndent=60, parent=styles['Normal'])),
    styles.add(ParagraphStyle(name='cNormal6', leftIndent=72, parent=styles['Normal'])),

    return styles


def get_title_style(styles, level):
    """ get title style by level """
    if level == 0:
        return styles["cTitle"]
    elif level in [1, 2, 3, 4, 5, 6]:
        return styles["{}{}".format("cHeading", str(level))]
    else:
        return styles["Italic"]


def get_normal_style(styles, level):
    """ get title style by level """
    if level == 0:
        return styles["cNormal"]
    elif level in [1, 2, 3, 4, 5, 6]:
        return styles["{}{}".format("cNormal", str(level))]
    else:
        return styles["cNormal6"]
