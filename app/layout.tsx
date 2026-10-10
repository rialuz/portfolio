import type { Metadata, Viewport } from 'next'
import { DM_Sans, Pixelify_Sans } from 'next/font/google'
import type { ReactNode } from 'react'
import { Footer } from '@/components/layout/Footer'
import { Header } from '@/components/layout/Header'
import { SceneStyles } from '@/components/scene/SceneStyles'
import { scene, site } from '@/content/site'
import { heroViewScript } from '@/lib/hero-view-script'
import { motionScript } from '@/lib/motion-script'
import { sceneScript } from '@/lib/scene-script'
import './globals.css'

const dmSans = DM_Sans({
  subsets: ['latin'],
  weight: ['400', '500', '700'],
  variable: '--font-dm-sans',
  display: 'swap',
})

const pixelify = Pixelify_Sans({
  subsets: ['latin'],
  weight: ['500', '700'],
  variable: '--font-pixelify',
  display: 'swap',
})

export const metadata: Metadata = {
  metadataBase: new URL(site.url),
  title: { default: site.title, template: `%s | ${site.name}` },
  description: site.description,
  alternates: { canonical: '/' },
  icons: {
    icon: [
      { url: '/favicon.ico', sizes: 'any' },
      { url: '/icon-16.png', sizes: '16x16', type: 'image/png' },
      { url: '/icon-32.png', sizes: '32x32', type: 'image/png' },
      { url: '/icon-192.png', sizes: '192x192', type: 'image/png' },
    ],
    apple: '/apple-touch-icon.png',
  },
  openGraph: {
    type: 'website',
    url: '/',
    siteName: site.name,
    title: site.title,
    description: site.description,
    images: [{ url: '/og-image.png', width: 1200, height: 630, alt: 'Pixel art of me waving outside a gingerbread house' }],
  },
  twitter: { card: 'summary_large_image', title: site.title, description: site.description, images: ['/og-image.png'] },
}

export const viewport: Viewport = { themeColor: '#FFF7EE' }

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    // The scripts below set a class, data-motion, data-hero and data-scene on <html> before React hydrates.
    <html lang="en" data-scene={scene} className={`${dmSans.variable} ${pixelify.variable}`} suppressHydrationWarning>
      <head>
        <script dangerouslySetInnerHTML={{ __html: motionScript }} />
        <script dangerouslySetInnerHTML={{ __html: heroViewScript }} />
        <script dangerouslySetInnerHTML={{ __html: sceneScript }} />
        <SceneStyles />
      </head>
      {/* Browser extensions add their own attributes to <body> before React loads (ColorZilla's
          cz-shortcut-listen, Grammarly's data-gr-*). This accepts them; it covers <body>'s own
          attributes only, not anything inside it. */}
      <body suppressHydrationWarning>
        <a
          href="#main"
          className="sr-only z-50 rounded border-[3px] border-navy bg-cream px-4 py-2 font-bold focus:not-sr-only focus:fixed focus:top-3 focus:left-3"
        >
          Skip to content
        </a>
        <Header />
        <main id="main">{children}</main>
        <Footer />
      </body>
    </html>
  )
}
