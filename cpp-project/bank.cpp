// bank.cpp
#include <iostream>
#include <string>
using namespace std;

class BankAccount {
private:
    double balance;
    string owner;

public:
    BankAccount(string owner, double initialBalance);
    void deposit(double amount);
    bool withdraw(double amount);
    double getBalance() const;
    string getOwner() const;
};

// ALL function BODIES must be here, OUTSIDE the class
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
