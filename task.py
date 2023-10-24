class ClientAccount:
    def __init__(self,name_of_client):
        self.client_name=name_of_client
        self.stored_value=0    

    def input_money(self,value):
        self.stored_value+=value

    def withdraw_money(self,value):
        if value>self.stored_value:
            print("There is not enough money in your account to withdraw {}$".format(value))
            return
        self.stored_value-=value

    def print_amount_of_money_on_account(self):
        print("there is {}$ on your account".format(self.stored_value))    


class Bank:
    def __init__(self,name_of_bank):
        self.bank_name=name_of_bank
        self.list_of_accounts=[]

    def create_account(self,name_of_client):
        self.list_of_accounts.append(ClientAccount(name_of_client))    

def make_transation(name_of_bank_of_account_sending_money,name_of_client_sending_money,name_of_bank_of_account_getting_money,name_of_client_getting_money,value):
    for account in name_of_bank_of_account_sending_money.list_of_accounts:
        if account.client_name==name_of_bank_of_account_sending_money:
            account.withdraw_money(value)
    for account in name_of_bank_of_account_getting_money.list_of_accounts:
        if account.client_name==name_of_bank_of_account_getting_money:
            account.input_money(value)        

if __name__ == "__main__":
    BigBank=Bank("BigBank")
    BigBank.create_account("John")
