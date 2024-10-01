import React from 'react';
import { Camera, Zap, Upload, Image as ImageIcon } from 'lucide-react';
import { Button } from 'src/components/ui/button';
import { Card, CardContent } from 'src/components/ui/card';
import { Badge } from 'src/components/ui/badge';

const LandingPage: React.FC = () => {
  return (
    <div className="bg-background text-foreground min-h-screen p-8">
      <header className="flex justify-between items-center mb-12">
        <div className="flex items-center">
          <Camera className="text-primary mr-2" />
          <span className="text-xl font-bold">Product Photo AI</span>
        </div>
        <nav>
          <ul className="flex space-x-6">
            <li><a href="#pricing" className="hover:text-primary">Pricing</a></li>
            <li><a href="#demo" className="hover:text-primary">Demo</a></li>
            <li><a href="#testimonials" className="hover:text-primary">Testimonials</a></li>
          </ul>
        </nav>
      </header>

      <main className="flex justify-between items-center">
        <div className="w-1/2">
          <div className="mb-4">
            <Badge variant="secondary">AI-powered product photography</Badge>
          </div>
          <h1 className="text-5xl font-bold mb-6">
            Create product photos
            <br />
            in minutes, <span className="bg-primary text-primary-foreground px-2">not hours</span>
          </h1>
          <p className="mb-8 text-muted-foreground">
            The AI tool with all you need to generate professional product photos.
            Upload your images and let AI do the magic.
          </p>
          <Button size="lg" className="font-bold">
            <Zap className="mr-2" />
            Get Product Photo AI
          </Button>
          <p className="mt-4 text-sm text-green-600 dark:text-green-400">
            $50 off for the first 1000 customers (213 left)
          </p>
          <div className="mt-8 flex items-center">
            <div className="flex -space-x-2 mr-4">
              {[...Array(5)].map((_, i) => (
                <img key={i} src={`/api/placeholder/40/40`} alt="User" className="w-8 h-8 rounded-full border-2 border-background" />
              ))}
            </div>
            <div>
              <div className="flex">
                {[...Array(5)].map((_, i) => (
                  <svg key={i} className="w-5 h-5 text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                  </svg>
                ))}
              </div>
              <p>2,345 creators ship faster</p>
            </div>
          </div>
        </div>
        <div className="w-1/2 relative">
          <div className="absolute inset-0 bg-gradient-to-r from-transparent to-background rounded-full" style={{transform: 'rotate(-5deg)'}}></div>
          <div className="relative z-10 flex justify-center items-center space-x-4">
            <Card>
              <CardContent className="flex flex-col items-center p-6">
                <Upload className="text-blue-400 mb-2" />
                <p className="text-sm">Upload Images</p>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="flex flex-col items-center p-6">
                <Zap className="text-yellow-400 mb-2" />
                <p className="text-sm">AI Processing</p>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="flex flex-col items-center p-6">
                <ImageIcon className="text-green-400 mb-2" />
                <p className="text-sm">Generate Photos</p>
              </CardContent>
            </Card>
          </div>
          <p className="absolute bottom-0 right-0 text-muted-foreground">
            git clone product-photo-ai
          </p>
        </div>
      </main>
    </div>
  );
};

export default LandingPage;
