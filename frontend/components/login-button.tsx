'use client'

import * as React from 'react'
import {Button, type ButtonProps} from '@/components/ui/button'
import {IconGoogle, IconSpinner} from "@/components/ui/icons";
import {cn} from "@/lib/utils";

interface LoginButtonProps extends ButtonProps {
  showIcon?: boolean
  text?: string
}

export function LoginButton(
  {
    text = 'Login with Google',
    showIcon = true,
    className,
    ...props
  }: LoginButtonProps) {
  const [isLoading, setIsLoading] = React.useState(false)
  return (
    <a
      href="/api/auth/login"
      onClick={() => {
        setIsLoading(true)
      }}
    >
      <Button variant="outline"
              disabled={isLoading}
              className={cn(className, "h-12")}
              {...props}>
        {isLoading ? (
          <IconSpinner className="mr-2 animate-spin"/>
        ) : showIcon ? (
          <IconGoogle className="mr-2"/>
        ) : null}
        {text}
      </Button>
    </a>
  )
}
