import { Home, Settings, FileCode, GitBranch, type LucideIcon } from "lucide-react"
import { Link, useLocation } from "react-router";

import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarHeader,
} from "@/components/ui/sidebar"

const items: { title: string; url: string; icon: LucideIcon }[] = [
  {
    title: "대시보드",
    url: "/",
    icon: Home,
  },
  {
    title: "문제 추천",
    url: "/problems",
    icon: FileCode,
  },
  {
    title: "개인 설정",
    url: "/user",
    icon: GitBranch,
  },
  {
    title: "그룹 설정",
    url: "/settings",
    icon: Settings,
  },
]

export function AppSidebar() {
  const { pathname } = useLocation();

  return (
    <Sidebar>
      <SidebarHeader className="border-b border-sidebar-border px-6 py-4">
        <Link to="/" className="flex items-center gap-2 font-mono font-semibold text-lg">
          <div className="flex h-8 w-8 items-center justify-center rounded-md bg-primary text-primary-foreground">
            <span className="text-sm font-bold">C</span>
          </div>
          <span>CoyoTe</span>
        </Link>
      </SidebarHeader>
      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupContent>
            <SidebarMenu>
              {items.map((item) => (
                <SidebarMenuItem key={item.title}>
                  <SidebarMenuButton asChild isActive={pathname === item.url}>
                    <Link to={item.url}>
                      <item.icon className="h-4 w-4" />
                      <span>{item.title}</span>
                    </Link>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              ))}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
    </Sidebar>
  )
}
