import json
import os
from bson import ObjectId, json_util
from datetime import datetime, timedelta
import boto3


def open_sqs_connection():
    return boto3.client("sqs")


def adicionar_horas(horario: str, horas: int):
    horario_datetime = datetime.strptime(horario, '%H')
    novo_horario = horario_datetime + timedelta(hours=horas)
    novo_horario_str = novo_horario.strftime('%H')
    return novo_horario_str


def usuario_valido(user: dict):
    if ('nome', 'email', 'telefone') == tuple(user.keys()):
        return True
    return False


def criar_notificacao(data: dict):
    inicio = data['inicio']
    horario = data['qtd_horas']
    proximo = adicionar_horas(inicio, horario)
    return {'proximo': proximo, 'qtd_horas': data['qtd_horas'], "nome": data["nome"], 'usuario': ObjectId(data['usuario'])}


def enviar_para_fila(data: dict, client=open_sqs_connection()):
    queue_url = client.get_queue_url(QueueName=os.getenv("")).get('QueueUrl')
    _ = client.send_message(QueueUrl=queue_url, MessageBody=json.dumps(data, default=json_util.default))
