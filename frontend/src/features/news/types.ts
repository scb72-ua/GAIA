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
