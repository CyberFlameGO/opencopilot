"use client"

import * as React from 'react'
import {useEffect, useState} from 'react'
import Link from 'next/link'
import Image from 'next/image'
import {CopilotConfig, getCopilotConfig} from '@/assets/config'
import {useCopilot} from "@/lib/hooks/copilot-provider";

export function HeaderLogo() {

  const {copilotName} = useCopilot()

  const [config, setConfig] = useState<CopilotConfig | undefined>();
  const [defaultCopilotName, setDefaultCopilotName] = useState<string | undefined>();
  useEffect(() => {
    setConfig(getCopilotConfig(process.env.NEXT_PUBLIC_COPILOT_NAME))
    if (process.env.NEXT_PUBLIC_COPILOT_NAME) {
      setDefaultCopilotName(process.env.NEXT_PUBLIC_COPILOT_NAME)
    }
  }, []);
  if (!config) {
    // Returns null on first render, so the client and server match
    return <></>;
  }

  return (
    <div className="flex items-center justify-end space-x-2">
      {copilotName && copilotName !== process.env.NEXT_PUBLIC_COPILOT_DISPLAY_NAME && <div className="mr-8">
          Copilot: {copilotName}
      </div>}
      <Link href={config.LOGO_LINK_URL} target="_blank" rel="nofollow">
        {defaultCopilotName !== "rpm" &&
            <Image src={config.LOGO_PATH} alt={config.LOGO_IMAGE_ATL}
                   width="100" height="60"/>
        }

      </Link>
    </div>
  )
}
