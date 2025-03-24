'use client';

import { JournalList } from './journal-list';

export default function JournalsPage() {
  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8">My Journal</h1>
      <JournalList />
    </div>
  );
}
