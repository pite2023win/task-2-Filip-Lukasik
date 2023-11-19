import unittest
import task
import logging


class TestBankandAccounts(unittest.TestCase):
    def setUp(self):
        self.bank_1 = task.Bank("Test Bank")
        logging.disable(logging.CRITICAL)
    
    def test_create_accouunt(self):
        self.bank_1.create_account("John","123")
        self.assertEqual(self.bank_1.list_of_accounts[0].client_name,"John")
        self.assertEqual(self.bank_1.list_of_accounts[0].bank_name,"Test Bank")
        self.assertEqual(self.bank_1.list_of_accounts[0].password,"123")
        self.assertEqual(len(self.bank_1.list_of_accounts),1)

    def test_delete_account(self):
        account = task.ClientAccount("John","Test Bank","123")
        self.bank_1.list_of_accounts.append(account)
        self.bank_1.delete_account("")
        self.assertEqual(len(self.bank_1.list_of_accounts),1)
        self.bank_1.delete_account("John")
        self.assertEqual(len(self.bank_1.list_of_accounts),0)
        self.bank_1.delete_account("John")
        self.assertEqual(len(self.bank_1.list_of_accounts),0)

    def test_login_to_account(self):
        account = task.ClientAccount("John","Test Bank","123")
        self.bank_1.list_of_accounts.append(account)
        account=self.bank_1.login_to_account("John","122")
        self.assertEqual(type(account), type(None))
        account=self.bank_1.login_to_account("john","123")
        self.assertEqual(type(account), type(None))
        account=self.bank_1.login_to_account("John","123")
        self.assertEqual(account.client_name,"John")
        self.assertEqual(account.bank_name,"Test Bank")
        self.assertEqual(account.password,"123")

    def test_delete_bank(self):
        list_of_banks=[]
        list_of_banks.append(self.bank_1)
        account = task.ClientAccount("John","Test Bank","123")
        self.bank_1.list_of_accounts.append(account)
        self.bank_1.delete_bank(list_of_banks)
        self.assertEqual(len(list_of_banks),0)

    def test_merge_banks(self):
        list_of_banks=[]
        list_of_banks.append(self.bank_1)
        account = task.ClientAccount("John","Test Bank","123")
        self.bank_1.list_of_accounts.append(account)
        bank_2=task.Bank("Merge Bank")
        list_of_banks.append(bank_2)
        account = task.ClientAccount("Mary","Merge Bank","120")
        bank_2.list_of_accounts.append(account)
        self.bank_1.merge_bank("Merge Bank",list_of_banks)
        self.assertEqual(len(list_of_banks),1)
        self.assertEqual(len(bank_2.list_of_accounts),2)
        self.assertEqual(bank_2.list_of_accounts[1].client_name,"John")
        self.assertEqual(bank_2.list_of_accounts[1].bank_name,"Merge Bank")
        self.assertEqual(bank_2.list_of_accounts[1].password,"123")

    def test_create_bank(self):
        list_of_banks=[]
        task.create_bank("New Bank",list_of_banks)
        self.assertEqual(len(list_of_banks),1)
        task.create_bank("New2 Bank")
        self.assertEqual(len(list_of_banks),1)
    
    def test_print_amount_of_money(self):
        account = task.ClientAccount("John","Test Bank","123")
        with self.assertLogs(account.print_amount_of_money_on_account(), level='INFO') as cm:
            logging.disable(logging.NOTSET)
            logging.getLogger(account.print_amount_of_money_on_account())
            self.assertEqual(cm.output, ['INFO:root:there is 0$ on your account'])
        logging.disable(logging.CRITICAL)    
        account.stored_value = 100
        with self.assertLogs(account.print_amount_of_money_on_account(), level='INFO') as cm:
            logging.disable(logging.NOTSET)
            logging.getLogger(account.print_amount_of_money_on_account())
            self.assertEqual(cm.output, ['INFO:root:there is 100$ on your account'])

    def test_input_money(self):
        account = task.ClientAccount("John","Test Bank","123")
        account.input_money(100)
        self.assertEqual(account.stored_value,100)
        account.input_money(100)
        self.assertEqual(account.stored_value,200)
        account.input_money(0)
        self.assertEqual(account.stored_value,200)
        account.input_money(-100)
        self.assertEqual(account.stored_value,200)
        with self.assertLogs(account.input_money(-100), level='INFO') as cm:
            logging.disable(logging.NOTSET)
            logging.getLogger(account.input_money(-100))
            self.assertEqual(cm.output, ["ERROR:root:value can't be negative"])

    def test_withdraw_money(self):
        account = task.ClientAccount("John","Test Bank","123")
        account.stored_value=500
        account.withdraw_money(100)
        self.assertEqual(account.stored_value,400)
        account.withdraw_money(200)
        self.assertEqual(account.stored_value,200)
        account.withdraw_money(0)
        self.assertEqual(account.stored_value,200)
        account.withdraw_money(-100)
        self.assertEqual(account.stored_value,200)
        with self.assertLogs(account.withdraw_money(-100), level='INFO') as cm:
            logging.disable(logging.NOTSET)
            logging.getLogger(account.withdraw_money(-100))
            self.assertEqual(cm.output, ["ERROR:root:value can't be negative"])
        logging.disable(logging.CRITICAL)
        account.withdraw_money(300)
        self.assertEqual(account.stored_value,200)
        with self.assertLogs(account.withdraw_money(300), level='INFO') as cm:
            logging.disable(logging.NOTSET)
            logging.getLogger(account.withdraw_money(300))
            self.assertEqual(cm.output, ["ERROR:root:There is not enough money in your account to withdraw 300$"])

    def test_transaction(self):
        list_of_banks=[]
        list_of_banks.append(self.bank_1)
        account = task.ClientAccount("John","Test Bank","123")
        self.bank_1.list_of_accounts.append(account)
        bank_2=task.Bank("Second Bank")
        list_of_banks.append(bank_2)
        account = task.ClientAccount("Mary","Second Bank","120")
        bank_2.list_of_accounts.append(account)
        account = task.ClientAccount("Elon","Test Bank","999")
        self.bank_1.list_of_accounts.append(account)
        account.stored_value=1000
        account.transfer_money("Test Bank","John",100,list_of_banks)
        self.assertEqual(account.stored_value,900)
        self.assertEqual(self.bank_1.list_of_accounts[0].stored_value,100)
        account.transfer_money("Second Bank","Mary",100,list_of_banks)
        self.assertEqual(account.stored_value,800)
        self.assertEqual(bank_2.list_of_accounts[0].stored_value,100)
        account.transfer_money("Test Bank","John",1000,list_of_banks)
        self.assertEqual(account.stored_value,800)
        self.assertEqual(self.bank_1.list_of_accounts[0].stored_value,100)
        with self.assertLogs(account.transfer_money("Test Bank","John",1000,list_of_banks), level='INFO') as cm:
            logging.disable(logging.NOTSET)
            logging.getLogger(account.transfer_money("Test Bank","John",1000,list_of_banks))
            self.assertEqual(cm.output, ["ERROR:root:There is not enough money in your account to withdraw 1000$","ERROR:root:Transaction Failure"])
        logging.disable(logging.CRITICAL)
        with self.assertLogs(account.transfer_money("Test Bank","John",-100,list_of_banks), level='INFO') as cm:
            logging.disable(logging.NOTSET)
            logging.getLogger(account.transfer_money("Test Bank","John",-100,list_of_banks))
            self.assertEqual(cm.output, ["ERROR:root:value can't be negative","ERROR:root:Transaction Failure"])

if __name__ == '__main__':
    unittest.main()        
        
