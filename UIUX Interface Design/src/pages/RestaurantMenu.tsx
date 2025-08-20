import React, { useState } from 'react';
import { Star, Leaf, Flame } from 'lucide-react';

const RestaurantMenu = () => {
  const [activeCategory, setActiveCategory] = useState('appetizers');
  const [selectedFilters, setSelectedFilters] = useState<string[]>([]);

  const categories = [
    { id: 'appetizers', name: 'Appetizers' },
    { id: 'mains', name: 'Mains' },
    { id: 'desserts', name: 'Desserts' },
    { id: 'drinks', name: 'Drinks' }
  ];

  const filters = [
    { id: 'popular', name: 'Popular', icon: Star },
    { id: 'vegetarian', name: 'Vegetarian', icon: Leaf },
    { id: 'spicy', name: 'Spicy', icon: Flame }
  ];

  const menuItems = {
    appetizers: [
      {
        id: 1,
        name: 'Truffle Arancini',
        description: 'Crispy risotto balls with black truffle and parmesan',
        price: '$18',
        tags: ['vegetarian', 'popular'],
        image: '🍚'
      },
      {
        id: 2,
        name: 'Seared Scallops',
        description: 'Pan-seared scallops with cauliflower purée and pancetta',
        price: '$24',
        tags: ['popular'],
        image: '🦪'
      },
      {
        id: 3,
        name: 'Spicy Tuna Tartare',
        description: 'Fresh tuna with avocado, sesame, and sriracha aioli',
        price: '$22',
        tags: ['spicy'],
        image: '🍣'
      }
    ],
    mains: [
      {
        id: 4,
        name: 'Wagyu Ribeye',
        description: 'Premium wagyu steak with roasted vegetables and red wine jus',
        price: '$65',
        tags: ['popular'],
        image: '🥩'
      },
      {
        id: 5,
        name: 'Lobster Risotto',
        description: 'Creamy arborio rice with fresh lobster and saffron',
        price: '$38',
        tags: ['popular'],
        image: '🦞'
      },
      {
        id: 6,
        name: 'Vegetarian Wellington',
        description: 'Mushroom and spinach wellington with herb gravy',
        price: '$28',
        tags: ['vegetarian'],
        image: '🥧'
      }
    ],
    desserts: [
      {
        id: 7,
        name: 'Chocolate Soufflé',
        description: 'Rich dark chocolate soufflé with vanilla ice cream',
        price: '$16',
        tags: ['popular'],
        image: '🍫'
      },
      {
        id: 8,
        name: 'Lemon Tart',
        description: 'Classic lemon tart with meringue and berry compote',
        price: '$14',
        tags: ['vegetarian'],
        image: '🍋'
      }
    ],
    drinks: [
      {
        id: 9,
        name: 'Signature Martini',
        description: 'House gin with dry vermouth and olive twist',
        price: '$18',
        tags: ['popular'],
        image: '🍸'
      },
      {
        id: 10,
        name: 'Spiced Old Fashioned',
        description: 'Bourbon with cinnamon syrup and orange bitters',
        price: '$16',
        tags: ['spicy'],
        image: '🥃'
      }
    ]
  };

  const toggleFilter = (filterId: string) => {
    setSelectedFilters(prev => 
      prev.includes(filterId)
        ? prev.filter(f => f !== filterId)
        : [...prev, filterId]
    );
  };

  const filteredItems = menuItems[activeCategory as keyof typeof menuItems]?.filter(item => 
    selectedFilters.length === 0 || 
    selectedFilters.some(filter => item.tags.includes(filter))
  ) || [];

  return (
    <div className="min-h-screen bg-cream">
      {/* Header */}
      <div className="bg-cream border-b border-amber/20 sticky top-0 z-10 backdrop-blur-md">
        <div className="max-w-6xl mx-auto px-6 py-8">
          <div className="text-center mb-8">
            <h1 className="font-playfair text-5xl font-bold text-navy mb-2 animate-fade-in-up">
              Bella Vista
            </h1>
            <p className="font-opensans text-lg text-charcoal animate-fade-in-up" style={{animationDelay: '0.2s'}}>
              Modern Italian Cuisine
            </p>
          </div>

          {/* Navigation Tabs */}
          <div className="flex justify-center mb-6">
            <div className="flex bg-white rounded-2xl p-2 shadow-soft">
              {categories.map((category) => (
                <button
                  key={category.id}
                  onClick={() => setActiveCategory(category.id)}
                  className={`px-6 py-3 rounded-xl font-opensans font-medium transition-all duration-300 ${
                    activeCategory === category.id
                      ? 'bg-coral text-white shadow-coral transform scale-105'
                      : 'text-charcoal hover:bg-coral/10'
                  }`}
                >
                  {category.name}
                </button>
              ))}
            </div>
          </div>

          {/* Filter Chips */}
          <div className="flex justify-center space-x-3">
            {filters.map((filter) => {
              const Icon = filter.icon;
              return (
                <button
                  key={filter.id}
                  onClick={() => toggleFilter(filter.id)}
                  className={`flex items-center space-x-2 px-4 py-2 rounded-full transition-all duration-300 ${
                    selectedFilters.includes(filter.id)
                      ? 'bg-teal text-white shadow-teal'
                      : 'bg-white text-charcoal hover:bg-teal/10 border border-gray-200'
                  }`}
                >
                  <Icon className="w-4 h-4" />
                  <span className="font-opensans text-sm">{filter.name}</span>
                </button>
              );
            })}
          </div>
        </div>
      </div>

      {/* Menu Content */}
      <div className="max-w-6xl mx-auto px-6 py-8">
        <div className="flex gap-8">
          {/* Main Menu Grid */}
          <div className="flex-1">
            <div className="mb-8">
              <h2 className="font-playfair text-3xl font-bold text-navy mb-2 capitalize">
                {activeCategory}
              </h2>
              <div className="w-20 h-1 bg-gradient-coral rounded-full"></div>
            </div>

            <div className="grid md:grid-cols-2 gap-6">
              {filteredItems.map((item) => (
                <div
                  key={item.id}
                  className="card-floating p-6 hover:shadow-medium transition-all duration-300 group"
                >
                  <div className="flex items-start space-x-4">
                    <div className="w-24 h-24 bg-gradient-to-br from-cream to-lemon rounded-2xl flex items-center justify-center text-3xl group-hover:scale-110 transition-transform duration-300">
                      {item.image}
                    </div>
                    
                    <div className="flex-1">
                      <div className="flex justify-between items-start mb-2">
                        <h3 className="font-lato font-bold text-xl text-navy group-hover:text-coral transition-colors">
                          {item.name}
                        </h3>
                        <span className="font-opensans font-bold text-lg text-teal">
                          {item.price}
                        </span>
                      </div>
                      
                      <p className="font-opensans text-charcoal text-sm leading-relaxed mb-3">
                        {item.description}
                      </p>
                      
                      <div className="flex space-x-2">
                        {item.tags.map((tag) => (
                          <span
                            key={tag}
                            className={`px-2 py-1 rounded-full text-xs font-medium ${
                              tag === 'popular' ? 'bg-amber/20 text-amber-dark' :
                              tag === 'vegetarian' ? 'bg-success/20 text-success' :
                              tag === 'spicy' ? 'bg-error/20 text-error' :
                              'bg-gray-100 text-gray-600'
                            }`}
                          >
                            {tag}
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Footer */}
      <div className="bg-navy text-white py-12 mt-16">
        <div className="max-w-6xl mx-auto px-6 text-center">
          <h3 className="font-playfair text-2xl font-bold mb-4">Dietary Information</h3>
          <div className="flex justify-center space-x-8">
            <div className="flex items-center space-x-2">
              <Leaf className="w-5 h-5 text-success" />
              <span className="font-opensans">Vegetarian</span>
            </div>
            <div className="flex items-center space-x-2">
              <Flame className="w-5 h-5 text-error" />
              <span className="font-opensans">Spicy</span>
            </div>
            <div className="flex items-center space-x-2">
              <Star className="w-5 h-5 text-amber" />
              <span className="font-opensans">Popular</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RestaurantMenu;