import argparse
from computeComplexity import DocumentComplexity

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--inputDoc', help='Input Document')
parser.add_argument('-m', '--metric', help='Metrics to Evaluate. Can take values : flesch, gfog, ari')
args = parser.parse_args()

text = open(args.inputDoc).read()
docComplexityObj = DocumentComplexity(text)

# method, score, grade = docComplexityObj.getMetricResults(args.metric)

grade = docComplexityObj.getCommonGrade()
print('Grade : ', grade.get('label'))
print('Score : ', grade.get('score'))
