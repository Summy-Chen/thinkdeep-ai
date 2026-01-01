import { Toaster } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import NotFound from "@/pages/NotFound";
import { Route, Router, Switch } from "wouter";
import ErrorBoundary from "./components/ErrorBoundary";
import { ThemeProvider } from "./contexts/ThemeContext";
import Home from "./pages/Home";

function AppRouter() {
  // 配置 wouter 的 base 路径，适配 GitHub Pages
  const base = import.meta.env.BASE_URL || "/thinkdeep-ai/";
  
  return (
    <Router base={base}>
      <Switch>
        <Route path="/" component={Home} />
        <Route path="/tech" component={Home} />
        <Route path="/company" component={Home} />
        <Route path="/research" component={Home} />
        <Route path="/blog" component={Home} />
        <Route path="/community" component={Home} />
        <Route path="/404" component={NotFound} />
        {/* Final fallback route */}
        <Route component={NotFound} />
      </Switch>
    </Router>
  );
}

function App() {
  return (
    <ErrorBoundary>
      <ThemeProvider defaultTheme="light">
        <TooltipProvider>
          <Toaster />
          <AppRouter />
        </TooltipProvider>
      </ThemeProvider>
    </ErrorBoundary>
  );
}

export default App;
