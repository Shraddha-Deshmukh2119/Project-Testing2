// test_bank.cpp
#include <iostream>
#include <cassert>
#include "bank.cpp"   // or separate header — see note below
using namespace std;

void testDeposit() {
    BankAccount acc("Alice", 1000.0);
    acc.deposit(500.0);
    assert(acc.getBalance() == 1500.0);
    cout << "testDeposit passed" << endl;
}

void testWithdrawSuccess() {
    BankAccount acc("Bob", 1000.0);
    bool result = acc.withdraw(400.0);
    assert(result == true);
    assert(acc.getBalance() == 600.0);
    cout << "testWithdrawSuccess passed" << endl;
}

void testWithdrawFailure() {
    BankAccount acc("Charlie", 200.0);
    bool result = acc.withdraw(500.0);
    assert(result == false);
    assert(acc.getBalance() == 200.0);
    cout << "testWithdrawFailure passed" << endl;
}

void testInitialBalance() {
    BankAccount acc("Dave", 750.0);
    assert(acc.getBalance() == 750.0);
    cout << "testInitialBalance passed" << endl;
}

int main() {
    testDeposit();
    testWithdrawSuccess();
    testWithdrawFailure();
    testInitialBalance();
    cout << "All test cases passed successfully!" << endl;
    return 0;
}
