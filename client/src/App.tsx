import React, { useEffect, useState } from "react";
import "./App.css";

import {
  getUsers,
  getAccounts,
  processFile,
  validateTransactions,
  submitImport,
} from "./api";
import type { Transaction } from "./types/transaction";
import FileUpload from "./components/FileUpload";
import TransactionList from "./components/TransactionList";
import FileAccountSelector from "./components/FileAccountSelector";
import PreviewTransactions from "./components/PreviewTransactions";

export default function App() {
  const [users, setUsers] = useState<string[]>([]);
  const [owner, setOwner] = useState<string>("");
  const [accounts, setAccounts] = useState<string[]>([]);
  const [csvTransactions, setCSVTransactions] = useState<Transaction[]>([]);
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [transactionStrings, setTransactionStrings] = useState<{
    [user: string]: string;
  }>({});
  const [submitError, setSubmitError] = useState<string | null>(null);
  const [submitSuccess, setSubmitSuccess] = useState<string | null>(null);

  const [showUpload, setShowUpload] = useState(false);
  const [showAccountSelector, setShowAccountSelector] = useState(false);
  const [showTransactionList, setShowTransactionList] = useState(false);
  const [showPreview, setShowPreview] = useState(false);

  const loadUsers = async () => {
    const fetchedUsers: string[] = await getUsers();
    setUsers(fetchedUsers);
    if (fetchedUsers.length > 0) {
      setTransactionStrings({
        [fetchedUsers[0]]: "",
        [fetchedUsers[1]]: "",
      });
    }
  };
  useEffect(() => {
    loadUsers();
  }, []);

  const onOwnerSelect = (selectedOwner: string) => {
    setOwner(selectedOwner);
    setSubmitSuccess(null);
    setSubmitError(null);
    setShowUpload(true);
    setShowAccountSelector(false);
    setShowTransactionList(false);
  };

  const onFileUpload = async (file: File) => {
    if (!owner) {
      return false;
    }

    const response = await processFile(file, owner);

    const accounts = await getAccounts(owner);
    setAccounts(accounts);

    setCSVTransactions(response);
    setShowAccountSelector(true);
    setShowTransactionList(false);
    setSubmitSuccess(null);
    setSubmitError(null);
    return true;
  };

  const onConfirmChoices = async (accountSelections: {
    [account_number: string]: string;
  }) => {
    const tempTransactions: Transaction[] = [];
    let plusAccount = "";
    let minusAccount = "";
    for (const csvTransaction of csvTransactions) {
      if (csvTransaction.amount > 0) {
        plusAccount = accountSelections[csvTransaction.account_number];
        minusAccount = "";
      } else {
        minusAccount = accountSelections[csvTransaction.account_number];
        plusAccount = "";
      }
      const transaction: Transaction = {
        account_type: csvTransaction.account_type,
        account_number: csvTransaction.account_number,
        plus_account: plusAccount,
        minus_account: minusAccount,
        transaction_date: csvTransaction.transaction_date,
        description: csvTransaction.description,
        extended_description: "",
        amount: csvTransaction.amount,
        shared_percentages: {},
        is_duplicate: csvTransaction.is_duplicate,
      };
      tempTransactions.push(transaction);
    }
    // const duplicatesDeterminedTransactions = await determineDuplicates(
      // tempTransactions,
      // owner
    // );
    setTransactions(tempTransactions);
    setShowTransactionList(true);
    setSubmitSuccess(null);
    setSubmitError(null);
  };

  const onValidate = async (transactions: Transaction[]) => {
    const previewStrings = await validateTransactions(transactions, owner);
    setTransactionStrings(previewStrings);
    setShowPreview(true);
    setSubmitSuccess(null);
    setSubmitError(null);
  };

  const onSubmit = async () => {
    try {
      await submitImport(transactionStrings);
      setSubmitError(null);
      setSubmitSuccess("Import submitted successfully!");
    } catch (error) {
      setSubmitError("Error submitting import: " + error.message);
      setSubmitSuccess(null);
    }
  };

  return (
    <>
      <h1>Bean Import</h1>
      <p>Import transactions!</p>
      <select
        value={owner || ""}
        onChange={(e) => {
          const selectedOwner = e.target.value;
          onOwnerSelect(selectedOwner);
        }}
      >
        <option value="" disabled={true}>
          Select an owner
        </option>
        {users.map((user, index) => (
          <option key={index} value={user}>
            {user}
          </option>
        ))}
      </select>
      {showUpload ? <FileUpload onFileUpload={onFileUpload} /> : null}
      {showUpload && showAccountSelector ? (
        <FileAccountSelector
          csvTransactions={csvTransactions}
          accounts={accounts}
          onConfirmChoices={onConfirmChoices}
        />
      ) : null}
      {showUpload && showAccountSelector && showTransactionList ? (
        <TransactionList
          transactions={transactions}
          setTransactions={setTransactions}
          accounts={accounts}
          users={users}
          onValidate={onValidate}
        />
      ) : null}
      {showUpload &&
      showAccountSelector &&
      showTransactionList &&
      showPreview ? (
        <PreviewTransactions
          users={users}
          transactionStrings={transactionStrings}
        />
      ) : null}
      {showUpload &&
      showAccountSelector &&
      showTransactionList &&
      showPreview &&
      submitError ? (
        <div className="error-message">{submitError}</div>
      ) : null}
      {showUpload &&
      showAccountSelector &&
      showTransactionList &&
      showPreview &&
      submitSuccess ? (
        <div className="success-message">{submitSuccess}</div>
      ) : null}
      {showUpload &&
      showAccountSelector &&
      showTransactionList &&
      showPreview &&
      !submitSuccess ? (
        <button onClick={() => onSubmit()}>Submit</button>
      ) : null}
    </>
  );
}
