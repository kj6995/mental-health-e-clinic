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
