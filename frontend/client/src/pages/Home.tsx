import { useState, useEffect } from "react";
import { useLocation } from "wouter";
import { Sidebar } from "@/components/Sidebar";
import { ArticleCard } from "@/components/ArticleCard";
import { MOCK_DATA } from "@/lib/mock-data";
import { DigestData } from "@/lib/types";
import { Article } from "@/lib/types";
import { Sparkles, TrendingUp, Star } from "lucide-react";

export default function Home() {
  const [location] = useLocation();
  const [articles, setArticles] = useState<Article[]>([]);
  const [filter, setFilter] = useState<string>("all");
  const [data, setData] = useState<DigestData>(MOCK_DATA);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // 尝试加载真实数据（使用 base 路径）
    const basePath = import.meta.env.BASE_URL || '/thinkdeep-ai/';
    fetch(basePath + 'data.json')
      .then(res => {
        if (!res.ok) throw new Error('Failed to load data');
        return res.json();
      })
      .then((realData: DigestData) => {
        setData(realData);
        setLoading(false);
      })
      .catch(err => {
        console.log('Using mock data due to:', err);
        setLoading(false);
      });
  }, []);

  useEffect(() => {
    // 根据路由设置过滤器
    const path = location === "/" ? "all" : location.substring(1);
    setFilter(path);
    
    // 过滤文章
    if (path === "all") {
      // 商业前沿（默认首页）：包含公司动态、新闻、创投
      setArticles(data.articles.filter(a => ['company', 'news', 'business'].includes(a.category)));
    } else if (path === "tech") {
      // 技术硬核：包含学术研究、技术博客、社区讨论
      setArticles(data.articles.filter(a => ['research', 'blog', 'community'].includes(a.category)));
    } else {
      setArticles(data.articles.filter(a => a.category === path));
    }
  }, [location, data]);

  const getPageTitle = () => {
    switch (filter) {
      case 'all': return '商业前沿';
      case 'tech': return '技术硬核';
      case 'company': return '公司动态';
      case 'research': return '学术研究';
      case 'blog': return '技术博客';
      case 'community': return '社区讨论';
      default: return '今日概览';
    }
  };

  const getPageDescription = () => {
    switch (filter) {
      case 'all': return '聚焦 AI 商业落地、巨头动态与创投趋势';
      case 'tech': return '深度解析 AI 算法突破、学术论文与工程实践';
      case 'company': return 'OpenAI, Google, Anthropic 等科技巨头的最新发布与动态';
      case 'research': return '来自 arXiv, BAIR, MIT 等机构的前沿学术论文与研究成果';
      case 'blog': return '知名 AI 专家与技术博主的深度分析与见解';
      case 'community': return 'Hacker News, Reddit 等社区的热门讨论话题';
      default: return '汇集全网最前沿的 AI 资讯，每日更新';
    }
  };

  return (
    <div className="min-h-screen bg-background font-sans">
      <Sidebar />
      
      <main className="lg:ml-64 min-h-screen">
        {/* Hero Section */}
        <div className="bg-white border-b-2 border-black p-8 md:p-12 relative overflow-hidden">
          <div className="absolute top-0 right-0 w-1/3 h-full opacity-10 bg-[url('/images/hero-bg.png')] bg-cover bg-center pointer-events-none"></div>
          
          <div className="relative z-10 max-w-5xl mx-auto">
            <div className="inline-block bg-black text-white px-3 py-1 text-xs font-mono font-bold mb-4 transform -rotate-1">
              THINKDEEP.AI
            </div>
            <h1 className="text-4xl md:text-6xl font-bold font-heading mb-4 tracking-tight">
              {getPageTitle()}
            </h1>
            <p className="text-lg md:text-xl text-gray-600 max-w-2xl leading-relaxed">
              {getPageDescription()}
            </p>
          </div>
        </div>

        <div className="max-w-7xl mx-auto p-6 md:p-10">
          {/* Analysis Section - Only show on home page */}
          {filter === "all" && data.analysis && (
            <div className="mb-12 grid grid-cols-1 md:grid-cols-3 gap-6">
              {/* Overview Card */}
              <div className="md:col-span-2 bg-blue-50 border-2 border-black p-6 shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]">
                <div className="flex items-center gap-2 mb-4">
                  <Sparkles className="w-5 h-5 text-blue-600" />
                  <h2 className="text-xl font-bold font-heading">今日分析</h2>
                </div>
                <p className="text-gray-800 leading-relaxed mb-4">
                  {data.analysis.overview}
                </p>
                <div className="space-y-2">
                  {data.analysis.highlights.map((highlight, i) => (
                    <div key={i} className="flex items-start gap-2">
                      <span className="bg-blue-600 text-white text-xs font-bold w-5 h-5 flex items-center justify-center rounded-full mt-0.5 flex-shrink-0">
                        {i + 1}
                      </span>
                      <span className="text-sm font-medium">{highlight}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Trends Card */}
              <div className="bg-orange-50 border-2 border-black p-6 shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]">
                <div className="flex items-center gap-2 mb-4">
                  <TrendingUp className="w-5 h-5 text-orange-600" />
                  <h2 className="text-xl font-bold font-heading">趋势观察</h2>
                </div>
                <ul className="space-y-3">
                  {data.analysis.trends.map((trend, i) => (
                    <li key={i} className="text-sm font-medium border-l-2 border-orange-300 pl-3 py-1">
                      {trend}
                    </li>
                  ))}
                </ul>
                
                <div className="mt-6 pt-4 border-t-2 border-orange-200">
                  <div className="flex items-center gap-2 mb-2">
                    <Star className="w-4 h-4 text-orange-600" />
                    <span className="text-xs font-bold uppercase tracking-wider text-orange-800">今日推荐</span>
                  </div>
                  <p className="text-xs italic text-gray-700">
                    {data.analysis.recommendation}
                  </p>
                </div>
              </div>
            </div>
          )}

          {/* Articles Grid */}
          <div className="mb-8 flex items-center justify-between">
            <h2 className="text-2xl font-bold font-heading flex items-center gap-2">
              <span className="w-3 h-8 bg-black block"></span>
              最新文章
            </h2>
            <div className="text-sm font-mono text-gray-500">
              共 {articles.length} 篇
            </div>
          </div>

          {articles.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
              {articles.map((article) => (
                <ArticleCard key={article.id} article={article} />
              ))}
            </div>
          ) : (
            <div className="text-center py-20 border-2 border-dashed border-gray-300 bg-gray-50">
              <p className="text-gray-500 font-mono">暂无相关文章</p>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
