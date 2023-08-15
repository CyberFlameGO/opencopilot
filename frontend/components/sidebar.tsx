'use client'

import * as React from 'react'

import { Button } from '@/components/ui/button'
import {
    Sheet,
    SheetContent,
    SheetHeader,
    SheetTitle,
    SheetTrigger
} from '@/components/ui/sheet'
import { IconSidebar } from '@/components/ui/icons'
import {useState} from 'react'

export interface SidebarProps {
  children?: React.ReactNode;
  initialIsOpen: boolean;
  onOpenChange: (isOpen: boolean) => void;
}

export function Sidebar({ children, initialIsOpen, onOpenChange  }: SidebarProps) {
  const [isOpen, setIsOpen] = useState<boolean>(initialIsOpen);

  React.useEffect(() => {
    onOpenChange(isOpen);
  }, [isOpen]);

  return (
    <Sheet open={isOpen} onOpenChange={() => setIsOpen(!isOpen)}>
      <SheetTrigger asChild>
        <Button variant="ghost" className="-ml-2 h-9 w-9 p-0" onClick={() => setIsOpen(!isOpen)}>
          <IconSidebar className="h-6 w-6" />
          <span className="sr-only">Toggle Sidebar</span>
        </Button>
      </SheetTrigger>
      <SheetContent className="inset-y-0 flex h-auto w-[300px] flex-col p-0">
        <SheetHeader className="p-4">
            {["default"].includes(process.env.NEXT_PUBLIC_COPILOT_NAME || "") ?
            <SheetTitle className="text-sm">My copilots</SheetTitle> : <></>}
        </SheetHeader>
        <SheetHeader className="p-4">
          <SheetTitle className="text-sm">Chat History</SheetTitle>
        </SheetHeader>
        {children}
      </SheetContent>
    </Sheet>
  )
}
