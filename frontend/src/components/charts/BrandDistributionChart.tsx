'use client'

import { useMemo } from 'react'
import { 
  PieChart, 
  Pie, 
  Cell, 
  ResponsiveContainer, 
  Tooltip, 
  Legend,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid
} from 'recharts'

interface BrandData {
  brand: string
  count: number
  averagePrice: number
  marketShare: number
}

interface BrandDistributionChartProps {
  data: BrandData[]
}

// Nigerian car market brand colors for visual consistency
const BRAND_COLORS = [
  '#3B82F6', // Toyota - Blue (most popular)
  '#10B981', // Honda - Green
  '#8B5CF6', // Mercedes-Benz - Purple (luxury)
  '#F59E0B', // BMW - Amber (luxury)
  '#EF4444', // Hyundai - Red
  '#6B7280', // Others - Gray
]

export function BrandDistributionChart({ data }: BrandDistributionChartProps) {
  // Format data for Nigerian market context
  const formattedData = useMemo(() => {
    return data.map((brand, index) => ({
      ...brand,
      name: brand.brand,
      value: brand.marketShare,
      color: BRAND_COLORS[index] || '#6B7280',
      formattedPrice: new Intl.NumberFormat('en-NG', {
        style: 'currency',
        currency: 'NGN',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
      }).format(brand.averagePrice)
    }))
  }, [data])

  const CustomTooltip = ({ active, payload }: any) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload
      return (
        <div className="bg-white p-4 border border-gray-200 rounded-lg shadow-lg">
          <p className="font-medium text-gray-900 capitalize">{data.brand}</p>
          <p className="text-primary-600">
            Market Share: {data.marketShare.toFixed(1)}%
          </p>
          <p className="text-gray-600">
            Count: {data.count.toLocaleString()} cars
          </p>
          <p className="text-gray-600">
            Avg Price: {data.formattedPrice}
          </p>
        </div>
      )
    }
    return null
  }

  const CustomLabel = ({ cx, cy, midAngle, innerRadius, outerRadius, percent }: any) => {
    if (percent < 0.05) return null // Don't show labels for slices < 5%
    
    const RADIAN = Math.PI / 180
    const radius = innerRadius + (outerRadius - innerRadius) * 0.5
    const x = cx + radius * Math.cos(-midAngle * RADIAN)
    const y = cy + radius * Math.sin(-midAngle * RADIAN)

    return (
      <text 
        x={x} 
        y={y} 
        fill="white" 
        textAnchor={x > cx ? 'start' : 'end'} 
        dominantBaseline="central"
        fontSize={12}
        fontWeight="bold"
      >
        {`${(percent * 100).toFixed(0)}%`}
      </text>
    )
  }

  return (
    <div className="space-y-6">
      {/* Pie Chart */}
      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={formattedData}
              cx="50%"
              cy="50%"
              labelLine={false}
              label={CustomLabel}
              outerRadius={80}
              fill="#8884d8"
              dataKey="value"
            >
              {formattedData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.color} />
              ))}
            </Pie>
            <Tooltip content={<CustomTooltip />} />
          </PieChart>
        </ResponsiveContainer>
      </div>

      {/* Brand Legend with Details */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
        {formattedData.map((brand, index) => (
          <div key={brand.brand} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
            <div className="flex items-center space-x-3">
              <div 
                className="w-4 h-4 rounded-full" 
                style={{ backgroundColor: brand.color }}
              />
              <div>
                <p className="font-medium text-gray-900 capitalize">{brand.brand}</p>
                <p className="text-xs text-gray-500">{brand.count.toLocaleString()} cars</p>
              </div>
            </div>
            <div className="text-right">
              <p className="font-medium text-gray-900">{brand.marketShare.toFixed(1)}%</p>
              <p className="text-xs text-gray-500">{brand.formattedPrice}</p>
            </div>
          </div>
        ))}
      </div>

      {/* Market Insights for Nigerian Context */}
      <div className="bg-blue-50 p-4 rounded-lg">
        <h4 className="font-medium text-blue-900 mb-2">Nigerian Market Insights</h4>
        <div className="text-sm text-blue-800 space-y-1">
          <p>• Toyota dominates with {formattedData[0]?.marketShare.toFixed(1)}% market share</p>
          <p>• Japanese brands (Toyota, Honda) control {(formattedData[0]?.marketShare + formattedData[1]?.marketShare).toFixed(1)}% of the market</p>
          <p>• Luxury brands (Mercedes-Benz, BMW) represent premium segment</p>
          <p>• Korean brands (Hyundai) offer value-for-money options</p>
        </div>
      </div>
    </div>
  )
}
