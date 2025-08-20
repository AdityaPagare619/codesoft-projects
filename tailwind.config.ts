import type { Config } from "tailwindcss";

export default {
	darkMode: ["class"],
	content: [
		"./pages/**/*.{ts,tsx}",
		"./components/**/*.{ts,tsx}",
		"./app/**/*.{ts,tsx}",
		"./src/**/*.{ts,tsx}",
	],
	prefix: "",
	theme: {
		container: {
			center: true,
			padding: '2rem',
			screens: {
				'2xl': '1400px'
			}
		},
		extend: {
			colors: {
				border: 'hsl(var(--border))',
				input: 'hsl(var(--input))',
				ring: 'hsl(var(--ring))',
				background: 'hsl(var(--background))',
				foreground: 'hsl(var(--foreground))',
				
				// Brand Colors
				teal: {
					DEFAULT: 'hsl(var(--teal))',
					light: 'hsl(var(--teal-light))'
				},
				coral: {
					DEFAULT: 'hsl(var(--coral))',
					dark: 'hsl(var(--coral-dark))'
				},
				amber: {
					DEFAULT: 'hsl(var(--amber))',
					dark: 'hsl(var(--amber-dark))'
				},
				lemon: 'hsl(var(--lemon))',
				charcoal: {
					DEFAULT: 'hsl(var(--charcoal))',
					light: 'hsl(var(--charcoal-light))'
				},
				cream: 'hsl(var(--cream))',
				navy: 'hsl(var(--navy))',
				slate: 'hsl(var(--slate))',
				
				// Semantic Colors
				success: 'hsl(var(--success))',
				error: 'hsl(var(--error))',
				warning: 'hsl(var(--warning))',
				
				primary: {
					DEFAULT: 'hsl(var(--teal))',
					foreground: 'hsl(var(--background))'
				},
				secondary: {
					DEFAULT: 'hsl(var(--coral))',
					foreground: 'hsl(var(--background))'
				},
				destructive: {
					DEFAULT: 'hsl(var(--error))',
					foreground: 'hsl(var(--background))'
				},
				muted: {
					DEFAULT: 'hsl(var(--cream))',
					foreground: 'hsl(var(--charcoal))'
				},
				accent: {
					DEFAULT: 'hsl(var(--amber))',
					foreground: 'hsl(var(--charcoal))'
				},
				popover: {
					DEFAULT: 'hsl(var(--background))',
					foreground: 'hsl(var(--foreground))'
				},
				card: {
					DEFAULT: 'hsl(var(--card))',
					foreground: 'hsl(var(--card-foreground))'
				},
				sidebar: {
					DEFAULT: 'hsl(var(--sidebar-background))',
					foreground: 'hsl(var(--sidebar-foreground))',
					primary: 'hsl(var(--sidebar-primary))',
					'primary-foreground': 'hsl(var(--sidebar-primary-foreground))',
					accent: 'hsl(var(--sidebar-accent))',
					'accent-foreground': 'hsl(var(--sidebar-accent-foreground))',
					border: 'hsl(var(--sidebar-border))',
					ring: 'hsl(var(--sidebar-ring))'
				}
			},
			borderRadius: {
				lg: 'var(--radius)',
				md: 'calc(var(--radius) - 2px)',
				sm: 'calc(var(--radius) - 4px)'
			},
			fontFamily: {
				sans: ['Roboto', 'sans-serif'],
				playfair: ['Playfair Display', 'serif'],
				montserrat: ['Montserrat', 'sans-serif'],
				opensans: ['Open Sans', 'sans-serif'],
				roboto: ['Roboto', 'sans-serif'],
				lato: ['Lato', 'sans-serif']
			},
			keyframes: {
				'accordion-down': {
					from: {
						height: '0'
					},
					to: {
						height: 'var(--radix-accordion-content-height)'
					}
				},
				'accordion-up': {
					from: {
						height: 'var(--radix-accordion-content-height)'
					},
					to: {
						height: '0'
					}
				},
				fadeInUp: {
					from: {
						opacity: '0',
						transform: 'translateY(30px)'
					},
					to: {
						opacity: '1',
						transform: 'translateY(0)'
					}
				},
				slideInRight: {
					from: {
						opacity: '0',
						transform: 'translateX(30px)'
					},
					to: {
						opacity: '1',
						transform: 'translateX(0)'
					}
				},
				pulseGlow: {
					'0%, 100%': {
						boxShadow: '0 0 20px hsl(var(--teal) / 0.4)'
					},
					'50%': {
						boxShadow: '0 0 40px hsl(var(--teal) / 0.6)'
					}
				},
				float: {
					'0%, 100%': {
						transform: 'translateY(0px)'
					},
					'50%': {
						transform: 'translateY(-10px)'
					}
				},
				rotateSlow: {
					from: {
						transform: 'rotate(0deg)'
					},
					to: {
						transform: 'rotate(360deg)'
					}
				},
				wiggle: {
					'0%, 7%': { transform: 'rotateZ(0)' },
					'15%': { transform: 'rotateZ(-15deg)' },
					'20%': { transform: 'rotateZ(10deg)' },
					'25%': { transform: 'rotateZ(-10deg)' },
					'30%': { transform: 'rotateZ(6deg)' },
					'35%': { transform: 'rotateZ(-4deg)' },
					'40%, 100%': { transform: 'rotateZ(0)' }
				},
				morphing: {
					'0%, 100%': {
						borderRadius: '30% 70% 40% 60%',
						transform: 'scale(1) rotate(0deg)'
					},
					'25%': {
						borderRadius: '60% 40% 70% 30%',
						transform: 'scale(1.1) rotate(90deg)'
					},
					'50%': {
						borderRadius: '40% 60% 30% 70%',
						transform: 'scale(0.9) rotate(180deg)'
					},
					'75%': {
						borderRadius: '70% 30% 60% 40%',
						transform: 'scale(1.05) rotate(270deg)'
					}
				},
				parallax: {
					'0%': { transform: 'translateY(0px) translateX(0px)' },
					'25%': { transform: 'translateY(-10px) translateX(5px)' },
					'50%': { transform: 'translateY(-5px) translateX(10px)' },
					'75%': { transform: 'translateY(-15px) translateX(-5px)' },
					'100%': { transform: 'translateY(0px) translateX(0px)' }
				},
				glow3d: {
					'0%, 100%': {
						boxShadow: '0 0 20px hsl(var(--teal) / 0.3), 0 0 40px hsl(var(--teal) / 0.2), 0 0 60px hsl(var(--teal) / 0.1), inset 0 0 20px hsl(var(--teal) / 0.1)',
						transform: 'translateZ(0px)'
					},
					'50%': {
						boxShadow: '0 0 30px hsl(var(--teal) / 0.4), 0 0 60px hsl(var(--teal) / 0.3), 0 0 80px hsl(var(--teal) / 0.2), inset 0 0 30px hsl(var(--teal) / 0.2)',
						transform: 'translateZ(10px)'
					}
				},
				floating3d: {
					'0%, 100%': { transform: 'translateY(0px) rotateX(0deg) rotateY(0deg)' },
					'25%': { transform: 'translateY(-8px) rotateX(5deg) rotateY(5deg)' },
					'50%': { transform: 'translateY(-15px) rotateX(0deg) rotateY(10deg)' },
					'75%': { transform: 'translateY(-8px) rotateX(-5deg) rotateY(5deg)' }
				},
				cardHover3d: {
					'0%': { transform: 'perspective(1000px) rotateX(0deg) rotateY(0deg) translateZ(0px)' },
					'100%': { transform: 'perspective(1000px) rotateX(-5deg) rotateY(5deg) translateZ(20px)' }
				}
			},
			animation: {
				'accordion-down': 'accordion-down 0.2s ease-out',
				'accordion-up': 'accordion-up 0.2s ease-out',
				'fade-in-up': 'fadeInUp 0.6s ease-out',
				'slide-in-right': 'slideInRight 0.5s ease-out',
				'pulse-glow': 'pulseGlow 2s ease-in-out infinite',
				'float': 'float 3s ease-in-out infinite',
				'rotate-slow': 'rotateSlow 20s linear infinite',
				'wiggle': 'wiggle 1s ease-in-out',
				'morphing': 'morphing 8s ease-in-out infinite',
				'parallax': 'parallax 6s ease-in-out infinite',
				'glow-3d': 'glow3d 3s ease-in-out infinite',
				'floating-3d': 'floating3d 4s ease-in-out infinite',
				'card-hover-3d': 'cardHover3d 0.3s ease-out forwards'
			}
		}
	},
	plugins: [require("tailwindcss-animate")],
} satisfies Config;
