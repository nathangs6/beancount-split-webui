import React, { useEffect, useState } from "react";
import { CSVTransaction } from "../types/transaction";

type SelectionAccount = {
  account_type: string;
  account_number: string;
};

export default function FileAccountSelector({
  csvTransactions,
  accounts,
  onConfirmChoices,
}: {
  csvTransactions: CSVTransaction[];
  accounts: string[];
  onConfirmChoices: (accountSelections: { [key: string]: string }) => void;
}) {
  const [accountSelections, setAccountSelections] = useState<{
    [key: string]: string;
  }>({});
  const [accountList, setAccountList] = useState<SelectionAccount[]>([]);
  const [allowedAccounts, setAllowedAccounts] = useState<string[]>([]);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  useEffect(() => {
    const uniqueAccounts: SelectionAccount[] = [];
    for (const transaction of csvTransactions) {
      const account = {
        account_type: transaction.account_type,
        account_number: transaction.account_number,
      };
      if (
        !uniqueAccounts.some(
          (acc) => acc.account_number === account.account_number
        )
      ) {
        uniqueAccounts.push(account);
      }
    }
    setAccountList(uniqueAccounts);
    setAccountSelections(
      uniqueAccounts.reduce((acc, transaction) => {
        acc[transaction.account_number] = "";
        return acc;
      }, {} as { [key: string]: string })
    );
  }, [csvTransactions]);

  useEffect(() => {
    const allowedAccountTypes = ["Assets", "Liabilities", "Equity"];
    const filteredAccountList = accounts.filter((account) => {
      for (const accType of allowedAccountTypes) {
        if (account.includes(accType)) {
          return true;
        }
      }
      return false;
    });
    setAllowedAccounts(filteredAccountList);
  }, [accountList]);

  const handleConfirm = (accountSelections: { [key: string]: string }) => {
    const validSelections = Object.values(accountSelections).every(
      (selection) => selection !== ""
    );
    if (validSelections) {
      onConfirmChoices(accountSelections);
      setErrorMessage(null);
    } else {
      setErrorMessage("Please select an account for each transaction.");
    }
  };

  return (
    <div>
      <h2>Choose Default Accounts</h2>
      <table>
        <thead>
          <tr>
            <th>Account Type</th>
            <th>Account Number</th>
            <th>Bean Account</th>
          </tr>
        </thead>
        <tbody>
          {accountList.map((transaction, index) => (
            <tr key={index}>
              <td>{transaction.account_type}</td>
              <td>{transaction.account_number}</td>
              <td>
                <select
                  value={
                    accountSelections[`${transaction.account_number}`] || ""
                  }
                  onChange={(e) => {
                    const selectedAccount = e.target.value;
                    setAccountSelections({
                      ...accountSelections,
                      [`${transaction.account_number}`]: selectedAccount,
                    });
                  }}
                >
                  <option value="" disabled={true}>
                    Select an account
                  </option>
                  {allowedAccounts.map((account, index) => (
                    <option key={index} value={account}>
                      {account}
                    </option>
                  ))}
                </select>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      {errorMessage && <p style={{ color: "red" }}>{errorMessage}</p>}
      <button
        onClick={() => {
          handleConfirm(accountSelections);
        }}
      >
        Confirm Choices
      </button>
    </div>
  );
}
