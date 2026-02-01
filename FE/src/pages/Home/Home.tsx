import { SidebarProvider, SidebarInset } from "@/components/ui/sidebar"
import { AppSidebar } from "@/components/app-sidebar"
import { Header } from "@/components/header"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Users, FileCode, CheckCircle2, GitCommit, RefreshCw, Zap } from "lucide-react"

function Home() {
    return (
        <SidebarProvider>
            <AppSidebar />
            <SidebarInset>
                <Header />
                <main className="flex-1 overflow-auto bg-background p-6">
                <div className="mx-auto max-w-7xl space-y-6">
                    {/* Summary Cards */}
                    <div className="grid gap-4 md:grid-cols-3">
                    <Card>
                        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">참여 인원</CardTitle>
                        <Users className="h-4 w-4 text-muted-foreground" />
                        </CardHeader>
                        <CardContent>
                        <div className="text-2xl font-bold">12명</div>
                        <p className="text-xs text-muted-foreground">전원 활성 상태</p>
                        </CardContent>
                    </Card>
                    <Card>
                        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">이번 주 추천 문제</CardTitle>
                        <FileCode className="h-4 w-4 text-muted-foreground" />
                        </CardHeader>
                        <CardContent>
                        <div className="text-2xl font-bold">8개</div>
                        <p className="text-xs text-muted-foreground">골드 3개, 실버 5개</p>
                        </CardContent>
                    </Card>
                    <Card>
                        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">이번 달 해결 문제</CardTitle>
                        <CheckCircle2 className="h-4 w-4 text-muted-foreground" />
                        </CardHeader>
                        <CardContent>
                        <div className="text-2xl font-bold">124개</div>
                        <p className="text-xs text-muted-foreground">지난 달 대비 +18%</p>
                        </CardContent>
                    </Card>
                    </div>

                    {/* Quick Actions */}
                    <Card>
                    <CardHeader>
                        <CardTitle>빠른 작업</CardTitle>
                        <CardDescription>자주 사용하는 기능에 빠르게 접근하세요</CardDescription>
                    </CardHeader>
                    <CardContent className="flex flex-wrap gap-3">
                        <Button className="gap-2">
                        <Zap className="h-4 w-4" />새 문제 추천 받기
                        </Button>
                        <Button variant="outline" className="gap-2 bg-transparent">
                        <RefreshCw className="h-4 w-4" />
                        문제집 즉시 동기화
                        </Button>
                    </CardContent>
                    </Card>

                    {/* Activity Log */}
                    <Card>
                    <CardHeader>
                        <CardTitle>활동 로그</CardTitle>
                        <CardDescription>최근 자동화 활동 내역</CardDescription>
                    </CardHeader>
                    <CardContent>
                        <div className="space-y-4">
                        {[
                            {
                            time: "5분 전",
                            action: "README.md 자동 업데이트",
                            detail: "8개의 새 문제 추가됨",
                            commit: "a4d3c2f",
                            },
                            {
                            time: "2시간 전",
                            action: "폴더 구조 생성",
                            detail: "2025-01-08/1234_문제제목",
                            commit: "b7e6f9a",
                            },
                            {
                            time: "어제",
                            action: "문제 해결 커밋",
                            detail: "김철수님이 BOJ 1234 해결",
                            commit: "c9d8e1b",
                            },
                            {
                            time: "2일 전",
                            action: "주간 문제 추천",
                            detail: "8개 문제 자동 추천 및 등록",
                            commit: "d2f1a4c",
                            },
                            {
                            time: "3일 전",
                            action: "README.md 자동 업데이트",
                            detail: "스터디 통계 갱신",
                            commit: "e5g3b2d",
                            },
                        ].map((log, index) => (
                            <div key={index} className="flex items-start gap-4 pb-4 last:pb-0">
                            <div className="mt-0.5">
                                <GitCommit className="h-4 w-4 text-primary" />
                            </div>
                            <div className="flex-1 space-y-1">
                                <div className="flex items-center justify-between">
                                <p className="text-sm font-medium leading-none">{log.action}</p>
                                <span className="text-xs text-muted-foreground">{log.time}</span>
                                </div>
                                <p className="text-sm text-muted-foreground">{log.detail}</p>
                                <code className="inline-block rounded bg-muted px-1.5 py-0.5 font-mono text-xs">
                                {log.commit}
                                </code>
                            </div>
                            </div>
                        ))}
                        </div>
                    </CardContent>
                    </Card>
                </div>
                </main>
            </SidebarInset>
        </SidebarProvider>
    )
}

export default Home;