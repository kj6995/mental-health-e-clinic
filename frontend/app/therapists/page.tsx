import { Suspense } from 'react';
import { TherapistsList } from './therapists-list';
import { Skeleton } from '@/components/ui/skeleton';
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { ArrowLeft } from 'lucide-react';

export default function TherapistsPage() {
  return (
    <div className="min-h-screen bg-background">
      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <Link href="/">
            <Button variant="ghost" className="gap-2">
              <ArrowLeft className="h-4 w-4" />
              Back to Home
            </Button>
          </Link>
          <h1 className="text-3xl font-bold mt-4">Find Your Therapist</h1>
          <p className="text-muted-foreground mt-2">
            Browse our directory of qualified mental health professionals
          </p>
        </div>
        
        <Suspense fallback={<TherapistsListSkeleton />}>
          <TherapistsList />
        </Suspense>
      </div>
    </div>
  );
}

function TherapistsListSkeleton() {
  return (
    <div>
      <div className="flex flex-col md:flex-row gap-4 mb-8">
        <Skeleton className="h-10 w-full md:w-64" />
        <Skeleton className="h-10 w-full md:w-48" />
        <Skeleton className="h-10 w-full md:w-48" />
      </div>
      
      <div className="grid gap-6">
        {Array(5).fill(0).map((_, i) => (
          <Skeleton key={i} className="h-64 w-full rounded-lg" />
        ))}
      </div>
      
      <div className="mt-8 flex justify-center">
        <Skeleton className="h-10 w-64" />
      </div>
    </div>
  );
}