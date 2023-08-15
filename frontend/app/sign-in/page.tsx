"use client"

import {LoginButton} from '@/components/login-button'
import {useUser} from "@/lib/hooks/user-provider";

export default function SignInPage() {
  const {jwt} = useUser()

  if (jwt || process.env.VERCEL_ENV === 'preview') {
    window.location.href = window.location.origin;
    // redirect('/')
  }

  return (
    <div className="flex h-[calc(100vh-theme(spacing.16))] items-center justify-center py-10">
      <LoginButton/>
    </div>
  )
}
