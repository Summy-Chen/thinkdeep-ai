export interface Article {
  id: string;
  title: string;
  link: string;
  summary: string;
  chinese_summary?: string;
  source_name: string;
  published: string;
  category: string;
  priority: number;
}

export interface DigestData {
  date: string;
  articles: Article[];
  analysis?: {
    overview: string;
    highlights: string[];
    trends: string[];
    recommendation: string;
  };
}
