from flask import Blueprint
from flask import request
from flask import jsonify
from gensim.models import doc2vec
from flask_restx import Resource, Namespace, fields

from app.service.InferVector import infer_vector
from app import modeldata
from ..model.user import Paper

class ModelDto:
    api = Namespace('model', description='')
    infer = api.model('model', {
        'email': fields.String(required=True, description=''),
        'password': fields.String(required=True, description=''),
    })

api = ModelDto.api
parser = api.parser()
infer = ModelDto.infer

@api.route('/getpaperlist')
class ModelInfer(Resource):
    @api.expect(infer, validate=False)
    def post(self):

        # 개인서재의 논문 목록을 받아온다. 여러개의 json을 받아오는 경우
        # 사용자 (user_id)
        params = request.get_json()
        UID = params["user_id"]
        category = params['category']
        #print(params)

        paper_list = Paper.query.filter_by(user_id = UID)
        #print(paper_list)

        text = []
        title_list = []

        if paper_list.first() == None:
            print("None!!!")
            text.append(category) # 개인서재에 아무것도 없을 경우를 위해 코드작성

        for paper in paper_list:
            print("HERE")
            title = paper.title
            text.append(modeldata[title][1])
            title_list.append(title)

        '''
        
        category = ''
        text = []
        name_list = []
        for json in params:
            name = json['name']
            category = json['category']
            text.append(modeldata[name][1])
            name_list.append(name)
        '''


        # 생성한 모델을 string parsing을 통해 로드한다.
        model_path = category.split('_')[0]
        model_name = category + '_한국어_model'
        model = doc2vec.Doc2Vec.load('app/service/Model/{}/{}'.format(model_path, model_name))


        # vector infer
        infer_vec = infer_vector(text, model)


        # topn = 5로 설정하여 5개까지 논문 리스트를 추천해주도록 한다.
        similar_doc = model.dv.most_similar(positive=[infer_vec], topn=20)


        # json_obj 형태로 논문들을 저장하고 리턴한다.
        json_obj = []
        count = 0
        for doc_name, cosine in similar_doc:
            # 기존에 사용자가 서재에 추가한 논문의 경우는 추천 논문 리스트에 포함시키지 않음
            if doc_name in title_list:
                continue;
            count+=1
            json = dict()
            json['title'] = doc_name
            json['abstract'] = modeldata[doc_name][1]
            json['author'] = modeldata[doc_name][2]
            json['year'] = modeldata[doc_name][3]
            json['link'] = modeldata[doc_name][4]
            json['category'] = modeldata[doc_name][5]
            json_obj.append(json)
            if count == 5:
                break

        return jsonify(json_obj)


@api.route('/getpaper')
class GetPaper(Resource):
    @api.expect(infer, validate=False)
    def post(self):

        # json을 받아와서, json 안의 category 정보를 받아온다.
        params = request.get_json()
        category = params['category']

        # 현재 개인서재 목록에 아무것도 없는 상태이므로, 임의의 논문 목록을 추천해주기 위해 카테고리 문자열 자체로 vector infer한다.
        text = []
        text.append(category)


        # 생성한 모델을 string parsing을 통해 로드한다.
        model_path = category.split('_')[0]
        model_name = category + '_한국어_model'
        model = doc2vec.Doc2Vec.load('app/service/Model/{}/{}'.format(model_path, model_name))


        # vector infer
        infer_vec = infer_vector(text, model)

        # topn = 5로 설정하여 5개까지 논문 리스트를 추천해주도록 한다.
        similar_doc = model.dv.most_similar(positive=[infer_vec], topn=5)

        # json_obj 형태로 논문들을 저장하고 리턴한다.
        json_obj = []
        for doc_name, cosine in similar_doc:
            json = dict()
            json['title'] = doc_name
            json['abstract'] = modeldata[doc_name][1]
            json['author'] = modeldata[doc_name][2]
            json['year'] = modeldata[doc_name][3]
            json['link'] = modeldata[doc_name][4]
            json['category'] = modeldata[doc_name][5]
            json_obj.append(json)
        return jsonify(json_obj)