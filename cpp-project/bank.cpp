#include <iostream>
#include <string>
using namespace std;

class BankAccount {
private:
    string accountHolder;
    string accountType;   // "Savings" or "Current"
    double balance;
    double loanAmount;

public:
    BankAccount(string name, string type, double initialBalance) {
        accountHolder = name;
        accountType = type;
        balance = initialBalance;
        loanAmount = 0;
    }

    bool deposit(double amount) {
        if (amount <= 0) {
            return false;
        }
        balance += amount;
        return true;
    }

    bool withdraw(double amount) {
        if (amount <= 0) {
            return false;
        }

        // Savings account must maintain minimum balance of 1000
        if (accountType == "Savings") {
            if (balance - amount < 1000) {
                return false;
            }
        }

        if (amount > balance) {
            return false;
        }

        balance -= amount;

        // Current account has transaction fee of 10
        if (accountType == "Current") {
            balance -= 10;
        }

        return true;
    }

    void applyInterest() {
        if (accountType == "Savings") {
            balance += balance * 0.04;  // 4% interest
        }
    }

    bool takeLoan(double amount) {
        if (amount <= 0) {
            return false;
        }

        // Loan limit = 2x current balance
        if (amount > balance * 2) {
            return false;
        }

        loanAmount += amount;
        balance += amount;
        return true;
    }

    double getBalance() const {
        return balance;
    }

    double getLoanAmount() const {
        return loanAmount;
    }

    string getAccountType() const {
        return accountType;
    }
};
