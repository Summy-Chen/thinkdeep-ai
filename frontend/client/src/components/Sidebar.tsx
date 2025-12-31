import { useState } from "react";
import { Link, useLocation } from "wouter";
import { LayoutGrid, BookOpen, Building2, Users, Newspaper, Menu, X } from "lucide-react";
import { Button } from "@/components/ui/button";
import { FeedbackDialog } from "./FeedbackDialog";

export function Sidebar() {
  const [location] = useLocation();
  const [isOpen, setIsOpen] = useState(false);

  const navItems = [
    { href: "/", icon: LayoutGrid, label: "商业前沿" },
    { href: "/tech", icon: BookOpen, label: "技术硬核" },
    { href: "/company", icon: Building2, label: "公司动态" },
    { href: "/research", icon: BookOpen, label: "学术研究" },
    { href: "/community", icon: Users, label: "社区讨论" },
  ];

  const toggleSidebar = () => setIsOpen(!isOpen);

  return (
    <>
      {/* Mobile Toggle */}
      <div className="lg:hidden fixed top-4 right-4 z-50">
        <Button variant="outline" size="icon" onClick={toggleSidebar} className="bg-white border-2 border-black shadow-[2px_2px_0px_0px_rgba(0,0,0,1)]">
          {isOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
        </Button>
      </div>

      {/* Sidebar Container */}
      <aside className={`
        fixed top-0 left-0 z-40 h-screen w-64 bg-sidebar border-r-2 border-black transition-transform duration-300 ease-in-out
        ${isOpen ? "translate-x-0" : "-translate-x-full lg:translate-x-0"}
      `}>
        <div className="flex flex-col h-full p-6">
          {/* Logo */}
          <div className="mb-10 flex items-center gap-3">
            <div className="w-10 h-10 bg-blue-600 border-2 border-black flex items-center justify-center shadow-[2px_2px_0px_0px_rgba(0,0,0,1)]">
              <span className="text-white font-bold text-xl">燊</span>
            </div>
            <div className="flex flex-col">
              <h1 className="text-xl font-bold font-heading tracking-tighter leading-none">燊思</h1>
              <span className="text-[10px] font-mono font-bold tracking-widest">THINKDEEP</span>
            </div>
          </div>

          {/* Navigation */}
          <nav className="flex-1 space-y-2">
            {navItems.map((item) => {
              const isActive = location === item.href || (item.href !== "/" && location.startsWith(item.href));
              return (
                <Link key={item.href} href={item.href}>
                  <div className={`
                    flex items-center gap-3 px-4 py-3 text-sm font-bold cursor-pointer transition-all border-2
                    ${isActive 
                      ? "bg-blue-50 border-black shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] translate-x-[-2px] translate-y-[-2px]" 
                      : "border-transparent hover:bg-gray-100 hover:border-black"}
                  `}>
                    <item.icon className={`w-5 h-5 ${isActive ? "text-blue-600" : "text-gray-500"}`} />
                    <span className={isActive ? "text-blue-900" : "text-gray-700"}>{item.label}</span>
                  </div>
                </Link>
              );
            })}
          </nav>

          {/* Footer */}
          <div className="mt-auto pt-6 border-t-2 border-black space-y-6">
            <FeedbackDialog />
            
            <div>
              <div className="text-xs font-mono text-gray-500 mb-1">
                最后更新:
              </div>
              <div className="text-sm font-bold font-mono">
                {new Date().toLocaleDateString()}
              </div>
              <div className="mt-2 text-xs text-gray-400">
                © 2025 ThinkDeep.ai
              </div>
            </div>
          </div>
        </div>
      </aside>
      
      {/* Overlay for mobile */}
      {isOpen && (
        <div 
          className="fixed inset-0 bg-black/50 z-30 lg:hidden"
          onClick={() => setIsOpen(false)}
        />
      )}
    </>
  );
}
