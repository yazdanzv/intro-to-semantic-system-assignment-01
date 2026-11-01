"""Build the editable report and ontology-derived figures.

Dependencies: python-docx, reportlab, rdflib, and Poppler (pdftoppm).
Run from any directory: python report/build_report.py
Use the documents skill's render_docx.py --emit_pdf for final PDF export.
"""
from pathlib import Path
import subprocess
import shutil
import tempfile
import re

from rdflib import Graph, Namespace, RDF, RDFS, OWL, URIRef
from reportlab.graphics.shapes import Drawing, Rect, Line, String, Polygon
from reportlab.graphics import renderSVG, renderPDF
from reportlab.lib.colors import HexColor, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT = Path(__file__).resolve().parent.parent
FIGURES = ROOT / 'report' / 'figures'
STEM = 'A1_ZandiyeVakili_12642780_Report'
TA = Namespace('https://example.org/travel-assistant#')
G = Graph().parse(ROOT / 'ontology' / 'travel-assistant.owl', format='turtle')
NAVY = HexColor('#315A74')
PALE = HexColor('#EEF4F7')
INK = HexColor('#17232D')
GRAY = HexColor('#74838E')

# Embed a regular font so the diagram raster does not depend on font substitution.
DIAGRAM_FONT = Path('/System/Library/Fonts/Supplemental/Arial.ttf')
if not DIAGRAM_FONT.exists():
    import reportlab
    DIAGRAM_FONT = Path(reportlab.__file__).parent / 'fonts' / 'Vera.ttf'
pdfmetrics.registerFont(TTFont('DiagramText', str(DIAGRAM_FONT)))


def line(d, x1, y1, x2, y2, color=GRAY):
    d.add(Line(x1, y1, x2, y2, strokeColor=color, strokeWidth=0.8))


def box(d, text, x, y, w, h=19, fill=PALE, fs=9):
    assert pdfmetrics.stringWidth(text, 'DiagramText', fs) < w - 6, text
    d.add(Rect(x, y-h/2, w, h, rx=3, ry=3, fillColor=fill,
               strokeColor=NAVY, strokeWidth=0.65))
    d.add(String(x+w/2, y-3, text, fontName='DiagramText', fontSize=fs,
                 textAnchor='middle', fillColor=INK))


def hierarchy():
    d = Drawing(514, 208)
    # Coordinates are in points. Every edge is checked against the ontology.
    nodes = {'Thing': (0, 101, 66), 'Place': (101, 189, 109)}
    top = ['Traveler', 'Interest', 'Activity', 'Cuisine', 'BudgetCategory',
           'TransportOption', 'TransportMode']
    for i, name in enumerate(top):
        nodes[name] = (101, 163 - 24*i, 109)
    for name, y in [('City', 189), ('Country', 159), ('Attraction', 123),
                    ('Accommodation', 63), ('Restaurant', 21)]:
        nodes[name] = (265, y, 112)
    for name, y in [('Museum', 147), ('Landmark', 123), ('Park', 99),
                    ('Hotel', 73), ('Hostel', 47)]:
        nodes[name] = (428, y, 82)
    classes = {s for s in G.subjects(RDF.type, OWL.Class) if isinstance(s, URIRef)}
    assert classes == {TA[n] for n in nodes if n != 'Thing'}
    parents = []
    for child in classes:
        for parent in G.objects(child, RDFS.subClassOf):
            if isinstance(parent, URIRef):
                parents.append(('Thing' if parent == OWL.Thing else str(parent).split('#')[-1],
                                str(child).split('#')[-1]))
    for parent, child in parents:
        x, y, w = nodes[parent]
        xx, yy, _ = nodes[child]
        mid = x+w+19
        line(d, x+w, y, mid, y)
        line(d, mid, y, mid, yy)
        line(d, mid, yy, xx, yy)
    for name, (x, y, w) in nodes.items():
        box(d, 'owl:Thing' if name == 'Thing' else name, x, y, w,
            fill=HexColor('#F6F7F8') if name == 'Thing' else PALE)
    return d


