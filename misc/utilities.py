#function to extract rules from brand guidelines document
import xlrd

def extractRules(document):
    wb = xlrd.open_workbook(document)
    sheet = wb.sheet_by_index(0)
    rules = {}
    rowCount = sheet.nrows
    for i in range(1,rowCount):
        element = sheet.cell_value(i,0)
        print("Element: ", element)
        element_rule = sheet.cell_value(i,1)
        parameterRules = {}
        for rule in element_rule.split("\n"):
            parameter = rule.split(":")[0].strip()
            value = rule.split(":")[1].strip()
            parameterRules[parameter] = value
        rules[element] = parameterRules

    return rules

document = 'EYResources//BrandGuidelines.xlsx'

extractRules(document)