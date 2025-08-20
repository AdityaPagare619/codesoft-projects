import React from 'react';
import { Facebook, Instagram, Twitter } from 'lucide-react';

const EmailTemplate = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-coral/20 to-lemon/30 py-8">
      <div className="max-w-2xl mx-auto bg-white shadow-strong rounded-2xl overflow-hidden">
        {/* Email Container */}
        <div className="max-w-xl mx-auto bg-white">
          {/* Header with Logo */}
          <div className="bg-white p-5">
            <div className="text-center">
              <div className="inline-block bg-gradient-coral text-white px-6 py-3 rounded-xl font-montserrat font-bold text-xl">
                SummerStyle
              </div>
            </div>
          </div>

          {/* Hero Section */}
          <div className="relative">
            <div className="h-64 bg-gradient-to-r from-coral to-amber rounded-t-lg overflow-hidden">
              <div className="absolute inset-0 bg-black/30 flex items-center justify-center">
                <div className="text-center text-white">
                  <h1 className="font-montserrat font-bold text-4xl mb-2 animate-fade-in-up">
                    Summer Sale
                  </h1>
                  <p className="text-2xl font-montserrat animate-fade-in-up" style={{animationDelay: '0.2s'}}>
                    50% Off
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* Body Section 1: Product Features */}
          <div className="p-6">
            <div className="grid md:grid-cols-2 gap-6 mb-8">
              {/* Product 1 */}
              <div className="card-floating p-4 hover:scale-105 transition-transform duration-300">
                <div className="w-full h-32 bg-gradient-to-br from-coral/20 to-coral/40 rounded-lg mb-4 flex items-center justify-center">
                  <div className="w-16 h-16 bg-coral rounded-full flex items-center justify-center">
                    <span className="text-white font-bold">👕</span>
                  </div>
                </div>
                <h3 className="font-opensans font-semibold text-lg text-charcoal mb-2">
                  Summer Essentials
                </h3>
                <p className="text-gray-600 text-sm mb-4">
                  Lightweight, breathable fabrics perfect for those hot summer days.
                </p>
                <button className="btn-coral w-full py-2 text-sm">
                  Shop Now
                </button>
              </div>

              {/* Product 2 */}
              <div className="card-floating p-4 hover:scale-105 transition-transform duration-300">
                <div className="w-full h-32 bg-gradient-to-br from-amber/20 to-amber/40 rounded-lg mb-4 flex items-center justify-center">
                  <div className="w-16 h-16 bg-amber rounded-full flex items-center justify-center">
                    <span className="text-charcoal font-bold">👒</span>
                  </div>
                </div>
                <h3 className="font-opensans font-semibold text-lg text-charcoal mb-2">
                  Beach Accessories
                </h3>
                <p className="text-gray-600 text-sm mb-4">
                  Complete your summer look with our stylish accessories collection.
                </p>
                <button className="btn-coral w-full py-2 text-sm">
                  Shop Now
                </button>
              </div>
            </div>

            {/* Body Section 2: Testimonial */}
            <div className="bg-cream p-6 rounded-xl mb-6">
              <div className="text-center">
                <p className="font-opensans italic text-lg text-charcoal mb-4">
                  "The quality is amazing and the summer collection is absolutely perfect! 
                  I've never felt more confident in my style choices."
                </p>
                <div className="flex items-center justify-center space-x-2">
                  <div className="w-8 h-8 bg-gradient-coral rounded-full"></div>
                  <span className="font-opensans font-medium text-charcoal">Sarah Johnson</span>
                </div>
              </div>
            </div>

            {/* CTA Section */}
            <div className="text-center mb-6">
              <button className="btn-coral px-8 py-4 text-lg font-semibold pulse-glow">
                Shop Summer Sale Now
              </button>
              <p className="text-sm text-gray-500 mt-2">
                Limited time offer. Sale ends July 31st.
              </p>
            </div>
          </div>

          {/* Footer */}
          <div className="bg-charcoal text-white p-6">
            <div className="text-center">
              {/* Social Icons */}
              <div className="flex justify-center space-x-6 mb-4">
                <Facebook className="w-6 h-6 hover:text-coral transition-colors cursor-pointer" />
                <Instagram className="w-6 h-6 hover:text-coral transition-colors cursor-pointer" />
                <Twitter className="w-6 h-6 hover:text-coral transition-colors cursor-pointer" />
              </div>

              {/* Legal Text */}
              <p className="text-xs text-gray-400 mb-2">
                © 2024 SummerStyle. All rights reserved.
              </p>
              <p className="text-xs text-gray-400">
                You received this email because you subscribed to our newsletter.
                <br />
                <a href="#" className="text-coral hover:underline">Unsubscribe</a> | 
                <a href="#" className="text-coral hover:underline"> Privacy Policy</a>
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Email Preview Info */}
      <div className="max-w-2xl mx-auto mt-8 p-6 bg-white/80 backdrop-blur-sm rounded-xl">
        <h2 className="font-montserrat font-bold text-xl text-charcoal mb-4">
          📧 Responsive Email Template
        </h2>
        <div className="grid md:grid-cols-2 gap-4 text-sm">
          <div>
            <h3 className="font-semibold text-coral mb-2">Features:</h3>
            <ul className="space-y-1 text-gray-600">
              <li>• 600px max width, centered</li>
              <li>• Mobile-responsive design</li>
              <li>• Coral (#FF6F61) & Lemon (#F9E79F) palette</li>
              <li>• Montserrat & Open Sans typography</li>
            </ul>
          </div>
          <div>
            <h3 className="font-semibold text-coral mb-2">Components:</h3>
            <ul className="space-y-1 text-gray-600">
              <li>• Hero banner with overlay text</li>
              <li>• Two-column product blocks</li>
              <li>• Customer testimonial section</li>
              <li>• Social icons & legal footer</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default EmailTemplate;