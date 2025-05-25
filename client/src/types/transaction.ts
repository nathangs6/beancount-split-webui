export type Transaction = {
    plus_account: string;
    minus_account: string;
    transaction_date: string;
    description: string;
    extended_description: string;
    amount: number;
    shared_percentages: { [index: string]: number };
    is_duplicate: boolean;
}

export type CSVTransaction = {
    account_type: string;
    account_number: string;
    amount: number;
    description: string;
    transaction_date: string;
}
