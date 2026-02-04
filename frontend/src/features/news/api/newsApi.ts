/**
 * News API functions.
 * [Feature: News Management] [Story: NM-PUBLIC-001] [Ticket: NM-PUBLIC-001-FE-T01]
 */
import { http } from '@/api/http';
import type { NewsListResponse } from '../types';

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
