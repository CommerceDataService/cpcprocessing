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
            #print('---------------------')
            main_cpc_code = item.find('classification-symbol').text
            cpc_content.append(main_cpc_code)
            #print('[main cpc code]: {}'.format(main_cpc_code))
            title_text = ''.join(item.xpath('definition-title/descendant-or-self::*/text()'))
            cpc_content.append(title_text)
            #print('[title text]: {}'.format(title_text))
            title_text_codes = '|'.join(item.xpath('definition-title//class-ref/text()'))
            cpc_content.append(title_text_codes)
            #print('[title cpc codes]: {}'.format(title_text_codes))
            informative_ref_text = ''.join(item.xpath('references/informative-references/section-body/table/table-row/table-column//paragraph-text/text()'))
            cpc_content.append(informative_ref_text)
            #print('[informative references text]: {}'.format(informative_ref_text))
            informative_ref_cpc_codes = '|'.join(item.xpath('references/informative-references/section-body/table/table-row/table-column//paragraph-text/class-ref/text()'))
            cpc_content.append(informative_ref_cpc_codes)
            #print('[informative references codes]: {}'.format(informative_ref_cpc_codes))
            special_rules_text = ''.join(item.xpath('special-rules/section-body//paragraph-text/text()'))
            cpc_content.append(special_rules_text)
            #print('[special rules text]: {}'.format(special_rules_text))
            special_rules_cpc_codes = '|'.join(item.xpath('special-rules/section-body//paragraph-text/class-ref/text()'))
            cpc_content.append(special_rules_cpc_codes)
            #print('[special rules codes]: {}'.format(special_rules_cpc_codes))
            glossary_of_terms = ''.join(item.xpath('glossary-of-terms/section-body/table/table-row/table-column//paragraph-text/text()'))
            cpc_content.append(glossary_of_terms)
            #print('[glossary of terms]: {}'.format(glossary_of_terms))
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
                writer.writerow(('cpc_code', 'title', 'title_cpc_codes', 'informative_references', 'informative_references_cpc_codes', 'special_rules', 'special_rules_cpc_codes',\
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
        print(fdir)
        for filename in os.listdir(os.path.join(scriptpath, 'xml_files', fdir)):
            if filename.endswith('.xml'):
                fname = os.path.join(scriptpath, 'xml_files', fdir, filename)
                print('FILE: {}'.format(fname))
                content = parseXML(fname)
                output_fname = os.path.join(scriptpath, 'xml_files', fdir, (os.path.basename(fname)).split('-')[2]) 
                output_fname = changeExt(output_fname, 'csv')
                writeResults(content, output_fname)


    #for root, dirs, files in os.walk(os.path.join(scriptpath, 'xml_files')):
        #print(dirs)
        #for fdir in dirs:
            #for file in os.listdir(fdir):
                #print(os.path.join(fdir, file))
            #fname = 'cpc-definition-A01B.xml'
            #filetoproc = os.path.join(scriptpath, fname)
            
            #content = parseXML(filetoproc)
            #output_fname = os.path.join(scriptpath, (os.path.basename(fname)).split('-')[2]) 
            #output_fname = changeExt(output_fname, 'csv')
            #writeResults(content, output_fname)

        

