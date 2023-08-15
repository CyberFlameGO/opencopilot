'use client'

import {cn} from "@/lib/utils";
import Link from "next/link";
import {buttonVariants} from "@/components/ui/button";
import {IconPlus} from "@/components/ui/icons";

interface NewCopilotItemProps {
}

export function NewCopilotItem({}: NewCopilotItemProps) {
  const isActive = true

  return (
    <div className="relative">
      <div className="absolute left-2 top-1 flex h-6 w-6 items-center justify-center">
        <IconPlus className="mr-2"/>
      </div>
      <Link
        href={"/new"}
        className={cn(
          buttonVariants({variant: 'ghost'}),
          'group w-full pl-8 pr-16',
          isActive && 'bg-accent'
        )}
      >
        <div
          className="relative max-h-5 flex-1 select-none overflow-hidden text-ellipsis break-all"
          title="New Copilot"
        >
          <span className="whitespace-nowrap">New Copilot</span>
        </div>
      </Link>
      {/*{isActive && <div className="absolute right-2 top-1">{children}</div>}*/}
    </div>
  )
}
