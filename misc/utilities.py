#function to extract rules from brand guidelines document
import xlrd

def extractRules(document):
    wb = xlrd.open_workbook(document)
    sheet = wb.sheet_by_index(0)
    rules = {}
    rowCount = sheet.nrows
    for i in range(1,rowCount):
        element = sheet.cell_value(i,0)
        element_rule = sheet.cell_value(i,1)
        parameterRules = {}
        for rule in element_rule.split("\n"):
            parameter = rule.split(":")[0].strip()
            value = rule.split(":")[1].strip()
            parameterRules[parameter] = value
        rules[element] = parameterRules

    return rules

document = 'EYResources//BrandGuidelines.xlsx'

#function to filter annotations based on matching conditions
def annotate(brandGuidlineDoc, inputDoc):
    '''
    :param brandGuidlineDoc: Choice of brand guideline from the UI (i.e. Risk, Audit, IT etc)
    :param inputDoc: Input Document: PDF/JPG
    :return: outputDoc: annotated document in temp. folder
    '''

    brandRules = extractRules(brandGuidlineDoc)
    inputHeading = {'Font Size': '24 pt', 'Font Color': '46,48,56', 'Font Style': 'Arial', 'Casing': 'sentence Case', 'Position': 'same'}

    #compare
    for element in brandRules.keys():
        for parameter in brandRules[element].keys():
            if inputHeading[parameter] == brandRules[element][parameter]:
                print("same")
            else:
                print("call annotate function for: " + element + " and parameter: " + parameter)
        break


annotate(document, "input")
