import { useState } from "react"
import { SidebarProvider, SidebarInset } from "@/components/ui/sidebar"
import { AppSidebar } from "@/components/app-sidebar"
import { Header } from "@/components/header"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Switch } from "@/components/ui/switch"
import { Badge } from "@/components/ui/badge"
import { GitBranch, Check, ExternalLink, CheckCircle2, XCircle, Clock } from "lucide-react"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"

const executionLogs = [
    {
      time: "2025-01-08 14:32:05",
      action: "README.md 자동 업데이트",
      status: "success",
      commit: "https://github.com/user/study-algorithm/commit/a4d3c2f",
    },
    {
      time: "2025-01-08 12:15:22",
      action: "폴더 자동 생성",
      status: "success",
      commit: "https://github.com/user/study-algorithm/commit/b7e6f9a",
    },
    {
      time: "2025-01-07 23:45:11",
      action: "커밋 메시지 자동 생성",
      status: "success",
      commit: "https://github.com/user/study-algorithm/commit/c9d8e1b",
    },
    {
      time: "2025-01-07 18:20:33",
      action: "README.md 자동 업데이트",
      status: "failed",
      commit: "-",
    },
    {
      time: "2025-01-06 09:10:44",
      action: "폴더 자동 생성",
      status: "success",
      commit: "https://github.com/user/study-algorithm/commit/d2f1a4c",
    },
  ]

