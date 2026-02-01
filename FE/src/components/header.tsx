import { Badge } from "@/components/ui/badge"

export function Header() {
  return (
    <header className="border-b border-border bg-card">
      <div className="flex h-14 items-center justify-between px-6">
        <div className="flex items-center gap-2">
          <h1 className="font-mono text-sm font-semibold">CoyoTe Studio</h1>
        </div>
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2">
            <span className="text-sm text-muted-foreground">백준</span>
            <Badge variant="outline" className="gap-1.5 border-success/50 bg-success/10 text-success">
              <div className="h-1.5 w-1.5 rounded-full bg-success" />
              연결됨
            </Badge>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-sm text-muted-foreground">GitHub</span>
            <Badge variant="outline" className="gap-1.5 border-success/50 bg-success/10 text-success">
              <div className="h-1.5 w-1.5 rounded-full bg-success" />
              연결됨
            </Badge>
          </div>
        </div>
      </div>
    </header>
  )
}