'use client'

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react'
import { AppConfig, UserSession, showConnect } from '@stacks/connect'
import { StacksTestnet, StacksMainnet } from '@stacks/network'
import { 
  makeContractCall,
  broadcastTransaction,
  AnchorMode,
  PostConditionMode,
  stringUtf8CV,
  uintCV,
  principalCV,
} from '@stacks/transactions'

interface StacksContextType {
  userSession: UserSession | null
  userData: any
  isConnected: boolean
  network: StacksTestnet | StacksMainnet
  connect: () => void
  disconnect: () => void
  callContract: (contractName: string, functionName: string, functionArgs: any[]) => Promise<any>
}

const StacksContext = createContext<StacksContextType | undefined>(undefined)

const appConfig = new AppConfig(['store_write', 'publish_data'])

interface StacksProviderProps {
  children: ReactNode
}

export function StacksProvider({ children }: StacksProviderProps) {
  const [userSession, setUserSession] = useState<UserSession | null>(null)
  const [userData, setUserData] = useState<any>(null)
  const [isConnected, setIsConnected] = useState(false)

  // Determine network based on environment
  const network = process.env.NEXT_PUBLIC_STACKS_NETWORK === 'mainnet' 
    ? new StacksMainnet() 
    : new StacksTestnet()

  useEffect(() => {
    const session = new UserSession({ appConfig })
    setUserSession(session)

    if (session.isSignInPending()) {
      session.handlePendingSignIn().then((userData) => {
        setUserData(userData)
        setIsConnected(true)
      })
    } else if (session.isUserSignedIn()) {
      const userData = session.loadUserData()
      setUserData(userData)
      setIsConnected(true)
    }
  }, [])

  const connect = () => {
    if (!userSession) return

    showConnect({
      appDetails: {
        name: 'Cars360',
        icon: '/logo.png',
      },
      redirectTo: '/',
      onFinish: () => {
        const userData = userSession.loadUserData()
        setUserData(userData)
        setIsConnected(true)
      },
      userSession,
    })
  }

  const disconnect = () => {
    if (userSession) {
      userSession.signUserOut()
      setUserData(null)
      setIsConnected(false)
    }
  }

  const callContract = async (
    contractName: string, 
    functionName: string, 
    functionArgs: any[]
  ) => {
    if (!userSession || !userData) {
      throw new Error('User not connected')
    }

    const contractAddress = process.env.NEXT_PUBLIC_CONTRACT_ADDRESS
    if (!contractAddress) {
      throw new Error('Contract address not configured')
    }

    const txOptions = {
      contractAddress,
      contractName,
      functionName,
      functionArgs,
      senderKey: userData.appPrivateKey,
      network,
      anchorMode: AnchorMode.Any,
      postConditionMode: PostConditionMode.Allow,
    }

    try {
      const transaction = await makeContractCall(txOptions)
      const broadcastResponse = await broadcastTransaction(transaction, network)
      return broadcastResponse
    } catch (error) {
      console.error('Contract call failed:', error)
      throw error
    }
  }

  const value: StacksContextType = {
    userSession,
    userData,
    isConnected,
    network,
    connect,
    disconnect,
    callContract,
  }

  return (
    <StacksContext.Provider value={value}>
      {children}
    </StacksContext.Provider>
  )
}

export function useStacks() {
  const context = useContext(StacksContext)
  if (context === undefined) {
    throw new Error('useStacks must be used within a StacksProvider')
  }
  return context
}
