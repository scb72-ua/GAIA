/**
 * News API functions.
 * [Feature: News Management] [Story: NM-PUBLIC-001] [Ticket: NM-PUBLIC-001-FE-T01]
 */
import { http } from '@/api/http';
import type { NewsListResponse, NewsDetail } from '../types';

export interface FetchNewsListParams {
  page?: number;
  pageSize?: number;
}

export async function fetchNewsList(params: FetchNewsListParams = {}): Promise<NewsListResponse> {
  const { page = 1, pageSize = 10 } = params;
  const response = await http.get<NewsListResponse>('/api/v1/news', {
    params: {
      page,
      page_size: pageSize,
    },
  });
  return response.data;
}

// [Feature: News Management] [Story: NM-PUBLIC-002] [Ticket: NM-PUBLIC-002-FE-T01]
export async function fetchNewsDetail(id: string): Promise<NewsDetail> {
  const response = await http.get<NewsDetail>(`/api/v1/news/${id}`);
  return response.data;
}
