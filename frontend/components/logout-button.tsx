'use client'

import * as React from 'react'
import {Button, type ButtonProps} from '@/components/ui/button'
import {IconGoogle, IconSpinner} from "@/components/ui/icons";
import {cn} from "@/lib/utils";

interface LogoutButtonProps extends ButtonProps {
  text?: string
}

export function LogoutButton(
  {
    text = 'Log out',
    className,
    ...props
  }: LogoutButtonProps) {
  const [isLoading, setIsLoading] = React.useState(false)
  return (
    <a
      href="/api/auth/logout"
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
        ) : null}
        {text}
      </Button>
    </a>
  )
}
