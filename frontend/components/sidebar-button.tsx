'use client'

import Link from 'next/link'
import {cn} from '@/lib/utils'
import {buttonVariants} from '@/components/ui/button'
import {IconPlus} from '@/components/ui/icons'

interface SidebarButtonProps {
}

export function SidebarButton({}: SidebarButtonProps) {
  const isActive = true

  return (
    <div className="relative"
         onClick={() => {
           // A bit hacky solution to actually force reload immediately
           window.location.href = window.location.origin
         }}
    >
      <div className="absolute left-2 top-1 flex h-6 w-6 items-center justify-center">
        <IconPlus className="mr-2"/>
      </div>
      <Link
        href={"/"}
        className={cn(
          buttonVariants({variant: 'ghost'}),
          'group w-full pl-8 pr-16',
          isActive && 'bg-accent'
        )}
      >
        <div
          className="relative max-h-5 flex-1 select-none overflow-hidden text-ellipsis break-all"
          title="New Chat"
        >
          <span className="whitespace-nowrap">New Chat</span>
        </div>
      </Link>
      {/*{isActive && <div className="absolute right-2 top-1">{children}</div>}*/}
    </div>
  )
}
