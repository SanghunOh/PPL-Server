from flask import Blueprint
from flask import request
from flask import jsonify
from gensim.models import doc2vec
from flask_restx import Resource, Namespace, fields

from ..service.InferVector import infer_vector
from app import modeldata

class ModelDto:
    api = Namespace('model', description='')
    infer = api.model('model', {
        'email': fields.String(required=True, description=''),
        'password': fields.String(required=True, description=''),
    })

api = ModelDto.api
parser = api.parser()
infer = ModelDto.infer

@api.route('/test')
class ModelInfer(Resource):
    @api.expect(infer, validate=False)
    def post(self):
        #여러개의 json을 받아오는 경우
        
        params = request.get_json()
        # print(params)
        category = ''
        text = []
        name_list = []
        for json in params:
            name = json['name']
            category = json['category']
            text.append(modeldata[name][1])
            name_list.append(name)

        model_path = category.split('_')[0]
        model_name = category + '_한국어_model'
        model = doc2vec.Doc2Vec.load('app/service/Model/{}/{}'.format(model_path, model_name))
        # 생성한 모델 로드
        infer_vec = infer_vector(text, model)
        similar_doc = model.dv.most_similar(positive=[infer_vec], topn=20)
        # 5개까지 추천해주도록 설정

        json_obj = []
        count = 0
        for doc_name, cosine in similar_doc:
            if doc_name in name_list: #기존에 사용자가 서재에 추가한 논문의 경우는 추천 논문 리스트에 포함시키지 않음
                continue;
            count+=1
            json = dict()
            json['name'] = doc_name
            json['abstract'] = modeldata[doc_name][1]
            json['author'] = modeldata[doc_name][2]
            json['year'] = modeldata[doc_name][3]
            json['link'] = modeldata[doc_name][4]
            json['category'] = modeldata[doc_name][5]
            json_obj.append(json)
            if count == 10:
                break

        return jsonify(json_obj)

@api.route('/post')
class GetPaper(Resource):
    @api.expect(infer, validate=True)
    def post(self):
        params = request.get_json()
        name = params['name']
        category = params['category']
        #json을 받아와서, 해당 논문의 이름과 분야를 받아온다

        model_path = category.split('_')[0]
        model_name = category + '_한국어_model'
        #print(model_name, model_path)
        model = doc2vec.Doc2Vec.load('app/service/Model/{}/{}'.format(model_path, model_name))
        #생성한 모델 로드

        similar_doc = model.dv.most_similar(name, topn=5)
        #5개까지 추천해주도록 설정

        json_obj = []
        for doc_name, cosine in similar_doc:
            json = dict()
            json['name'] = doc_name
            json['abstract'] = modeldata[doc_name][1]
            json['author'] = modeldata[doc_name][2]
            json['year'] = modeldata[doc_name][3]
            json['link'] = modeldata[doc_name][4]
            json['category'] = modeldata[doc_name][5]
            json_obj.append(json)
        return jsonify(json_obj)