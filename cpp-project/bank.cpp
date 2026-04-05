#include "bank.h"

BankAccount::BankAccount(string owner, double initialBalance) {
    this->owner = owner;
    this->balance = initialBalance;
}

void BankAccount::deposit(double amount) {
    if (amount > 0) {
        balance += amount;
    }
}

bool BankAccount::withdraw(double amount) {
    if (amount > 0 && amount <= balance) {
        balance -= amount;
        return true;
    }
    return false;
}

double BankAccount::getBalance() const {
    return balance;
}

string BankAccount::getOwner() const {
    return owner;
}
