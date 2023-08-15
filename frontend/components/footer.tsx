"use client"

import React, {useEffect, useState} from 'react'

import {cn} from '@/lib/utils'
import {CopilotConfig, getCopilotConfig} from '@/assets/config'
import {useCopilot} from "@/lib/hooks/copilot-provider";

export function FooterText({className}: React.ComponentProps<'p'>) {

  const {footer} = useCopilot()


  const [config, setConfig] = useState<CopilotConfig | undefined>();
  useEffect(() => {
    setConfig(getCopilotConfig(process.env.NEXT_PUBLIC_COPILOT_NAME))
  }, []);
  if (!config) {
    // Returns null on first render, so the client and server match
    return null;
  }

  return (<span
      style={{width: "80%"}}
      className={cn(
        'px-2 text-center text-xs leading-normal text-muted-foreground',
        className
      )}
    >
      {footer || config.FOOTER}
    </span>
  )
}
