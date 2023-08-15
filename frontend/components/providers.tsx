'use client'

import * as React from 'react'
import {useEffect, useState} from 'react'
import {ThemeProvider as NextThemesProvider} from 'next-themes'
import {ThemeProviderProps} from 'next-themes/dist/types'

import {TooltipProvider} from '@/components/ui/tooltip'
import {CopilotProvider} from "@/lib/hooks/copilot-provider";
import {UserProvider as Auth0UserProvider} from "@auth0/nextjs-auth0/client";
import {UserProvider} from "@/lib/hooks/user-provider";
import { SidebarProvider } from '@/lib/hooks/sidebar-provider'

export function Providers({children, ...props}: ThemeProviderProps) {

  const [copilotName, setCopilotName] = useState<string | undefined>();
  useEffect(() => {
    if (process.env.NEXT_PUBLIC_COPILOT_NAME) {
      setCopilotName(process.env.NEXT_PUBLIC_COPILOT_NAME)
    }
  }, []);
  if (!copilotName) {
    // Returns null on first render, so the client and server match
    return <></>;
  }

  return (
    // TODO: provide based on copilot
    <NextThemesProvider {...props} enableSystem={false} forcedTheme={copilotName === "rpm" ? "dark" : "light"}>
      <TooltipProvider>
        <CopilotProvider>
          <UserProvider>
            <Auth0UserProvider>
              <SidebarProvider>
                {children}
              </SidebarProvider>
            </Auth0UserProvider>
          </UserProvider>
        </CopilotProvider>
      </TooltipProvider>
    </NextThemesProvider>
  )
}
