/**
 * NewsDetailPage - Page component for displaying a single news article.
 * [Feature: News Management] [Story: NM-PUBLIC-002] [Ticket: NM-PUBLIC-002-FE-T01]
 */
import { useParams, Link } from 'react-router-dom';
import { ArrowLeft } from 'lucide-react';
import { useNewsDetail } from '../hooks/useNewsDetail';
import { NewsArticle } from '../components/NewsArticle';

/**
 * Loading skeleton for article detail.
 */
function ArticleSkeleton() {
  return (
    <div className="max-w-3xl mx-auto animate-pulse">
      <div className="h-4 w-32 bg-gray-200 dark:bg-gray-700 rounded mb-6" />
      <div className="h-10 w-3/4 bg-gray-200 dark:bg-gray-700 rounded mb-4" />
      <div className="flex gap-4 mb-8">
        <div className="h-4 w-24 bg-gray-200 dark:bg-gray-700 rounded" />
        <div className="h-4 w-24 bg-gray-200 dark:bg-gray-700 rounded" />
      </div>
      <div className="space-y-3">
        <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded" />
        <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded" />
        <div className="h-4 w-2/3 bg-gray-200 dark:bg-gray-700 rounded" />
        <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded mt-6" />
        <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded" />
      </div>
    </div>
  );
}

/**
 * Error state for 404 or other errors.
 */
function NotFoundState() {
  return (
    <div className="max-w-3xl mx-auto text-center py-16">
      <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
        Noticia no encontrada
      </h1>
      <p className="text-gray-600 dark:text-gray-400 mb-8">
        La noticia que buscas no existe o ha sido eliminada.
      </p>
      <Link
        to="/noticias"
        className="inline-flex items-center gap-2 text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-300 transition-colors"
      >
        <ArrowLeft className="h-4 w-4" />
        Volver a noticias
      </Link>
    </div>
  );
}

/**
 * NewsDetailPage - Page for viewing a single news article.
 * [Feature: News Management] [Story: NM-PUBLIC-002] [Ticket: NM-PUBLIC-002-FE-T01]
 */
export function NewsDetailPage() {
  const { id } = useParams<{ id: string }>();
  const { data: article, isLoading, isError, error } = useNewsDetail(id || '');

  // Handle loading state
  if (isLoading) {
    return (
      <main className="container mx-auto px-4 py-8">
        <ArticleSkeleton />
      </main>
    );
  }

  // Handle 404 or error state
  if (isError || !article) {
    const is404 = error?.message?.includes('404') || 
                  error?.message?.includes('Request failed with status code 404');
    
    if (is404 || !article) {
      return (
        <main className="container mx-auto px-4 py-8">
          <NotFoundState />
        </main>
      );
    }

    return (
      <main className="container mx-auto px-4 py-8">
        <div className="text-center py-12">
          <p className="text-red-600 dark:text-red-400">
            Error al cargar la noticia: {error?.message || 'Error desconocido'}
          </p>
        </div>
      </main>
    );
  }

  return (
    <main className="container mx-auto px-4 py-8">
      <NewsArticle article={article} />
    </main>
  );
}
