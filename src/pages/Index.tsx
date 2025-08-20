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
      <header className="relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-hero opacity-90"></div>
        <div className="relative z-10 max-w-7xl mx-auto px-6 py-20 text-center text-white">
          <div className="inline-block mb-6">
            <div className="w-20 h-20 bg-gradient-teal rounded-3xl mx-auto flex items-center justify-center rotate-slow shadow-teal">
              <Zap className="w-10 h-10 text-white" />
            </div>
          </div>
          
          <h1 className="font-montserrat font-bold text-6xl mb-6 animate-fade-in-up">
            Front-End Animation Lab
          </h1>
          <p className="font-opensans text-xl mb-8 max-w-2xl mx-auto text-gray-200 animate-fade-in-up" style={{animationDelay: '0.2s'}}>
            A showcase of modern web design with stunning animations, responsive layouts, and professional UX patterns
          </p>
          
          <div className="flex flex-wrap justify-center gap-4 animate-fade-in-up" style={{animationDelay: '0.4s'}}>
            <div className="flex items-center space-x-2 bg-white/10 backdrop-blur-md px-4 py-2 rounded-full">
              <Star className="w-4 h-4 text-amber" />
              <span className="text-sm">4 Unique Projects</span>
            </div>
            <div className="flex items-center space-x-2 bg-white/10 backdrop-blur-md px-4 py-2 rounded-full">
              <Palette className="w-4 h-4 text-coral" />
              <span className="text-sm">Professional Design</span>
            </div>
            <div className="flex items-center space-x-2 bg-white/10 backdrop-blur-md px-4 py-2 rounded-full">
              <Zap className="w-4 h-4 text-teal" />
              <span className="text-sm">Smooth Animations</span>
            </div>
          </div>
        </div>

        {/* Floating Elements */}
        <div className="absolute top-20 left-10 w-4 h-4 bg-coral rounded-full animate-float opacity-60"></div>
        <div className="absolute top-40 right-20 w-6 h-6 bg-amber rounded-full animate-float opacity-40" style={{animationDelay: '1s'}}></div>
        <div className="absolute bottom-20 left-1/4 w-3 h-3 bg-teal rounded-full animate-float opacity-50" style={{animationDelay: '2s'}}></div>
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
                className="card-floating p-8 hover:shadow-strong transition-all duration-500 group animate-fade-in-up"
                style={{animationDelay: project.delay}}
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
                className="card-floating p-6 text-center hover:scale-105 transition-all duration-300 animate-fade-in-up"
                style={{animationDelay: `${index * 0.1}s`}}
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
