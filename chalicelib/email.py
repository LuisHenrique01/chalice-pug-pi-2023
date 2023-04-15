import boto3


def enviar_email(email: str, nome: str, remedio: str) -> None:
    SENDER = f'Contato API<monitoringamazon@gmail.comclea>'
    CHARSET = "UTF-8"
    client = boto3.client('ses')

    _ = client.send_email(
        Destination={
            "ToAddresses": [
                email,
            ],
        },
        Message={
            "Body": {
                "Text": {
                    "Charset": CHARSET,
                    "Data": f"Olá {nome}! Hora de tomar o {remedio}",
                }
            },
            "Subject": {
                "Charset": CHARSET,
                "Data": f"Tomar o {remedio}",
            },
        },
        Source=SENDER,
    )