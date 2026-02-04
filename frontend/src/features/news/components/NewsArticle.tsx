/**
 * NewsArticle - Component for displaying full article content.
 * [Feature: News Management] [Story: NM-PUBLIC-002] [Ticket: NM-PUBLIC-002-FE-T01]
 */
import { Link } from 'react-router-dom';
import { ArrowLeft, Calendar, User } from 'lucide-react';
import type { NewsDetail } from '../types';

interface NewsArticleProps {
  article: NewsDetail;
}

/**
 * Format date to DD/MM/YYYY.
 */
function formatDate(dateString: string | null): string {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toLocaleDateString('es-ES', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
  });
}

/**
 * NewsArticle displays full article content with semantic HTML.
 * [Feature: News Management] [Story: NM-PUBLIC-002] [Ticket: NM-PUBLIC-002-FE-T01]
 */
export function NewsArticle({ article }: NewsArticleProps) {
  return (
    <article className="max-w-3xl mx-auto">
      <Link
        to="/noticias"
        className="inline-flex items-center gap-2 text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-300 mb-6 transition-colors"
      >
        <ArrowLeft className="h-4 w-4" />
        Volver a noticias
      </Link>

      <header className="mb-8">
        <h1 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-4">
          {article.title}
        </h1>

        <div className="flex flex-wrap items-center gap-4 text-sm text-gray-600 dark:text-gray-400">
          <span className="inline-flex items-center gap-1.5">
            <User className="h-4 w-4" />
            {article.author_name}
          </span>

          {article.published_at && (
            <span className="inline-flex items-center gap-1.5">
              <Calendar className="h-4 w-4" />
              <time dateTime={article.published_at}>
                {formatDate(article.published_at)}
              </time>
            </span>
          )}
        </div>
      </header>

      <div 
        className="prose prose-lg dark:prose-invert max-w-none"
        dangerouslySetInnerHTML={{ __html: article.content }}
      />
    </article>
  );
}
