import React, { useState } from 'react';
import { ArrowLeft, Eye, EyeOff, Mail } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';

const MobileSignup = () => {
  const [currentStep, setCurrentStep] = useState(1);
  const [showPassword, setShowPassword] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    interests: [] as string[]
  });

  const interests = ['Sports', 'News', 'Music', 'Tech', 'Art', 'Food', 'Travel', 'Gaming'];

  const nextStep = () => {
    if (currentStep < 3) setCurrentStep(currentStep + 1);
  };

  const prevStep = () => {
    if (currentStep > 1) setCurrentStep(currentStep - 1);
  };

  const toggleInterest = (interest: string) => {
    setFormData(prev => ({
      ...prev,
      interests: prev.interests.includes(interest) 
        ? prev.interests.filter(i => i !== interest)
        : [...prev.interests, interest]
    }));
  };

  const updateField = (field: string, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-teal/10 to-coral/10 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        {/* Progress Indicator */}
        <div className="flex justify-center mb-8">
          <div className="flex space-x-2">
            {[1, 2, 3].map((step) => (
              <div
                key={step}
                className={`w-3 h-3 rounded-full transition-all duration-300 ${
                  step === currentStep ? 'bg-teal scale-125' : 
                  step < currentStep ? 'bg-teal/60' : 'bg-gray-300'
                }`}
              />
            ))}
          </div>
        </div>

        {/* Step 1: Welcome & Basic Info */}
        {currentStep === 1 && (
          <div className="card-floating p-8 text-center fade-in-up">
            <div className="w-16 h-16 bg-gradient-teal rounded-full mx-auto mb-6 flex items-center justify-center">
              <span className="text-white font-bold text-xl">AL</span>
            </div>
            
            <h1 className="font-roboto font-bold text-2xl text-charcoal mb-2">
              Welcome to AnimationLab
            </h1>
            <p className="text-gray-600 italic mb-8">Let's get you started!</p>
            
            <div className="relative mb-6">
              <Input
                type="text"
                placeholder="Jane Doe"
                value={formData.name}
                onChange={(e) => updateField('name', e.target.value)}
                className="input-floating text-center"
              />
              <label className={`absolute left-4 transition-all duration-300 pointer-events-none ${
                formData.name ? '-top-2 text-xs text-teal bg-white px-2' : 'top-3 text-gray-400'
              }`}>
                Your Name
              </label>
            </div>
            
            <Button 
              onClick={nextStep}
              disabled={!formData.name.trim()}
              className="btn-teal w-full py-4 text-lg"
            >
              Continue
            </Button>
          </div>
        )}

        {/* Step 2: Contact & Credentials */}
        {currentStep === 2 && (
          <div className="card-floating p-8 fade-in-up">
            <div className="flex items-center mb-6">
              <Button variant="ghost" onClick={prevStep} className="p-2">
                <ArrowLeft className="w-5 h-5" />
              </Button>
              <h2 className="font-roboto font-bold text-xl text-charcoal ml-4">
                Account Details
              </h2>
            </div>

            <div className="space-y-6">
              <div className="relative">
                <Mail className="absolute left-3 top-3 w-5 h-5 text-gray-400" />
                <Input
                  type="email"
                  placeholder="jane@example.com"
                  value={formData.email}
                  onChange={(e) => updateField('email', e.target.value)}
                  className="input-floating pl-12"
                />
                {formData.email && formData.email.includes('@') && (
                  <div className="text-success text-sm mt-1 flex items-center">
                    ✓ Valid email format
                  </div>
                )}
              </div>

              <div className="relative">
                <Input
                  type={showPassword ? 'text' : 'password'}
                  placeholder="Create password"
                  value={formData.password}
                  onChange={(e) => updateField('password', e.target.value)}
                  className="input-floating pr-12"
                />
                <button
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-3 text-gray-400 hover:text-gray-600"
                >
                  {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                </button>
                {formData.password && (
                  <div className={`text-sm mt-1 ${
                    formData.password.length >= 6 ? 'text-success' : 'text-error'
                  }`}>
                    {formData.password.length >= 6 ? '✓ Strong password' : '✗ At least 6 characters'}
                  </div>
                )}
              </div>

              <p className="text-xs text-gray-500 text-center">
                We'll never share your info.
              </p>
            </div>

            <div className="flex space-x-4 mt-8">
              <Button variant="outline" onClick={prevStep} className="flex-1">
                Back
              </Button>
              <Button 
                onClick={nextStep}
                disabled={!formData.email || !formData.password || formData.password.length < 6}
                className="btn-teal flex-1"
              >
                Continue
              </Button>
            </div>
          </div>
        )}

        {/* Step 3: Onboarding Preferences */}
        {currentStep === 3 && (
          <div className="card-floating p-8 fade-in-up">
            <div className="flex items-center mb-6">
              <Button variant="ghost" onClick={prevStep} className="p-2">
                <ArrowLeft className="w-5 h-5" />
              </Button>
              <h2 className="font-roboto font-bold text-xl text-charcoal ml-4">
                Your Interests
              </h2>
            </div>

            <p className="text-gray-600 mb-6">
              Hi, {formData.name}! What are you interested in?
            </p>

            <div className="grid grid-cols-2 gap-3 mb-8">
              {interests.map((interest) => (
                <button
                  key={interest}
                  onClick={() => toggleInterest(interest)}
                  className={`p-3 rounded-xl border-2 transition-all duration-300 ${
                    formData.interests.includes(interest)
                      ? 'border-teal bg-teal/10 text-teal transform scale-105'
                      : 'border-gray-200 hover:border-teal/50 hover:bg-teal/5'
                  }`}
                >
                  {interest}
                </button>
              ))}
            </div>

            <Button 
              onClick={() => alert('Welcome to AnimationLab!')}
              disabled={formData.interests.length === 0}
              className="btn-teal w-full py-4 text-lg pulse-glow"
            >
              Sign Up
            </Button>
          </div>
        )}
      </div>
    </div>
  );
};

export default MobileSignup;