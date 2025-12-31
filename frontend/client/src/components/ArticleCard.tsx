import { Article } from "@/lib/types";
import { ExternalLink, Calendar, Tag, Share2, Check, Copy, Twitter, Linkedin } from "lucide-react";
import { useState } from "react";
import { Button } from "./ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { toast } from "sonner";

interface ArticleCardProps {
  article: Article;
}

export function ArticleCard({ article }: ArticleCardProps) {
  const [copied, setCopied] = useState(false);

  const handleShare = async () => {
    // 优先尝试原生分享
    if (navigator.share) {
      try {
        await navigator.share({
          title: article.title,
          text: article.chinese_summary || article.summary,
          url: article.link,
        });
        return;
      } catch (err) {
        console.log('Error sharing:', err);
      }
    }
  };

  const copyToClipboard = () => {
    navigator.clipboard.writeText(`${article.title}\n${article.link}`);
    setCopied(true);
    toast.success("链接已复制");
    setTimeout(() => setCopied(false), 2000);
  };

  const shareToTwitter = () => {
    const text = encodeURIComponent(`${article.title}\nvia ThinkDeep.ai`);
    const url = encodeURIComponent(article.link);
    window.open(`https://twitter.com/intent/tweet?text=${text}&url=${url}`, '_blank');
  };

  const shareToLinkedin = () => {
    const url = encodeURIComponent(article.link);
    window.open(`https://www.linkedin.com/sharing/share-offsite/?url=${url}`, '_blank');
  };

  const formatDate = (dateString: string) => {
    try {
      const date = new Date(dateString);
      return date.toLocaleDateString('zh-CN', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' });
    } catch (e) {
      return dateString;
    }
  };

  const getCategoryColor = (category: string) => {
    switch (category) {
      case 'company': return 'bg-blue-100 text-blue-800 border-blue-800';
      case 'research': return 'bg-orange-100 text-orange-800 border-orange-800';
      case 'blog': return 'bg-purple-100 text-purple-800 border-purple-800';
      case 'community': return 'bg-green-100 text-green-800 border-green-800';
      default: return 'bg-gray-100 text-gray-800 border-gray-800';
    }
  };

  const getCategoryName = (category: string) => {
    switch (category) {
      case 'company': return '公司动态';
      case 'research': return '学术研究';
      case 'blog': return '技术博客';
      case 'community': return '社区讨论';
      case 'news': return '新闻资讯';
      default: return category;
    }
  };

  return (
    <div className="group relative bg-card border-2 border-black p-5 shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] transition-all hover:translate-x-[-2px] hover:translate-y-[-2px] hover:shadow-[6px_6px_0px_0px_rgba(0,0,0,1)] flex flex-col h-full">
      <div className="flex justify-between items-start mb-3">
        <span className={`text-xs font-mono font-bold px-2 py-1 border border-black ${getCategoryColor(article.category)}`}>
          {getCategoryName(article.category)}
        </span>
        <span className="text-xs font-mono text-muted-foreground flex items-center gap-1">
          <Calendar className="w-3 h-3" />
          {formatDate(article.published)}
        </span>
      </div>
      
      <h3 className="text-xl font-bold font-heading leading-tight mb-2 group-hover:text-blue-700 transition-colors line-clamp-2">
        <a href={article.link} target="_blank" rel="noopener noreferrer" className="flex items-center gap-2">
          {article.title}
          <ExternalLink className="w-4 h-4 opacity-0 group-hover:opacity-100 transition-opacity" />
        </a>
      </h3>
      
      <div className="text-sm font-bold text-muted-foreground mb-3 font-mono border-b-2 border-dashed border-gray-200 pb-2 w-full">
        {article.source_name}
      </div>
      
      <p className="text-sm text-foreground/80 leading-relaxed line-clamp-4 flex-grow">
        {article.chinese_summary || article.summary}
      </p>
      
      <div className="mt-4 pt-3 border-t-2 border-black flex justify-between items-center">
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="ghost" size="sm" className="h-8 px-2 hover:bg-gray-100 rounded-none border border-transparent hover:border-black transition-all" onClick={handleShare}>
              <Share2 className="w-4 h-4 mr-2" />
              <span className="text-xs font-bold">分享</span>
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="start" className="w-48 font-sans border-2 border-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] rounded-none">
            <DropdownMenuItem onClick={copyToClipboard} className="cursor-pointer focus:bg-blue-50 focus:text-blue-600">
              {copied ? <Check className="w-4 h-4 mr-2" /> : <Copy className="w-4 h-4 mr-2" />}
              复制链接
            </DropdownMenuItem>
            <DropdownMenuItem onClick={shareToTwitter} className="cursor-pointer focus:bg-blue-50 focus:text-blue-600">
              <Twitter className="w-4 h-4 mr-2" />
              分享到 X
            </DropdownMenuItem>
            <DropdownMenuItem onClick={shareToLinkedin} className="cursor-pointer focus:bg-blue-50 focus:text-blue-600">
              <Linkedin className="w-4 h-4 mr-2" />
              分享到 LinkedIn
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>

        <a 
          href={article.link} 
          target="_blank" 
          rel="noopener noreferrer"
          className="text-sm font-bold hover:underline flex items-center gap-1"
        >
          阅读原文 <ExternalLink className="w-3 h-3" />
        </a>
      </div>
    </div>
  );
}
