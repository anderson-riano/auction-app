import boto3
import smtplib
import json
from decimal import Decimal
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

dynamodb = boto3.resource('dynamodb')

items_table = dynamodb.Table("AuctionAppStack-ItemsTable5AAC2C46-SBSP6TXX75G1")
bids_table = dynamodb.Table("AuctionAppStack-BidsTableE1AD1632-14HE7UVGQNPYW")

SENDER_EMAIL = "anderson24sep@gmail.com"
GMAIL_APP_PASSWORD = "wgic yqvc hojo mfup" 

def send_email(to_email, subject, body):
    """ Función para enviar un correo usando Gmail SMTP """
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, GMAIL_APP_PASSWORD)
            server.sendmail(SENDER_EMAIL, to_email, msg.as_string())
        print(f"Correo enviado a {to_email}")
    except Exception as e:
        print(f"Error al enviar correo a {to_email}: {e}")

def lambda_handler(event, context):    

    response = items_table.scan(
        FilterExpression="#status = :status_value",
        ExpressionAttributeNames={"#status": "status"},
        ExpressionAttributeValues={":status_value": "active"}
    )

    
    for item in response.get("Items", []):
        if item["expires_at"] <= str(event.get("current_time", "")): 
        
            bids = bids_table.scan(
                FilterExpression="item_id = :item_id",
                ExpressionAttributeValues={":item_id": item["id"]}
            )["Items"]
            
            if not bids:
            
                items_table.update_item(
                    Key={"id": item["id"]},
                    UpdateExpression="SET #status = :status",
                    ExpressionAttributeNames={"#status": "status"},
                    ExpressionAttributeValues={":status": "closed"}
                )
                continue

            bids.sort(key=lambda x: Decimal(x["amount"]), reverse=True)
            winner = bids[0] 
            losers = bids[1:] 
            
            winner_subject = "¡Felicidades! Ganaste la subasta"
            winner_body = f"""
            Hola {winner['user_email']},
            ¡Felicidades! Has ganado la subasta de {item['name']} con una oferta de {winner['amount']}.
            Pronto nos pondremos en contacto contigo.
            """
            send_email(winner["user_email"], winner_subject, winner_body)

            for loser in losers:
                loser_subject = "Subasta finalizada"
                loser_body = f"""
                Hola {loser['user_email']},
                La subasta de {item['name']} ha finalizado. Lamentablemente, no ganaste esta vez.
                ¡Sigue participando en futuras subastas!
                """
                send_email(loser["user_email"], loser_subject, loser_body)

            items_table.update_item(
                Key={"id": item["id"]},
                UpdateExpression="SET #status = :status",
                ExpressionAttributeNames={"#status": "status"},
                ExpressionAttributeValues={":status": "closed"}
            )


    return {"status": "ok"}
