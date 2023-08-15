'use client'

import {type Copilot} from '@/lib/types'
import {cn} from "@/lib/utils";
import {buttonVariants} from "@/components/ui/button";
import Link from "next/link";
import {useCopilot} from "@/lib/hooks/copilot-provider";
import {IconCopilotDots} from "@/components/ui/icons";
import {useEffect} from "react";

interface CopilotItemProps {
  copilot: Copilot
}

export function CopilotItem({copilot}: CopilotItemProps) {
  const {copilotName, setCopilotName} = useCopilot()

  const isActive = copilotName === copilot.name || (copilotName === null && copilot.name === "Default")

  function getConfigurationField(option: Copilot, field: string) {
    try {
      return option.configuration[field] || null;
    } catch (e) {
      return null
    }
  }

  const handleClick = (option: Copilot) => (event: React.MouseEvent) => {
    // Hacky solution to use default copilot here
    if (!option.status) {
      setCopilotName(
        process.env.NEXT_PUBLIC_COPILOT_DISPLAY_NAME || "Default",
        null,
        null,
        null,
        null,
      )
    } else {
      setCopilotName(
        option.name,
        getConfigurationField(option, "title"),
        getConfigurationField(option, "example_messages"),
        getConfigurationField(option, "description"),
        getConfigurationField(option, "footer"),
      )
    }
    window.location.href = window.location.origin;
  };

  if (!copilot.name) return null
  const option = {
    name: copilot.name,
    github_url: copilot.github_url,
    status: copilot.status,
    configuration: copilot.configuration,
    git_hash: copilot.git_hash,
    git_message: copilot.git_message
  }
  return (
    <div className={"relative"}>
      <div className="absolute top-1 flex h-6 w-6 items-center justify-center">
        <IconCopilotDots className="mr-2"/>
      </div>
      <Link href={'#'}
            className={cn(
              buttonVariants({variant: 'ghost'}),
              'group w-full pl-8 pr-16',
              isActive && 'bg-accent'
            )}
            onClick={handleClick(option)}
      >
        <div
          className="relative max-h-5 flex-1 select-none overflow-hidden text-ellipsis break-all"
          title={option.name}
        >
          <span className="whitespace-nowrap">{option.name}</span>
        </div>
      </Link>
    </div>
  )
}
