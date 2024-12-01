import Link from 'next/link'

export default function NavBar() {
  return (
    <nav className="bg-white shadow-md">
      <div className="container mx-auto px-6 py-3">
        <div className="flex justify-between items-center">
          <Link href="/" className="text-xl font-semibold text-gray-800">
            Alertly
          </Link>
          <div className="flex space-x-4">
            <Link href="/" className="text-gray-600 hover:text-gray-800">Home</Link>
            <Link href="/report" className="text-gray-600 hover:text-gray-800">Make a Report</Link>
            <Link href="/admin" className="text-gray-600 hover:text-gray-800">Administration</Link>
          </div>
        </div>
      </div>
    </nav>
  )
}