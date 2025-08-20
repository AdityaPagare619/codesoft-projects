import React, { useState } from 'react';
import { Search, ShoppingCart, Filter, Star, Heart, ChevronLeft, ChevronRight } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';

const EcommerceListing = () => {
  const [cartCount, setCartCount] = useState(0);
  const [currentSlide, setCurrentSlide] = useState(0);
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [priceRange, setPriceRange] = useState([0, 500]);

  const heroSlides = [
    {
      title: 'New Arrivals',
      subtitle: 'Spring Collection 2024',
      image: '🌸',
      gradient: 'from-coral to-amber'
    },
    {
      title: 'Summer Sale',
      subtitle: 'Up to 70% Off',
      image: '☀️',
      gradient: 'from-amber to-teal'
    },
    {
      title: 'Premium Quality',
      subtitle: 'Crafted with Care',
      image: '✨',
      gradient: 'from-teal to-coral'
    }
  ];

  const categories = [
    { id: 'all', name: 'All Products', image: '🛍️' },
    { id: 'clothing', name: 'Clothing', image: '👕' },
    { id: 'accessories', name: 'Accessories', image: '👒' },
    { id: 'shoes', name: 'Shoes', image: '👟' },
    { id: 'bags', name: 'Bags', image: '👜' }
  ];

  const products = [
    {
      id: 1,
      name: 'Premium Cotton T-Shirt',
      price: 45,
      originalPrice: 65,
      rating: 4.8,
      reviews: 124,
      category: 'clothing',
      image: '👕',
      badge: 'Sale'
    },
    {
      id: 2,
      name: 'Leather Crossbody Bag',
      price: 120,
      rating: 4.9,
      reviews: 89,
      category: 'bags',
      image: '👜',
      badge: 'New'
    },
    {
      id: 3,
      name: 'Classic Sneakers',
      price: 85,
      originalPrice: 110,
      rating: 4.7,
      reviews: 256,
      category: 'shoes',
      image: '👟',
      badge: 'Popular'
    },
    {
      id: 4,
      name: 'Summer Hat',
      price: 35,
      rating: 4.6,
      reviews: 67,
      category: 'accessories',
      image: '👒',
      badge: null
    },
    {
      id: 5,
      name: 'Denim Jacket',
      price: 89,
      originalPrice: 120,
      rating: 4.8,
      reviews: 143,
      category: 'clothing',
      image: '🧥',
      badge: 'Sale'
    },
    {
      id: 6,
      name: 'Gold Watch',
      price: 299,
      rating: 4.9,
      reviews: 78,
      category: 'accessories',
      image: '⌚',
      badge: 'Premium'
    }
  ];

  const filteredProducts = products.filter(product => 
    (selectedCategory === 'all' || product.category === selectedCategory) &&
    product.price >= priceRange[0] && product.price <= priceRange[1]
  );

  const addToCart = () => {
    setCartCount(prev => prev + 1);
  };

  const nextSlide = () => {
    setCurrentSlide((prev) => (prev + 1) % heroSlides.length);
  };

  const prevSlide = () => {
    setCurrentSlide((prev) => (prev - 1 + heroSlides.length) % heroSlides.length);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-cream">
      {/* Top Navigation */}
      <nav className="bg-white/90 backdrop-blur-md border-b border-gray-200 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            {/* Logo */}
            <div className="flex items-center space-x-4">
              <div className="w-10 h-10 bg-gradient-amber rounded-xl flex items-center justify-center">
                <span className="font-bold text-charcoal">SC</span>
              </div>
              <h1 className="font-montserrat font-bold text-xl text-charcoal">StyleCraft</h1>
            </div>

            {/* Search Bar */}
            <div className="flex-1 max-w-md mx-8">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                <Input
                  type="text"
                  placeholder="Search products..."
                  className="pl-10 bg-gray-50 border-gray-200 focus:border-teal focus:ring-teal/20"
                />
              </div>
            </div>

            {/* Cart */}
            <div className="relative">
              <Button variant="outline" className="relative p-3">
                <ShoppingCart className="w-5 h-5" />
                {cartCount > 0 && (
                  <Badge className="absolute -top-2 -right-2 bg-coral text-white min-w-[20px] h-5 flex items-center justify-center text-xs">
                    {cartCount}
                  </Badge>
                )}
              </Button>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Carousel */}
      <div className="relative h-96 overflow-hidden">
        <div 
          className="flex transition-transform duration-500 ease-in-out h-full"
          style={{ transform: `translateX(-${currentSlide * 100}%)` }}
        >
          {heroSlides.map((slide, index) => (
            <div
              key={index}
              className={`min-w-full h-full bg-gradient-to-r ${slide.gradient} flex items-center justify-center text-white relative`}
            >
              <div className="text-center">
                <div className="text-6xl mb-4 animate-float">{slide.image}</div>
                <h2 className="font-montserrat font-bold text-5xl mb-4 animate-fade-in-up">
                  {slide.title}
                </h2>
                <p className="font-opensans text-xl mb-8 animate-fade-in-up" style={{animationDelay: '0.2s'}}>
                  {slide.subtitle}
                </p>
                <Button className="btn-amber px-8 py-3 text-lg animate-fade-in-up" style={{animationDelay: '0.4s'}}>
                  Shop Now
                </Button>
              </div>
            </div>
          ))}
        </div>
        
        {/* Carousel Controls */}
        <button
          onClick={prevSlide}
          className="absolute left-4 top-1/2 transform -translate-y-1/2 bg-white/80 hover:bg-white text-charcoal p-2 rounded-full transition-all duration-200"
        >
          <ChevronLeft className="w-6 h-6" />
        </button>
        <button
          onClick={nextSlide}
          className="absolute right-4 top-1/2 transform -translate-y-1/2 bg-white/80 hover:bg-white text-charcoal p-2 rounded-full transition-all duration-200"
        >
          <ChevronRight className="w-6 h-6" />
        </button>

        {/* Carousel Indicators */}
        <div className="absolute bottom-4 left-1/2 transform -translate-x-1/2 flex space-x-2">
          {heroSlides.map((_, index) => (
            <button
              key={index}
              onClick={() => setCurrentSlide(index)}
              className={`w-3 h-3 rounded-full transition-all duration-200 ${
                index === currentSlide ? 'bg-white scale-125' : 'bg-white/50'
              }`}
            />
          ))}
        </div>
      </div>

      {/* Category Section */}
      <div className="max-w-7xl mx-auto px-6 py-12">
        <h2 className="font-montserrat font-bold text-3xl text-center text-charcoal mb-8">
          Shop by Category
        </h2>
        <div className="grid grid-cols-2 md:grid-cols-5 gap-6">
          {categories.map((category) => (
            <button
              key={category.id}
              onClick={() => setSelectedCategory(category.id)}
              className={`card-floating p-6 text-center hover:scale-105 transition-all duration-300 ${
                selectedCategory === category.id ? 'ring-2 ring-teal shadow-teal' : ''
              }`}
            >
              <div className="text-4xl mb-3">{category.image}</div>
              <h3 className="font-opensans font-medium text-charcoal">{category.name}</h3>
            </button>
          ))}
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-6 pb-12">
        <div className="flex gap-8">
          {/* Sidebar Filters */}
          <div className="w-64 hidden lg:block">
            <div className="card-floating p-6 sticky top-24">
              <div className="flex items-center space-x-2 mb-6">
                <Filter className="w-5 h-5 text-teal" />
                <h3 className="font-montserrat font-semibold text-lg text-charcoal">Filters</h3>
              </div>

              <div className="space-y-6">
                <div>
                  <h4 className="font-opensans font-medium text-charcoal mb-3">Price Range</h4>
                  <div className="space-y-2">
                    <div className="flex justify-between text-sm text-gray-600">
                      <span>${priceRange[0]}</span>
                      <span>${priceRange[1]}</span>
                    </div>
                    <input
                      type="range"
                      min="0"
                      max="500"
                      value={priceRange[1]}
                      onChange={(e) => setPriceRange([priceRange[0], parseInt(e.target.value)])}
                      className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer slider"
                    />
                  </div>
                </div>

                <div>
                  <h4 className="font-opensans font-medium text-charcoal mb-3">Rating</h4>
                  <div className="space-y-2">
                    {[5, 4, 3].map((rating) => (
                      <label key={rating} className="flex items-center space-x-2 cursor-pointer">
                        <input type="checkbox" className="w-4 h-4 text-teal" />
                        <div className="flex items-center space-x-1">
                          {[...Array(rating)].map((_, i) => (
                            <Star key={i} className="w-4 h-4 fill-amber text-amber" />
                          ))}
                          <span className="text-sm text-gray-600">& up</span>
                        </div>
                      </label>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Product Grid */}
          <div className="flex-1">
            <div className="flex justify-between items-center mb-8">
              <h2 className="font-montserrat font-bold text-2xl text-charcoal">
                {selectedCategory === 'all' ? 'All Products' : categories.find(c => c.id === selectedCategory)?.name}
                <span className="text-gray-500 font-normal text-base ml-2">
                  ({filteredProducts.length} items)
                </span>
              </h2>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
              {filteredProducts.map((product) => (
                <div
                  key={product.id}
                  className="card-floating p-4 hover:shadow-medium transition-all duration-300 group relative"
                >
                  {/* Badge */}
                  {product.badge && (
                    <Badge
                      className={`absolute top-2 left-2 z-10 ${
                        product.badge === 'Sale' ? 'bg-error text-white' :
                        product.badge === 'New' ? 'bg-teal text-white' :
                        product.badge === 'Popular' ? 'bg-amber text-charcoal' :
                        'bg-navy text-white'
                      }`}
                    >
                      {product.badge}
                    </Badge>
                  )}

                  {/* Heart Icon */}
                  <button className="absolute top-2 right-2 z-10 p-2 bg-white/80 rounded-full hover:bg-white transition-colors">
                    <Heart className="w-4 h-4 text-gray-600 hover:text-coral" />
                  </button>

                  {/* Product Image */}
                  <div className="aspect-square bg-gradient-to-br from-gray-100 to-gray-200 rounded-lg mb-4 flex items-center justify-center text-6xl group-hover:scale-105 transition-transform duration-300">
                    {product.image}
                  </div>

                  {/* Product Info */}
                  <div>
                    <h3 className="font-opensans font-semibold text-charcoal mb-2 group-hover:text-teal transition-colors">
                      {product.name}
                    </h3>
                    
                    <div className="flex items-center space-x-1 mb-2">
                      <div className="flex items-center">
                        {[...Array(5)].map((_, i) => (
                          <Star
                            key={i}
                            className={`w-3 h-3 ${
                              i < Math.floor(product.rating) ? 'fill-amber text-amber' : 'text-gray-300'
                            }`}
                          />
                        ))}
                      </div>
                      <span className="text-xs text-gray-600">({product.reviews})</span>
                    </div>

                    <div className="flex items-center justify-between mb-4">
                      <div className="flex items-center space-x-2">
                        <span className="font-opensans font-bold text-lg text-charcoal">
                          ${product.price}
                        </span>
                        {product.originalPrice && (
                          <span className="text-sm text-gray-500 line-through">
                            ${product.originalPrice}
                          </span>
                        )}
                      </div>
                    </div>

                    <Button
                      onClick={addToCart}
                      className="w-full btn-teal py-2 text-sm"
                    >
                      Add to Cart
                    </Button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Newsletter Section */}
      <div className="bg-charcoal text-white py-16">
        <div className="max-w-4xl mx-auto text-center px-6">
          <h2 className="font-montserrat font-bold text-3xl mb-4">Stay Updated</h2>
          <p className="font-opensans text-lg mb-8 text-gray-300">
            Subscribe to our newsletter for exclusive deals and new arrivals
          </p>
          <div className="flex max-w-md mx-auto">
            <Input
              type="email"
              placeholder="Enter your email"
              className="flex-1 bg-white text-charcoal border-0 rounded-r-none"
            />
            <Button className="btn-coral rounded-l-none px-6">
              Subscribe
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default EcommerceListing;