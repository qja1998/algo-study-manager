"use client"

import { useState } from "react"
import { SidebarProvider, SidebarInset } from "@/components/ui/sidebar"
import { AppSidebar } from "@/components/app-sidebar"
import { Header } from "@/components/header"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Checkbox } from "@/components/ui/checkbox"
import { Label } from "@/components/ui/label"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Plus, GitBranch, Eye, Trash2 } from "lucide-react"

const tierColors = {
  bronze: "bg-amber-700/20 text-amber-700 border-amber-700/50",
  silver: "bg-slate-400/20 text-slate-400 border-slate-400/50",
  gold: "bg-yellow-500/20 text-yellow-500 border-yellow-500/50",
  platinum: "bg-cyan-400/20 text-cyan-400 border-cyan-400/50",
  diamond: "bg-blue-400/20 text-blue-400 border-blue-400/50",
  ruby: "bg-red-500/20 text-red-500 border-red-500/50",
}

const problems = [
  { id: 1234, title: "최단 경로", tier: "gold", tierLevel: "III", difficulty: 12, tags: ["그래프", "다익스트라"] },
  { id: 5678, title: "동적 계획법 연습", tier: "silver", tierLevel: "II", difficulty: 8, tags: ["DP"] },
  { id: 9012, title: "문자열 처리", tier: "silver", tierLevel: "I", difficulty: 7, tags: ["문자열", "구현"] },
  { id: 3456, title: "트리 순회", tier: "gold", tierLevel: "IV", difficulty: 11, tags: ["트리", "DFS"] },
  { id: 7890, title: "그리디 알고리즘", tier: "gold", tierLevel: "V", difficulty: 10, tags: ["그리디"] },
  { id: 2345, title: "백트래킹 심화", tier: "platinum", tierLevel: "V", difficulty: 15, tags: ["백트래킹", "DFS"] },
  { id: 6789, title: "이진 탐색 트리", tier: "silver", tierLevel: "III", difficulty: 9, tags: ["트리", "이진탐색"] },
  { id: 1357, title: "최소 신장 트리", tier: "gold", tierLevel: "II", difficulty: 13, tags: ["그래프", "MST"] },
]

const tiers = [
  { name: "브론즈", value: "bronze", levels: ["V", "IV", "III", "II", "I"] },
  { name: "실버", value: "silver", levels: ["V", "IV", "III", "II", "I"] },
  { name: "골드", value: "gold", levels: ["V", "IV", "III", "II", "I"] },
  { name: "플래티넘", value: "platinum", levels: ["V", "IV", "III", "II", "I"] },
  { name: "다이아몬드", value: "diamond", levels: ["V", "IV", "III", "II", "I"] },
  { name: "루비", value: "ruby", levels: ["V", "IV", "III", "II", "I"] },
]

const algorithmTags = [
  "DP",
  "그래프",
  "그리디",
  "구현",
  "문자열",
  "트리",
  "DFS",
  "BFS",
  "이진탐색",
  "다익스트라",
  "MST",
  "백트래킹",
]

