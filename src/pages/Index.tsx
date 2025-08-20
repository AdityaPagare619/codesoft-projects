import React from 'react';
import { Link } from 'react-router-dom';
import { Smartphone, Mail, ChefHat, ShoppingBag, ArrowRight, Star, Zap, Palette } from 'lucide-react';
import { Button } from '@/components/ui/button';

const Index = () => {
  const projects = [
    {
      title: 'Mobile Signup Flow',
      description: '3-step personalized signup with floating labels, real-time validation, and smooth animations',
      icon: Smartphone,
      path: '/mobile-signup',
      gradient: 'from-teal to-teal-light',
      features: ['Floating Labels', 'Real-time Validation', 'Progress Indicators'],
      preview: '📱',
      delay: '0s'
    },
    {
      title: 'Email Template',
      description: 'Responsive marketing newsletter with hero banners, product grids, and social integration',
      icon: Mail,
      path: '/email-template',
      gradient: 'from-coral to-coral-dark',
      features: ['Responsive Design', 'Hero Banners', 'Social Links'],
      preview: '📧',
      delay: '0.1s'
    },
    {
      title: 'Restaurant Menu',
      description: 'Elegant digital menu with category filtering, dietary tags, and beautiful food presentation',
      icon: ChefHat,
      path: '/restaurant-menu',
      gradient: 'from-amber to-amber-dark',
      features: ['Category Filters', 'Dietary Tags', 'Elegant Typography'],
      preview: '🍽️',
      delay: '0.2s'
    },
    {
      title: 'E-commerce Store',
      description: 'Full-featured product listing with carousel, filters, shopping cart, and premium animations',
      icon: ShoppingBag,
      path: '/ecommerce-listing',
      gradient: 'from-navy to-teal',
      features: ['Product Carousel', 'Smart Filters', 'Shopping Cart'],
      preview: '🛍️',
      delay: '0.3s'
    }
  ];

  const techStack = [
    { name: 'React', icon: '⚛️' },
    { name: 'TypeScript', icon: '📘' },
    { name: 'Tailwind CSS', icon: '🎨' },
    { name: 'Framer Motion', icon: '🎬' },
    { name: 'Lucide Icons', icon: '🎯' },
    { name: 'Shadcn/ui', icon: '🔧' }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-cream/30 to-teal/5">
      {/* Header */}
      <header className="relative overflow-hidden min-h-[90vh] flex items-center">
        {/* Dynamic Background with 3D Perspective */}
        <div className="absolute inset-0 bg-gradient-hero opacity-90 before:content-[''] before:absolute before:inset-0 before:bg-[radial-gradient(circle_at_center,rgba(168,255,242,0.15)_0%,transparent_70%)]">
          {/* Animated Grid Lines */}
          <div className="absolute inset-0 opacity-20" 
               style={{
                 backgroundImage: `linear-gradient(to right, rgba(255,255,255,0.1) 1px, transparent 1px), 
                                  linear-gradient(to bottom, rgba(255,255,255,0.1) 1px, transparent 1px)`,
                 backgroundSize: '40px 40px',
                 backgroundPosition: 'center',
               }}></div>
        </div>

        <div className="relative z-10 max-w-7xl mx-auto px-6 py-20 text-center text-white">
          {/* Animated Logo */}
          <div className="inline-block mb-8" style={{perspective: '1000px'}}>
            <div className="w-24 h-24 bg-gradient-teal rounded-[30%_70%_40%_60%] mx-auto flex items-center justify-center shadow-teal transform hover:scale-110 transition-transform duration-500">
              <Zap className="w-12 h-12 text-white" />
            </div>
          </div>
          
          {/* Heading with Simple Effect */}
          <h1 className="font-playfair font-bold text-7xl mb-6 tracking-tight">
            <span className="inline-block">Front-End</span>{' '}
            <span className="bg-clip-text text-transparent bg-gradient-to-r from-teal-light via-white to-coral inline-block">Animation Lab</span>
          </h1>

          {/* Simple Subtitle */}
          <p className="font-montserrat text-xl mb-10 max-w-2xl mx-auto text-gray-200 leading-relaxed">
            Explore a collection of <span className="text-teal-light font-semibold">stunning animations</span>, <span className="text-coral font-semibold">responsive layouts</span>, and <span className="text-amber font-semibold">professional UX patterns</span> for modern web experiences
          </p>
          
          {/* Feature Pills with Simple Hover Effects */}
          <div className="flex flex-wrap justify-center gap-4">
            <div className="flex items-center space-x-2 bg-white/10 backdrop-blur-md px-5 py-3 rounded-full border border-white/10 hover:bg-white/20 transition-all duration-300 group cursor-pointer">
              <Star className="w-5 h-5 text-amber" />
              <span className="text-sm font-medium">4 Unique Projects</span>
            </div>
            <div className="flex items-center space-x-2 bg-white/10 backdrop-blur-md px-5 py-3 rounded-full border border-white/10 hover:bg-white/20 transition-all duration-300 group cursor-pointer">
              <Palette className="w-5 h-5 text-coral" />
              <span className="text-sm font-medium">Professional Design</span>
            </div>
            <div className="flex items-center space-x-2 bg-white/10 backdrop-blur-md px-5 py-3 rounded-full border border-white/10 hover:bg-white/20 transition-all duration-300 group cursor-pointer">
              <Zap className="w-5 h-5 text-teal" />
              <span className="text-sm font-medium">Smooth Animations</span>
            </div>
          </div>

          {/* CTA Button */}
          <div className="mt-12">
            <Button className="bg-gradient-to-r from-teal to-teal-light text-white px-8 py-6 rounded-full text-lg font-medium hover:shadow-teal transition-all duration-300 group">
              <span>Explore Projects</span>
              <ArrowRight className="w-5 h-5 ml-2" />
            </Button>
          </div>
        </div>

        {/* Simple Floating Elements */}
        <div className="absolute top-1/4 left-[10%] w-16 h-16 rounded-full opacity-30"
             style={{background: 'radial-gradient(circle at center, rgba(255,138,115,0.8), rgba(255,138,115,0))'}}>  
        </div>
        <div className="absolute top-1/3 right-[15%] w-24 h-24 rounded-full opacity-20" 
             style={{background: 'radial-gradient(circle at center, rgba(255,204,77,0.8), rgba(255,204,77,0))'}}>  
        </div>
        <div className="absolute bottom-1/4 left-[20%] w-20 h-20 rounded-full opacity-25" 
             style={{background: 'radial-gradient(circle at center, rgba(77,219,197,0.8), rgba(77,219,197,0))'}}>  
        </div>
        <div className="absolute top-[60%] right-[25%] w-12 h-12 rounded-full opacity-30" 
             style={{background: 'radial-gradient(circle at center, rgba(255,255,255,0.8), rgba(255,255,255,0))'}}>  
        </div>

        {/* Simple Shapes */}
        <div className="absolute top-[15%] left-[15%] w-8 h-8 border-2 border-teal/30 rounded-md" 
             style={{transform: 'rotate(45deg)'}}></div>
        <div className="absolute bottom-[20%] right-[20%] w-10 h-10 border-2 border-coral/30 rounded-full"></div>
        <div className="absolute top-[70%] left-[30%] w-6 h-6 border-2 border-amber/30" 
             style={{clipPath: 'polygon(50% 0%, 0% 100%, 100% 100%)'}}></div>
      </header>

      {/* Project Showcase */}
      <section className="max-w-7xl mx-auto px-6 py-20">
        <div className="text-center mb-16">
          <h2 className="font-montserrat font-bold text-4xl text-charcoal mb-4">
            Explore the Projects
          </h2>
          <p className="font-opensans text-lg text-gray-600 max-w-2xl mx-auto">
            Each project demonstrates different aspects of modern web development, from mobile-first design to complex user interactions
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-8">
          {projects.map((project, index) => {
            const Icon = project.icon;
            return (
              <div
                key={project.path}
                className="card-floating p-8 hover:shadow-strong transition-all duration-500 group"
              >
                <div className="flex items-start space-x-6">
                  <div className="flex-shrink-0">
                    <div className={`w-16 h-16 bg-gradient-to-r ${project.gradient} rounded-2xl flex items-center justify-center shadow-medium group-hover:scale-110 transition-transform duration-300`}>
                      <Icon className="w-8 h-8 text-white" />
                    </div>
                  </div>
                  
                  <div className="flex-1">
                    <div className="flex items-center justify-between mb-3">
                      <h3 className="font-montserrat font-bold text-xl text-charcoal group-hover:text-teal transition-colors">
                        {project.title}
                      </h3>
                      <span className="text-4xl group-hover:scale-110 transition-transform duration-300">
                        {project.preview}
                      </span>
                    </div>
                    
                    <p className="font-opensans text-gray-600 mb-4 leading-relaxed">
                      {project.description}
                    </p>
                    
                    <div className="flex flex-wrap gap-2 mb-6">
                      {project.features.map((feature) => (
                        <span
                          key={feature}
                          className="px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-sm font-medium"
                        >
                          {feature}
                        </span>
                      ))}
                    </div>
                    
                    <Link to={project.path}>
                      <Button className={`bg-gradient-to-r ${project.gradient} text-white hover:shadow-lg hover:scale-105 transition-all duration-300 group/btn`}>
                        <span>View Project</span>
                        <ArrowRight className="w-4 h-4 ml-2 group-hover/btn:translate-x-1 transition-transform duration-200" />
                      </Button>
                    </Link>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </section>

      {/* Tech Stack */}
      <section className="bg-white/50 backdrop-blur-sm py-20">
        <div className="max-w-6xl mx-auto px-6 text-center">
          <h2 className="font-montserrat font-bold text-3xl text-charcoal mb-4">
            Built with Modern Technologies
          </h2>
          <p className="font-opensans text-gray-600 mb-12">
            Leveraging the latest tools and frameworks for optimal performance and developer experience
          </p>
          
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-6">
            {techStack.map((tech, index) => (
              <div
                key={tech.name}
                className="card-floating p-6 text-center hover:scale-105 transition-all duration-300"
              >
                <div className="text-3xl mb-3">{tech.icon}</div>
                <h3 className="font-opensans font-medium text-charcoal">{tech.name}</h3>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-charcoal text-white py-12">
        <div className="max-w-6xl mx-auto px-6 text-center">
          <div className="w-12 h-12 bg-gradient-teal rounded-2xl mx-auto mb-6 flex items-center justify-center">
            <Zap className="w-6 h-6 text-white" />
          </div>
          <h3 className="font-montserrat font-bold text-xl mb-2">Front-End Animation Lab</h3>
          <p className="font-opensans text-gray-400 mb-6">
            Crafted with passion for modern web development
          </p>
          <div className="flex justify-center space-x-6">
            {projects.map((project) => (
              <Link
                key={project.path}
                to={project.path}
                className="text-gray-400 hover:text-white transition-colors duration-200"
              >
                {project.title.split(' ')[0]}
              </Link>
            ))}
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Index;
