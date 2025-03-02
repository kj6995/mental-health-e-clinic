import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { HeartPulse } from 'lucide-react';

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-background to-secondary/20">
      <div className="container mx-auto px-4 py-16 flex flex-col items-center justify-center min-h-[80vh] text-center">
        <h1 className="text-4xl md:text-6xl font-bold tracking-tight mb-6">
          Find Your Perfect <span className="text-primary">Therapist</span>
        </h1>
        <p className="text-lg md:text-xl text-muted-foreground max-w-2xl mb-10">
          Connect with qualified mental health professionals who can help you on your journey to wellness.
        </p>
        <Link href="/therapists">
          <Button size="lg" className="gap-2">
            <HeartPulse className="h-5 w-5" />
            Find Therapists
          </Button>
        </Link>
      </div>
    </div>
  );
}