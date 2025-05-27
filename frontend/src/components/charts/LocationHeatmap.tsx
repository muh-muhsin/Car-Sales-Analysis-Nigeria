'use client'

import { useMemo } from 'react'
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  Cell
} from 'recharts'
import { MapPinIcon } from '@heroicons/react/24/outline'

interface LocationData {
  state: string
  count: number
  averagePrice: number
  coordinates: [number, number]
}

interface LocationHeatmapProps {
  data: LocationData[]
}

export function LocationHeatmap({ data }: LocationHeatmapProps) {
  // Sort data by count for better visualization
  const sortedData = useMemo(() => {
    return [...data]
      .sort((a, b) => b.count - a.count)
      .map((location, index) => ({
        ...location,
        formattedPrice: new Intl.NumberFormat('en-NG', {
          style: 'currency',
          currency: 'NGN',
          minimumFractionDigits: 0,
          maximumFractionDigits: 0
        }).format(location.averagePrice),
        // Color intensity based on activity level
        intensity: (location.count / Math.max(...data.map(d => d.count))) * 100,
        rank: index + 1
      }))
  }, [data])

  // Get color based on activity intensity
  const getBarColor = (intensity: number) => {
    if (intensity > 80) return '#1E40AF' // Dark blue for highest activity
    if (intensity > 60) return '#3B82F6' // Blue for high activity
    if (intensity > 40) return '#60A5FA' // Light blue for medium activity
    if (intensity > 20) return '#93C5FD' // Lighter blue for low activity
    return '#DBEAFE' // Very light blue for minimal activity
  }

  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload
      return (
        <div className="bg-white p-4 border border-gray-200 rounded-lg shadow-lg">
          <p className="font-medium text-gray-900">{label} State</p>
          <p className="text-primary-600">
            Listings: {data.count.toLocaleString()}
          </p>
          <p className="text-gray-600">
            Avg Price: {data.formattedPrice}
          </p>
          <p className="text-gray-600">
            Market Rank: #{data.rank}
          </p>
        </div>
      )
    }
    return null
  }

  return (
    <div className="space-y-6">
      {/* Bar Chart */}
      <div className="h-80">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            data={sortedData}
            margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
          >
            <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
            <XAxis 
              dataKey="state" 
              stroke="#6B7280"
              fontSize={12}
              tickLine={false}
              axisLine={false}
              angle={-45}
              textAnchor="end"
              height={80}
            />
            <YAxis 
              stroke="#6B7280"
              fontSize={12}
              tickLine={false}
              axisLine={false}
              tickFormatter={(value) => value.toLocaleString()}
            />
            <Tooltip content={<CustomTooltip />} />
            <Bar dataKey="count" radius={[4, 4, 0, 0]}>
              {sortedData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={getBarColor(entry.intensity)} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* State Rankings */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {sortedData.slice(0, 6).map((location, index) => (
          <div key={location.state} className="bg-white p-4 rounded-lg border border-gray-200">
            <div className="flex items-center justify-between mb-2">
              <div className="flex items-center space-x-2">
                <div className={`w-6 h-6 rounded-full flex items-center justify-center text-white text-xs font-bold ${
                  index === 0 ? 'bg-yellow-500' : 
                  index === 1 ? 'bg-gray-400' : 
                  index === 2 ? 'bg-amber-600' : 'bg-blue-500'
                }`}>
                  {index + 1}
                </div>
                <h4 className="font-medium text-gray-900">{location.state}</h4>
              </div>
              <MapPinIcon className="h-5 w-5 text-gray-400" />
            </div>
            
            <div className="space-y-1">
              <div className="flex justify-between text-sm">
                <span className="text-gray-600">Listings:</span>
                <span className="font-medium">{location.count.toLocaleString()}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-600">Avg Price:</span>
                <span className="font-medium">{location.formattedPrice}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-600">Market Share:</span>
                <span className="font-medium">
                  {((location.count / sortedData.reduce((sum, d) => sum + d.count, 0)) * 100).toFixed(1)}%
                </span>
              </div>
            </div>

            {/* Activity indicator */}
            <div className="mt-3">
              <div className="flex justify-between text-xs text-gray-500 mb-1">
                <span>Activity Level</span>
                <span>{location.intensity.toFixed(0)}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div 
                  className="h-2 rounded-full transition-all duration-300"
                  style={{ 
                    width: `${location.intensity}%`,
                    backgroundColor: getBarColor(location.intensity)
                  }}
                />
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Regional Insights */}
      <div className="bg-green-50 p-4 rounded-lg">
        <h4 className="font-medium text-green-900 mb-2">Regional Market Analysis</h4>
        <div className="text-sm text-green-800 space-y-1">
          <p>• <strong>Lagos State</strong> leads with {sortedData[0]?.count.toLocaleString()} listings ({((sortedData[0]?.count / sortedData.reduce((sum, d) => sum + d.count, 0)) * 100).toFixed(1)}% market share)</p>
          <p>• <strong>FCT Abuja</strong> shows premium pricing with higher average values</p>
          <p>• <strong>Southern states</strong> (Lagos, Rivers) dominate car trading activity</p>
          <p>• <strong>Northern markets</strong> (Kano, Kaduna) show growing potential</p>
        </div>
      </div>
    </div>
  )
}
