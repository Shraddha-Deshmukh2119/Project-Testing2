#ifndef BANK_H
#define BANK_H

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

#endif
