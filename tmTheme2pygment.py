import os
import sys
from xml.dom.minidom import parse
from collections import defaultdict


class Style:
    # .highlight is the wrapper class for highlighting therefore
    # all css rules are prefixed with .highlight
    PREFIX = '.highlight'

    # -----------------------------------------
    #  Params
    #  name: the name of the class
    #  args: each argument is an array.
    #  Each array consists of css properties
    #  that is either a color or font style
    #  ----------------------------------------

    def __init__(self, name, *args):
        self.name = name   # Name of the class
        self.rules = {}   # The css rules
        for arr in args:
            for value in arr:
                # Only define properties if they are already not defined
                # This allows "cascading" if rules to be applied
                if value.startswith('#') and 'color' not in self.rules:
                    self.rules['color'] = value
                else:
                    if 'italic' in value and 'font-style' not in self.rules:
                        self.rules['font-style'] = 'italic'
                    if 'underline' in value and 'text-decoration' not in self.rules:
                        self.rules['text-decoration'] = 'underline'
                    if 'bold' in value and 'font-weight' not in self.rules:
                        self.rules['font-weight'] = 'bold'

    # Helper method for creating the css rule
    def _join_attr(self):
        temp = []
        if(len(self.rules) == 0):
            return ''
        for key in self.rules:
            temp.append(key + ': ' + self.rules[key])
        return '; '.join(temp) + ';'

    def toString(self):
        joined = self._join_attr()
        if joined:
            return "%s .%s { %s }" % (Style.PREFIX, self.name, joined)
        return ''


# Crappy xml parsing function for getting the
# colors and font styles from colortheme file


def get_settings(file_name):
    settings = defaultdict(lambda: [])
    dom = parse(file_name)
    arr = dom.getElementsByTagName('array')[0]
    editor_cfg = arr.getElementsByTagName('dict')[0].getElementsByTagName('dict')[0]
    editor_vals = editor_cfg.getElementsByTagName('string')
    background = editor_vals[0].firstChild.nodeValue
    text_color = editor_vals[2].firstChild.nodeValue
    settings['editor_bg'] = background
    settings['text_color'] = text_color
    for node in arr.childNodes:
        if node.nodeName == "dict":
            try:
                setting = node.getElementsByTagName('string')[1].firstChild.nodeValue
                attrs = []
                values = node.getElementsByTagName('dict')[0].getElementsByTagName('string')
                for v in values:
                    if v.firstChild:
                        a = str(v.firstChild.nodeValue).strip()
                        attrs.append(a)
                for s in setting.split(', '):
                    settings[s] = attrs
            except:
                continue
    return settings


if __name__ == "__main__":
    args = sys.argv[1:]
    if(len(args) < 1):
        print "Please provide the .tmTheme file!"
        sys.exit(0)
    s = get_settings(args[0])
    styles = []

    #Generic
    styles.append(Style('ge', ['italic']))
    styles.append(Style('gs', ['bold']))

    # Comments
    styles.append(Style('c', s['comment']))
    styles.append(Style('cp', s['comment']))
    styles.append(Style('c1', s['comment']))
    styles.append(Style('cs', s['comment']))
    styles.append(Style('cm', s['comment.block'], s['comment']))

    # Constants
    styles.append(Style('m', s['constant.numeric'], s['constant.other'], s['constant'], s['support.constant']))
    styles.append(Style('mf', s['constant.numeric'], s['constant.other'], s['constant'], s['support.constant']))
    styles.append(Style('mi', s['constant.numeric'], s['constant.other'], s['constant'], s['support.constant']))
    styles.append(Style('mo', s['constant.numeric'], s['constant.other'], s['constant'], s['support.constant']))
    styles.append(Style('se', s['constant.language'], s['constant.other'], s['constant'], s['support.constant']))
    styles.append(Style('kc', s['constant.language'], s['constant.other'], s['constant'], s['support.constant']))

    #Keywords
    styles.append(Style('k', s['entity.name.type'], s['support.type'], s['keyword']))
    styles.append(Style('kd', s['storage.type'], s['storage']))
    styles.append(Style('kn', s['support.function.construct'], s['keyword.control'], s['keyword']))
    styles.append(Style('kt', s['entity.name.type'], s['support.type'], s['support.constant']))

    #String
    styles.append(Style('s', s['string.quoted.double'], s['string.quoted'], s['string']))
    styles.append(Style('sb', s['string.quoted.double'], s['string.quoted'], s['string']))
    styles.append(Style('sc', s['string.quoted.single'], s['string.quoted'], s['string']))
    styles.append(Style('sd', s['string.quoted.double'], s['string.quoted'], s['string']))
    styles.append(Style('s2', s['string.quoted.double'], s['string.quoted'], s['string']))
    styles.append(Style('sh', s['string']))
    styles.append(Style('si', s['string.interpolated'], s['string']))
    styles.append(Style('sx', s['string.other'], s['string']))
    styles.append(Style('sr', s['string.regexp'], s['string']))
    styles.append(Style('s1', s['string.quoted.single'], s['string']))
    styles.append(Style('ss', s['string']))

    #Name
    styles.append(Style('na', s['entity.other.attribute-name'], s['entity.other']))
    styles.append(Style('bp', s['variable.language'], s['variable']))
    styles.append(Style('nc', s['entity.name.class'], s['entity.other.inherited-class'], s['support.class']))
    styles.append(Style('no', s['constant.language'], s['constant']))
    styles.append(Style('nd', s['entity.name.class']))
    styles.append(Style('ne', s['entity.name.class']))
    styles.append(Style('nf', s['entity.name.function'], s['support.function']))
    styles.append(Style('nt', s['entity.name.tag'], s['keyword']))
    styles.append(Style('nv', s['variable'], [s['text_color']]))
    styles.append(Style('vc', s['variable.language']))
    styles.append(Style('vg', s['variable.language']))
    styles.append(Style('vi', s['variable.language']))

    #Operator
    styles.append(Style('ow', s['keyword.operator'], s['keyword.operator'], s['keyword']))
    styles.append(Style('o', s['keyword.operator'], s['keyword.operator'], s['keyword']))

    # Text
    styles.append(Style('n', [s['text_color']]))
    styles.append(Style('nl', [s['text_color']]))
    styles.append(Style('nn', [s['text_color']]))
    styles.append(Style('nx', [s['text_color']]))
    styles.append(Style('bp', s['variable.language'], s['variable'], [s['text_color']]))
    styles.append(Style('p', [s['text_color']]))

    directory = os.path.abspath(os.path.dirname(args[0]))
    # default file output will be in the
    # same directory as the tmfile, but with a .css extension
    fname = os.path.join(directory, os.path.splitext(os.path.basename(args[0]))[0] + '-Highlight.css')

    # If a 2nd argument is provided (the output file), use that instead
    if(len(args) == 2):
        fname = os.path.abspath(args[1])

    # write to the file
    f = open(fname, 'w')
    f.write('.highlight { background-color: ' + s['editor_bg'] + '; color: ' + s['text_color'] + '; }\n')
    for st in styles:
        css_style = st.toString()
        if css_style:
            f.write(css_style + '\n')
    f.close()
