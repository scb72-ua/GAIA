/**
 * useNewsDetail hook for fetching a single news article.
 * [Feature: News Management] [Story: NM-PUBLIC-002] [Ticket: NM-PUBLIC-002-FE-T01]
 */
import { useQuery } from '@tanstack/react-query';
import { fetchNewsDetail } from '../api/newsApi';
import type { NewsDetail } from '../types';

export function useNewsDetail(id: string) {
  return useQuery<NewsDetail, Error>({
    queryKey: ['news', 'detail', id],
    queryFn: () => fetchNewsDetail(id),
    enabled: !!id,
  });
}
