from flask import Flask,request,render_template,redirect,url_for
from elasticsearch import Elasticsearch
es=Elasticsearch([{'host':'localhost','port':9200}])
app = Flask(__name__)

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        try:
            search=request.form.get('search')
            print(search)
            res = es.search(index='helpandsupport', body={'query': {'match': {'question': search}}})
            records = []
            for hit in res['hits']['hits']:
                data = [hit['_source']['question'],hit['_source']['answer']]
                records.append(data)
            return render_template('search.html',records =records)
        except Exception as ex:
            print(str(ex.args[0]))
    else:
        return render_template('search.html')

@app.route('/')
@app.route('/companyName/newQuery/', methods=['GET', 'POST'])
def newQuery():
    if request.method == 'POST':
        try:
            question=request.form.get('question')
            answer = request.form.get('answer')
            e1 = {
                "question": question,
                "answer": answer
            }
            res = es.index(index='helpandsupport', doc_type='vodafone', body=e1)
            print("Created")
            return redirect(url_for('newQuery'))
        except Exception as ex:
            #logging.ERROR(str(ex))
            print(str(ex.args[0]))
    else:
        return render_template('qa.html')


if __name__ == '__main__':
    app.run()
