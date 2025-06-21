import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import AnalyticsPage from '../page'

// Mock the chart components
jest.mock('@/components/charts/PriceChart', () => ({
  PriceChart: ({ data }: any) => <div data-testid="price-chart">Price Chart with {data.length} data points</div>
}))

jest.mock('@/components/charts/BrandDistributionChart', () => ({
  BrandDistributionChart: ({ data }: any) => <div data-testid="brand-chart">Brand Chart with {data.length} brands</div>
}))

jest.mock('@/components/charts/LocationHeatmap', () => ({
  LocationHeatmap: ({ data }: any) => <div data-testid="location-chart">Location Chart with {data.length} locations</div>
}))

// Mock the useStacks hook
jest.mock('@/hooks/useStacks', () => ({
  useStacks: () => ({
    isConnected: false,
    userSession: null,
    connect: jest.fn(),
    disconnect: jest.fn()
  })
}))

// Mock fetch
global.fetch = jest.fn()

const createTestQueryClient = () => new QueryClient({
  defaultOptions: {
    queries: {
      retry: false,
    },
  },
})

const renderWithQueryClient = (component: React.ReactElement) => {
  const queryClient = createTestQueryClient()
  return render(
    <QueryClientProvider client={queryClient}>
      {component}
    </QueryClientProvider>
  )
}