def preference_relationships():
    d = Drawing(514, 150)
    # Repeated Traveler boxes denote the same class, avoiding crossing arrows.
    rows = [
        ('Interest', 'hasInterest', 'Attraction', 'hasAttractionTheme', 127),
        ('Interest', 'hasInterest', 'Activity', 'hasActivityTheme', 91),
        ('BudgetCategory', 'prefersBudgetCategory', 'Accommodation', 'hasBudgetCategory', 55),
        ('Cuisine', 'prefersCuisine', 'Restaurant', 'servesCuisine', 19),
    ]
    for shared, left_prop, right_class, right_prop, y in rows:
        for source, prop, target in [('Traveler', left_prop, shared), (right_class, right_prop, shared)]:
            assert (TA[prop], RDF.type, OWL.ObjectProperty) in G
            assert (TA[prop], RDFS.domain, TA[source]) in G
            assert (TA[prop], RDFS.range, TA[target]) in G
        box(d, 'Traveler', 0, y, 68, fs=9)
        box(d, shared, 212, y, 100, fs=9)
        box(d, right_class, 398, y, 112, fs=9)
        for x1, x2, label in [(68,212,left_prop),(398,312,right_prop)]:
            line(d,x1,y,x2,y,NAVY)
            sign = 1 if x2 > x1 else -1
            d.add(Polygon([x2,y,x2-sign*5,y+2.5,x2-sign*5,y-2.5],
                          fillColor=NAVY,strokeColor=NAVY))
            fs=7.7
            center=(x1+x2)/2
            width=pdfmetrics.stringWidth(label,'DiagramText',fs)
            d.add(Rect(center-width/2-2,y+2,width+4,10,fillColor=white,strokeColor=None))
            d.add(String(center,y+4,label,fontName='DiagramText',fontSize=fs,
                         textAnchor='middle',fillColor=INK))
    return d


def figures():
    FIGURES.mkdir(parents=True, exist_ok=True)
    for name, drawing in [('class-hierarchy', hierarchy()),
                          ('preference-relationships', preference_relationships())]:
        for item in drawing.contents:
            if hasattr(item, 'x'): item.x += 2
            if hasattr(item, 'y'): item.y += 2
            if isinstance(item, Line):
                item.x1 += 2; item.x2 += 2; item.y1 += 2; item.y2 += 2
            if isinstance(item, Polygon):
                item.points = [v + 2 for v in item.points]
        svg_path = FIGURES / (name+'.svg')
        renderSVG.drawToFile(drawing, str(svg_path))
        svg_path.write_text(svg_path.read_text().replace(
            'font-family: DiagramText;', 'font-family: Arial, sans-serif; font-style: normal;'))
        with tempfile.TemporaryDirectory(prefix='travel-report-figure-') as temp:
            pdf = Path(temp) / 'figure.pdf'
            renderPDF.drawToFile(drawing, str(pdf))
            subprocess.run([shutil.which('pdftoppm'), '-singlefile', '-r', '300', '-png',
                            str(pdf), str(FIGURES / name)], check=True)


def add_inline(p, text, bold=False, italic=False):
    """Render bold lead-ins and italic identifiers, including nested emphasis."""
    for part in re.split(r'(\*\*.*?\*\*|\*[^*]+\*)',text):
        if not part:
            continue
        if part.startswith('**'):
            add_inline(p, part[2:-2], bold=True, italic=italic)
        elif part.startswith('*') and part.endswith('*'):
            add_inline(p, part[1:-1], bold=bold, italic=True)
        else:
            run=p.add_run(part)
            run.bold=bold
            run.italic=italic


def shade(cell, color):
    shd=OxmlElement('w:shd'); shd.set(qn('w:fill'),color)
    cell._tc.get_or_add_tcPr().append(shd)


def table(doc, lines):
    records=[[s.strip() for s in row.strip().strip('|').split('|')] for row in lines]
    records=[r for r in records if not all(re.fullmatch(r'[-: ]+',c) for c in r)]
    t=doc.add_table(rows=0, cols=3)
    t.alignment=WD_TABLE_ALIGNMENT.CENTER; t.autofit=False
    widths=[1.25,2.65,2.15]
    for col,w in zip(t.columns,widths): col.width=Inches(w)
    props=t._tbl.tblPr
    borders=OxmlElement('w:tblBorders')
    for side in ['top','left','bottom','right','insideH','insideV']:
        el=OxmlElement('w:'+side)
        for k,v in [('val','single'),('sz','4'),('color','D9D9D9')]: el.set(qn('w:'+k),v)
        borders.append(el)
    props.append(borders)
    for i,row in enumerate(records):
        cells=t.add_row().cells
        trpr=t.rows[-1]._tr.get_or_add_trPr()
        no_split=OxmlElement('w:cantSplit'); trpr.append(no_split)
        if i==0:
            repeat=OxmlElement('w:tblHeader'); trpr.append(repeat)
        for j,(cell,value) in enumerate(zip(cells,row)):
            cell.width=Inches(widths[j]); cell.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
            tcpr=cell._tc.get_or_add_tcPr(); margins=OxmlElement('w:tcMar')
            for side in ['top','left','bottom','right']:
                el=OxmlElement('w:'+side); el.set(qn('w:w'),'85'); el.set(qn('w:type'),'dxa'); margins.append(el)
            tcpr.append(margins)
            p=cell.paragraphs[0]; p.paragraph_format.space_after=Pt(0)
            p.paragraph_format.line_spacing=1.03
            add_inline(p,value)
            for run in p.runs:
                run.font.size=Pt(9.5)
                if i==0:
                    run.bold=True; run.font.color.rgb=RGBColor(0,0,0)
            if i==0: shade(cell,'E6EEF3')
            elif i%2==0: shade(cell,'F6F8FA')


