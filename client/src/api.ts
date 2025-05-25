import apiClient from './axios';
import type { CSVTransaction, Transaction } from './types/transaction';

export async function getUsers(): Promise<string[]> {
  return await apiClient.get('/users')
  .then((response) => {
    return response.data.users;
  })
  .catch((error) => {
    throw error;
  });
}

export async function getAccounts(owner: string): Promise<string[]> {
  return await apiClient.get('/accounts/' + owner)
  .then((response) => {
    return response.data.accounts;
  })
  .catch((error) => {
    throw error;
  });
}

export async function processFile(file: File): Promise<CSVTransaction[]> {
  const formData = new FormData();
  formData.append('file', file);

  return await apiClient.post('/importer/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })
  .then((response) => {
    return response.data;
  })
  .catch((error) => {
    throw error;
  });
}

export async function determineDuplicates(transactions: Transaction[], owner: string) : Promise<Transaction[]> {
  return await apiClient.post('/importer/determine_duplicates/' + owner, transactions)
  .then((response) => {
    return response.data.transactions;
  })
  .catch((error) => {
    throw error;
  });
}

export async function validateTransactions(transactions: Transaction[], owner: string): Promise<{[user: string]: string}> {
  return await apiClient.post('/importer/validate/' + owner, transactions)
  .then((response) => {
    return response.data.transaction_strings;
  })
  .catch((error) => {
    throw error;
  });
}

export async function submitImport(entries: {[owner: string]: string}) : Promise<void> {
  return await apiClient.post('/importer/import', entries)
  .then((response) => {
  })
  .catch((error) => {
    throw error;
  });
}
