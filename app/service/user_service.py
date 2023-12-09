import re
from flask import jsonify

from ..model.user import User
from ..model.user import Interest
from ..model.user import Paper
from app import db

# 회원가입한 회원 정보를 user모델(즉, user테이블에 넣기)
def save_new_user(data):
    # 맞는 email 형식인지 먼저 체크
    try:
        if checkmail(data['email']):
            user = User.query.filter_by(email=data['email']).first()
            # db에 중복되는 email 주소 없음.
            if user == None:
                new_user = User(
                    email=data['email'],
                    password=data['password'],
                )
                response_object = {
                    'status': 'success',
                    'message': '회원가입 되었습니다.'
                }
                db.session.add(new_user)
                db.session.commit()
                interests = data['interests'];
                for interest in interests:
                    new_interest = Interest(name=interest, user_id=new_user.id)
                    db.session.add(new_interest);
            
                db.session.commit()
                # db.session.close()
                return response_object, 201
            else:
                response_object = {
                    'status': 'fail',
                    'message': '이미 가입된 email 주소입니다.',
                }
                db.session.close()
                return response_object, 401
        else:
            response_object = {
                'status': 'fail',
                'message': '입력한 email 주소는 맞는 형식이 아닙니다.'
            }
            db.session.close()
            return response_object, 402
    except Exception as e:
        response_object = {
            'status': 'error',
            'message': str(e)
        }
        return response_object, 500
    finally:
        db.session.close()

def save_changes(data):
    try:
        db.session.add(data)
        db.session.commit()
    except Exception as e:
        response_object = {
            'status': 'error',
            'message': str(e)
        }
        return response_object, 500
    finally:
        db.session.close()

def get_user(email):
    try:
        user = User.query.filter_by(email=email).first()
        if user:
            interests = [interest.to_dict() for interest in user.interests]
            papers = [paper.to_dict() for paper in user.papers]
            response_object = {
                'status': 'success',
                'message': '회원 조회에 성공했습니다.',
                'data': {
                    'id': user.id,
                    'email' : user.email,
                    'category' : interests,
                    'library' : papers,
                }
            }
            db.session.close()
            return response_object, 201
        else:
            response_object = {
                'status': 'fail',
                'message': '해당 회원이 없습니다.',
                'data': {},
            }
            db.session.close()
            return response_object, 401
    except Exception as e:
        response_object = {
            'status': 'error',
            'message': str(e)
        }
        return response_object, 500
    finally:
        db.session.close()

def add_user_paper(data):
    try:
        user = User.query.filter_by(id=data['user_id']).first()
        # db에 중복되는 email 주소 없음.
        if user != None:
            paper = Paper.query.filter_by(title=data['title'])
            ids = [p.user_id for p in paper]
            if paper.count == 0 or user.id not in ids:
                new_paper = Paper(
                    abstract=data['abstract'],
                    author=data['author'],
                    category=data['category'],
                    link=data['link'],
                    title=data['title'],
                    year=data['year'],
                    user_id=data['user_id']
                )
                
                interests = [interest.to_dict() for interest in user.interests]
                user.papers.append(new_paper)
                papers = [paper.to_dict() for paper in user.papers]
                response_object = {
                    'status': 'success',
                    'message': 'library에 paper를 추가하였습니다.',
                    'data': {
                        'id': user.id,
                        'email' : user.email,
                        'category' : interests,
                        'library' : papers,
                    }
                }
                db.session.commit()
                # db.session.close()
                return response_object, 201
            else:
                response_object = {
                    'status': 'fail',
                    'message': '이미 저장된 논문입니다.',
                    'data': {},
                }
                db.session.close()
                return response_object, 401
        else:
            response_object = {
                'status': 'fail',
                'message': '해당 회원이 없습니다.',
                'data': {},
            }
            db.session.close()
            return response_object, 401
    except Exception as e:
        response_object = {
            'status': 'error',
            'message': str(e)
        }
        return response_object, 500
    finally:
        db.session.close()

