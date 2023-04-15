from datetime import datetime
import json
import os
import time
from bson import ObjectId, json_util
from chalice import Chalice, Response, Cron
from chalicelib.database import Database
from chalicelib.utils import criar_notificacao, usuario_valido, enviar_para_fila, adicionar_horas
from chalicelib.email import enviar_email

app = Chalice(app_name='meuremedioapi')

time.tzset()


def success_response(data=None, status_code=200, headers=None):
    if not data:
        data = {'message': 'SUCCESS!'}
    return Response(
        body=json.loads(json_util.dumps(data)),
        status_code=status_code,
        headers=headers
    )


def bad_response(data=None, status_code=400, headers=None):
    if not data:
        data = {'error': 'NONE_RETURNED', 'status_code': 400}
    return Response(
        body=json.loads(json_util.dumps(data)),
        status_code=status_code,
        headers=headers
    )


@app.route('/', methods=['GET'], content_types=['application/json'])
def home():
    request = app.current_request
    _db = Database()
    params, query = request.query_params, {}
    try:
        if params:
            query = {'email': params['email']}
    except KeyError:
        return bad_response(data={'error': 'Usuário não indentificado.'}, status_code=404)
    data = _db.get_user(query)
    if data:
        return success_response(data=data)
    return bad_response(data={'error': 'Usuário não indentificado.'}, status_code=404)


@app.route('/criar-usuario', methods=['POST'], content_types=['application/json'])
def criar_usuario():
    request = app.current_request
    _db = Database()
    body = request.json_body
    if usuario_valido(body):
        data = {'_id': _db.create_user(body).inserted_id}
        return success_response(data=data)
    return bad_response(data={'error': 'Usuário inválido.'}, status_code=400)


@app.route('/criar-notificacao', methods=['POST'], content_types=['application/json'])
def gerar_notificacao():
    request = app.current_request
    _db = Database()
    body = request.json_body
    try:
        notificacao = criar_notificacao(body)
        data = {'_id': _db.create_notification(notificacao).inserted_id}
        return success_response(data=data)
    except KeyError:
        return bad_response(data={'error': 'Dados inválido.'}, status_code=400)


@app.route('/criar-notificacoes', methods=['POST'], content_types=['application/json'])
def criar_notificacoes():
    request = app.current_request
    _db = Database()
    body = request.json_body
    try:
        notificacoes = list(map(criar_notificacao, body))
        data = {'_ids': _db.create_notification(notificacoes, many=True).inserted_ids}
        return success_response(data=data)
    except KeyError:
        return bad_response(data={'error': 'Dados inválido.'}, status_code=400)


@app.route('/deletar-notificacao/{_id}', methods=['DELETE'], content_types=['application/json'])
def deletar_notificacao(_id):
    _db = Database()
    if isinstance(_id, ObjectId):
        _db.delete_notification(_id)
    else:
        _db.delete_notification(ObjectId(_id))
    return success_response(data={'message': 'SUCCESS!'})


@app.schedule(Cron(30, '*', '*', '*', '?', '*'))
def validar_notificacao(_):
    _db = Database()
    hora = datetime.now().strftime('%H')
    notificacoes = _db.get_notificacoes_agora(hora)
    for notificacao in notificacoes:
        for user in notificacao['users']:
            enviar_para_fila({**user, 'remedio': notificacao['nome']})
        proximo = adicionar_horas(notificacao['proximo'], notificacao['qtd_horas'])
        _db.update_notification(notificacao['_id'], proximo)


@app.on_sqs_message(queue=os.getenv("SQS_SEND_EMAIL"))
def fila_de_email(event): 
    for record in event:
        user = json.loads(record.body)
        enviar_email(user['email'], user['nome'], user['remedio'])
