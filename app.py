from flask import Flask, render_template, request
from computeComplexity import DocumentComplexity

app = Flask(__name__, template_folder='html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/evaluate', methods=['POST'])
def evaluate():
    print(request.form)
    docComplexityObj = DocumentComplexity(request.form.get('inputText'))
    return render_template('result.html', result=docComplexityObj.getCommonGrade())

if __name__ == 'main':
    app.run(debug=True)