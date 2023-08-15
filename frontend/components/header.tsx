"use client"

import * as React from 'react'
import {Sidebar} from '@/components/sidebar'
import {SidebarList} from '@/components/sidebar-list'
import {SidebarFooter} from '@/components/sidebar-footer'
import {HeaderLogo} from "@/components/header-logo";
import {useUser} from "@/lib/hooks/user-provider";
import {useSidebar} from "@/lib/hooks/sidebar-provider";
import {useUser as auth0useUser} from "@auth0/nextjs-auth0/client";

export function Header() {
  const { isSidebarOpen, setIsSidebarOpen } = useSidebar() // Use the hook

  let {userId} = useUser()
  const {user} = auth0useUser()
  if (!userId) {
    if (user && user.email) {
      userId = user.email
    }
  }

  if (!userId) {
    return <header
      className="sticky top-0 z-50 flex items-center justify-end gap-3 w-full h-16 px-4 border-b shrink-0 bg-gradient-to-b from-background/10 via-background/50 to-background/80 backdrop-blur-xl">
      <div className="flex items-center">
        <div className="flex items-center">
        </div>
      </div>
      <HeaderLogo/>
    </header>
  }

  return (
    <header
      className="sticky top-0 z-50 flex items-center justify-end gap-3 w-full h-16 px-4 border-b shrink-0 bg-gradient-to-b from-background/10 via-background/50 to-background/80 backdrop-blur-xl">
      <div className="flex items-center">
        {((userId)) &&
            <Sidebar initialIsOpen={isSidebarOpen} onOpenChange={setIsSidebarOpen} >
                <React.Suspense fallback={<div className="flex-1 overflow-auto"/>}>
                    <SidebarList userId={userId}/>
                </React.Suspense>
                <SidebarFooter>
                  {/*<LogoutButton/>*/}
                </SidebarFooter>
            </Sidebar>
        }

        <div className="flex items-center">
        </div>
      </div>
      <HeaderLogo/>
    </header>
  )
}