def add_user_interest(data):
    try:
        user = User.query.filter_by(id=data['user_id']).first()
        # db에 중복되는 email 주소 없음.
        if user != None:
            interest = Interest.query.filter_by(name=data['category'])
            ids = [i.user_id for i in interest]
            if interest.count == 0 or user.id not in ids:
                new_interest = Interest(
                    name=data['category'],
                    user_id=data['user_id']
                )
                
                user.interests.append(new_interest)
                db.session.commit()
                interests = [interest.to_dict() for interest in user.interests]
                papers = [paper.to_dict() for paper in user.papers]
                response_object = {
                    'status': 'success',
                    'message': 'library에 paper를 추가하였습니다.',
                    'data': {
                        'id': user.id,
                        'email' : user.email,
                        'category' : interests,
                        'library' : papers,
                    }
                }
                # db.session.close()
                return response_object, 201
            else:
                response_object = {
                    'status': 'fail',
                    'message': '이미 저장된 논문입니다.',
                    'data': {},
                }
                db.session.close()
                return response_object, 401
        else:
            response_object = {
                'status': 'fail',
                'message': '해당 회원이 없습니다.',
                'data': {},
            }
            db.session.close()
            return response_object, 401
    except Exception as e:
        response_object = {
            'status': 'error',
            'message': str(e)
        }
        return response_object, 500
    finally:
        db.session.close()

def delete_user_paper(data):
    try:
        user = User.query.filter_by(id=data['user_id']).first()
        if user != None:
            # paper_to_remove = Paper.query.filter_by(title=data['title']).first()
            paper_to_remove = [paper for paper in user.papers if paper.title == data['title']][0]
            if paper_to_remove:
                # user.papers.remove(paper_to_remove)
                print(paper_to_remove)
                interests = [interest.to_dict() for interest in user.interests]
                papers = [paper.to_dict() for paper in user.papers if paper.title != data['title']]
                response_object = {
                    'status': 'success',
                    'message': 'library에 paper를 삭제하였습니다.',
                    'data': {
                        'id': user.id,
                        'email' : user.email,
                        'category' : interests,
                        'library' : papers,
                    }
                }
                db.session.delete(paper_to_remove)
                db.session.commit()
                db.session.close()
                return response_object, 201
            else :
                interests = [interest.to_dict() for interest in user.interests]
                papers = [paper.to_dict() for paper in user.papers]
                response_object = {
                    'status': 'success',
                    'message': 'library에 paper가 없습니다.',
                    'data': {
                        'id': user.id,
                        'email' : user.email,
                        'category' : interests,
                        'library' : papers,
                    }
                }
                return response_object, 201
        else:
            response_object = {
                'status': 'fail',
                'message': '해당 회원이 없습니다.',
                'data': {},
            }
            db.session.close()
            return response_object, 401
    except Exception as e:
        response_object = {
            'status': 'error',
            'message': str(e)
        }
        return response_object, 500
    finally:
        db.session.close()

def delete_user_interest(data):
    try:
        user = User.query.filter_by(id=data['user_id']).first()
        if user != None:
            print(data)
            interest_to_remove = Interest.query.filter_by(name=data['category']).first()
            if interest_to_remove:
                interests = [interest.to_dict() for interest in user.interests if interest.name != data['category']]
                papers = [paper.to_dict() for paper in user.papers]
                response_object = {
                    'status': 'success',
                    'message': 'interest를 삭제하였습니다.',
                    'data': {
                        'id': user.id,
                        'email' : user.email,
                        'category' : interests,
                        'library' : papers,
                    }
                }
                db.session.delete(interest_to_remove)
                db.session.commit()
                db.session.close()
                return response_object, 201
            else:
                interests = [interest.to_dict() for interest in user.interests]
                papers = [paper.to_dict() for paper in user.papers]
                response_object = {
                    'status': 'success',
                    'message': 'interest가 없습니다.',
                    'data': {
                        'id': user.id,
                        'email' : user.email,
                        'category' : interests,
                        'library' : papers,
                    }
                }
                return response_object, 201
        else:
            response_object = {
                'status': 'fail',
                'message': '해당 회원이 없습니다.',
                'data': {},
            }
            db.session.close()
            return response_object, 401
    except Exception as e:
        response_object = {
            'status': 'error',
            'message': str(e)
        }
        return response_object, 500
    finally:
        db.session.close()


# email 형식 체크
def checkmail(email):
    p = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
    result = p.match(email) != None
    
    #True, False로 return
    return result