def build():
    figures()
    doc=Document(); sec=doc.sections[0]
    sec.page_width=Inches(8.5); sec.page_height=Inches(11)
    sec.top_margin=Inches(.63); sec.bottom_margin=Inches(.58)
    sec.left_margin=sec.right_margin=Inches(.7)
    sec.footer_distance=Inches(.25)
    for border in list(doc.styles.element.iter(qn('w:pBdr'))):
        border.getparent().remove(border)
    normal=doc.styles['Normal']; normal.font.name='Arial'; normal.font.size=Pt(11)
    normal.font.color.rgb=RGBColor(0,0,0)
    normal.paragraph_format.line_spacing=1.03
    normal.paragraph_format.space_after=Pt(5)
    for style,size in [('Title',22),('Subtitle',11),('Heading 1',13),('Heading 2',11)]:
        s=doc.styles[style]; s.font.name='Arial'; s.font.size=Pt(size); s.font.color.rgb=RGBColor(0,0,0)
        s.paragraph_format.space_before=Pt(9 if style=='Heading 1' else 0)
        s.paragraph_format.space_after=Pt(6)
    doc.styles['Title'].font.bold=True
    doc.styles['Heading 1'].font.bold=True
    doc.styles['Caption'].font.name='Arial'; doc.styles['Caption'].font.size=Pt(9)
    doc.styles['Caption'].font.color.rgb=RGBColor(55,55,55)
    doc.styles['Caption'].paragraph_format.space_after=Pt(6)
    doc.styles['Caption'].paragraph_format.line_spacing=1.0
    doc.core_properties.title='Travel Assistant Ontology'
    doc.core_properties.subject='Assignment 1 Ontology Modeling'
    doc.core_properties.author='Yazdan ZandiyeVakili'
    doc.core_properties.keywords='12642780; Introduction to Semantic Systems; OWL; ontology'
    f=sec.footer.paragraphs[0]; f.alignment=WD_ALIGN_PARAGRAPH.RIGHT
    run=f.add_run(); fld=OxmlElement('w:fldSimple'); fld.set(qn('w:instr'),'PAGE'); run._r.addnext(fld)
    f.style='Caption'
    lines=(ROOT/'report/report.md').read_text().splitlines()
    i=0
    while i<len(lines):
        s=lines[i].strip()
        if not s: i+=1; continue
        if s=='<!-- pagebreak -->':
            doc.add_page_break()
        elif s.startswith('# '): doc.add_paragraph(s[2:],'Title')
        elif s.startswith('## '): doc.add_paragraph(s[3:],'Heading 1')
        elif s.startswith('!['):
            name=re.search(r'\]\((.*?)\)',s).group(1)
            p=doc.add_paragraph(); p.paragraph_format.space_after=Pt(3)
            p.paragraph_format.keep_with_next=True
            run=p.add_run(); inline=run.add_picture(str(ROOT/'report'/name.replace('.svg','.png')),width=Inches(7.1))
            inline._inline.docPr.set('descr',re.search(r'!\[(.*?)\]',s).group(1))
        elif s.startswith('|'):
            rows=[]
            while i<len(lines) and lines[i].strip().startswith('|'):
                rows.append(lines[i]); i+=1
            table(doc,rows)
            continue
        elif s.startswith('*Figure') or s.startswith('*Table'):
            p=doc.add_paragraph(style='Caption'); add_inline(p,s)
        elif re.match(r'^\d+\. ',s):
            n,text=s.split('. ',1)
            p=doc.add_paragraph()
            p.paragraph_format.left_indent=Inches(.22)
            p.paragraph_format.first_line_indent=Inches(-.22)
            p.paragraph_format.space_after=Pt(6)
            add_inline(p,n+'. '+text)
        elif s.startswith('Assignment 1'):
            doc.add_paragraph(s,'Subtitle')
        elif s.startswith('Yazdan ') or s.startswith('188.399 '):
            p=doc.add_paragraph(s); p.paragraph_format.space_after=Pt(4)
            for r in p.runs: r.font.size=Pt(10)
        else:
            p=doc.add_paragraph(); add_inline(p,s)
            p.alignment=WD_ALIGN_PARAGRAPH.JUSTIFY_LOW
        i+=1
    path=ROOT/'report'/f'{STEM}.docx'
    doc.save(path)
    print(path)

if __name__=='__main__': build()
