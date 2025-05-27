'use client'

import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { 
  ChartBarIcon,
  CloudArrowUpIcon,
  CurrencyDollarIcon,
  UserGroupIcon,
  TrendingUpIcon,
  DocumentTextIcon,
  StarIcon,
  EyeIcon
} from '@heroicons/react/24/outline'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card'
import { Badge } from '@/components/ui/Badge'
import { Button } from '@/components/ui/Button'
import { useStacks } from '@/hooks/useStacks'
import Link from 'next/link'

// Mock data for dashboard
const mockUserData = {
  totalUploads: 5,
  totalEarnings: 245.5,
  totalPurchases: 12,
  reputationScore: 4.8,
  datasets: [
    {
      id: 1,
      title: "Nigerian Car Sales Data 2023",
      sales: 24,
      revenue: 120.0,
      views: 156,
      rating: 4.8,
      status: "active"
    },
    {
      id: 2,
      title: "Lagos Car Market Analysis",
      sales: 18,
      revenue: 90.0,
      views: 89,
      rating: 4.6,
      status: "active"
    },
    {
      id: 3,
      title: "Used Car Condition Dataset",
      sales: 8,
      revenue: 35.5,
      views: 45,
      rating: 4.4,
      status: "active"
    }
  ],
  recentPurchases: [
    {
      id: 1,
      title: "Abuja Car Pricing Data",
      price: 45,
      purchasedAt: "2024-01-15",
      seller: "DataExpert"
    },
    {
      id: 2,
      title: "Car Insurance Claims Data",
      price: 65,
      purchasedAt: "2024-01-12",
      seller: "InsureAnalytics"
    }
  ]
}

export default function DashboardPage() {
  const [userData, setUserData] = useState(mockUserData)
  const { isConnected, userSession } = useStacks()

  if (!isConnected) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <Card className="max-w-md w-full">
          <CardHeader className="text-center">
            <CardTitle>Connect Your Wallet</CardTitle>
            <CardDescription>
              You need to connect your wallet to access your dashboard
            </CardDescription>
          </CardHeader>
          <CardContent className="text-center">
            <Link href="/">
              <Button>Go to Home Page</Button>
            </Link>
          </CardContent>
        </Card>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
          <p className="mt-2 text-lg text-gray-600">
            Welcome back! Here's your marketplace overview.
          </p>
        </div>

        {/* Stats Grid */}
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
                    <CloudArrowUpIcon className="h-8 w-8 text-primary-600" />
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-600">Total Uploads</p>
                    <p className="text-2xl font-bold text-gray-900">{userData.totalUploads}</p>
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
                    <p className="text-sm font-medium text-gray-600">Total Earnings</p>
                    <p className="text-2xl font-bold text-gray-900">{userData.totalEarnings} STX</p>
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
                    <ChartBarIcon className="h-8 w-8 text-blue-600" />
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-600">Purchases</p>
                    <p className="text-2xl font-bold text-gray-900">{userData.totalPurchases}</p>
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
                    <StarIcon className="h-8 w-8 text-yellow-600" />
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-600">Reputation</p>
                    <p className="text-2xl font-bold text-gray-900">{userData.reputationScore}/5</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        </div>

        <div className="grid gap-8 lg:grid-cols-2">
          {/* My Datasets */}
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle>My Datasets</CardTitle>
                <Link href="/upload">
                  <Button size="sm">
                    <CloudArrowUpIcon className="mr-2 h-4 w-4" />
                    Upload New
                  </Button>
                </Link>
              </div>
              <CardDescription>
                Your uploaded datasets and their performance
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {userData.datasets.map((dataset, index) => (
                  <motion.div
                    key={dataset.id}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.3, delay: index * 0.1 }}
                    className="flex items-center justify-between p-4 bg-gray-50 rounded-lg"
                  >
                    <div className="flex-1">
                      <h4 className="font-medium text-gray-900">{dataset.title}</h4>
                      <div className="flex items-center space-x-4 mt-2 text-sm text-gray-600">
                        <div className="flex items-center">
                          <UserGroupIcon className="h-4 w-4 mr-1" />
                          {dataset.sales} sales
                        </div>
                        <div className="flex items-center">
                          <EyeIcon className="h-4 w-4 mr-1" />
                          {dataset.views} views
                        </div>
                        <div className="flex items-center">
                          <StarIcon className="h-4 w-4 mr-1 fill-yellow-400 text-yellow-400" />
                          {dataset.rating}
                        </div>
                      </div>
                    </div>
                    <div className="text-right">
                      <p className="font-bold text-gray-900">{dataset.revenue} STX</p>
                      <Badge variant="success" className="mt-1">
                        {dataset.status}
                      </Badge>
                    </div>
                  </motion.div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Recent Purchases */}
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle>Recent Purchases</CardTitle>
                <Link href="/datasets">
                  <Button size="sm" variant="outline">
                    Browse More
                  </Button>
                </Link>
              </div>
              <CardDescription>
                Datasets you've recently purchased
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {userData.recentPurchases.map((purchase, index) => (
                  <motion.div
                    key={purchase.id}
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.3, delay: index * 0.1 }}
                    className="flex items-center justify-between p-4 bg-gray-50 rounded-lg"
                  >
                    <div className="flex-1">
                      <h4 className="font-medium text-gray-900">{purchase.title}</h4>
                      <p className="text-sm text-gray-600 mt-1">
                        by {purchase.seller} • {new Date(purchase.purchasedAt).toLocaleDateString()}
                      </p>
                    </div>
                    <div className="text-right">
                      <p className="font-bold text-gray-900">{purchase.price} STX</p>
                      <Button size="sm" variant="outline" className="mt-2">
                        Download
                      </Button>
                    </div>
                  </motion.div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Quick Actions */}
        <Card className="mt-8">
          <CardHeader>
            <CardTitle>Quick Actions</CardTitle>
            <CardDescription>
              Common tasks and shortcuts
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid gap-4 md:grid-cols-3">
              <Link href="/upload">
                <Button className="w-full h-20 flex-col space-y-2" variant="outline">
                  <CloudArrowUpIcon className="h-6 w-6" />
                  <span>Upload Dataset</span>
                </Button>
              </Link>
              <Link href="/datasets">
                <Button className="w-full h-20 flex-col space-y-2" variant="outline">
                  <ChartBarIcon className="h-6 w-6" />
                  <span>Browse Datasets</span>
                </Button>
              </Link>
              <Link href="/analytics">
                <Button className="w-full h-20 flex-col space-y-2" variant="outline">
                  <TrendingUpIcon className="h-6 w-6" />
                  <span>View Analytics</span>
                </Button>
              </Link>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
