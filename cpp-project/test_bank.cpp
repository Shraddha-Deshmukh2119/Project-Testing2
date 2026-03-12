#include <iostream>
#include <cassert>

// Include the implementation file directly (since no .h file)
#include "bank.cpp"

using namespace std;

/* ------------------- Deposit Tests ------------------- */
void testDeposit() {
    BankAccount acc("TestUser", "Savings", 5000);

    assert(acc.deposit(2000) == true);
    assert(acc.getBalance() == 7000);

    assert(acc.deposit(-100) == false);
    assert(acc.getBalance() == 7000);
}

/* ------------------- Withdraw Tests ------------------- */
void testWithdrawSavings() {
    BankAccount acc("TestUser", "Savings", 5000);

    // valid withdraw
    assert(acc.withdraw(3000) == true);
    assert(acc.getBalance() == 2000);

    // minimum balance violation (should fail)
    assert(acc.withdraw(1500) == false);
    assert(acc.getBalance() == 2000);

    // negative withdraw
    assert(acc.withdraw(-100) == false);
}

void testWithdrawCurrent() {
    BankAccount acc("TestUser", "Current", 5000);

    // valid withdraw (with transaction fee)
    assert(acc.withdraw(1000) == true);
    assert(acc.getBalance() == 3990); // 5000 - 1000 - 10 fee
}

/* ------------------- Interest Tests ------------------- */
void testInterest() {
    BankAccount acc("TestUser", "Savings", 10000);

    acc.applyInterest();
    assert(acc.getBalance() == 10400); // 4% interest

    BankAccount acc2("TestUser", "Current", 10000);
    acc2.applyInterest();
    assert(acc2.getBalance() == 10000); // no interest for current
}

/* ------------------- Loan Tests ------------------- */
void testLoan() {
    BankAccount acc("TestUser", "Savings", 5000);

    // valid loan (limit = 2x balance = 10000)
    assert(acc.takeLoan(8000) == true);
    assert(acc.getLoanAmount() == 8000);
    assert(acc.getBalance() == 13000);

    // loan exceeding limit
    assert(acc.takeLoan(30000) == false);

    // negative loan
    assert(acc.takeLoan(-100) == false);
}

/* ------------------- MAIN ------------------- */
int main() {
    testDeposit();
    testWithdrawSavings();
    testWithdrawCurrent();
    testInterest();
    testLoan();

    cout << "All test cases passed successfully!\n";
    return 0;
}