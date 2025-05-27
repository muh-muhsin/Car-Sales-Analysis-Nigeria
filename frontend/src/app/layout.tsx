import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import { Providers } from '@/components/providers'
import { Header } from '@/components/layout/Header'
import { Footer } from '@/components/layout/Footer'
import { Toaster } from 'react-hot-toast'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Cars360 - Decentralized Car Sales Data Marketplace',
  description: 'Buy and sell authenticated Nigerian car sales data using STX tokens on the Stacks blockchain',
  keywords: ['cars', 'nigeria', 'data', 'marketplace', 'blockchain', 'stacks', 'automotive'],
  authors: [{ name: 'Muhammad Muhsin Muhammad' }],
  creator: 'Cars360',
  publisher: 'Cars360',
  formatDetection: {
    email: false,
    address: false,
    telephone: false,
  },
  metadataBase: new URL('https://cars360.ng'),
  openGraph: {
    title: 'Cars360 - Decentralized Car Sales Data Marketplace',
    description: 'Buy and sell authenticated Nigerian car sales data using STX tokens',
    url: 'https://cars360.ng',
    siteName: 'Cars360',
    images: [
      {
        url: '/og-image.png',
        width: 1200,
        height: 630,
        alt: 'Cars360 Marketplace',
      },
    ],
    locale: 'en_US',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Cars360 - Decentralized Car Sales Data Marketplace',
    description: 'Buy and sell authenticated Nigerian car sales data using STX tokens',
    images: ['/twitter-image.png'],
    creator: '@DataPeritus',
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
  verification: {
    google: 'your-google-verification-code',
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="h-full">
      <body className={`${inter.className} h-full bg-gray-50 antialiased`}>
        <Providers>
          <div className="flex min-h-full flex-col">
            <Header />
            <main className="flex-1">
              {children}
            </main>
            <Footer />
          </div>
          <Toaster
            position="top-right"
            toastOptions={{
              duration: 4000,
              style: {
                background: '#363636',
                color: '#fff',
              },
              success: {
                duration: 3000,
                iconTheme: {
                  primary: '#22c55e',
                  secondary: '#fff',
                },
              },
              error: {
                duration: 5000,
                iconTheme: {
                  primary: '#ef4444',
                  secondary: '#fff',
                },
              },
            }}
          />
        </Providers>
      </body>
    </html>
  )
}
