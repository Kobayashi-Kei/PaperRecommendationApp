import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import csr_matrix
from sklearn.metrics.pairwise import cosine_similarity
import argparse



"""
関連研究推薦の実験
・アブストラクト全体でコサイン類似度を測り、高い順に並べて推薦順位とする
・ランキングのメトリクスで評価する
"""	
def main():    
    """
    引数を読み込み
    """
    args = arg_parse_from_commandline(['method', 'query'])
    method = args.method
    query = args.query

    if method != 'tf-idf' and \
            method != 'bow' and \
            method != 'bm25' and \
            method != 'Bert' and \
            method != 'SciBert' and \
            method != 'Specter':
        print("Methodの引数が間違っています")
        exit()
    

"""
Class & Methods
"""
def recom(method, query):
    """
    データ構造の定義
    """
    allPaperData = allPaperDataClass()

    """
    データファイルの読み込み
    """
    size = "medium"
    # size = "small"

    path = "dataserver/axcell/" + size + "/paperDict.json"
    with open(path, 'r') as f:
        allPaperData.paperDict = json.load(f)

    if method == 'tf-idf' or method == 'bow':
        # ラベル毎のアブストをロード
        path = "dataserver/axcell/" + size + "/labeledAbst.json"
        with open(path, 'r') as f:
            labeledAbstDict = json.load(f)
        # 扱いやすいようにアブストだけでなくタイトルもvalueで参照できるようにしておく
        for title in labeledAbstDict:
            labeledAbstDict[title]["title"] = title
    else:
        # アブスト全体の埋め込みをロード
        # タイトルを用いず、アブストのみを用いる場合
        path = "dataserver/axcell/" + size + "/embedding/titleAbst" + method + ".json"
        with open(path, 'r') as f:
            abstEmb = json.load(f)
        
        # ラベル毎のアブスト埋め込みをロード
        path = "dataserver/axcell/" + size + "/embLabel/labeledAbst" + method + ".json"
        with open(path, 'r') as f:
            labeledAbstDict = json.load(f)

    
    
    """
    データの整形
    """
    labelList = ['title', 'bg', 'obj', 'method', 'res']

    for title, paper in allPaperData.paperDict.items():
        # Vectorizerに合うようにアブストラクトのみをリストに抽出
        allPaperData.abstList.append(paper["abstract"])

        # 分類されたアブストラクトごとにリストに抽出
        labelAbst = labeledAbstDict[paper["title"]]
        for label in labelList:
            allPaperData.labelList[label].append(labelAbst[label])

    # 辞書をリストに変換
    allPaperData.paperList = list(allPaperData.paperDict.values())
    
    # Bert系の場合は埋め込みをリストに変換
    if 'Bert' in method or method == 'Specter':
        for title, embedAbst in abstEmb.items():
            allPaperData.abstEmbList.append(embedAbst)
                
    # 予測結果の分析のため、タイトルをキーとして、indexをバリューとする辞書を生成
    for i, paper in enumerate(allPaperData.paperList):
        allPaperData.titleToIndex[paper['title']] = i

    """
    BOW・TF-IDFを算出
    """
    # TF-IDF
    if method == 'tf-idf': 
        vectorizer = TfidfVectorizer()
        simMatrix = calcSimMatrix(allPaperData, query, vectorizer=vectorizer)
            
    # BOW
    elif method == 'bow':
        vectorizer = CountVectorizer()
        simMatrix = calcSimMatrix(allPaperData, query, vectorizer=vectorizer)

    # BERT系
    elif 'Bert' in method or 'Specter' in method:
        if method == 'Bert':
            from transformers import BertModel, BertTokenizer
            tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
            model = BertModel.from_pretrained("bert-base-uncased")

        elif method == "Specter":
            from transformers import AutoModel, AutoTokenizer
            tokenizer = AutoTokenizer.from_pretrained('allenai/specter')
            model = AutoModel.from_pretrained('allenai/specter')

        input = tokenizer(query, padding=True, truncation=True, return_tensors="pt", max_length=512)
        output = model(**input).last_hidden_state[:, 0, :]

        simMatrix = calcSimMatrix(allPaperData, output)
    

    """
    推薦結果を生成
    """
    for i, row in enumerate(simMatrix):
        row_dict = {i: row[i] for i in range(0, len(row))}
        row_dict = dict(sorted(row_dict.items(), key=lambda x:x[1], reverse=True))
        row_rankedIndexList = list(row_dict.keys())
        result = []
        for rank, idx in enumerate(row_rankedIndexList):
            # if tmpResult['queryTitle'] == allPaperData.paperList[idx]["title"]:
            #     continue
            result.append({
                "title": allPaperData.paperList[idx]["title"],
                "abst": allPaperData.paperList[idx]["abstract"]
                })
        # print(result)  

    return result

class PaperDataClass:
    def __init__(self):
        self.paperDict = {}
        self.paperList = [] # ランダムに論文を選択する都合上、数字のインデックスでアクセスできるようにリストも持っておく
        self.abstList = []
        self.abstEmbList = []
        self.labelList = { # TF-IDFの処理の都合上、観点毎にリストに切り出す
            'title': [],
            'bg': [],
            'obj': [],
            'method': [],
            'res': [],
            'other': [],
        }

class allPaperDataClass(PaperDataClass):
    def __init__(self):
        super().__init__()
        self.testDataIndex = []
        self.titleToIndex = {}

class testPaperDataClass(PaperDataClass):
    def __init__(self):
        super().__init__()
        self.allDataIndex = []

def arg_parse_from_commandline(argNameList):
    parser = argparse.ArgumentParser()
    for argName in argNameList:
        parser.add_argument(argName, help=argName)
    args = parser.parse_args()
    return args

def calcSimMatrix(allPaperData: allPaperDataClass, query, vectorizer=None):
    # TF-IDFやbowの計算を行う
    tmpVectorList = []
    if vectorizer:
        # 全体の語彙の取得とTF-IDF(bow)の計算の実行、返り値はScipyのオブジェクトとなる
        # vectorizer.fit(allPaperData.abstList)
        vectorizer.fit(allPaperData.abstList + allPaperData.labelList['title'])
        for i, text in enumerate(allPaperData.abstList):
            # vector = vectorizer.transform([text]).toarray().tolist()[0]
            titleAndAbst = text + allPaperData.labelList['title'][i]
            vector = vectorizer.transform([titleAndAbst]).toarray().tolist()[0]
            tmpVectorList.append(vector)
        
        queryVector = vectorizer.transform([query]).toarray().tolist()[0]
    else:
        queryVector = query
        tmpVectorList = allPaperData.abstEmbList
    
    # TF-IDFやBOWの場合は疎行列となるため、csr_sparse_matrixに変換して速度を上げる
    if vectorizer:
        queryVector = csr_matrix(queryVector)
        tmpVectorList = csr_matrix(tmpVectorList)
        
    simMatrix = cosine_similarity(queryVector, tmpVectorList)
    
    return simMatrix       

if __name__ == "__main__":
    main()