function User() {
    const [repoUrl, setRepoUrl] = useState("user/study-algorithm")
    const [folderStructure, setFolderStructure] = useState("[Date]/[ProblemNo]_[Title]")
    const [autoCreateFolders, setAutoCreateFolders] = useState(true)
    const [autoUpdateReadme, setAutoUpdateReadme] = useState(true)
    const [autoCommitMessage, setAutoCommitMessage] = useState(true)

    const previewPath = "2025-01-08/1234_최단경로"

    return (
        <SidebarProvider>
            <AppSidebar />
            <SidebarInset>
                <Header />
                <main className="flex-1 overflow-auto bg-background p-6">
                <div className="mx-auto max-w-5xl space-y-6">
                    <div>
                    <h1 className="text-2xl font-bold">GitHub 자동화 설정</h1>
                    <p className="text-sm text-muted-foreground">GitHub 레포지토리 연동 및 자동화 규칙을 설정하세요</p>
                    </div>

                    {/* Repository Connection */}
                    <Card>
                    <CardHeader>
                        <CardTitle>저장소 연결</CardTitle>
                        <CardDescription>GitHub 레포지토리 정보를 관리합니다</CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        <div className="space-y-2">
                        <Label htmlFor="repo-url">레포지토리 주소</Label>
                        <div className="flex gap-2">
                            <div className="relative flex-1">
                            <span className="absolute left-3 top-1/2 -translate-y-1/2 text-sm text-muted-foreground">
                                github.com/
                            </span>
                            <Input
                                id="repo-url"
                                value={repoUrl}
                                onChange={(e) => setRepoUrl(e.target.value)}
                                className="pl-24"
                                placeholder="user/repository"
                            />
                            </div>
                            <Button variant="outline" className="gap-2 bg-transparent">
                            <GitBranch className="h-4 w-4" />
                            저장소 변경
                            </Button>
                        </div>
                        </div>

                        <div className="flex items-center gap-2 rounded-md border border-success/50 bg-success/10 p-3">
                        <Check className="h-4 w-4 text-success" />
                        <span className="text-sm text-success">연결 상태: 정상</span>
                        <Button variant="link" size="sm" className="ml-auto h-auto p-0 text-success">
                            연결 테스트
                        </Button>
                        </div>
                    </CardContent>
                    </Card>

                    {/* Folder Structure Settings */}
                    <Card>
                    <CardHeader>
                        <CardTitle>경로 및 구조 설정</CardTitle>
                        <CardDescription>스터디 산출물이 저장될 폴더 구조를 정의합니다</CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        <div className="space-y-2">
                        <Label htmlFor="folder-structure">폴더 구조 형식</Label>
                        <Input
                            id="folder-structure"
                            value={folderStructure}
                            onChange={(e) => setFolderStructure(e.target.value)}
                            placeholder="[Date]/[ProblemNo]_[Title]"
                            className="font-mono"
                        />
                        <p className="text-xs text-muted-foreground">
                            사용 가능한 변수: [Date], [ProblemNo], [Title], [Tier], [Author]
                        </p>
                        </div>

                        <div className="space-y-2">
                        <Label>생성될 경로 미리보기</Label>
                        <div className="rounded-md border border-border bg-muted/50 p-3">
                            <code className="text-sm font-mono text-foreground">{previewPath}</code>
                        </div>
                        <p className="text-xs text-muted-foreground">예시: BOJ 1234번 문제를 오늘 날짜로 생성한 경우</p>
                        </div>
                    </CardContent>
                    </Card>

                    {/* Automation Toggles */}
                    <Card>
                    <CardHeader>
                        <CardTitle>자동화 기능</CardTitle>
                        <CardDescription>자동으로 실행할 작업을 선택하세요</CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-6">
                        <div className="flex items-center justify-between space-x-2 rounded-lg border border-border p-4">
                        <div className="space-y-0.5 flex-1">
                            <Label htmlFor="auto-folders" className="text-base cursor-pointer">
                            문제 확정 시 폴더 자동 생성
                            </Label>
                            <p className="text-sm text-muted-foreground">
                            선택된 문제가 확정되면 자동으로 폴더 구조를 생성합니다
                            </p>
                        </div>
                        <Switch id="auto-folders" checked={autoCreateFolders} onCheckedChange={setAutoCreateFolders} />
                        </div>

                        <div className="flex items-center justify-between space-x-2 rounded-lg border border-border p-4">
                        <div className="space-y-0.5 flex-1">
                            <Label htmlFor="auto-readme" className="text-base cursor-pointer">
                            README.md 자동 업데이트
                            </Label>
                            <p className="text-sm text-muted-foreground">
                            문제 목록과 진행 상황을 README에 자동으로 반영합니다
                            </p>
                        </div>
                        <Switch id="auto-readme" checked={autoUpdateReadme} onCheckedChange={setAutoUpdateReadme} />
                        </div>

                        <div className="flex items-center justify-between space-x-2 rounded-lg border border-border p-4">
                        <div className="space-y-0.5 flex-1">
                            <Label htmlFor="auto-commit" className="text-base cursor-pointer">
                            해결 시 커밋 메시지 자동 생성
                            </Label>
                            <p className="text-sm text-muted-foreground">
                            문제 해결 시 일관된 형식의 커밋 메시지를 자동으로 작성합니다
                            </p>
                        </div>
                        <Switch id="auto-commit" checked={autoCommitMessage} onCheckedChange={setAutoCommitMessage} />
                        </div>
                    </CardContent>
                    </Card>

                    {/* Execution Log */}
                    <Card>
                    <CardHeader>
                        <CardTitle>실행 로그</CardTitle>
                        <CardDescription>최근 자동화 작업 실행 내역</CardDescription>
                    </CardHeader>
                    <CardContent>
                        <Table>
                        <TableHeader>
                            <TableRow>
                            <TableHead>실행 시간</TableHead>
                            <TableHead>작업 종류</TableHead>
                            <TableHead>상태</TableHead>
                            <TableHead>커밋 주소</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {executionLogs.map((log, index) => (
                            <TableRow key={index}>
                                <TableCell className="font-mono text-xs">{log.time}</TableCell>
                                <TableCell className="text-sm">{log.action}</TableCell>
                                <TableCell>
                                {log.status === "success" ? (
                                    <Badge variant="outline" className="gap-1 border-success/50 bg-success/10 text-success">
                                    <CheckCircle2 className="h-3 w-3" />
                                    성공
                                    </Badge>
                                ) : log.status === "failed" ? (
                                    <Badge
                                    variant="outline"
                                    className="gap-1 border-destructive/50 bg-destructive/10 text-destructive"
                                    >
                                    <XCircle className="h-3 w-3" />
                                    실패
                                    </Badge>
                                ) : (
                                    <Badge variant="outline" className="gap-1">
                                    <Clock className="h-3 w-3" />
                                    대기 중
                                    </Badge>
                                )}
                                </TableCell>
                                <TableCell>
                                {log.commit !== "-" ? (
                                    <Button variant="link" size="sm" className="h-auto p-0 font-mono text-xs" asChild>
                                    <a
                                        href={log.commit}
                                        target="_blank"
                                        rel="noopener noreferrer"
                                        className="flex items-center gap-1"
                                    >
                                        {log.commit.split("/").pop()}
                                        <ExternalLink className="h-3 w-3" />
                                    </a>
                                    </Button>
                                ) : (
                                    <span className="text-xs text-muted-foreground">-</span>
                                )}
                                </TableCell>
                            </TableRow>
                            ))}
                        </TableBody>
                        </Table>
                    </CardContent>
                    </Card>
                </div>
                </main>
            </SidebarInset>
            </SidebarProvider>
    )
}

export default User;