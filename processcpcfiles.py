#!/usr/bin/python3.5

#Author:        Sasan Bahadaran
#Date:          3/31/17
#Organization:  Commerce Data Service
#Description:   This script is meant to parse files from
# http://www.cooperativepatentclassification.org/cpcSchemeAndDefinitions/Bulk.html
# in order to output cpc codes and related information into a structured csv file.


import sys, os, csv
from lxml import etree


def parseXML(filetoproc):
    try:
        doccontent = []
        parser = etree.XMLParser(remove_pis=True)
        tree = etree.parse(filetoproc, parser=parser)
        root = tree.getroot()
        for item in root.xpath('//definitions/definition-item'):
            cpc_content = []
            main_cpc_code = item.find('classification-symbol').text
            cpc_content.append(main_cpc_code)
            title_text = ''.join(item.xpath('definition-title/descendant-or-self::*/text()'))
            cpc_content.append(title_text)
            title_text_codes = '|'.join(item.xpath('definition-title//class-ref/text()'))
            cpc_content.append(title_text_codes)
            informative_ref_text = ''.join(item.xpath('references/informative-references/section-body/table/table-row/table-column//paragraph-text/text()'))
            cpc_content.append(informative_ref_text)
            informative_ref_cpc_codes = '|'.join(item.xpath('references/informative-references/section-body/table/table-row/table-column//paragraph-text/class-ref/text()'))
            cpc_content.append(informative_ref_cpc_codes)
            special_rules_text = ''.join(item.xpath('special-rules/section-body//paragraph-text/text()'))
            cpc_content.append(special_rules_text)
            special_rules_cpc_codes = '|'.join(item.xpath('special-rules/section-body//paragraph-text/class-ref/text()'))
            cpc_content.append(special_rules_cpc_codes)
            glossary_of_terms = ''.join(item.xpath('glossary-of-terms/section-body/table/table-row/table-column//paragraph-text/text()'))
            cpc_content.append(glossary_of_terms)
            doccontent.append(cpc_content)
        return doccontent 
    except IOError as e:
        print('I/O error({0}): {1}'.format(e.errno,e.strerror))

def writeResults(content, fname):
    try:
        if(os.path.isfile(fname)):
            print('file: {} exists!'.format(fname))
        else:
            with open(fname,'w') as outfile:
                writer = csv.writer(outfile, quoting=csv.QUOTE_ALL)
                writer.writerow(('cpc_code', 'title', 'title_cpc_codes', 'informative_references', \
                        'informative_references_cpc_codes', 'special_rules', 'special_rules_cpc_codes',\
                        'glossary_of_terms'))
                writer.writerows(content)
    except IOError as e:
        print('I/O error({0}): {1}'.format(e.errno,e.strerror))

#change extension of file name to specified extension
def changeExt(fname, ext):
    seq = (os.path.splitext(fname)[0], ext)
    return '.'.join(seq)

if __name__ == '__main__':
    scriptpath = os.path.dirname(os.path.abspath(__file__))
    for fdir in os.listdir(os.path.join(scriptpath, 'xml_files')):
        if os.path.isdir(os.path.join(scriptpath, 'xml_files', fdir)):
            print(fdir)
            for filename in os.listdir(os.path.join(scriptpath, 'xml_files', fdir)):
                if filename.endswith('.xml'):
                    fname = os.path.join(scriptpath, 'xml_files', fdir, filename)
                    print('FILE: {}'.format(fname))
                    output_fname = os.path.join(scriptpath, 'xml_files', fdir, (os.path.basename(fname)).split('-')[2]) 
                    output_fname = changeExt(output_fname, 'csv')
                    if (os.path.isfile(output_fname)):
                        print('FILE: {} already exists!'.format(output_fname))
                    else:
                        content = parseXML(fname)
                        writeResults(content, output_fname)
