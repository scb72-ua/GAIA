/**
 * News list query hook.
 * [Feature: News Management] [Story: NM-PUBLIC-001] [Ticket: NM-PUBLIC-001-FE-T01]
 */
import { useQuery } from '@tanstack/react-query';
import { fetchNewsList, type FetchNewsListParams } from '../api/newsApi';

export const NEWS_LIST_QUERY_KEY = 'newsList';

export function useNewsList(params: FetchNewsListParams = {}) {
  return useQuery({
    queryKey: [NEWS_LIST_QUERY_KEY, params],
    queryFn: () => fetchNewsList(params),
    staleTime: 30 * 1000, // 30 seconds
  });
}
