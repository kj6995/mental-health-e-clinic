"use client";

import { useEffect, useState } from 'react';
import { Card, CardContent, CardHeader } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Slider } from '@/components/ui/slider';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Pagination, PaginationContent, PaginationItem, PaginationLink, PaginationNext, PaginationPrevious } from '@/components/ui/pagination';
import { Star, Search, Filter } from 'lucide-react';
import { getTherapists, getCategories, type TherapistResponse } from '@/lib/api';

export function TherapistsList() {
  const [therapists, setTherapists] = useState<TherapistResponse | null>(null);
  const [categories, setCategories] = useState<string[]>([]);
  const [search, setSearch] = useState('');
  const [category, setCategory] = useState('all');
  const [minRating, setMinRating] = useState(0);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const perPage = 10;
  
  // Fetch categories on component mount
  useEffect(() => {
    async function fetchCategories() {
      try {
        const data = await getCategories();
        setCategories(data);
      } catch (err) {
        console.error('Error fetching categories:', err);
        setError('Failed to load categories. Please try again later.');
      }
    }
    fetchCategories();
  }, []);
  
  // Fetch therapists based on filters
  useEffect(() => {
    async function fetchTherapists() {
      try {
        setLoading(true);
        const data = await getTherapists(
          page,
          perPage,
          search,
          category !== 'all' ? category : '',
          minRating
        );
        setTherapists(data);
        setError(null);
      } catch (err) {
        console.error('Error fetching therapists:', err);
        setError('Failed to fetch therapists. Please try again later.');
        setTherapists(null);
      } finally {
        setLoading(false);
      }
    }

    // Debounce the search to avoid too many API calls
    const timeoutId = setTimeout(() => {
      fetchTherapists();
    }, 300);

    return () => clearTimeout(timeoutId);
  }, [search, category, minRating, page]);

  // Handle search input
  const handleSearch = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearch(e.target.value);
    setPage(1); // Reset to first page on new search
  };
  
  // Handle category selection
  const handleCategoryChange = (value: string) => {
    setCategory(value);
    setPage(1); // Reset to first page on new filter
  };
  
  // Handle rating filter
  const handleRatingChange = (value: number[]) => {
    setMinRating(value[0]);
    setPage(1); // Reset to first page on new filter
  };
  
  // Clear all filters
  const clearFilters = () => {
    setSearch('');
    setCategory('all');
    setMinRating(0);
    setPage(1);
  };
  
  // Render star ratings
  const renderRating = (rating: number) => {
    return (
      <div className="flex items-center">
        {[...Array(5)].map((_, i) => (
          <Star
            key={i}
            className={`h-4 w-4 ${
              i < Math.floor(rating) 
                ? 'text-yellow-500 fill-yellow-500' 
                : i < rating 
                  ? 'text-yellow-500 fill-yellow-500 opacity-50' 
                  : 'text-gray-300'
            }`}
          />
        ))}
        <span className="ml-2 text-sm font-medium">{rating.toFixed(1)}</span>
      </div>
    );
  };
  
  if (error) {
    return (
      <div className="text-center py-12">
        <p className="text-destructive">{error}</p>
        <Button onClick={() => window.location.reload()} className="mt-4">
          Try Again
        </Button>
      </div>
    );
  }
  
  return (
    <div>
      {/* Search and Filters */}
      <div className="mb-8 space-y-4">
        <div className="flex flex-col md:flex-row gap-4">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
            <Input
              placeholder="Search by name or description..."
              value={search}
              onChange={handleSearch}
              className="pl-10"
            />
          </div>
          
          <Select value={category} onValueChange={handleCategoryChange}>
            <SelectTrigger className="w-full md:w-[200px]">
              <SelectValue placeholder="All Categories" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Categories</SelectItem>
              {categories.map((cat) => (
                <SelectItem key={cat} value={cat}>
                  {cat}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
          
          <div className="w-full md:w-[250px] flex flex-col">
            <div className="flex justify-between mb-2">
              <span className="text-sm">Min Rating: {minRating}</span>
              <span className="text-sm">5.0</span>
            </div>
            <Slider
              value={[minRating]}
              min={0}
              max={5}
              step={0.1}
              onValueChange={handleRatingChange}
            />
          </div>
          
          <Button variant="outline" onClick={clearFilters} className="whitespace-nowrap">
            <Filter className="mr-2 h-4 w-4" />
            Clear Filters
          </Button>
        </div>
      </div>
      
      {/* Results Summary */}
      {therapists && (
        <div className="mb-6">
          <p className="text-sm text-muted-foreground">
            Showing {therapists.items.length} of {therapists.total_records} therapists
            {search && ` matching "${search}"`}
            {category !== 'all' && ` in category "${category}"`}
            {minRating > 0 && ` with rating ${minRating}+`}
          </p>
        </div>
      )}
      
      {/* Therapists List */}
      <div className="space-y-6">
        {loading ? (
          <div className="text-center py-12">
            <p>Loading therapists...</p>
          </div>
        ) : therapists?.items.length === 0 ? (
          <div className="text-center py-12 border rounded-lg bg-muted/20">
            <p className="text-muted-foreground">No therapists found matching your criteria.</p>
            <Button onClick={clearFilters} variant="link" className="mt-2">
              Clear all filters
            </Button>
          </div>
        ) : (
          therapists?.items.map((therapist) => (
            <TherapistCard key={therapist.id} therapist={therapist} />
          ))
        )}
      </div>
      
      {/* Pagination */}
      {therapists && therapists.total_pages > 1 && (
        <Pagination className="mt-8">
          <PaginationContent>
            <PaginationItem>
              <PaginationPrevious
                onClick={() => setPage(Math.max(1, page - 1))}
                className={page <= 1 ? 'pointer-events-none opacity-50' : 'cursor-pointer'}
              />
            </PaginationItem>
            
            {Array.from({ length: therapists.total_pages }, (_, i) => i + 1)
              .filter(p => {
                // Show first page, last page, current page, and pages around current page
                return (
                  p === 1 || 
                  p === therapists.total_pages || 
                  (p >= page - 1 && p <= page + 1)
                );
              })
              .map((p, i, arr) => {
                // Add ellipsis where needed
                const showEllipsisBefore = i > 0 && arr[i - 1] !== p - 1;
                const showEllipsisAfter = i < arr.length - 1 && arr[i + 1] !== p + 1;
                
                return (
                  <div key={p} className="flex items-center">
                    {showEllipsisBefore && (
                      <PaginationItem>
                        <span className="px-2">...</span>
                      </PaginationItem>
                    )}
                    
                    <PaginationItem>
                      <PaginationLink
                        onClick={() => setPage(p)}
                        isActive={page === p}
                        className="cursor-pointer"
                      >
                        {p}
                      </PaginationLink>
                    </PaginationItem>
                    
                    {showEllipsisAfter && (
                      <PaginationItem>
                        <span className="px-2">...</span>
                      </PaginationItem>
                    )}
                  </div>
                );
              })}
            
            <PaginationItem>
              <PaginationNext
                onClick={() => setPage(Math.min(therapists.total_pages, page + 1))}
                className={page >= therapists.total_pages ? 'pointer-events-none opacity-50' : 'cursor-pointer'}
              />
            </PaginationItem>
          </PaginationContent>
        </Pagination>
      )}
    </div>
  );
}

function TherapistCard({ therapist }: { therapist: Therapist }) {
  return (
    <Card className="overflow-hidden transition-all hover:shadow-md">
      <CardHeader className="bg-muted/30 pb-2">
        <div className="flex justify-between items-start">
          <div>
            <h3 className="text-lg font-semibold">{therapist.name}</h3>
            <p className="text-sm text-muted-foreground">{therapist.category}</p>
          </div>
          <div className="text-right">
            <div className="mb-1">{renderRating(therapist.rating)}</div>
            <p className="text-sm text-muted-foreground">{therapist.experience}</p>
          </div>
        </div>
      </CardHeader>
      <CardContent className="pt-4">
        <p className="mb-4">{therapist.description}</p>
        <div className="flex flex-col gap-2">
          <div>
            <span className="text-sm font-medium">Qualification:</span>
            <span className="text-sm ml-2">{therapist.qualification}</span>
          </div>
          <div>
            <span className="text-sm font-medium">Specialization:</span>
            <div className="flex flex-wrap gap-1 mt-1">
              {therapist.specialization.map((spec) => (
                <Badge key={spec} variant="secondary" className="text-xs">
                  {spec}
                </Badge>
              ))}
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

// Helper function to render star ratings
function renderRating(rating: number) {
  return (
    <div className="flex items-center">
      {[...Array(5)].map((_, i) => (
        <Star
          key={i}
          className={`h-4 w-4 ${
            i < Math.floor(rating) 
              ? 'text-yellow-500 fill-yellow-500' 
              : i < rating 
                ? 'text-yellow-500 fill-yellow-500 opacity-50' 
                : 'text-gray-300'
          }`}
        />
      ))}
      <span className="ml-2 text-sm font-medium">{rating.toFixed(1)}</span>
    </div>
  );
}