describe('Analytics Page', () => {
  beforeEach(() => {
    // Mock successful API response
    ;(fetch as jest.Mock).mockResolvedValue({
      ok: true,
      json: async () => ({
        overview: {
          totalListings: 2650,
          averagePrice: 4200000,
          priceChange: 5.2,
          mostPopularBrand: 'toyota',
          mostActiveState: 'lagos'
        },
        priceData: [
          { date: '2024-01-01', averagePrice: 4000000, volume: 120 },
          { date: '2024-01-08', averagePrice: 4100000, volume: 135 }
        ],
        brandData: [
          { brand: 'Toyota', count: 856, averagePrice: 3800000, marketShare: 32.3 },
          { brand: 'Honda', count: 495, averagePrice: 4200000, marketShare: 18.7 }
        ],
        locationData: [
          { state: 'Lagos', count: 1193, averagePrice: 4500000, coordinates: [6.5244, 3.3792] },
          { state: 'Abuja', count: 610, averagePrice: 4800000, coordinates: [9.0765, 7.3986] }
        ],
        trends: {
          priceDirection: 'up',
          volumeDirection: 'up',
          topGrowingBrands: ['Hyundai', 'Kia', 'Mazda'],
          emergingMarkets: ['Plateau', 'Enugu', 'Delta']
        }
      })
    })
  })

  afterEach(() => {
    jest.clearAllMocks()
  })

  it('renders analytics page with Nigerian market title', async () => {
    renderWithQueryClient(<AnalyticsPage />)
    
    expect(screen.getByText('Nigerian Car Market Analytics')).toBeInTheDocument()
    expect(screen.getByText('Real-time insights from verified automotive datasets across Nigeria')).toBeInTheDocument()
  })

  it('displays loading state initially', () => {
    renderWithQueryClient(<AnalyticsPage />)
    
    expect(screen.getByRole('status', { hidden: true })).toBeInTheDocument()
  })

  it('displays key metrics after loading', async () => {
    renderWithQueryClient(<AnalyticsPage />)
    
    await waitFor(() => {
      expect(screen.getByText('2,650')).toBeInTheDocument() // Total listings
      expect(screen.getByText('₦4,200,000')).toBeInTheDocument() // Average price
      expect(screen.getByText('Toyota')).toBeInTheDocument() // Most popular brand
      expect(screen.getByText('Lagos')).toBeInTheDocument() // Most active state
    })
  })

  it('displays price change indicator', async () => {
    renderWithQueryClient(<AnalyticsPage />)
    
    await waitFor(() => {
      expect(screen.getByText('+5.2%')).toBeInTheDocument()
    })
  })

  it('renders filter controls', async () => {
    renderWithQueryClient(<AnalyticsPage />)
    
    await waitFor(() => {
      expect(screen.getByDisplayValue('Last 30 days')).toBeInTheDocument()
      expect(screen.getByDisplayValue('All States')).toBeInTheDocument()
      expect(screen.getByDisplayValue('All Brands')).toBeInTheDocument()
    })
  })

  it('updates filters and refetches data', async () => {
    renderWithQueryClient(<AnalyticsPage />)
    
    await waitFor(() => {
      expect(screen.getByDisplayValue('Last 30 days')).toBeInTheDocument()
    })

    // Change time range filter
    const timeRangeSelect = screen.getByDisplayValue('Last 30 days')
    fireEvent.change(timeRangeSelect, { target: { value: '7d' } })
    
    expect(timeRangeSelect).toHaveValue('7d')
    
    // Verify API was called again with new parameters
    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith(
        expect.stringContaining('timeRange=7d')
      )
    })
  })

  it('renders chart components with data', async () => {
    renderWithQueryClient(<AnalyticsPage />)
    
    await waitFor(() => {
      expect(screen.getByTestId('price-chart')).toBeInTheDocument()
      expect(screen.getByTestId('brand-chart')).toBeInTheDocument()
      expect(screen.getByTestId('location-chart')).toBeInTheDocument()
    })
  })

  it('displays trending brands section', async () => {
    renderWithQueryClient(<AnalyticsPage />)
    
    await waitFor(() => {
      expect(screen.getByText('Trending Brands')).toBeInTheDocument()
      expect(screen.getByText('Hyundai')).toBeInTheDocument()
      expect(screen.getByText('Kia')).toBeInTheDocument()
      expect(screen.getByText('Mazda')).toBeInTheDocument()
    })
  })

  it('displays emerging markets section', async () => {
    renderWithQueryClient(<AnalyticsPage />)
    
    await waitFor(() => {
      expect(screen.getByText('Emerging Markets')).toBeInTheDocument()
      expect(screen.getByText('Plateau')).toBeInTheDocument()
      expect(screen.getByText('Enugu')).toBeInTheDocument()
      expect(screen.getByText('Delta')).toBeInTheDocument()
    })
  })

  it('displays market summary insights', async () => {
    renderWithQueryClient(<AnalyticsPage />)
    
    await waitFor(() => {
      expect(screen.getByText('Market Summary')).toBeInTheDocument()
      expect(screen.getByText('Prices are increasing')).toBeInTheDocument()
      expect(screen.getByText('Sales volume increasing')).toBeInTheDocument()
    })
  })

  it('shows connect wallet CTA when not connected', async () => {
    renderWithQueryClient(<AnalyticsPage />)
    
    await waitFor(() => {
      expect(screen.getByText('Access Premium Analytics')).toBeInTheDocument()
      expect(screen.getByText('Connect Wallet')).toBeInTheDocument()
    })
  })

  it('handles API error gracefully', async () => {
    ;(fetch as jest.Mock).mockRejectedValue(new Error('API Error'))
    
    renderWithQueryClient(<AnalyticsPage />)
    
    // Should still render with mock data fallback
    await waitFor(() => {
      expect(screen.getByText('Nigerian Car Market Analytics')).toBeInTheDocument()
    })
  })

  it('formats Nigerian currency correctly', async () => {
    renderWithQueryClient(<AnalyticsPage />)
    
    await waitFor(() => {
      // Check for Nigerian Naira formatting
      expect(screen.getByText('₦4,200,000')).toBeInTheDocument()
    })
  })

  it('displays Nigerian market specific insights', async () => {
    renderWithQueryClient(<AnalyticsPage />)
    
    await waitFor(() => {
      expect(screen.getByText(/Lagos and Abuja dominate with 68% of total listings/)).toBeInTheDocument()
    })
  })
})
