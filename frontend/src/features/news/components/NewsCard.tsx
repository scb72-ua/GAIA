/**
 * NewsCard component - displays a single news item in card format.
 * [Feature: News Management] [Story: NM-PUBLIC-001] [Ticket: NM-PUBLIC-001-FE-T01]
 */
import { Link } from 'react-router-dom';
import { Calendar, User } from 'lucide-react';
import { cn } from '@/lib/utils';
import type { NewsListItem } from '../types';

interface NewsCardProps {
  news: NewsListItem;
  className?: string;
}

/**
 * Formats a date string to DD/MM/YYYY format.
 */
function formatDate(dateString: string): string {
  const date = new Date(dateString);
  return date.toLocaleDateString('es-ES', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
  });
}

/**
 * NewsCard - Reusable card for displaying news in lists.
 * [Feature: News Management] [Story: NM-PUBLIC-001] [Ticket: NM-PUBLIC-001-FE-T01]
 */
export function NewsCard({ news, className }: NewsCardProps) {
  return (
    <article
      className={cn(
        'rounded-lg border bg-white p-6 shadow-sm transition-shadow hover:shadow-md',
        'dark:bg-gray-900 dark:border-gray-800',
        className
      )}
    >
      <Link to={`/noticias/${news.id}`} className="block group">
        <h3 className="text-xl font-semibold text-gray-900 dark:text-white group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">
          {news.title}
        </h3>
        
        {news.excerpt && (
          <p className="mt-2 text-gray-600 dark:text-gray-300 line-clamp-3">
            {news.excerpt}
          </p>
        )}
        
        <div className="mt-4 flex items-center gap-4 text-sm text-gray-500 dark:text-gray-400">
          <span className="flex items-center gap-1">
            <User className="h-4 w-4" aria-hidden="true" />
            <span>{news.author_name}</span>
          </span>
          <span className="flex items-center gap-1">
            <Calendar className="h-4 w-4" aria-hidden="true" />
            <time dateTime={news.published_at}>
              {formatDate(news.published_at)}
            </time>
          </span>
        </div>
      </Link>
    </article>
  );
}
