const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

export interface Therapist {
  id: number;
  name: string;
  category: string;
  qualification: string;
  experience: string;
  description: string;
  rating: number;
  specialization: string[];
}

export interface TherapistResponse {
  page: number;
  per_page: number;
  total_pages: number;
  total_records: number;
  items: Therapist[];
}

export interface Journal {
  id: string;
  title: string;
  content: string;
  tags: string[];
  createdAt: string;
  updatedAt: string;
}

export interface JournalResponse {
  page: number;
  per_page: number;
  total_pages: number;
  total_records: number;
  data: Journal[];
}

export async function getTherapists(
  page: number = 1,
  per_page: number = 10,
  search: string = '',
  category: string = '',
  minRating: number = 0
): Promise<TherapistResponse> {
  const params = new URLSearchParams({
    page: page.toString(),
    per_page: per_page.toString(),
    ...(search && { search }),
    ...(category && { category }),
    ...(minRating > 0 && { minRating: minRating.toString() })
  });

  const response = await fetch(`${API_BASE_URL}/therapists?${params}`);
  if (!response.ok) {
    throw new Error('Failed to fetch therapists');
  }
  return response.json();
}

export async function getCategories(): Promise<string[]> {
  const response = await fetch(`${API_BASE_URL}/therapists/categories`);
  if (!response.ok) {
    throw new Error('Failed to fetch categories');
  }
  return response.json();
}

export async function getTherapist(id: number): Promise<Therapist> {
  const response = await fetch(`${API_BASE_URL}/therapists/${id}`);
  if (!response.ok) {
    throw new Error('Failed to fetch therapist');
  }
  return response.json();
}

export async function getJournals(
  page: number = 1,
  search: string = ''
): Promise<JournalResponse> {
  const params = new URLSearchParams({
    page: page.toString(),
    ...(search && { search })
  });

  const response = await fetch(`${API_BASE_URL}/journals?${params}`);
  if (!response.ok) {
    throw new Error('Failed to fetch journals');
  }
  return response.json();
}

export async function createJournal(journalData: {
  title: string;
  content: string;
  tags: string[];
}): Promise<Journal> {
  const response = await fetch(`${API_BASE_URL}/journals`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(journalData),
  });
  
  if (!response.ok) {
    throw new Error('Failed to create journal');
  }
  return response.json();
}

export async function updateJournal(
  id: string,
  journalData: {
    title: string;
    content: string;
    tags: string[];
  }
): Promise<Journal> {
  const response = await fetch(`${API_BASE_URL}/journals/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(journalData),
  });
  
  if (!response.ok) {
    throw new Error('Failed to update journal');
  }
  return response.json();
}

export async function deleteJournal(id: string): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/journals/${id}`, {
    method: 'DELETE',
  });
  
  if (!response.ok) {
    throw new Error('Failed to delete journal');
  }
}