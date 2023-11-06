import logging

logging.basicConfig(level=logging.INFO, format= '%(levelname)s:%(message)s')

def value_check(func):
    def value_is_not_negative(self,value):
        if value<0:
            logging.error("value can't be negative")
            global is_sucess
            is_sucess = False
            return
        func(self,value)
    return value_is_not_negative

def enough_money(func):
    def enough_money_check(self,value):
        if value>self.stored_value:
            logging.error("There is not enough money in your account to withdraw {}$".format(value))
            global is_sucess
            is_sucess = False
            return
        func(self,value)
    return enough_money_check    
            
class ClientAccount:
    def __init__(self,name_of_client,bank_name,password):
        self.client_name=name_of_client
        self.bank_name=bank_name
        self.stored_value=0
        self.password=password

    def login(self,password):
        if password == self.password:
            logging.info("Log in Sucessful")
            return self
        else:
            logging.error("Incorrect password")
            return
        
    @value_check
    def input_money(self,value):
        self.stored_value+=value

    @value_check
    @enough_money
    def withdraw_money(self,value):
        self.stored_value-=value
        global is_sucess
        is_sucess = True

    def print_amount_of_money_on_account(self):
        logging.info("there is {}$ on your account".format(self.stored_value))

    def transfer_money(self,name_of_bank_of_account_getting_money,name_of_client_getting_money,value,list_of_banks=[]):
        make_transation(self.bank_name,self.client_name,name_of_bank_of_account_getting_money,name_of_client_getting_money,value,list_of_banks)    


class Bank:
    def __init__(self,name_of_bank):
        self.bank_name=name_of_bank
        self.list_of_accounts=[]

    def create_account(self,name_of_client,password):
        self.list_of_accounts.append(ClientAccount(name_of_client,self.bank_name,password))

    def delete_account(self,name_of_client):
        for account in self.list_of_accounts:
                if account.client_name==name_of_client:
                    self.list_of_accounts.remove(account)
                    logging.info("account sucessfully deleted")    

    def login_to_account(self,name_of_client,password):
         for account in self.list_of_accounts:
                if account.client_name==name_of_client:
                    return account.login(password)

    def delete_bank(self,list_of_banks=[]):
        self.list_of_accounts.clear
        list_of_banks.remove(self)                   
        logging.info("Bank sucessfully deleted")
        return
    
    def merge_bank(self,name_of_bank_to_merge_with,list_of_banks=[]):
        for bank in list_of_banks:
            if bank.bank_name == name_of_bank_to_merge_with:
                for account in self.list_of_accounts:
                    account.bank_name = name_of_bank_to_merge_with
                    bank.list_of_accounts.append(account)
                logging.info("Banks sucessfully Merged")
                self.delete_bank(list_of_banks)

    @staticmethod
    def how_many_banks_exist(list_of_banks=[]):
        logging.info("There are {} banks in system".format(len(list_of_banks)))                

def make_transation(name_of_bank_of_account_sending_money,name_of_client_sending_money,name_of_bank_of_account_getting_money,name_of_client_getting_money,value,list_of_banks=[]):
    for bank in list_of_banks:
        if bank.bank_name == name_of_bank_of_account_sending_money:
            for account in bank.list_of_accounts:
                if account.client_name==name_of_client_sending_money:
                    account.withdraw_money(value)
                    global is_sucess
                    if not is_sucess:
                       logging.error("Transaction Failure")
                       return
    for bank in list_of_banks:
        if bank.bank_name == name_of_bank_of_account_getting_money:
            for account in bank.list_of_accounts:
                if account.client_name==name_of_client_getting_money:
                    account.input_money(value)        

def create_bank(bank_name,list_of_banks=[]):
    list_of_banks.append(Bank(bank_name))
 
if __name__ == "__main__":
    is_sucess = True
    list_of_banks=[]
    create_bank("First Bank",list_of_banks)
    create_bank("Second Bank",list_of_banks)
    bank = list_of_banks[0]
    bank.create_account("John","123")
    bank.create_account("Mary","222")
    bank.create_account("Sam","2a2")
    account = bank.login_to_account("John","123")
    account.input_money(-10)
    account.print_amount_of_money_on_account()
    account.input_money(100)
    account.print_amount_of_money_on_account()
    account.withdraw_money(200)
    account.print_amount_of_money_on_account()
    account.withdraw_money(50)
    account.print_amount_of_money_on_account()
    account.transfer_money("First Bank","Mary",50,list_of_banks)
    account.print_amount_of_money_on_account()
    account.transfer_money("First Bank","Sam",50,list_of_banks)
    account.transfer_money("First Bank","Mary",50,list_of_banks)
    account.print_amount_of_money_on_account()
    account = bank.login_to_account("Mary","123")
    account = bank.login_to_account("Mary","222")
    account.print_amount_of_money_on_account()
    bank.delete_account("Sam")
    bank = list_of_banks[1]
    bank.delete_bank(list_of_banks)
    bank = list_of_banks[0]
    create_bank("New Bank",list_of_banks)
    bank.how_many_banks_exist(list_of_banks)
    bank.merge_bank("New Bank",list_of_banks)
    bank = list_of_banks[0]
    bank.how_many_banks_exist(list_of_banks)
