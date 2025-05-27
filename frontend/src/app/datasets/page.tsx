'use client'

import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { 
  MagnifyingGlassIcon,
  FunnelIcon,
  ChartBarIcon,
  StarIcon,
  CloudArrowDownIcon
} from '@heroicons/react/24/outline'
import { Button } from '@/components/ui/Button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card'
import { Badge } from '@/components/ui/Badge'
import { useStacks } from '@/hooks/useStacks'

// Mock data for development
const mockDatasets = [
  {
    id: 1,
    title: "Nigerian Car Sales Data 2023",
    description: "Comprehensive dataset of car sales across Nigeria including pricing, brands, and regional data.",
    price: 50,
    records: 2600,
    rating: 4.8,
    reviews: 24,
    tags: ["cars", "nigeria", "sales", "2023"],
    owner: "ST1PQHQKV0RJXZFY1DGX8MNSNYVE3VGZJSRTPGZGM",
    created: "2024-01-15",
    quality_score: 95
  },
  {
    id: 2,
    title: "Lagos Car Market Analysis",
    description: "Detailed analysis of car market trends in Lagos state with price predictions.",
    price: 75,
    records: 1800,
    rating: 4.6,
    reviews: 18,
    tags: ["lagos", "market", "analysis", "predictions"],
    owner: "ST2PQHQKV0RJXZFY1DGX8MNSNYVE3VGZJSRTPGZGM",
    created: "2024-01-10",
    quality_score: 88
  },
  {
    id: 3,
    title: "Used Car Condition Dataset",
    description: "Dataset focusing on used car conditions and their impact on pricing.",
    price: 30,
    records: 950,
    rating: 4.4,
    reviews: 12,
    tags: ["used-cars", "condition", "pricing"],
    owner: "ST3PQHQKV0RJXZFY1DGX8MNSNYVE3VGZJSRTPGZGM",
    created: "2024-01-05",
    quality_score: 82
  }
]

export default function DatasetsPage() {
  const [datasets, setDatasets] = useState(mockDatasets)
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedTags, setSelectedTags] = useState<string[]>([])
  const [sortBy, setSortBy] = useState('newest')
  const { isConnected } = useStacks()

  // Get all unique tags
  const allTags = Array.from(new Set(mockDatasets.flatMap(d => d.tags)))

  // Filter datasets based on search and tags
  const filteredDatasets = datasets.filter(dataset => {
    const matchesSearch = dataset.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         dataset.description.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesTags = selectedTags.length === 0 || 
                       selectedTags.some(tag => dataset.tags.includes(tag))
    return matchesSearch && matchesTags
  })

  // Sort datasets
  const sortedDatasets = [...filteredDatasets].sort((a, b) => {
    switch (sortBy) {
      case 'newest':
        return new Date(b.created).getTime() - new Date(a.created).getTime()
      case 'price-low':
        return a.price - b.price
      case 'price-high':
        return b.price - a.price
      case 'rating':
        return b.rating - a.rating
      case 'quality':
        return b.quality_score - a.quality_score
      default:
        return 0
    }
  })

  const toggleTag = (tag: string) => {
    setSelectedTags(prev => 
      prev.includes(tag) 
        ? prev.filter(t => t !== tag)
        : [...prev, tag]
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Datasets</h1>
          <p className="mt-2 text-lg text-gray-600">
            Discover and purchase authenticated Nigerian car sales data
          </p>
        </div>

        {/* Search and Filters */}
        <div className="mb-8 space-y-4">
          {/* Search Bar */}
          <div className="relative">
            <MagnifyingGlassIcon className="absolute left-3 top-1/2 h-5 w-5 -translate-y-1/2 text-gray-400" />
            <input
              type="text"
              placeholder="Search datasets..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full rounded-lg border border-gray-300 pl-10 pr-4 py-3 text-sm focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
            />
          </div>

          {/* Filters Row */}
          <div className="flex flex-wrap items-center gap-4">
            {/* Tags Filter */}
            <div className="flex items-center space-x-2">
              <FunnelIcon className="h-5 w-5 text-gray-400" />
              <span className="text-sm font-medium text-gray-700">Tags:</span>
              <div className="flex flex-wrap gap-2">
                {allTags.map(tag => (
                  <button
                    key={tag}
                    onClick={() => toggleTag(tag)}
                    className={`px-3 py-1 rounded-full text-xs font-medium transition-colors ${
                      selectedTags.includes(tag)
                        ? 'bg-primary-600 text-white'
                        : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                    }`}
                  >
                    {tag}
                  </button>
                ))}
              </div>
            </div>

            {/* Sort */}
            <div className="ml-auto">
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value)}
                className="rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
              >
                <option value="newest">Newest First</option>
                <option value="price-low">Price: Low to High</option>
                <option value="price-high">Price: High to Low</option>
                <option value="rating">Highest Rated</option>
                <option value="quality">Best Quality</option>
              </select>
            </div>
          </div>
        </div>

        {/* Results Count */}
        <div className="mb-6">
          <p className="text-sm text-gray-600">
            Showing {sortedDatasets.length} of {datasets.length} datasets
          </p>
        </div>

        {/* Dataset Grid */}
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {sortedDatasets.map((dataset, index) => (
            <motion.div
              key={dataset.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3, delay: index * 0.1 }}
            >
              <Card className="h-full hover:shadow-lg transition-shadow">
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <CardTitle className="text-lg">{dataset.title}</CardTitle>
                      <CardDescription className="mt-2">
                        {dataset.description}
                      </CardDescription>
                    </div>
                    <Badge variant="secondary" className="ml-2">
                      {dataset.quality_score}% Quality
                    </Badge>
                  </div>
                </CardHeader>
                
                <CardContent>
                  <div className="space-y-4">
                    {/* Stats */}
                    <div className="flex items-center justify-between text-sm text-gray-600">
                      <div className="flex items-center space-x-1">
                        <ChartBarIcon className="h-4 w-4" />
                        <span>{dataset.records.toLocaleString()} records</span>
                      </div>
                      <div className="flex items-center space-x-1">
                        <StarIcon className="h-4 w-4 fill-yellow-400 text-yellow-400" />
                        <span>{dataset.rating} ({dataset.reviews})</span>
                      </div>
                    </div>

                    {/* Tags */}
                    <div className="flex flex-wrap gap-1">
                      {dataset.tags.slice(0, 3).map(tag => (
                        <Badge key={tag} variant="outline" className="text-xs">
                          {tag}
                        </Badge>
                      ))}
                      {dataset.tags.length > 3 && (
                        <Badge variant="outline" className="text-xs">
                          +{dataset.tags.length - 3}
                        </Badge>
                      )}
                    </div>

                    {/* Price and Action */}
                    <div className="flex items-center justify-between pt-4 border-t">
                      <div>
                        <span className="text-2xl font-bold text-gray-900">
                          {dataset.price} STX
                        </span>
                      </div>
                      <Button 
                        size="sm" 
                        disabled={!isConnected}
                        className="group"
                      >
                        <CloudArrowDownIcon className="mr-2 h-4 w-4 transition-transform group-hover:scale-110" />
                        {isConnected ? 'Purchase' : 'Connect Wallet'}
                      </Button>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          ))}
        </div>

        {/* Empty State */}
        {sortedDatasets.length === 0 && (
          <div className="text-center py-12">
            <ChartBarIcon className="mx-auto h-12 w-12 text-gray-400" />
            <h3 className="mt-4 text-lg font-medium text-gray-900">No datasets found</h3>
            <p className="mt-2 text-gray-600">
              Try adjusting your search terms or filters
            </p>
          </div>
        )}
      </div>
    </div>
  )
}
