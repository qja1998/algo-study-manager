import { SidebarProvider, SidebarInset } from "@/components/ui/sidebar"
import { AppSidebar } from "@/components/app-sidebar"
import { Header } from "@/components/header"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"

function Settings() {
    return (
        <SidebarProvider>
            <AppSidebar />
            <SidebarInset>
                <Header />
                <main className="flex-1 overflow-auto bg-background p-6">
                <div className="mx-auto max-w-5xl space-y-6">
                    <div>
                    <h1 className="text-2xl font-bold">그룹 설정</h1>
                    <p className="text-sm text-muted-foreground">스터디 그룹 설정을 관리합니다</p>
                    </div>

                    <Card>
                    <CardHeader>
                        <CardTitle>그룹 정보</CardTitle>
                        <CardDescription>스터디 그룹의 기본 정보입니다</CardDescription>
                    </CardHeader>
                    <CardContent>
                        <p className="text-sm text-muted-foreground">그룹 설정 기능은 준비 중입니다.</p>
                    </CardContent>
                    </Card>
                </div>
                </main>
            </SidebarInset>
        </SidebarProvider>
    )
}

export default Settings;