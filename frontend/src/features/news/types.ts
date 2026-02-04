/**
 * News feature types.
 * [Feature: News Management] [Story: NM-PUBLIC-001] [Ticket: NM-PUBLIC-001-FE-T01]
 */

export interface NewsListItem {
  id: string;
  title: string;
  excerpt: string | null;
  author_name: string;
  published_at: string;
}

export interface NewsListResponse {
  items: NewsListItem[];
  total: number;
  page: number;
  page_size: number;
}

// [Feature: News Management] [Story: NM-PUBLIC-002] [Ticket: NM-PUBLIC-002-FE-T01]
export interface NewsDetail {
  id: string;
  title: string;
  content: string;
  author_name: string;
  published_at: string | null;
}
