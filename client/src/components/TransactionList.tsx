import React, { useState } from "react";
import { Transaction } from "../types/transaction";

export default function TransactionList({
  transactions,
  setTransactions,
  accounts,
  users,
  onValidate
}: {
  transactions: Transaction[];
  setTransactions: (transactions: Transaction[]) => void;
  accounts: string[];
  users: string[];
  onValidate: (transactions: Transaction[]) => void;
}) {

    const [errorMessage, setErrorMessage] = useState<string | null>(null);

    const handlePercentChange = (index: number, user: string, value: number) => {
        if (value < 0 || value > 100) {
            return;
        }
        if (Number.isNaN(value)) {
            value = 0;
        }
        value = Math.floor(value * 100) / 100;
        let baseUser: string, otherUser: string;
        if (user == users[0]) {
            baseUser = users[0];
            otherUser = users[1];
        } else {
            baseUser = users[1];
            otherUser = users[0];
        }
        transactions[index].shared_percentages[baseUser] = value;
        transactions[index].shared_percentages[otherUser] = 100 - value;
        setTransactions([...transactions]);
    }

    const handleValidate = (transactions: Transaction[]) => {
        if (!transactions.every((transaction) => transaction.is_duplicate || (transaction.plus_account && transaction.minus_account))) {
            setErrorMessage("Invalid transactions: missing plus or minus account");
            return;
        }
        onValidate(transactions);
        setErrorMessage(null);
    }
  return (
    <div>
      <h2>Transaction List</h2>
      <table>
        <thead>
          <tr>
            <th>Description</th>
            <th>Date</th>
            <th>Amount</th>
            <th>Extended Description</th>
            <th>Plus Account</th>
            <th>Minus Account</th>
            <th>Duplicate?</th>
            <th>Shared?</th>
            <th>{users[0] + " Percent"}</th>
            <th>{users[1] + " Percent"}</th>
          </tr>
        </thead>
        <tbody>
          {transactions.map((transaction, index) => (
            <tr key={index}>
              <td style={(transaction.minus_account == "" || transaction.plus_account == "") ? {color: "red"} : {}}>{transaction.description}</td>
              <td>{transaction.transaction_date}</td>
              <td>{Math.abs(transaction.amount).toFixed(2)}</td>
              <td>
                <input
                  type="text"
                  value={transaction.extended_description}
                  onChange={(e) => {
                    transaction.extended_description = e.target.value;
                    setTransactions([...transactions]);
                  }}
                  disabled={transaction.is_duplicate}
                />
              </td>
              <td>
                <select
                  value={transaction.plus_account}
                  onChange={(e) => {
                    transaction.plus_account = e.target.value;
                    setTransactions([...transactions]);
                  }}
                  disabled={transaction.is_duplicate}
                >
                  <option value="" disabled={true}>
                    Select an account
                  </option>
                  {accounts.map((account, index) => (
                    <option key={index} value={account}>
                      {account}
                    </option>
                  ))}
                </select>
              </td>
              <td>
                <select
                  value={transaction.minus_account}
                  onChange={(e) => {
                    transaction.minus_account = e.target.value;
                    setTransactions([...transactions]);
                  }}
                  disabled={transaction.is_duplicate}
                >
                  <option value="" disabled={true}>
                    Select an account
                  </option>
                  {accounts.map((account, index) => (
                    <option key={index} value={account}>
                      {account}
                    </option>
                  ))}
                </select>
              </td>
              <td>
                <input
                  type="checkbox"
                  checked={transaction.is_duplicate}
                  onChange={(e) => {
                    transaction.is_duplicate = e.target.checked;
                    setTransactions([...transactions]);
                  }}
                />
              </td>
              <td>
                <input
                  type="checkbox"
                  checked={Object.keys(transaction.shared_percentages).length > 0}
                  onChange={(e) => {
                    if (e.target.checked) {
                      transaction.shared_percentages[users[0]] = 50;
                      transaction.shared_percentages[users[1]] = 50;
                    } else {
                      transaction.shared_percentages = {}
                    }
                    setTransactions([...transactions]);
                  }}
                  disabled={transaction.is_duplicate}
                />
              </td>
              <td>
                <input
                  type="number"
                  value={parseFloat(transaction.shared_percentages[users[0]]?.toString() || "0").toString()}
                  disabled={!Object.keys(transaction.shared_percentages).length || transaction.is_duplicate}
                  onChange={(e) => {
                    handlePercentChange(index, users[0], parseFloat(e.target.value));
                  }}
                />
              </td>
              <td>
                <input
                  type="number"
                  value={parseFloat(transaction.shared_percentages[users[1]]?.toString() || "0").toString()}
                  disabled={!Object.keys(transaction.shared_percentages).length || transaction.is_duplicate}
                  onChange={(e) => {
                    handlePercentChange(index, users[1], parseFloat(e.target.value));
                  }}
                />
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      {errorMessage && <p style={{ color: "red" }}>{errorMessage}</p>}
      <button onClick={() => {handleValidate(transactions)}
      }>Validate Transactions</button>
    </div>
  );
}
