'use client'

import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import {
  ChartBarIcon,
  TrendingUpIcon,
  TrendingDownIcon,
  MapPinIcon,
  CurrencyDollarIcon,
  CalendarIcon,
  FunnelIcon
} from '@heroicons/react/24/outline'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card'
import { Badge } from '@/components/ui/Badge'
import { Button } from '@/components/ui/Button'
import { PriceChart } from '@/components/charts/PriceChart'
import { BrandDistributionChart } from '@/components/charts/BrandDistributionChart'
import { LocationHeatmap } from '@/components/charts/LocationHeatmap'
import { useStacks } from '@/hooks/useStacks'

interface MarketAnalytics {
  overview: {
    totalListings: number
    averagePrice: number
    priceChange: number
    mostPopularBrand: string
    mostActiveState: string
  }
  priceData: Array<{
    date: string
    averagePrice: number
    volume: number
  }>
  brandData: Array<{
    brand: string
    count: number
    averagePrice: number
    marketShare: number
  }>
  locationData: Array<{
    state: string
    count: number
    averagePrice: number
    coordinates: [number, number]
  }>
  trends: {
    priceDirection: 'up' | 'down' | 'stable'
    volumeDirection: 'up' | 'down' | 'stable'
    topGrowingBrands: string[]
    emergingMarkets: string[]
  }
}

