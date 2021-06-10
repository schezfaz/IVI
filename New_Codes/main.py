import os
# set the paths
pathToScript = 'pdf2txt.py'
pathPDFinput = 'ivi.pdf'
pathHTMLoutput = 'test.html'

# call the pdf2txt.py from the command line
os.system('python {} -o {} -S {} -t html'.format(pathToScript, pathHTMLoutput, pathPDFinput))
  