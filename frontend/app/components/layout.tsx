import { Inter } from 'next/font/google';
import NavBar from './navbar';

const inter = Inter({ subsets: ['latin'] });

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <div className={`min-h-screen bg-white text-gray-800 ${inter.className}`}>
      <NavBar />
      <div className="container mx-auto px-4 py-8">
        <main>{children}</main>
      </div>
    </div>
  );
}
