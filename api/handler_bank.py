# bank_handlers.py

from decimal import Decimal
import random
import string

import psycopg2
from .config.db import get_db_cursor

def generate_account_number():
    """Génère un numéro de compte aléatoire"""
    return ''.join(random.choices(string.digits, k=10))

def create_bank_account(self, user_id):
    """Créer un nouveau compte bancaire"""
    try:
        with get_db_cursor() as cur:
            account_number = generate_account_number()
            cur.execute("""
                INSERT INTO bank_accounts (user_id, account_number)
                VALUES (%s, %s)
                RETURNING id, account_number, balance
            """, (user_id, account_number))
            
            account = cur.fetchone()
            return {
                "id": account['id'],
                "account_number": account['account_number'],
                "balance": float(account['balance'])
            }
    except psycopg2.Error as e:
        raise Exception(f"Database error: {str(e)}")

#@require_auth
def handle_get_balance(self):
    """Consultation du solde"""
    try:
        with get_db_cursor() as cur:
            cur.execute("""
                SELECT id, account_number, balance 
                FROM bank_accounts 
                WHERE user_id = %s
            """, (self.user['user_id'],))
            
            if cur.rowcount == 0:
                # Créer un compte si l'utilisateur n'en a pas
                account = create_bank_account(self, self.user['user_id'])
            else:
                account = cur.fetchone()
                account = {
                    "id": account['id'],
                    "account_number": account['account_number'],
                    "balance": float(account['balance'])
                }
            
            self._send_json_response(200, {"account": account})
            
    except Exception as e:
        self._send_json_response(500, {"error": str(e)})

#@require_auth
def handle_deposit(self, data):
    """Dépôt d'argent"""
    amount = Decimal(str(data.get('amount', 0)))
    
    if amount <= 0:
        self._send_json_response(400, {"error": "Amount must be positive"})
        return

    try:
        with get_db_cursor() as cur:
            # Mettre à jour le solde
            cur.execute("""
                UPDATE bank_accounts 
                SET balance = balance + %s 
                WHERE user_id = %s
                RETURNING id, balance
            """, (amount, self.user['user_id']))
            
            if cur.rowcount == 0:
                self._send_json_response(404, {"error": "Account not found"})
                return
                
            account = cur.fetchone()
            
            # Enregistrer la transaction
            cur.execute("""
                INSERT INTO transactions 
                (from_account_id, to_account_id, amount, transaction_type)
                VALUES (%s, %s, %s, 'DEPOSIT')
            """, (None, account['id'], amount))
            
            self._send_json_response(200, {
                "message": "Deposit successful",
                "new_balance": float(account['balance'])
            })
            
    except Exception as e:
        self._send_json_response(500, {"error": str(e)})

#@require_auth
def handle_withdrawal(self, data):
    """Retrait d'argent"""
    amount = Decimal(str(data.get('amount', 0)))
    
    if amount <= 0:
        self._send_json_response(400, {"error": "Amount must be positive"})
        return

    try:
        with get_db_cursor() as cur:
            # Vérifier le solde
            cur.execute("""
                SELECT id, balance 
                FROM bank_accounts 
                WHERE user_id = %s
                FOR UPDATE
            """, (self.user['user_id'],))
            
            account = cur.fetchone()
            if not account:
                self._send_json_response(404, {"error": "Account not found"})
                return
                
            if account['balance'] < amount:
                self._send_json_response(400, {"error": "Insufficient funds"})
                return
            
            # Effectuer le retrait
            cur.execute("""
                UPDATE bank_accounts 
                SET balance = balance - %s 
                WHERE id = %s
                RETURNING balance
            """, (amount, account['id']))
            
            new_balance = cur.fetchone()['balance']
            
            # Enregistrer la transaction
            cur.execute("""
                INSERT INTO transactions 
                (from_account_id, to_account_id, amount, transaction_type)
                VALUES (%s, %s, %s, 'WITHDRAWAL')
            """, (account['id'], None, amount))
            
            self._send_json_response(200, {
                "message": "Withdrawal successful",
                "new_balance": float(new_balance)
            })
            
    except Exception as e:
        self._send_json_response(500, {"error": str(e)})

#@require_auth
def handle_transfer(self, data):
    """Transfert d'argent"""
    amount = Decimal(str(data.get('amount', 0)))
    to_account_number = data.get('to_account_number')
    
    if amount <= 0:
        self._send_json_response(400, {"error": "Amount must be positive"})
        return
        
    if not to_account_number:
        self._send_json_response(400, {"error": "Recipient account number required"})
        return

    try:
        with get_db_cursor() as cur:
            # Vérifier le compte source
            cur.execute("""
                SELECT id, balance 
                FROM bank_accounts 
                WHERE user_id = %s
                FOR UPDATE
            """, (self.user['user_id'],))
            
            from_account = cur.fetchone()
            if not from_account:
                self._send_json_response(404, {"error": "Your account not found"})
                return
                
            if from_account['balance'] < amount:
                self._send_json_response(400, {"error": "Insufficient funds"})
                return
            
            # Vérifier le compte destinataire
            cur.execute("""
                SELECT id 
                FROM bank_accounts 
                WHERE account_number = %s
                FOR UPDATE
            """, (to_account_number,))
            
            to_account = cur.fetchone()
            if not to_account:
                self._send_json_response(404, {"error": "Recipient account not found"})
                return
            
            # Effectuer le transfert
            # Débiter le compte source
            cur.execute("""
                UPDATE bank_accounts 
                SET balance = balance - %s 
                WHERE id = %s
            """, (amount, from_account['id']))
            
            # Créditer le compte destinataire
            cur.execute("""
                UPDATE bank_accounts 
                SET balance = balance + %s 
                WHERE id = %s
            """, (amount, to_account['id']))
            
            # Enregistrer la transaction
            cur.execute("""
                INSERT INTO transactions 
                (from_account_id, to_account_id, amount, transaction_type)
                VALUES (%s, %s, %s, 'TRANSFER')
            """, (from_account['id'], to_account['id'], amount))
            
            self._send_json_response(200, {
                "message": "Transfer successful",
                "transaction_id": cur.fetchone()['id']
            })
            
    except Exception as e:
        self._send_json_response(500, {"error": str(e)})