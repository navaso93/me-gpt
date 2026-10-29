import type { Metadata } from 'next';
import { Geist, Geist_Mono } from 'next/font/google';
import './globals.css';

const geistSans = Geist({
  variable: '--font-geist-sans',
  subsets: ['latin'],
});

const geistMono = Geist_Mono({
  variable: '--font-geist-mono',
  subsets: ['latin'],
});

export const metadata: Metadata = {
  metadataBase: new URL('https://marc-gpt.mnavarrosotes.chatgpt.site'),
  title: 'Marc GPT — Ask about Marc Navarro Sotés',
  description: 'A conversational portfolio for Marc Navarro Sotés, Data & AI professional with renewable-energy expertise.',
  openGraph: {
    title: 'Marc GPT',
    description: 'A conversational portfolio for Marc Navarro Sotés',
    type: 'website',
    images: [{ url: '/og.png', width: 1200, height: 630, alt: 'Marc GPT — A conversational portfolio for Marc Navarro Sotés' }],
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Marc GPT',
    description: 'A conversational portfolio for Marc Navarro Sotés',
    images: ['/og.png'],
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        {children}
      </body>
    </html>
  );
}