export default function AnalyticsPage() {
  const [analytics, setAnalytics] = useState<MarketAnalytics | null>(null)
  const [loading, setLoading] = useState(true)
  const [timeRange, setTimeRange] = useState<'7d' | '30d' | '90d' | '1y'>('30d')
  const [selectedState, setSelectedState] = useState<string>('all')
  const [selectedBrand, setSelectedBrand] = useState<string>('all')
  const { isConnected } = useStacks()

  useEffect(() => {
    fetchAnalytics()
  }, [timeRange, selectedState, selectedBrand])

  const fetchAnalytics = async () => {
    try {
      setLoading(true)
      const params = new URLSearchParams({
        timeRange,
        state: selectedState,
        brand: selectedBrand
      })

      const response = await fetch(`/api/v1/analytics/market-data?${params}`)
      if (!response.ok) throw new Error('Failed to fetch analytics')

      const data = await response.json()
      setAnalytics(data)
    } catch (error) {
      console.error('Error fetching analytics:', error)
      // Use mock data for development
      setAnalytics(getMockAnalytics())
    } finally {
      setLoading(false)
    }
  }

  const getMockAnalytics = (): MarketAnalytics => ({
    overview: {
      totalListings: 2650,
      averagePrice: 4200000,
      priceChange: 5.2,
      mostPopularBrand: 'toyota',
      mostActiveState: 'lagos'
    },
    priceData: [
      { date: '2024-01-01', averagePrice: 4000000, volume: 120 },
      { date: '2024-01-08', averagePrice: 4100000, volume: 135 },
      { date: '2024-01-15', averagePrice: 4150000, volume: 142 },
      { date: '2024-01-22', averagePrice: 4200000, volume: 158 },
    ],
    brandData: [
      { brand: 'Toyota', count: 856, averagePrice: 3800000, marketShare: 32.3 },
      { brand: 'Honda', count: 495, averagePrice: 4200000, marketShare: 18.7 },
      { brand: 'Mercedes-Benz', count: 326, averagePrice: 8500000, marketShare: 12.3 },
      { brand: 'BMW', count: 236, averagePrice: 7200000, marketShare: 8.9 },
      { brand: 'Hyundai', count: 164, averagePrice: 2800000, marketShare: 6.2 },
    ],
    locationData: [
      { state: 'Lagos', count: 1193, averagePrice: 4500000, coordinates: [6.5244, 3.3792] },
      { state: 'Abuja', count: 610, averagePrice: 4800000, coordinates: [9.0765, 7.3986] },
      { state: 'Rivers', count: 212, averagePrice: 3900000, coordinates: [4.8156, 7.0498] },
      { state: 'Oyo', count: 186, averagePrice: 3600000, coordinates: [8.0000, 4.0000] },
      { state: 'Kano', count: 159, averagePrice: 3200000, coordinates: [12.0022, 8.5920] },
    ],
    trends: {
      priceDirection: 'up',
      volumeDirection: 'up',
      topGrowingBrands: ['Hyundai', 'Kia', 'Mazda'],
      emergingMarkets: ['Plateau', 'Enugu', 'Delta']
    }
  })

  const formatNaira = (amount: number) => {
    return new Intl.NumberFormat('en-NG', {
      style: 'currency',
      currency: 'NGN',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(amount)
  }

  const formatPercentage = (value: number) => {
    const sign = value >= 0 ? '+' : ''
    return `${sign}${value.toFixed(1)}%`
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  if (!analytics) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <ChartBarIcon className="mx-auto h-12 w-12 text-gray-400" />
          <h3 className="mt-4 text-lg font-medium text-gray-900">No data available</h3>
          <p className="mt-2 text-gray-600">Unable to load market analytics</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Nigerian Car Market Analytics</h1>
          <p className="mt-2 text-lg text-gray-600">
            Real-time insights from verified automotive datasets across Nigeria
          </p>
        </div>

        {/* Filters */}
        <Card className="mb-8">
          <CardContent className="p-6">
            <div className="flex flex-wrap items-center gap-4">
              <div className="flex items-center space-x-2">
                <CalendarIcon className="h-5 w-5 text-gray-400" />
                <span className="text-sm font-medium text-gray-700">Time Range:</span>
                <select
                  value={timeRange}
                  onChange={(e) => setTimeRange(e.target.value as any)}
                  className="rounded-md border border-gray-300 px-3 py-1 text-sm focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
                >
                  <option value="7d">Last 7 days</option>
                  <option value="30d">Last 30 days</option>
                  <option value="90d">Last 3 months</option>
                  <option value="1y">Last year</option>
                </select>
              </div>

              <div className="flex items-center space-x-2">
                <MapPinIcon className="h-5 w-5 text-gray-400" />
                <span className="text-sm font-medium text-gray-700">State:</span>
                <select
                  value={selectedState}
                  onChange={(e) => setSelectedState(e.target.value)}
                  className="rounded-md border border-gray-300 px-3 py-1 text-sm focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
                >
                  <option value="all">All States</option>
                  <option value="lagos">Lagos</option>
                  <option value="abuja">Abuja (FCT)</option>
                  <option value="rivers">Rivers</option>
                  <option value="oyo">Oyo</option>
                  <option value="kano">Kano</option>
                </select>
              </div>

              <div className="flex items-center space-x-2">
                <FunnelIcon className="h-5 w-5 text-gray-400" />
                <span className="text-sm font-medium text-gray-700">Brand:</span>
                <select
                  value={selectedBrand}
                  onChange={(e) => setSelectedBrand(e.target.value)}
                  className="rounded-md border border-gray-300 px-3 py-1 text-sm focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
                >
                  <option value="all">All Brands</option>
                  <option value="toyota">Toyota</option>
                  <option value="honda">Honda</option>
                  <option value="mercedes-benz">Mercedes-Benz</option>
                  <option value="bmw">BMW</option>
                  <option value="hyundai">Hyundai</option>
                </select>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Key Metrics */}
        <div className="grid gap-6 mb-8 md:grid-cols-2 lg:grid-cols-4">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
          >
            <Card>
              <CardContent className="p-6">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <ChartBarIcon className="h-8 w-8 text-primary-600" />
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-600">Total Listings</p>
                    <p className="text-2xl font-bold text-gray-900">
                      {analytics.overview.totalListings.toLocaleString()}
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: 0.1 }}
          >
            <Card>
              <CardContent className="p-6">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <CurrencyDollarIcon className="h-8 w-8 text-green-600" />
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-600">Average Price</p>
                    <p className="text-2xl font-bold text-gray-900">
                      {formatNaira(analytics.overview.averagePrice)}
                    </p>
                    <div className="flex items-center mt-1">
                      {analytics.overview.priceChange >= 0 ? (
                        <TrendingUpIcon className="h-4 w-4 text-green-600 mr-1" />
                      ) : (
                        <TrendingDownIcon className="h-4 w-4 text-red-600 mr-1" />
                      )}
                      <span className={`text-sm ${analytics.overview.priceChange >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                        {formatPercentage(analytics.overview.priceChange)}
                      </span>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: 0.2 }}
          >
            <Card>
              <CardContent className="p-6">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <div className="h-8 w-8 bg-blue-100 rounded-lg flex items-center justify-center">
                      <span className="text-blue-600 font-bold text-sm">#{analytics.overview.mostPopularBrand.charAt(0).toUpperCase()}</span>
                    </div>
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-600">Top Brand</p>
                    <p className="text-2xl font-bold text-gray-900 capitalize">
                      {analytics.overview.mostPopularBrand}
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: 0.3 }}
          >
            <Card>
              <CardContent className="p-6">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <MapPinIcon className="h-8 w-8 text-purple-600" />
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-600">Most Active</p>
                    <p className="text-2xl font-bold text-gray-900 capitalize">
                      {analytics.overview.mostActiveState}
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        </div>

        {/* Charts Grid */}
        <div className="grid gap-8 lg:grid-cols-2 mb-8">
          {/* Price Trends Chart */}
          <Card>
            <CardHeader>
              <CardTitle>Price Trends</CardTitle>
              <CardDescription>
                Average car prices over time in Nigerian market
              </CardDescription>
            </CardHeader>
            <CardContent>
              <PriceChart data={analytics.priceData} />
            </CardContent>
          </Card>

          {/* Brand Distribution */}
          <Card>
            <CardHeader>
              <CardTitle>Brand Market Share</CardTitle>
              <CardDescription>
                Distribution of car brands in Nigerian market
              </CardDescription>
            </CardHeader>
            <CardContent>
              <BrandDistributionChart data={analytics.brandData} />
            </CardContent>
          </Card>
        </div>

        {/* Location Heatmap */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle>Geographic Distribution</CardTitle>
            <CardDescription>
              Car sales activity across Nigerian states
            </CardDescription>
          </CardHeader>
          <CardContent>
            <LocationHeatmap data={analytics.locationData} />
          </CardContent>
        </Card>

        {/* Market Insights */}
        <div className="grid gap-8 lg:grid-cols-2">
          {/* Trending Brands */}
          <Card>
            <CardHeader>
              <CardTitle>Trending Brands</CardTitle>
              <CardDescription>
                Fastest growing car brands in Nigeria
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {analytics.trends.topGrowingBrands.map((brand, index) => (
                  <div key={brand} className="flex items-center justify-between">
                    <div className="flex items-center">
                      <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center mr-3">
                        <span className="text-green-600 font-bold text-sm">#{index + 1}</span>
                      </div>
                      <span className="font-medium text-gray-900 capitalize">{brand}</span>
                    </div>
                    <Badge variant="success">
                      <TrendingUpIcon className="h-3 w-3 mr-1" />
                      Growing
                    </Badge>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Emerging Markets */}
          <Card>
            <CardHeader>
              <CardTitle>Emerging Markets</CardTitle>
              <CardDescription>
                States with increasing car sales activity
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {analytics.trends.emergingMarkets.map((state, index) => (
                  <div key={state} className="flex items-center justify-between">
                    <div className="flex items-center">
                      <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center mr-3">
                        <MapPinIcon className="h-4 w-4 text-blue-600" />
                      </div>
                      <span className="font-medium text-gray-900 capitalize">{state}</span>
                    </div>
                    <Badge variant="secondary">
                      <TrendingUpIcon className="h-3 w-3 mr-1" />
                      Emerging
                    </Badge>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Market Summary */}
        <Card className="mt-8">
          <CardHeader>
            <CardTitle>Market Summary</CardTitle>
            <CardDescription>
              Key insights from Nigerian automotive data analysis
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid gap-6 md:grid-cols-3">
              <div className="text-center p-4 bg-green-50 rounded-lg">
                <TrendingUpIcon className="h-8 w-8 text-green-600 mx-auto mb-2" />
                <h4 className="font-semibold text-gray-900">Price Trend</h4>
                <p className="text-sm text-gray-600 mt-1">
                  {analytics.trends.priceDirection === 'up' ? 'Prices are increasing' :
                   analytics.trends.priceDirection === 'down' ? 'Prices are decreasing' :
                   'Prices are stable'}
                </p>
              </div>

              <div className="text-center p-4 bg-blue-50 rounded-lg">
                <ChartBarIcon className="h-8 w-8 text-blue-600 mx-auto mb-2" />
                <h4 className="font-semibold text-gray-900">Volume Trend</h4>
                <p className="text-sm text-gray-600 mt-1">
                  {analytics.trends.volumeDirection === 'up' ? 'Sales volume increasing' :
                   analytics.trends.volumeDirection === 'down' ? 'Sales volume decreasing' :
                   'Sales volume stable'}
                </p>
              </div>

              <div className="text-center p-4 bg-purple-50 rounded-lg">
                <MapPinIcon className="h-8 w-8 text-purple-600 mx-auto mb-2" />
                <h4 className="font-semibold text-gray-900">Market Activity</h4>
                <p className="text-sm text-gray-600 mt-1">
                  Lagos and Abuja dominate with 68% of total listings
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Call to Action */}
        {!isConnected && (
          <Card className="mt-8 bg-gradient-to-r from-primary-50 to-blue-50">
            <CardContent className="p-8 text-center">
              <h3 className="text-xl font-bold text-gray-900 mb-2">
                Access Premium Analytics
              </h3>
              <p className="text-gray-600 mb-4">
                Connect your wallet to access detailed market insights and purchase verified datasets
              </p>
              <Button className="bg-primary-600 hover:bg-primary-700">
                Connect Wallet
              </Button>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  )
}
