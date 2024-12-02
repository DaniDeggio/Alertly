import Link from 'next/link';

interface ButtonProps {
  href: string;
  children: React.ReactNode;
  variant: 'light' | 'dark';
}

export default function Button({ href, children, variant }: ButtonProps) {
  const baseClasses =
    'w-full px-6 py-3 text-lg font-semibold rounded-lg transition-colors duration-300 ease-in-out shadow-md';
  const variantClasses =
    variant === 'light'
      ? 'text-gray-900 bg-white hover:bg-gray-100 border border-gray-300'
      : 'text-white bg-gray-900 hover:bg-gray-800';

  return (
    <Link href={href} className={`${baseClasses} ${variantClasses}`}>
      {children}
    </Link>
  );
}