export default function ProblemsPage() {
  const [selectedTiers, setSelectedTiers] = useState<string[]>(["silver", "gold"])
  const [selectedTags, setSelectedTags] = useState<string[]>([])
  const [selectedProblems, setSelectedProblems] = useState<number[]>([])

  const toggleTier = (tier: string) => {
    setSelectedTiers((prev) => (prev.includes(tier) ? prev.filter((t) => t !== tier) : [...prev, tier]))
  }

  const toggleTag = (tag: string) => {
    setSelectedTags((prev) => (prev.includes(tag) ? prev.filter((t) => t !== tag) : [...prev, tag]))
  }

  const toggleProblem = (id: number) => {
    setSelectedProblems((prev) => (prev.includes(id) ? prev.filter((p) => p !== id) : [...prev, id]))
  }

  const filteredProblems = problems.filter((problem) => {
    const tierMatch = selectedTiers.length === 0 || selectedTiers.includes(problem.tier)
    const tagMatch = selectedTags.length === 0 || problem.tags.some((tag) => selectedTags.includes(tag))
    return tierMatch && tagMatch
  })

  return (
    <SidebarProvider>
      <AppSidebar />
      <SidebarInset>
        <Header />
        <main className="flex-1 overflow-auto bg-background">
          <div className="flex h-[calc(100vh-3.5rem)]">
            {/* Main Content */}
            <div className="flex-1 overflow-auto p-6">
              <div className="mx-auto max-w-5xl space-y-6">
                <div>
                  <h1 className="text-xl font-bold">문제 추천</h1>
                  <p className="text-sm text-muted-foreground">solved.ac 데이터 기반 스터디 문제 추천</p>
                </div>

                {/* Filters */}
                <Card>
                  <CardHeader>
                    <CardTitle className="text-base">필터</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-6">
                    {/* Tier Filter */}
                    <div className="space-y-3">
                      <Label className="text-sm font-medium">티어 선택</Label>
                      <div className="flex flex-wrap gap-2">
                        {tiers.map((tier) => (
                          <Button
                            key={tier.value}
                            variant={selectedTiers.includes(tier.value) ? "default" : "outline"}
                            size="sm"
                            onClick={() => toggleTier(tier.value)}
                            className="h-8"
                          >
                            {tier.name}
                          </Button>
                        ))}
                      </div>
                    </div>

                    {/* Algorithm Tag Filter */}
                    <div className="space-y-3">
                      <Label className="text-sm font-medium">알고리즘 태그</Label>
                      <div className="flex flex-wrap gap-2">
                        {algorithmTags.map((tag) => (
                          <Button
                            key={tag}
                            variant={selectedTags.includes(tag) ? "default" : "outline"}
                            size="sm"
                            onClick={() => toggleTag(tag)}
                            className="h-8"
                          >
                            {tag}
                          </Button>
                        ))}
                      </div>
                    </div>
                  </CardContent>
                </Card>

                {/* Problem List */}
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <p className="text-sm text-muted-foreground">{filteredProblems.length}개의 문제</p>
                  </div>
                  <div className="grid gap-3">
                    {filteredProblems.map((problem) => (
                      <Card key={problem.id} className="transition-colors hover:bg-accent/50">
                        <CardContent className="flex items-center gap-4 p-4">
                          <Checkbox
                            checked={selectedProblems.includes(problem.id)}
                            onCheckedChange={() => toggleProblem(problem.id)}
                          />
                          <div className="flex-1 space-y-1">
                            <div className="flex items-center gap-2">
                              <span className="font-mono text-sm font-medium">#{problem.id}</span>
                              <span className="text-sm font-medium">{problem.title}</span>
                            </div>
                            <div className="flex items-center gap-2">
                              <Badge variant="outline" className={tierColors[problem.tier as keyof typeof tierColors]}>
                                {problem.tier.toUpperCase()} {problem.tierLevel}
                              </Badge>
                              <span className="text-xs text-muted-foreground">난이도 {problem.difficulty}</span>
                              <div className="flex gap-1">
                                {problem.tags.map((tag) => (
                                  <Badge key={tag} variant="secondary" className="text-xs">
                                    {tag}
                                  </Badge>
                                ))}
                              </div>
                            </div>
                          </div>
                          <Button size="sm" variant="outline" className="gap-2 bg-transparent">
                            <Plus className="h-3 w-3" />
                            추가
                          </Button>
                        </CardContent>
                      </Card>
                    ))}
                  </div>
                </div>
              </div>
            </div>

            {/* Selection Basket Sidebar */}
            <div className="w-80 border-l border-border bg-card">
              <div className="flex h-full flex-col">
                <div className="border-b border-border p-4">
                  <h2 className="font-semibold">선택된 문제</h2>
                  <p className="text-xs text-muted-foreground">{selectedProblems.length}개 선택됨</p>
                </div>

                <ScrollArea className="flex-1">
                  <div className="space-y-2 p-4">
                    {selectedProblems.length === 0 ? (
                      <p className="text-center text-sm text-muted-foreground py-8">선택된 문제가 없습니다</p>
                    ) : (
                      selectedProblems.map((id) => {
                        const problem = problems.find((p) => p.id === id)
                        if (!problem) return null
                        return (
                          <Card key={id} className="p-3">
                            <div className="flex items-start justify-between gap-2">
                              <div className="flex-1 space-y-1">
                                <p className="font-mono text-xs">#{problem.id}</p>
                                <p className="text-sm font-medium leading-tight">{problem.title}</p>
                                <Badge
                                  variant="outline"
                                  className={`${tierColors[problem.tier as keyof typeof tierColors]} text-xs`}
                                >
                                  {problem.tier.toUpperCase()}
                                </Badge>
                              </div>
                              <Button
                                size="sm"
                                variant="ghost"
                                className="h-6 w-6 p-0"
                                onClick={() => toggleProblem(id)}
                              >
                                <Trash2 className="h-3 w-3" />
                              </Button>
                            </div>
                          </Card>
                        )
                      })
                    )}
                  </div>
                </ScrollArea>

                <div className="space-y-2 border-t border-border p-4">
                  <Button className="w-full gap-2" disabled={selectedProblems.length === 0}>
                    <Plus className="h-4 w-4" />
                    문제집 업데이트
                  </Button>
                  <Button
                    variant="outline"
                    className="w-full gap-2 bg-transparent"
                    disabled={selectedProblems.length === 0}
                  >
                    <GitBranch className="h-4 w-4" />
                    GitHub 자동 반영
                  </Button>
                  <Button
                    variant="outline"
                    className="w-full gap-2 bg-transparent"
                    disabled={selectedProblems.length === 0}
                  >
                    <Eye className="h-4 w-4" />
                    README 미리보기
                  </Button>
                </div>
              </div>
            </div>
          </div>
        </main>
      </SidebarInset>
    </SidebarProvider>
  )
}
