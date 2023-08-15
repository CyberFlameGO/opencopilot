"use client"; // If your framework requires this directive

import { Header } from '@/components/header';
import { useSidebar } from "@/lib/hooks/sidebar-provider";

export function AnimatedSidebar({ children }: { children: React.ReactNode }) {
  const {isSidebarOpen, setIsSidebarOpen} = useSidebar();

  return (
    <>
      <Header />
      <main className={`main-flex flex-col flex-1 ${isSidebarOpen ? 'pushed' : 'main-animated'}`}>{children}</main>
    </>
  );
}
