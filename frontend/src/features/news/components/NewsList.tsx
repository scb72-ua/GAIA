/**
 * NewsList component - displays a list of news items with loading and empty states.
 * [Feature: News Management] [Story: NM-PUBLIC-001] [Ticket: NM-PUBLIC-001-FE-T01]
 */
import { cn } from '@/lib/utils';
import type { NewsListItem } from '../types';
import { NewsCard } from './NewsCard';

interface NewsListProps {
  items: NewsListItem[];
  isLoading?: boolean;
  className?: string;
}

/**
 * Skeleton placeholder for loading state.
 */
function NewsCardSkeleton() {
  return (
    <div className="rounded-lg border bg-white p-6 animate-pulse dark:bg-gray-900 dark:border-gray-800">
      <div className="h-6 bg-gray-200 dark:bg-gray-700 rounded w-3/4" />
      <div className="mt-3 space-y-2">
        <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded" />
        <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-5/6" />
      </div>
      <div className="mt-4 flex gap-4">
        <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-24" />
        <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-20" />
      </div>
    </div>
  );
}

/**
 * Empty state component.
 */
function EmptyState() {
  return (
    <div className="text-center py-12">
      <p className="text-gray-500 dark:text-gray-400 text-lg">
        No hay noticias publicadas
      </p>
    </div>
  );
}

/**
 * NewsList - List container with empty and loading states.
 * [Feature: News Management] [Story: NM-PUBLIC-001] [Ticket: NM-PUBLIC-001-FE-T01]
 */
export function NewsList({ items, isLoading = false, className }: NewsListProps) {
  if (isLoading) {
    return (
      <div className={cn('space-y-4', className)} aria-busy="true" aria-label="Cargando noticias">
        {[...Array(3)].map((_, index) => (
          <NewsCardSkeleton key={index} />
        ))}
      </div>
    );
  }

  if (items.length === 0) {
    return <EmptyState />;
  }

  return (
    <div className={cn('space-y-4', className)}>
      {items.map((news) => (
        <NewsCard key={news.id} news={news} />
      ))}
    </div>
  );
}
