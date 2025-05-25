import React from "react";

export default function PreviewTransactions({
  users,
  transactionStrings,
}: {
  users: string[];
  transactionStrings: { [user: string]: string };
}) {
  return (
    <div>
      <h2>Preview Transactions</h2>
      {transactionStrings[users[0]] ? (
        <>
          <h3>{users[0] + "'s Transactions"}</h3>
          <pre style={{ textAlign: "left" }}>
            {transactionStrings[users[0]]}
          </pre>
        </>
      ) : null}
      {transactionStrings[users[1]] ? (
        <>
          <h3>{users[1] + "'s Transactions"}</h3>
          <pre style={{ textAlign: "left" }}>
            {transactionStrings[users[1]]}
          </pre>
        </>
      ) : null}
    </div>
  );
}
