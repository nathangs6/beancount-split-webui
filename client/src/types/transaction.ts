export type Transaction = {
    account_type: string;
    account_number: string;
    plus_account: string;
    minus_account: string;
    transaction_date: string;
    description: string;
    extended_description: string;
    amount: number;
    shared_percentages: { [index: string]: number };
    is_duplicate: boolean;
}
