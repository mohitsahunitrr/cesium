from xml.etree import ElementTree
from pprint import pprint

# calling example
def main():
    configdict = ConvertXmlToDict(ElementTree.parse('test_tdf.xml').getroot())
    return configdict
    pprint(configdict)

    # you can access the data as a dictionary
    #print configdict['settings']['color']
    #configdict['settings']['color'] = 'red'

    # or you can access it like object attributes
    print configdict.tdf.created_by
    configdict.tdf.created_by = 'red'

    root = ConvertDictToXml(configdict)

    tree = ElementTree.ElementTree(root)
    tree.write('config.new.xml')


# Module Code:

class XmlDictObject(dict):
    def __init__(self, initdict=None):
        if initdict is None:
            initdict = {}
        dict.__init__(self, initdict)

    def __getattr__(self, item):
        return self.__getitem__(item)

    def __setattr__(self, item, value):
        self.__setitem__(item, value)

    def __str__(self):
        if self.has_key('_text'):
            return self.__getitem__('_text')
        else:
            return ''

    @staticmethod
    def Wrap(x):
        if isinstance(x, dict):
            return XmlDictObject((k, XmlDictObject.Wrap(v)) for (k, v) in x.iteritems())
        elif isinstance(x, list):
            return [XmlDictObject.Wrap(v) for v in x]
        else:
            return x

    @staticmethod
    def _UnWrap(x):
        if isinstance(x, dict):
            return dict((k, XmlDictObject._UnWrap(v)) for (k, v) in x.iteritems())
        elif isinstance(x, list):
            return [XmlDictObject._UnWrap(v) for v in x]
        else:
            return x

    def UnWrap(self):
        return XmlDictObject._UnWrap(self)

def _ConvertDictToXmlRecurse(parent, dictitem):
    assert type(dictitem) is not type([])

    if isinstance(dictitem, dict):
        for (tag, child) in dictitem.iteritems():
            if str(tag) == '_text':
                parent.text = str(child)
            elif type(child) is type([]):
                for listchild in child:
                    elem = ElementTree.Element(tag)
                    parent.append(elem)
                    _ConvertDictToXmlRecurse(elem, listchild)
            else:
                elem = ElementTree.Element(tag)
                parent.append(elem)
                _ConvertDictToXmlRecurse(elem, child)
    else:
        parent.text = str(dictitem)

def ConvertDictToXml(xmldict):
    roottag = xmldict.keys()[0]
    root = ElementTree.Element(roottag)
    _ConvertDictToXmlRecurse(root, xmldict[roottag])
    return root

def _ConvertXmlToDictRecurse(node, dictclass):
    nodedict = dictclass()

    if len(node.items()) > 0:
        # if we have attributes, set them
        nodedict.update(dict(node.items()))

    for child in node:
        # recursively add the element's children
        newitem = _ConvertXmlToDictRecurse(child, dictclass)
        if nodedict.has_key(child.tag):
            # found duplicate tag, force a list
            if type(nodedict[child.tag]) is type([]):
                # append to existing list
                nodedict[child.tag].append(newitem)
            else:
                # convert to list
                nodedict[child.tag] = [nodedict[child.tag], newitem]
        else:
            # only one, directly set the dictionary
            nodedict[child.tag] = newitem

    if node.text is None:
        text = ''
    else:
        text = node.text.strip()

    if len(nodedict) > 0:
        # if we have a dictionary add the text as a dictionary value (if there is any)
        if len(text) > 0:
            nodedict['_text'] = text
    else:
        # if we don't have child nodes or attributes, just set the text
        try:
            nodedict = node.text.strip()
        except:
            #print node.text
            nodedict = None
    #print nodedict
    return nodedict

def ConvertXmlToDict(root, dictclass=XmlDictObject):
    return dictclass({root.tag: _ConvertXmlToDictRecurse(root, dictclass)})


if __name__ == '__main__':
    main()
