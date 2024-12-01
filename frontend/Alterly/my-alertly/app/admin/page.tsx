import Layout from './components/layout'
import Button from './components/button'

export default function Home() {
  return (
    <Layout>
      <div className="max-w-4xl mx-auto space-y-8">
        <h1 className="text-4xl font-bold text-center text-gray-900 mb-8">Welcome to Alertly</h1>
        <p className="text-xl text-center mb-8 text-gray-700">
          Help improve your city by reporting issues or accessing administrative data.
        </p>
        <div className="flex flex-col sm:flex-row gap-4">
          <div className="w-full sm:w-1/2">
            <Button href="/report" variant="dark">Make a Report</Button>
          </div>
          <div className="w-full sm:w-1/2">
            <Button href="/admin" variant="light">Administration Access</Button>
          </div>
        </div>
      </div>
    </Layout>
  )
}