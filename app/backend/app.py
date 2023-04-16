# render_templete：参照するテンプレートを指定
# jsonify：json出力（WebAPIの出力）
from flask import Flask, render_template, jsonify, request

# CORS：Ajaxのためのライブラリ
from flask_cors import CORS
from random import *

from paperRecom import paperRecommendation_entire

app = Flask(__name__)

app.config.from_object(__name__)

CORS(app)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch(path):
    return render_template("../paper-recommendation/index.html")


# '/rand'が叩かれた時、乱数を生成
@app.route('/rand')
def random():
    response = {
        'randomNum': randint(1,100)
    }
    return jsonify(response)

@app.route('/search', methods=['POST'])
# @app.route('/search', methods=['POST'])
def searchPaper():
    # app.logger.debug(request.get_json())
    
    # ダミーデータ
    # paperList = [
    #     {
    #         'title': 'Attention Is All You Need',
    #         'abst': 'The dominant sequence transduction models are based on complex recurrent or convolutional neural networks in an encoder-decoder configuration. The best performing models also connect the encoder and decoder through an attention mechanism. We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely. Experiments on two machine translation tasks show these models to be superior in quality while being more parallelizable and requiring significantly less time to train. Our model achieves 28.4 BLEU on the WMT 2014 English-to-German translation task, improving over the existing best results, including ensembles by over 2 BLEU. On the WMT 2014 English-to-French translation task, our model establishes a new single-model state-of-the-art BLEU score of 41.8 after training for 3.5 days on eight GPUs, a small fraction of the training costs of the best models from the literature. We show that the Transformer generalizes well to other tasks by applying it successfully to English constituency parsing both with large and limited training data.'
    #     },
    #     {
    #         'title': 'BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding',
    #         'abst': 'We introduce a new language representation model called BERT, which stands for Bidirectional Encoder Representations from Transformers. Unlike recent language representation models, BERT is designed to pre-train deep bidirectional representations from unlabeled text by jointly conditioning on both left and right context in all layers. As a result, the pre-trained BERT model can be fine-tuned with just one additional output layer to create state-of-the-art models for a wide range of tasks, such as question answering and language inference, without substantial task-specific architecture modifications. BERT is conceptually simple and empirically powerful. It obtains new state-of-the-art results on eleven natural language processing tasks, including pushing the GLUE score to 80.5% (7.7% point absolute improvement), MultiNLI accuracy to 86.7% (4.6% absolute improvement), SQuAD v1.1 question answering Test F1 to 93.2 (1.5 point absolute improvement) and SQuAD v2.0 Test F1 to 83.1 (5.1 point absolute improvement).'
    #     }
    # ]
    
    
    # postで渡された検索クエリを受け取る
    query = request.get_json()['query']

    # 検索クエリで論文検索
    method = "tf-idf"
    response = paperRecommendation_entire.recom(method, query)

    print(response[:10])
    return jsonify(response[:10])

# app.run(host, port)：hostとportを指定してflaskサーバを起動
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
